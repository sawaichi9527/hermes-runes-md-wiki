#!/usr/bin/env python3

import argparse
import json

from proposal_governance_timeline import build_timeline
from build_proposal_manifest import build_manifest

OUTPUT_CHOICES = ("table", "json")


def build_history():
    manifest = build_manifest()
    histories = []

    for entry in manifest["entries"]:
        proposal_id = entry["proposal_id"]
        timeline = build_timeline(proposal_id)

        histories.append(
            {
                "proposal_id": proposal_id,
                "validation_status": entry["validation_status"],
                "sample_status": entry["sample_status"],
                "event_count": timeline["event_count"],
                "latest_event": timeline["events"][-1]["event"],
                "write": False,
            }
        )

    return {
        "history_version": "m48-governance-history-v1",
        "proposal_count": len(histories),
        "write": False,
        "histories": histories,
    }


def render_table(payload):
    lines = [
        "proposal_id                 validation  events  latest_event",
        "--------------------------  ----------  ------  --------------------------",
    ]

    for item in payload["histories"]:
        lines.append(
            f"{item['proposal_id']:<26}  "
            f"{item['validation_status']:<10}  "
            f"{item['event_count']:<6}  "
            f"{item['latest_event']}"
        )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Build governance history projection across proposals."
    )
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="table")

    args = parser.parse_args()

    payload = build_history()

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(render_table(payload))


if __name__ == "__main__":
    main()
