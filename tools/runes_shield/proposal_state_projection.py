#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

from build_proposal_manifest import build_manifest
from proposal_attunement_decision import find_decisions

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_CHOICES = ("table", "json")
DECISION_STATE_MAP = {
    "approved": "approved_pending_apply",
    "rejected": "rejected",
    "quarantined": "quarantined",
}


def derive_state(entry, decisions):
    if entry["validation_status"] != "PASS":
        return "invalid"

    if not decisions:
        return "pending_review"

    latest_decision = decisions[-1]["payload"]["decision"]
    return DECISION_STATE_MAP.get(latest_decision, "pending_review")


def build_projection():
    manifest = build_manifest()
    states = []

    for entry in manifest["entries"]:
        decisions = find_decisions(entry["proposal_id"])
        effective_state = derive_state(entry, decisions)
        latest_decision = decisions[-1]["payload"] if decisions else None

        states.append(
            {
                "proposal_id": entry["proposal_id"],
                "proposal_source": entry.get("proposal_source", "fixture"),
                "proposal_path": entry.get("proposal_path", entry["proposal_fixture"]),
                "validation_status": entry["validation_status"],
                "sample_status": entry["sample_status"],
                "effective_state": effective_state,
                "decision_count": len(decisions),
                "latest_decision": latest_decision["decision"] if latest_decision else None,
                "write": False,
            }
        )

    return {
        "projection_version": "m43-proposal-state-projection-v1",
        "source_manifest": manifest["manifest_version"],
        "entry_count": len(states),
        "write": False,
        "effects": {
            "proposal_file_modified": False,
            "trusted_wiki_write": False,
            "automatic_approval": False,
            "automatic_promotion": False,
            "apply_execution": False,
            "database_mutation": False,
        },
        "states": states,
    }


def find_state(states, proposal_id):
    for state in states:
        if state["proposal_id"] == proposal_id:
            return state
    return None


def render_table(states):
    if not states:
        return "No proposal states found."

    headers = ["effective_state", "validation", "decisions", "proposal_id"]
    rows = [
        [
            state["effective_state"],
            state["validation_status"],
            str(state["decision_count"]),
            state["proposal_id"],
        ]
        for state in states
    ]

    widths = [
        max(len(str(row[index])) for row in [headers] + rows)
        for index in range(len(headers))
    ]

    def fmt(row):
        return "  ".join(
            str(value).ljust(widths[index])
            for index, value in enumerate(row)
        )

    lines = [fmt(headers), fmt(["-" * width for width in widths])]
    lines.extend(fmt(row) for row in rows)
    return "\n".join(lines)


def emit_json(payload):
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="Derived-only proposal lifecycle state projection."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List derived proposal states.")
    list_parser.add_argument("--format", choices=OUTPUT_CHOICES, default="table")

    show_parser = subparsers.add_parser("show", help="Show derived state for one proposal_id.")
    show_parser.add_argument("proposal_id")
    show_parser.add_argument("--format", choices=OUTPUT_CHOICES, default="table")

    args = parser.parse_args()
    projection = build_projection()

    if args.command == "list":
        if args.format == "json":
            emit_json(projection)
            return
        print(render_table(projection["states"]))
        return

    if args.command == "show":
        state = find_state(projection["states"], args.proposal_id)
        if state is None:
            raise SystemExit(f"proposal state not found: {args.proposal_id}")

        if args.format == "json":
            emit_json(
                {
                    "projection_version": projection["projection_version"],
                    "write": False,
                    "state": state,
                }
            )
            return

        print(render_table([state]))
        return


if __name__ == "__main__":
    main()
