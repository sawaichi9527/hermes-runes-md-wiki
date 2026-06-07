#!/usr/bin/env python3
# M28.2 controlled importer refresh helper.

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "m28.2.p0.v1"
DEFAULT_PROJECT = "k6-freelancer"
SUMMARY_RE = re.compile(
    r"summary:\s+schema=(?P<schema>\S+)\s+"
    r"imported_or_changed=(?P<imported>\d+)\s+"
    r"updated=(?P<updated>\d+)\s+"
    r"skipped=(?P<skipped>\d+)\s+"
    r"chunks_written=(?P<chunks>\d+)"
)


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def find_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def parse_summary(stdout: str) -> dict[str, Any]:
    match = SUMMARY_RE.search(stdout or "")
    if not match:
        return {
            "summary_found": False,
            "schema": None,
            "imported_or_changed": None,
            "updated": None,
            "skipped": None,
            "chunks_written": None,
        }
    return {
        "summary_found": True,
        "schema": match.group("schema"),
        "imported_or_changed": int(match.group("imported")),
        "updated": int(match.group("updated")),
        "skipped": int(match.group("skipped")),
        "chunks_written": int(match.group("chunks")),
    }


def build_refresh_operation_record(root: Path, payload: dict[str, Any]) -> Path:
    stamp = payload["timestamp_utc"]
    out_dir = root / "operations" / "runes-refresh" / stamp[:8]
    out_dir.mkdir(parents=True, exist_ok=True)
    record = out_dir / f"{stamp}-{payload['project']}-import-refresh.json"
    record.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return record


def run_import_refresh(
    *,
    root: Path,
    project: str,
    target_path: str | None,
    actor: str,
    reason: str | None,
    refresh: bool,
    write_record: bool,
) -> dict[str, Any]:
    stamp = utc_stamp()
    importer_dir = root / "tools" / "importer"
    importer_script = importer_dir / "importer.py"

    hard_errors: list[str] = []
    if not refresh:
        hard_errors.append("--refresh is required for controlled importer refresh")
    if not importer_script.exists():
        hard_errors.append("tools/importer/importer.py not found")
    if target_path is not None:
        rel = Path(target_path)
        try:
            abs_target = (root / rel).resolve()
            abs_target.relative_to(root.resolve())
        except ValueError:
            hard_errors.append("target path escapes repository root")
        if not str(rel).startswith("wiki/"):
            hard_errors.append("target path must be under wiki/")

    if hard_errors:
        return {
            "schema_version": SCHEMA_VERSION,
            "suite": "M28.2 Controlled importer refresh",
            "status": "BLOCKED",
            "mode": "controlled_refresh",
            "timestamp_utc": stamp,
            "project": project,
            "target_path": target_path,
            "actor": actor,
            "reason": reason,
            "hard_errors": hard_errors,
            "mutations": {
                "trusted_wiki_mutated": False,
                "database_refresh_attempted": False,
                "importer_executed": False,
                "operation_record_written": False,
            },
        }

    env = os.environ.copy()
    env.setdefault("PYTHONUNBUFFERED", "1")

    proc = subprocess.run(
        ["python", str(importer_script)],
        cwd=str(importer_dir),
        env=env,
        text=True,
        capture_output=True,
        timeout=300,
        check=False,
    )

    summary = parse_summary(proc.stdout)
    status = "PASS" if proc.returncode == 0 and summary.get("summary_found") else "FAIL"

    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "suite": "M28.2 Controlled importer refresh",
        "status": status,
        "mode": "controlled_refresh",
        "timestamp_utc": stamp,
        "project": project,
        "target_path": target_path,
        "actor": actor,
        "reason": reason,
        "command": ["python", "tools/importer/importer.py"],
        "returncode": proc.returncode,
        "summary": summary,
        "stdout_tail": "\n".join((proc.stdout or "").splitlines()[-30:]),
        "stderr_tail": "\n".join((proc.stderr or "").splitlines()[-30:]),
        "evidence": {
            "operation_record": None,
            "post_refresh_recall_verification_required": True,
            "retrieval_refresh_explicitly_invoked": True,
        },
        "mutations": {
            "trusted_wiki_mutated": False,
            "database_refresh_attempted": True,
            "importer_executed": True,
            "operation_record_written": False,
            "proposal_state_mutated": False,
            "attunement_state_mutated": False,
            "promotion_state_mutated": False,
        },
        "boundaries": {
            "trusted_wiki_apply_is_not_implicit_importer_refresh": True,
            "refresh_is_explicit": True,
            "autonomous_refresh": False,
            "post_refresh_recall_required": True,
        },
    }

    if write_record:
        record = build_refresh_operation_record(root, payload)
        payload["evidence"]["operation_record"] = str(record.relative_to(root))
        payload["mutations"]["operation_record_written"] = True
        record.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return payload


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    mutations = payload.get("mutations", {})
    evidence = payload.get("evidence", {})
    lines = [
        "## Controlled Importer Refresh",
        "",
        f"Status: {payload.get('status')}",
        f"Mode: {payload.get('mode')}",
        f"Project: {payload.get('project')}",
        f"Target path: {payload.get('target_path')}",
        "",
        "### Import summary",
        "",
        f"- Summary found: {summary.get('summary_found')}",
        f"- Schema: {summary.get('schema')}",
        f"- Imported or changed: {summary.get('imported_or_changed')}",
        f"- Updated: {summary.get('updated')}",
        f"- Skipped: {summary.get('skipped')}",
        f"- Chunks written: {summary.get('chunks_written')}",
        "",
        "### Evidence",
        "",
        f"- Operation record: {evidence.get('operation_record')}",
        f"- Post-refresh recall verification required: {evidence.get('post_refresh_recall_verification_required')}",
        "",
        "### Boundary",
        "",
        f"- Trusted wiki mutated: {mutations.get('trusted_wiki_mutated')}",
        f"- Importer executed: {mutations.get('importer_executed')}",
        f"- Database refresh attempted: {mutations.get('database_refresh_attempted')}",
        f"- Proposal state mutated: {mutations.get('proposal_state_mutated')}",
        f"- Operation record written: {mutations.get('operation_record_written')}",
        "",
    ]
    if payload.get("hard_errors"):
        lines.extend(["### Blocking errors", ""])
        lines.extend(f"- {item}" for item in payload["hard_errors"])
        lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Controlled importer refresh boundary helper.")
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--target-path")
    parser.add_argument("--actor", default="human")
    parser.add_argument("--reason")
    parser.add_argument("--refresh", action="store_true", required=True)
    parser.add_argument("--write-record", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--markdown", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = find_repo_root()
    payload = run_import_refresh(
        root=root,
        project=args.project,
        target_path=args.target_path,
        actor=args.actor,
        reason=args.reason,
        refresh=args.refresh,
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
