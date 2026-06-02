#!/usr/bin/env python3
"""M23.2 Runes Attunement dry-run helper.

Dry-run only:
- no proposal state mutation
- no trusted wiki mutation
- no database mutation
- no importer mutation
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from proposal_reader_m22_2 import resolve_proposal, show_proposal
except ImportError:  # pragma: no cover
    from tools.runes.proposal_reader_m22_2 import resolve_proposal, show_proposal

SCHEMA_VERSION = "m23.2.p0.v1"
DEFAULT_PROJECT = "k6-freelancer"
VALID_ACTIONS = {"attune", "reject", "supersede"}


def attunement_dry_run(
    root: Path,
    project: str,
    proposal_id: str,
    action: str,
    reason: str | None = None,
    superseded_by: str | None = None,
    output_root: str | None = None,
) -> dict[str, Any]:
    if action not in VALID_ACTIONS:
        raise ValueError(f"unsupported attunement action: {action}")

    resolved = resolve_proposal(root, project, proposal_id, output_root)
    if not resolved:
        return {
            "schema_version": SCHEMA_VERSION,
            "suite": "M23.2 Runes Attunement dry-run",
            "status": "NOT_FOUND",
            "mode": "dry_run_only",
            "project": project,
            "proposal_id": proposal_id,
            "action": action,
            "mutations": _no_mutations(),
        }

    current_state, path = resolved
    proposal = show_proposal(root, project, proposal_id, output_root, include_body=False)

    target_state = {
        "attune": "approved",
        "reject": "rejected",
        "supersede": "superseded",
    }[action]

    blockers = []
    if action == "supersede" and not superseded_by:
        blockers.append("supersede_requires_superseded_by")
    if current_state == "approved" and action == "attune":
        blockers.append("already_attuned")
    if current_state == "rejected" and action == "reject":
        blockers.append("already_rejected")

    status = "PASS" if not blockers else "BLOCKED"

    return {
        "schema_version": SCHEMA_VERSION,
        "suite": "M23.2 Runes Attunement dry-run",
        "status": status,
        "mode": "dry_run_only",
        "project": project,
        "proposal_id": proposal_id,
        "action": action,
        "attunement": {
            "name": "Runes Attunement",
            "chinese": "符文調律",
            "approved_does_not_mean_promoted": True,
            "promotion_execution_implemented": False,
        },
        "proposal": proposal.get("proposal"),
        "current_state": current_state,
        "target_state": target_state,
        "reason": reason,
        "superseded_by": superseded_by,
        "blockers": blockers,
        "preview": {
            "would_update_proposal_metadata": True,
            "would_move_or_reclassify_proposal": True,
            "would_create_trusted_memory": False,
            "would_promote_to_wiki": False,
            "would_mutate_database": False,
            "would_run_importer": False,
            "human_confirmation_required_for_future_execute": True,
        },
        "attunement_trail_preview": {
            "event_type": f"proposal.{action}.dry_run",
            "old_state": current_state,
            "new_state": target_state,
            "path": str(path),
            "decision_reason": reason,
            "superseded_by": superseded_by,
        },
        "mutations": _no_mutations(),
    }


def _no_mutations() -> dict[str, bool]:
    return {
        "proposal_state_mutated": False,
        "trusted_memory_created": False,
        "curated_wiki_mutated": False,
        "database_mutated": False,
        "importer_mutated": False,
        "files_written": False,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Runes Attunement dry-run helper.")
    parser.add_argument("action", choices=sorted(VALID_ACTIONS))
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--id", required=True)
    parser.add_argument("--reason")
    parser.add_argument("--superseded-by")
    parser.add_argument("--output-root")
    parser.add_argument("--dry-run", action="store_true", required=True)
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(__file__).resolve().parents[2]
    result = attunement_dry_run(
        root=root,
        project=args.project,
        proposal_id=args.id,
        action=args.action,
        reason=args.reason,
        superseded_by=args.superseded_by,
        output_root=args.output_root,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"{result['suite']}: {result['status']}")
        print(f"action={result['action']} mode={result['mode']}")
        print("Use --json for details.")

    return 0 if result["status"] in {"PASS", "NOT_FOUND"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
