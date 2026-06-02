#!/usr/bin/env python3
# M29.1 P0 pre-trial add-knowledge scenario helper.

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from promotion_apply_preflight_m26_2 import sha256_file
    from promotion_apply_m27_2 import build_apply_result
    from import_refresh_m28_2 import run_import_refresh
    from recall_verify_m28_3 import build_recall_verification
except ImportError:  # pragma: no cover
    from tools.runes.promotion_apply_preflight_m26_2 import sha256_file
    from tools.runes.promotion_apply_m27_2 import build_apply_result
    from tools.runes.import_refresh_m28_2 import run_import_refresh
    from tools.runes.recall_verify_m28_3 import build_recall_verification

SCHEMA_VERSION = "m29.1.p0.v2"
DEFAULT_PROJECT = "k6-freelancer"
DEFAULT_TARGET_PATH = "wiki/k6-freelancer/p0-trial-scenarios.md"
DEFAULT_HEADING = "Scenario Evidence"
DEFAULT_PROPOSAL_ID = "m29-1-add-knowledge-scenario"
DEFAULT_MARKER = "M29.1_ADD_KNOWLEDGE_CANONICAL_MARKER"

DEFAULT_INSERT_TEXT = f"""\

### M29.1 Add Knowledge Scenario

Status: PASS CANDIDATE / controlled scenario evidence
Scenario ID: m29.1-add-knowledge
Marker: {DEFAULT_MARKER}

This scenario validates that newly provided knowledge can be appended to a trusted Markdown target through the governed P0 pipeline.

Knowledge statement:

```text
Hermes Runes MD Wiki P0 add-knowledge flow requires controlled apply, explicit importer refresh, and post-refresh recall verification before the knowledge is considered retrievable trusted memory.
```

Governance expectation:

- proposal-derived evidence is not trusted memory by itself
- controlled apply is required for trusted wiki mutation
- importer refresh is explicit and separate from apply
- recall verification is required after refresh
"""


def find_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def build_confirmation_token(proposal_id: str, target_path: str, pre_hash: str | None) -> str:
    return f"APPLY-PREFLIGHT:{proposal_id}:{target_path}:{pre_hash or 'missing'}"


def run_add_knowledge_scenario(
    *,
    root: Path,
    project: str,
    proposal_id: str,
    target_path: str,
    heading: str,
    insert_text: str,
    required_marker: str,
    actor: str,
    apply: bool,
    refresh: bool,
    verify_recall: bool,
    write_records: bool,
    recall_heading: str | None,
) -> dict[str, Any]:
    target_abs = root / target_path
    pre_hash = sha256_file(target_abs)
    confirmation = build_confirmation_token(proposal_id, target_path, pre_hash)

    if not apply:
        return {
            "schema_version": SCHEMA_VERSION,
            "suite": "M29.1 P0 add-knowledge scenario",
            "status": "BLOCKED",
            "reason": "--apply is required because M29.1 is an end-to-end controlled scenario",
            "project": project,
            "proposal_id": proposal_id,
            "target_path": target_path,
            "required_confirmation_token": confirmation,
            "pre_apply_sha256": pre_hash,
            "mutations": {
                "trusted_wiki_mutated": False,
                "refresh_attempted": False,
                "recall_verified": False,
            },
        }

    apply_result = build_apply_result(
        root=root,
        project=project,
        proposal_id=proposal_id,
        target_path=target_path,
        heading=heading,
        insert_text=insert_text,
        expected_pre_hash=pre_hash,
        human_confirmation=confirmation,
        reason="M29.1 P0 add-knowledge scenario controlled apply",
        apply=True,
        actor=actor,
    )

    refresh_result: dict[str, Any] | None = None
    recall_result: dict[str, Any] | None = None

    if apply_result.get("status") == "PASS" and refresh:
        refresh_result = run_import_refresh(
            root=root,
            project=project,
            target_path=target_path,
            actor=actor,
            reason="M29.1 P0 add-knowledge scenario refresh",
            refresh=True,
            write_record=write_records,
        )

    if (
        apply_result.get("status") == "PASS"
        and (refresh_result is None or refresh_result.get("status") == "PASS")
        and verify_recall
    ):
        recall_result = build_recall_verification(
            root=root,
            project=project,
            query=required_marker,
            expected_path=target_path,
            required_marker=required_marker,
            heading=recall_heading,
            limit=5,
            write_record=write_records,
        )

    checks = {
        "controlled_apply_pass": apply_result.get("status") == "PASS",
        "refresh_pass": refresh_result is not None and refresh_result.get("status") == "PASS",
        "recall_pass": recall_result is not None and recall_result.get("status") == "PASS",
        "marker_verified": bool((recall_result or {}).get("checks", {}).get("required_marker_found")),
        "expected_path_verified": bool((recall_result or {}).get("checks", {}).get("expected_path_found")),
        "result_count_positive": bool((recall_result or {}).get("checks", {}).get("result_count_positive")),
    }

    status = "PASS" if all(checks.values()) else "FAIL"

    return {
        "schema_version": SCHEMA_VERSION,
        "suite": "M29.1 P0 add-knowledge scenario",
        "status": status,
        "project": project,
        "proposal_id": proposal_id,
        "target_path": target_path,
        "heading": heading,
        "recall_heading": recall_heading,
        "required_marker": required_marker,
        "checks": checks,
        "apply": apply_result,
        "refresh": refresh_result,
        "recall": recall_result,
        "mutations": {
            "trusted_wiki_mutated": apply_result.get("status") == "PASS",
            "refresh_attempted": refresh_result is not None,
            "recall_verified": recall_result is not None and recall_result.get("status") == "PASS",
            "proposal_state_mutated": False,
            "attunement_state_mutated": False,
            "promotion_state_mutated": False,
        },
        "boundaries": {
            "scenario_target_is_dedicated": True,
            "controlled_apply_required": True,
            "explicit_refresh_required": True,
            "post_refresh_recall_required": True,
            "autonomous_apply": False,
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="M29.1 add-knowledge P0 scenario runner.")
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--proposal-id", default=DEFAULT_PROPOSAL_ID)
    parser.add_argument("--target-path", default=DEFAULT_TARGET_PATH)
    parser.add_argument("--heading", default=DEFAULT_HEADING)
    parser.add_argument("--recall-heading", default=None)
    parser.add_argument("--required-marker", default=DEFAULT_MARKER)
    parser.add_argument("--actor", default="human")
    parser.add_argument("--insert-text", default=DEFAULT_INSERT_TEXT)
    parser.add_argument("--apply", action="store_true", required=True)
    parser.add_argument("--refresh", action="store_true", required=True)
    parser.add_argument("--verify-recall", action="store_true", required=True)
    parser.add_argument("--write-records", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    payload = run_add_knowledge_scenario(
        root=find_repo_root(),
        project=args.project,
        proposal_id=args.proposal_id,
        target_path=args.target_path,
        heading=args.heading,
        insert_text=args.insert_text,
        required_marker=args.required_marker,
        actor=args.actor,
        apply=args.apply,
        refresh=args.refresh,
        verify_recall=args.verify_recall,
        write_records=args.write_records,
        recall_heading=args.recall_heading,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload.get("status") == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
