#!/usr/bin/env python3
"""M24.2 Runes Attunement trail dry-run helper.

Dry-run only:
- no trail file write
- no proposal state mutation
- no trusted wiki mutation
- no database mutation
- no importer mutation
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from proposal_attunement_m23_2 import TARGET_STATES, VALID_ACTIONS, attunement_dry_run
except ImportError:  # pragma: no cover
    from tools.runes.proposal_attunement_m23_2 import TARGET_STATES, VALID_ACTIONS, attunement_dry_run

SCHEMA_VERSION = "m24.2.p0.v1"
DEFAULT_PROJECT = "k6-freelancer"


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def build_attunement_trail_dry_run(
    root: Path,
    project: str,
    proposal_id: str,
    action: str,
    reason: str | None = None,
    actor: str = "human",
    superseded_by: str | None = None,
    output_root: str | None = None,
) -> dict[str, Any]:
    if action not in VALID_ACTIONS:
        raise ValueError(f"unsupported attunement action: {action}")

    attunement = attunement_dry_run(
        root=root,
        project=project,
        proposal_id=proposal_id,
        action=action,
        reason=reason,
        superseded_by=superseded_by,
        output_root=output_root,
    )

    current_state = attunement.get("current_state")
    target_state = attunement.get("target_state") or TARGET_STATES[action]
    trail_preview = attunement.get("attunement_trail_preview") or {}

    event = {
        "event_id": "DRY-RUN",
        "event_type": f"proposal.{action}.dry_run",
        "proposal_id": proposal_id,
        "project": project,
        "old_state": current_state,
        "new_state": target_state,
        "actor": actor,
        "decision_reason": reason,
        "superseded_by": superseded_by,
        "timestamp": _now_iso(),
        "dry_run": True,
        "trusted_wiki_mutated": False,
        "database_mutated": False,
        "proposal_state_mutated": False,
        "importer_mutated": False,
        "promotion_executed": False,
        "source_attunement_status": attunement.get("status"),
        "source_path": trail_preview.get("path"),
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "suite": "M24.2 Runes Attunement trail dry-run",
        "status": "PASS",
        "mode": "dry_run_only",
        "project": project,
        "proposal_id": proposal_id,
        "action": action,
        "trail": {
            "name": "Runes Attunement Trail",
            "chinese": "符文調律軌跡",
            "append_only_design": True,
            "trail_write_implemented": False,
            "trusted_memory": False,
            "governance_evidence": True,
        },
        "event_preview": event,
        "source_attunement": attunement,
        "preview": {
            "would_write_trail_file": False,
            "would_append_event_later": True,
            "would_update_proposal_metadata": False,
            "would_promote_to_wiki": False,
            "would_mutate_database": False,
            "would_run_importer": False,
        },
        "mutations": {
            "trail_file_written": False,
            "proposal_state_mutated": False,
            "trusted_memory_created": False,
            "curated_wiki_mutated": False,
            "database_mutated": False,
            "importer_mutated": False,
            "files_written": False,
        },
    }


def render_trail_markdown_preview(result: dict[str, Any]) -> str:
    event = result.get("event_preview") or {}
    mutations = result.get("mutations") or {}
    preview = result.get("preview") or {}

    lines = [
        "## Runes Attunement Trail Event Preview",
        "",
        f"Status: {result.get('status')}",
        f"Mode: {result.get('mode')}",
        f"Project: {result.get('project')}",
        f"Proposal ID: {result.get('proposal_id')}",
        f"Action: {result.get('action')}",
        "",
        "### Event",
        "",
        f"- Event ID: {event.get('event_id')}",
        f"- Event type: {event.get('event_type')}",
        f"- Old state: {event.get('old_state')}",
        f"- New state: {event.get('new_state')}",
        f"- Actor: {event.get('actor')}",
        f"- Decision reason: {event.get('decision_reason')}",
        f"- Timestamp: {event.get('timestamp')}",
        f"- Dry-run: {event.get('dry_run')}",
        "",
        "### Boundary",
        "",
        "- Trail is governance evidence, not trusted wiki memory.",
        f"- Would write trail file now: {preview.get('would_write_trail_file', False)}",
        f"- Would append event later: {preview.get('would_append_event_later', False)}",
        f"- Proposal state mutation now: {mutations.get('proposal_state_mutated', False)}",
        f"- Trusted wiki mutation now: {mutations.get('curated_wiki_mutated', False)}",
        f"- Trusted memory created now: {mutations.get('trusted_memory_created', False)}",
        f"- Database mutation now: {mutations.get('database_mutated', False)}",
        f"- Importer mutation now: {mutations.get('importer_mutated', False)}",
        f"- Files written now: {mutations.get('files_written', False)}",
        "",
        "### Current scope",
        "",
        "This is a Markdown preview only. M24.3 does not write an append-only trail file.",
        "",
    ]

    superseded_by = event.get("superseded_by")
    if superseded_by:
        lines.insert(16, f"- Superseded by: {superseded_by}")

    return "\n".join(lines)

def print_trail_preview(result: dict[str, Any]) -> None:
    event = result.get("event_preview") or {}
    preview = result.get("preview") or {}
    mutations = result.get("mutations") or {}

    print("Runes Attunement Trail Preview")
    print("==============================")
    print(f"Status: {result.get('status')}")
    print(f"Mode: {result.get('mode')}")
    print(f"Project: {result.get('project')}")
    print(f"Proposal ID: {result.get('proposal_id')}")
    print(f"Action: {result.get('action')}")

    print("")
    print("Event preview:")
    print(f"- Event type: {event.get('event_type')}")
    print(f"- Old state: {event.get('old_state')}")
    print(f"- New state: {event.get('new_state')}")
    print(f"- Actor: {event.get('actor')}")
    print(f"- Reason: {event.get('decision_reason')}")
    print(f"- Dry-run: {event.get('dry_run')}")

    superseded_by = event.get("superseded_by")
    if superseded_by:
        print(f"- Superseded by: {superseded_by}")

    print("")
    print("Trail boundary:")
    print("- Trail is governance evidence, not trusted wiki memory.")
    print(f"- Would write trail file now: {preview.get('would_write_trail_file', False)}")
    print(f"- Would append event later: {preview.get('would_append_event_later', False)}")
    print(f"- Proposal state mutation now: {mutations.get('proposal_state_mutated', False)}")
    print(f"- Trusted wiki mutation now: {mutations.get('curated_wiki_mutated', False)}")
    print(f"- Database mutation now: {mutations.get('database_mutated', False)}")
    print(f"- Importer mutation now: {mutations.get('importer_mutated', False)}")
    print(f"- Files written now: {mutations.get('files_written', False)}")

    print("")
    print("Use --json for agent-facing structured output.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Runes Attunement trail dry-run helper.")
    parser.add_argument("action", choices=sorted(VALID_ACTIONS))
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--id", required=True)
    parser.add_argument("--reason")
    parser.add_argument("--actor", default="human")
    parser.add_argument("--superseded-by")
    parser.add_argument("--output-root")
    parser.add_argument("--dry-run", action="store_true", required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--markdown", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(__file__).resolve().parents[2]
    result = build_attunement_trail_dry_run(
        root=root,
        project=args.project,
        proposal_id=args.id,
        action=args.action,
        reason=args.reason,
        actor=args.actor,
        superseded_by=args.superseded_by,
        output_root=args.output_root,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    elif args.markdown:
        print(render_trail_markdown_preview(result))
    else:
        print_trail_preview(result)

    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
