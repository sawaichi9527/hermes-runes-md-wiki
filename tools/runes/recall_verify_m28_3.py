#!/usr/bin/env python3
# M28.3 post-refresh recall verification helper.

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "m28.3.p0.v2"
DEFAULT_PROJECT = "freelancer"


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def find_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def extract_text_values(value: Any) -> list[str]:
    texts: list[str] = []
    if isinstance(value, str):
        texts.append(value)
    elif isinstance(value, dict):
        for item in value.values():
            texts.extend(extract_text_values(item))
    elif isinstance(value, list):
        for item in value:
            texts.extend(extract_text_values(item))
    return texts


def parse_json_stdout(stdout: str) -> tuple[Any | None, str | None]:
    text = stdout or ""
    try:
        return json.loads(text), None
    except Exception as first_exc:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(text[start : end + 1]), None
            except Exception as second_exc:
                return None, str(second_exc)
        return None, str(first_exc)


def result_items(data: Any) -> list[dict[str, Any]]:
    if not isinstance(data, dict):
        return []
    results = data.get("results")
    if not isinstance(results, list):
        return []
    return [item for item in results if isinstance(item, dict)]


def result_path_matches(item: dict[str, Any], expected_path: str) -> bool:
    if item.get("path") == expected_path:
        return True
    citation = item.get("citation")
    if isinstance(citation, dict) and citation.get("path") == expected_path:
        return True
    return False


def result_marker_matches(item: dict[str, Any], marker: str) -> bool:
    searchable = "\n".join([
        str(item.get("content") or ""),
        str(item.get("section_heading") or ""),
        json.dumps(item.get("citation") or {}, ensure_ascii=False, sort_keys=True),
    ])
    return marker in searchable


def path_seen_in_results(data: Any, expected_path: str) -> bool:
    return any(result_path_matches(item, expected_path) for item in result_items(data))


def marker_seen_in_results(data: Any, expected_path: str, marker: str) -> bool:
    return any(
        result_path_matches(item, expected_path) and result_marker_matches(item, marker)
        for item in result_items(data)
    )


def build_recall_verification(
    *,
    root: Path,
    project: str,
    query: str,
    expected_path: str,
    required_marker: str | None,
    heading: str | None,
    limit: int,
    write_record: bool,
) -> dict[str, Any]:
    stamp = utc_stamp()
    hermes_recall = root / "bin" / "hermes-recall"

    hard_errors: list[str] = []
    if not hermes_recall.exists():
        hard_errors.append("bin/hermes-recall not found")
    if not expected_path.startswith("wiki/"):
        hard_errors.append("expected path must be under wiki/")

    if hard_errors:
        return {
            "schema_version": SCHEMA_VERSION,
            "suite": "M28.3 Post-refresh recall verification",
            "status": "BLOCKED",
            "timestamp_utc": stamp,
            "project": project,
            "query": query,
            "expected_path": expected_path,
            "required_marker": required_marker,
            "hard_errors": hard_errors,
        }

    cmd = [
        str(hermes_recall),
        query,
        "--project", project,
        "--mode", "hybrid",
        "--path", expected_path,
        "--limit", str(limit),
        "--json",
    ]
    if heading:
        cmd.extend(["--heading", heading])

    env = os.environ.copy()
    env.setdefault("PYTHONUNBUFFERED", "1")
    env.setdefault("HF_HUB_DISABLE_IMPLICIT_TOKEN", "1")
    env.setdefault("TOKENIZERS_PARALLELISM", "false")

    proc = subprocess.run(
        cmd,
        cwd=str(root),
        env=env,
        text=True,
        capture_output=True,
        timeout=300,
        check=False,
    )

    parsed, parse_error = parse_json_stdout(proc.stdout)
    results = result_items(parsed)

    path_found = parsed is not None and path_seen_in_results(parsed, expected_path)
    marker_found = True if required_marker is None else (
        parsed is not None and marker_seen_in_results(parsed, expected_path, required_marker)
    )
    recall_pass = proc.returncode == 0 and parsed is not None and path_found and marker_found

    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "suite": "M28.3 Post-refresh recall verification",
        "status": "PASS" if recall_pass else "FAIL",
        "mode": "post_refresh_recall_verification",
        "timestamp_utc": stamp,
        "project": project,
        "query": query,
        "expected_path": expected_path,
        "heading": heading,
        "required_marker": required_marker,
        "command": cmd,
        "returncode": proc.returncode,
        "parse_error": parse_error,
        "result_count": len(results),
        "checks": {
            "json_parse_ok": parsed is not None,
            "result_count_positive": len(results) > 0,
            "expected_path_found": path_found,
            "required_marker_found": marker_found,
            "recall_returncode_ok": proc.returncode == 0,
        },
        "evidence": {
            "operation_record": None,
            "post_refresh_recall_verified": recall_pass,
            "retrieval_provenance_checked": True,
            "checked_only_retrieval_results": True,
        },
        "mutations": {
            "trusted_wiki_mutated": False,
            "database_mutated": False,
            "importer_mutated": False,
            "proposal_state_mutated": False,
            "operation_record_written": False,
        },
        "stdout_tail": "\n".join((proc.stdout or "").splitlines()[-60:]),
        "stderr_tail": "\n".join((proc.stderr or "").splitlines()[-30:]),
    }

    if write_record:
        out_dir = root / "operations" / "runes-recall-verify" / stamp[:8]
        out_dir.mkdir(parents=True, exist_ok=True)
        record = out_dir / f"{stamp}-{project}-recall-verify.json"
        payload["evidence"]["operation_record"] = str(record.relative_to(root))
        payload["mutations"]["operation_record_written"] = True
        record.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return payload


def render_markdown(payload: dict[str, Any]) -> str:
    checks = payload.get("checks", {})
    evidence = payload.get("evidence", {})
    return "\n".join([
        "## Post-refresh Recall Verification",
        "",
        f"Status: {payload.get('status')}",
        f"Project: {payload.get('project')}",
        f"Query: {payload.get('query')}",
        f"Expected path: {payload.get('expected_path')}",
        f"Required marker: {payload.get('required_marker')}",
        f"Result count: {payload.get('result_count')}",
        "",
        "### Checks",
        "",
        f"- JSON parse OK: {checks.get('json_parse_ok')}",
        f"- Result count positive: {checks.get('result_count_positive')}",
        f"- Recall returncode OK: {checks.get('recall_returncode_ok')}",
        f"- Expected path found: {checks.get('expected_path_found')}",
        f"- Required marker found: {checks.get('required_marker_found')}",
        "",
        "### Evidence",
        "",
        f"- Operation record: {evidence.get('operation_record')}",
        f"- Post-refresh recall verified: {evidence.get('post_refresh_recall_verified')}",
        f"- Checked only retrieval results: {evidence.get('checked_only_retrieval_results')}",
        "",
    ])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Post-refresh recall verification helper.")
    parser.add_argument("query")
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--expected-path", required=True)
    parser.add_argument("--required-marker")
    parser.add_argument("--heading")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--write-record", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--markdown", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    payload = build_recall_verification(
        root=find_repo_root(),
        project=args.project,
        query=args.query,
        expected_path=args.expected_path,
        required_marker=args.required_marker,
        heading=args.heading,
        limit=args.limit,
        write_record=args.write_record,
    )
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    elif args.markdown:
        print(render_markdown(payload))
    else:
        print(render_markdown(payload))
    return 0 if payload.get("status") == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
