#!/usr/bin/env python3
"""M22.4 human cleanup plan dry-run.

Transforms proposal hygiene warnings into human-reviewable cleanup steps.
This module never moves files, rewrites metadata, changes proposal states,
promotes content, imports content, or mutates database/index records.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from proposal_hygiene_m22_3 import hygiene_report
except ImportError:  # pragma: no cover
    from tools.runes.proposal_hygiene_m22_3 import hygiene_report

SCHEMA_VERSION = "m22.4.p0.v1"
DEFAULT_PROJECT = "k6-freelancer"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def action_for_issue(issue: dict[str, Any]) -> dict[str, Any]:
    issue_type = issue.get("type")
    directory_state = issue.get("directory_state")
    metadata_status = issue.get("metadata_status")
    relative_path = issue.get("relative_path")

    if issue_type == "directory_state_metadata_status_mismatch":
        return {
            "action_type": "review_state_mismatch",
            "proposal_id": issue.get("proposal_id"),
            "title": issue.get("title"),
            "relative_path": relative_path,
            "current_directory_state": directory_state,
            "frontmatter_status": metadata_status,
            "recommended_human_decision": "choose_directory_state_or_metadata_status_as_source_of_truth",
            "candidate_manual_resolutions": [
                {
                    "option": "treat_as_historical_draft",
                    "description": "Keep file in forge-inbox and manually change frontmatter status to draft after human review.",
                    "requires_write": True,
                    "human_only": True,
                },
                {
                    "option": "move_to_matching_state_folder",
                    "description": "Move file to the folder matching frontmatter status after human review.",
                    "requires_write": True,
                    "human_only": True,
                },
                {
                    "option": "leave_as_known_legacy_mismatch",
                    "description": "Do not change content; keep warning as known historical hygiene issue.",
                    "requires_write": False,
                    "human_only": True,
                },
            ],
            "dry_run_only": True,
        }

    if issue_type == "missing_metadata_status":
        return {
            "action_type": "review_missing_status",
            "proposal_id": issue.get("proposal_id"),
            "title": issue.get("title"),
            "relative_path": relative_path,
            "recommended_human_decision": "add_frontmatter_status_after_review",
            "candidate_manual_resolutions": [
                {
                    "option": "add_status_draft",
                    "description": "Manually add status: draft if the file should remain in forge-inbox.",
                    "requires_write": True,
                    "human_only": True,
                },
                {
                    "option": "leave_as_known_legacy_missing_status",
                    "description": "Do not change content; keep warning as known historical hygiene issue.",
                    "requires_write": False,
                    "human_only": True,
                },
            ],
            "dry_run_only": True,
        }

    return {
        "action_type": "review_unknown_issue",
        "proposal_id": issue.get("proposal_id"),
        "title": issue.get("title"),
        "relative_path": relative_path,
        "recommended_human_decision": "manual_review_required",
        "candidate_manual_resolutions": [
            {
                "option": "manual_review",
                "description": "Inspect the issue and decide whether a separate human-approved cleanup is needed.",
                "requires_write": False,
                "human_only": True,
            }
        ],
        "dry_run_only": True,
    }


def cleanup_plan(root: Path, project: str, output_root: str | None = None) -> dict[str, Any]:
    report = hygiene_report(root, project, output_root)
    actions = [action_for_issue(issue) for issue in report.get("issues", [])]

    return {
        "schema_version": SCHEMA_VERSION,
        "suite": "M22.4 Human cleanup plan dry-run",
        "status": "PASS",
        "mode": "dry_run_only",
        "project": project,
        "source_report_schema_version": report.get("schema_version"),
        "source_report_status": report.get("status"),
        "proposal_count": report.get("proposal_count"),
        "issue_count": report.get("issue_count"),
        "planned_action_count": len(actions),
        "planned_actions": actions,
        "execution_allowed": False,
        "human_approval_required_before_any_cleanup": True,
        "agent_may_execute_cleanup": False,
        "mutations": {
            "files_moved": False,
            "metadata_mutated": False,
            "proposal_state_mutated": False,
            "trusted_memory_created": False,
            "curated_wiki_mutated": False,
            "database_mutated": False,
            "importer_mutated": False,
        },
        "next_human_actions": [
            "review planned_actions",
            "choose whether each issue should be fixed or kept as legacy mismatch",
            "create a separate human-approved cleanup operation if writes are desired",
            "run proposal hygiene again after any future human cleanup",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate human cleanup plan dry-run from proposal hygiene report.")
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--output-root", help="Optional alternate root for sandbox/smoke proposal reads.")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = cleanup_plan(repo_root(), args.project, args.output_root)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"{result['suite']}: {result['status']}")
        print(f"issue_count={result['issue_count']} planned_action_count={result['planned_action_count']}")
        print("Use --json for details.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
