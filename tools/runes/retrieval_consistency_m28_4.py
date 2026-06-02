#!/usr/bin/env python3
# M28.4 retrieval consistency smoke helper.

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from recall_verify_m28_3 import build_recall_verification, find_repo_root
except ImportError:  # pragma: no cover
    from tools.runes.recall_verify_m28_3 import build_recall_verification, find_repo_root

SCHEMA_VERSION = "m28.4.p0.v1"
DEFAULT_PROJECT = "k6-freelancer"

DEFAULT_CASES = [
    {
        "id": "m27_controlled_apply_baseline",
        "query": "controlled trusted wiki mutation baseline",
        "expected_path": "wiki/k6-freelancer/verification-m27-human-approved-apply-mvp.md",
        "required_marker": "CONTROLLED TRUSTED WIKI MUTATION BASELINE",
    },
    {
        "id": "m27_smoke_lock",
        "query": "M27.3 Controlled Apply Smoke Lock wrong-hash blocking verified",
        "expected_path": "wiki/k6-freelancer/verification-m27-3-controlled-apply-smoke-lock.md",
        "required_marker": "PASS / smoke verified / regression baseline locked",
    },
    {
        "id": "m28_refresh_boundary",
        "query": "trusted wiki apply != implicit importer mutation",
        "expected_path": "wiki/k6-freelancer/verification-m28-importer-retrieval-refresh-boundary.md",
        "required_marker": "trusted wiki apply != implicit importer mutation",
    },
]


def run_consistency_smoke(
    *,
    root: Path,
    project: str,
    limit: int,
    write_record: bool,
) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for case in DEFAULT_CASES:
        payload = build_recall_verification(
            root=root,
            project=project,
            query=case["query"],
            expected_path=case["expected_path"],
            required_marker=case["required_marker"],
            heading=None,
            limit=limit,
            write_record=write_record,
        )
        results.append({
            "id": case["id"],
            "status": payload.get("status"),
            "query": case["query"],
            "expected_path": case["expected_path"],
            "required_marker": case["required_marker"],
            "checks": payload.get("checks"),
            "evidence": payload.get("evidence"),
            "returncode": payload.get("returncode"),
            "parse_error": payload.get("parse_error"),
            "stderr_tail": payload.get("stderr_tail"),
        })

    failed = [item for item in results if item.get("status") != "PASS"]
    return {
        "schema_version": SCHEMA_VERSION,
        "suite": "M28.4 Retrieval Consistency Smoke",
        "status": "PASS" if not failed else "FAIL",
        "project": project,
        "case_count": len(results),
        "failed_count": len(failed),
        "results": results,
        "mutations": {
            "trusted_wiki_mutated": False,
            "database_mutated": False,
            "importer_mutated": False,
            "proposal_state_mutated": False,
            "operation_records_written_by_case_helpers": write_record,
        },
        "boundaries": {
            "retrieval_consistency_only": True,
            "post_refresh_recall_verification_reused": True,
            "refresh_not_executed_here": True,
            "apply_not_executed_here": True,
        },
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "## Retrieval Consistency Smoke",
        "",
        f"Status: {payload.get('status')}",
        f"Project: {payload.get('project')}",
        f"Cases: {payload.get('case_count')}",
        f"Failed: {payload.get('failed_count')}",
        "",
        "### Cases",
        "",
    ]
    for item in payload.get("results", []):
        checks = item.get("checks") or {}
        lines.extend([
            f"- {item.get('id')}: {item.get('status')}",
            f"  - expected_path_found: {checks.get('expected_path_found')}",
            f"  - required_marker_found: {checks.get('required_marker_found')}",
            f"  - json_parse_ok: {checks.get('json_parse_ok')}",
        ])
    lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="M28.4 retrieval consistency smoke helper.")
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--write-record", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--markdown", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    payload = run_consistency_smoke(
        root=find_repo_root(),
        project=args.project,
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
