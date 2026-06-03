#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

from proposal_state_projection import build_projection

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_CHOICES = ("table", "json")


def slugify(value):
    return value.lower().replace(" ", "-").replace("_", "-")


def derive_target_path(state):
    source = state["proposal_source"]
    proposal_id = slugify(state["proposal_id"])
    return f"wiki/proposals/{source}/{proposal_id}.md"


def derive_heading(state):
    proposal_id = state["proposal_id"]
    return f"Proposal Apply Candidate: {proposal_id}"


def derive_index_hint(state):
    return "wiki/_system/proposal_apply_index.md"


def derive_metadata(state):
    return {
        "proposal_id": state["proposal_id"],
        "effective_state": state["effective_state"],
        "validation_status": state["validation_status"],
        "source": state["proposal_source"],
    }


def build_apply_plans():
    projection = build_projection()
    plans = []

    for state in projection["states"]:
        if state["effective_state"] != "approved_pending_apply":
            continue

        plans.append(
            {
                "proposal_id": state["proposal_id"],
                "effective_state": state["effective_state"],
                "candidate_target_path": derive_target_path(state),
                "candidate_heading": derive_heading(state),
                "candidate_index_hint": derive_index_hint(state),
                "candidate_metadata": derive_metadata(state),
                "write": False,
                "effects": {
                    "trusted_wiki_write": False,
                    "automatic_apply": False,
                    "automatic_promotion": False,
                    "database_mutation": False,
                },
            }
        )

    return {
        "apply_plan_version": "m44-apply-plan-v1",
        "source_projection": projection["projection_version"],
        "entry_count": len(plans),
        "write": False,
        "plans": plans,
    }


def find_plan(plans, proposal_id):
    for plan in plans:
        if plan["proposal_id"] == proposal_id:
            return plan
    return None


def render_table(plans):
    if not plans:
        return "No approved_pending_apply plans found."

    headers = ["proposal_id", "effective_state", "target_path"]
    rows = [
        [
            plan["proposal_id"],
            plan["effective_state"],
            plan["candidate_target_path"],
        ]
        for plan in plans
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
        description="Derived-only apply planning layer."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List apply plans.")
    list_parser.add_argument("--format", choices=OUTPUT_CHOICES, default="table")

    show_parser = subparsers.add_parser("show", help="Show apply plan.")
    show_parser.add_argument("proposal_id")
    show_parser.add_argument("--format", choices=OUTPUT_CHOICES, default="table")

    args = parser.parse_args()
    plans = build_apply_plans()

    if args.command == "list":
        if args.format == "json":
            emit_json(plans)
            return
        print(render_table(plans["plans"]))
        return

    if args.command == "show":
        plan = find_plan(plans["plans"], args.proposal_id)
        if plan is None:
            raise SystemExit(f"apply plan not found: {args.proposal_id}")

        if args.format == "json":
            emit_json(
                {
                    "apply_plan_version": plans["apply_plan_version"],
                    "write": False,
                    "plan": plan,
                }
            )
            return

        print(render_table([plan]))
        return


if __name__ == "__main__":
    main()
