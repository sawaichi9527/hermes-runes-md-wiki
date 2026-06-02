#!/usr/bin/env python3
"""M22.3 read-only proposal status hygiene report.

This helper detects proposal state hygiene issues without mutating files.
It reports mismatches between directory-derived state and frontmatter status,
plus draft proposals that accidentally claim trusted memory.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from proposal_reader_m22_2 import list_proposals
except ImportError:  # pragma: no cover
    from tools.runes.proposal_reader_m22_2 import list_proposals

SCHEMA_VERSION = "m22.3.p0.v1"
DEFAULT_PROJECT = "k6-freelancer"
VALID_STATES = {"draft", "approved", "rejected"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def normalize_status(value: str | None) -> str | None:
    if value is None:
        return None
    return str(value).strip().lower() or None


def classify_item(item: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    directory_state = item.get("state")
    metadata_status = normalize_status(item.get("metadata_status"))
    trusted_memory = normalize_status(item.get("trusted_memory"))

    if metadata_status is None:
        issues.append(
            {
                "type": "missing_metadata_status",
                "severity": "warning",
                "message": "proposal frontmatter has no status field",
            }
        )
    elif metadata_status not in VALID_STATES:
        issues.append(
            {
                "type": "unknown_metadata_status",
                "severity": "warning",
                "message": f"proposal frontmatter status is not recognized: {metadata_status}",
            }
        )
    elif directory_state != metadata_status:
        issues.append(
            {
                "type": "directory_state_metadata_status_mismatch",
                "severity": "warning",
                "message": f"directory state is {directory_state}, but frontmatter status is {metadata_status}",
            }
        )

    if directory_state == "draft" and trusted_memory == "true":
        issues.append(
            {
                "type": "draft_claims_trusted_memory",
                "severity": "error",
                "message": "draft proposal claims trusted_memory=true",
            }
        )

    return issues


def hygiene_report(root: Path, project: str, output_root: str | None = None) -> dict[str, Any]:
    listing = list_proposals(root, project, "all", output_root)
    items = listing.get("items", [])

    issues: list[dict[str, Any]] = []
    for item in items:
        for issue in classify_item(item):
            issues.append(
                {
                    **issue,
                    "proposal_id": item.get("proposal_id"),
                    "title": item.get("title"),
                    "directory_state": item.get("state"),
                    "metadata_status": item.get("metadata_status"),
                    "trusted_memory": item.get("trusted_memory"),
                    "relative_path": item.get("relative_path"),
                }
            )

    issue_counts: dict[str, int] = {}
    severity_counts: dict[str, int] = {}
    for issue in issues:
        issue_counts[issue["type"]] = issue_counts.get(issue["type"], 0) + 1
        severity_counts[issue["severity"]] = severity_counts.get(issue["severity"], 0) + 1

    status = "PASS" if not any(issue.get("severity") == "error" for issue in issues) else "FAIL"

    return {
        "schema_version": SCHEMA_VERSION,
        "suite": "M22.3 Read-only proposal status hygiene report",
        "status": status,
        "mode": "read_only",
        "project": project,
        "proposal_count": len(items),
        "issue_count": len(issues),
        "issue_counts": issue_counts,
        "severity_counts": severity_counts,
        "issues": issues,
        "mutations": {
            "proposal_state_mutated": False,
            "metadata_mutated": False,
            "trusted_memory_created": False,
            "curated_wiki_mutated": False,
            "database_mutated": False,
            "importer_mutated": False,
        },
        "next_human_actions": [
            "review mismatch warnings",
            "decide whether old forge-inbox files should remain historical drafts",
            "if needed, create a separate human-approved cleanup plan",
            "do not automatically move, rewrite, approve, reject, promote, import, or index from this report",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate read-only proposal status hygiene report.")
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--output-root", help="Optional alternate root for sandbox/smoke proposal reads.")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = hygiene_report(repo_root(), args.project, args.output_root)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"{result['suite']}: {result['status']}")
        print(f"proposal_count={result['proposal_count']} issue_count={result['issue_count']}")
        print("Use --json for details.")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
