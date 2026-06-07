#!/usr/bin/env python3
"""M23.2/M23.3 Runes Attunement dry-run helper.

Dry-run only:
- no proposal state mutation
- no trusted wiki mutation
- no database mutation
- no importer mutation

M23.3 adds a human-readable non-JSON preview while preserving the
machine-readable JSON payload from M23.2.
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

SCHEMA_VERSION = "m23.3.p0.v1"
DEFAULT_PROJECT = "k6-freelancer"
VALID_ACTIONS = {"attune", "reject", "supersede"}

ACTION_MEANINGS = {
    "attune": "Accept this proposal as an attuned promotion candidate. This does not promote it into trusted wiki memory.",
    "reject": "Reject this proposal's attunement. This does not delete the proposal or mutate trusted memory.",
    "supersede": "Mark this proposal as conceptually replaced by a newer attunement candidate. This does not move files in M23.",
}

TARGET_STATES = {
    "attune": "approved",
    "reject": "rejected",
    "supersede": "superseded",
}


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
            "suite": "M23.3 Runes Attunement readable dry-run",
            "status": "NOT_FOUND",
            "mode": "dry_run_only",
            "project": project,
            "proposal_id": proposal_id,
            "action": action,
            "readable_preview_available": True,
            "meaning": ACTION_MEANINGS[action],
            "mutations": _no_mutations(),
        }

    current_state, path = resolved
    proposal = show_proposal(root, project, proposal_id, output_root, include_body=False)
    target_state = TARGET_STATES[action]

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
        "suite": "M23.3 Runes Attunement readable dry-run",
        "status": status,
        "mode": "dry_run_only",
        "project": project,
        "proposal_id": proposal_id,
        "action": action,
        "readable_preview_available": True,
        "meaning": ACTION_MEANINGS[action],
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


def print_readable_preview(result: dict[str, Any]) -> None:
    proposal = result.get("proposal") or {}
    preview = result.get("preview") or {}
    mutations = result.get("mutations") or {}
    trail = result.get("attunement_trail_preview") or {}

    print("Runes Attunement Preview")
    print("=========================")
    print(f"Status: {result.get('status')}")
    print(f"Mode: {result.get('mode')}")
    print(f"Project: {result.get('project')}")
    print(f"Proposal ID: {result.get('proposal_id')}")
    print(f"Action: {result.get('action')}")

    title = proposal.get("title")
    if title:
        print(f"Title: {title}")

    rel_path = proposal.get("relative_path") or trail.get("path")
    if rel_path:
        print(f"Path: {rel_path}")

    if result.get("current_state") or result.get("target_state"):
        print(f"State: {result.get('current_state')} -> {result.get('target_state')}")

    print("")
    print("Meaning:")
    print(f"- {result.get('meaning')}")
    print("- Approval/attunement does not mean trusted wiki promotion.")
    print("- Promotion remains a later human-governed memory forging step.")

    reason = result.get("reason")
    if reason:
        print("")
        print("Decision reason:")
        print(f"- {reason}")

    superseded_by = result.get("superseded_by")
    if superseded_by:
        print("")
        print("Superseded by:")
        print(f"- {superseded_by}")

    blockers = result.get("blockers") or []
    if blockers:
        print("")
        print("Blockers:")
        for blocker in blockers:
            print(f"- {blocker}")

    print("")
    print("Dry-run boundary:")
    print(f"- Would update proposal metadata later: {preview.get('would_update_proposal_metadata', False)}")
    print(f"- Would move/reclassify proposal later: {preview.get('would_move_or_reclassify_proposal', False)}")
    print(f"- Trusted wiki mutation now: {mutations.get('curated_wiki_mutated', False)}")
    print(f"- Trusted memory created now: {mutations.get('trusted_memory_created', False)}")
    print(f"- Database mutation now: {mutations.get('database_mutated', False)}")
    print(f"- Importer mutation now: {mutations.get('importer_mutated', False)}")
    print(f"- Files written now: {mutations.get('files_written', False)}")

    if trail:
        print("")
        print("Attunement trail preview:")
        print(f"- Event: {trail.get('event_type')}")
        print(f"- Old state: {trail.get('old_state')}")
        print(f"- New state: {trail.get('new_state')}")

    print("")
    print("Use --json for agent-facing structured output.")


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
        print_readable_preview(result)

    return 0 if result["status"] in {"PASS", "NOT_FOUND"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
