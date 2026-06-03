#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

from proposal_apply_execute import request_apply
from proposal_apply_preview import build_previews
from proposal_attunement_decision import load_decisions
from proposal_review_queue import build_review_queue
from proposal_state_projection import build_projection

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_CHOICES = ("table", "json")


def build_timeline(proposal_id):
    timeline = []

    queue = build_review_queue()
    queue_entry = next(
        (
            entry
            for entry in queue["entries"]
            if entry["proposal_id"] == proposal_id
        ),
        None,
    )

    if queue_entry:
        timeline.append(
            {
                "event": "proposal_queued",
                "source": "review_queue",
                "state": queue_entry["queue_status"],
                "write": False,
            }
        )

    decisions = load_decisions(include_payload=True)

    for decision in decisions:
        if decision["proposal_id"] != proposal_id:
            continue

        timeline.append(
            {
                "event": "human_attunement_decision",
                "source": decision["decision_file"],
                "decision": decision["decision"],
                "reviewer": decision["reviewer"],
                "write": False,
            }
        )

    projection = build_projection()
    state_entry = next(
        (
            state
            for state in projection["states"]
            if state["proposal_id"] == proposal_id
        ),
        None,
    )

    if state_entry:
        timeline.append(
            {
                "event": "state_projected",
                "effective_state": state_entry["effective_state"],
                "validation_status": state_entry["validation_status"],
                "write": False,
            }
        )

    previews = build_previews()
    preview_entry = next(
        (
            preview
            for preview in previews["previews"]
            if preview["proposal_id"] == proposal_id
        ),
        None,
    )

    if preview_entry:
        timeline.append(
            {
                "event": "apply_preview_generated",
                "target_path": preview_entry["candidate_target_path"],
                "write": False,
            }
        )

    execution = request_apply(proposal_id)

    timeline.append(
        {
            "event": "apply_execution_requested",
            "status": execution["status"],
            "reason": execution["reason"],
            "write": False,
        }
    )

    return {
        "timeline_version": "m47-governance-timeline-v1",
        "proposal_id": proposal_id,
        "event_count": len(timeline),
        "write": False,
        "events": timeline,
    }


def render_table(payload):
    lines = [
        f"proposal_id: {payload['proposal_id']}",
        f"event_count: {payload['event_count']}",
        "events:",
    ]

    for event in payload["events"]:
        lines.append(f"  - {event['event']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Build governance audit timeline for proposal lifecycle."
    )
    parser.add_argument("proposal_id")
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="table")

    args = parser.parse_args()

    payload = build_timeline(args.proposal_id)

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(render_table(payload))


if __name__ == "__main__":
    main()
