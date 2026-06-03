#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

from build_proposal_manifest import build_manifest


ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = ROOT / "tools" / "runes_shield" / "fixtures"
OUTPUT_CHOICES = ("table", "json")
REVIEWABLE_STATUSES = {"pending_human_review"}


def build_queue():
    manifest = build_manifest()
    entries = []

    for entry in manifest["entries"]:
        if entry["validation_status"] != "PASS":
            continue
        if entry["sample_status"] not in REVIEWABLE_STATUSES:
            continue

        entries.append(
            {
                "proposal_id": entry["proposal_id"],
                "proposal_fixture": entry["proposal_fixture"],
                "queue_status": "pending_human_review",
                "validation_status": entry["validation_status"],
                "sample_status": entry["sample_status"],
                "write": False,
            }
        )

    return {
        "queue_version": "m39-runes-attunement-queue-v1",
        "source_manifest": manifest["manifest_version"],
        "queue_name": "Runes Attunement Queue",
        "entry_count": len(entries),
        "write": False,
        "capabilities": {
            "trusted_wiki_write": False,
            "automatic_approval": False,
            "automatic_promotion": False,
            "apply_execution": False,
            "database_mutation": False,
        },
        "entries": entries,
    }


def find_queue_entry(entries, proposal_id):
    for entry in entries:
        if entry["proposal_id"] == proposal_id:
            return entry
    return None


def load_payload(entry):
    fixture_path = FIXTURE_DIR / entry["proposal_fixture"]
    return json.loads(fixture_path.read_text(encoding="utf-8"))


def render_table(entries):
    headers = [
        "queue_status",
        "validation",
        "proposal_id",
        "fixture",
    ]

    rows = [
        [
            entry["queue_status"],
            entry["validation_status"],
            entry["proposal_id"],
            entry["proposal_fixture"],
        ]
        for entry in entries
    ]

    if not rows:
        return "No proposals pending human review."

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


def render_detail(entry, payload=None):
    lines = [
        f"proposal_id: {entry['proposal_id']}",
        f"fixture: {entry['proposal_fixture']}",
        f"queue_status: {entry['queue_status']}",
        f"validation_status: {entry['validation_status']}",
        f"sample_status: {entry['sample_status']}",
        f"write: {entry['write']}",
    ]

    if payload is not None:
        lines.extend(
            [
                "payload:",
                json.dumps(payload, indent=2, ensure_ascii=False),
            ]
        )

    return "\n".join(lines)


def emit_json(payload):
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="Read-only Runes Attunement proposal review queue."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser(
        "list",
        help="List proposals pending human review.",
    )
    list_parser.add_argument(
        "--format",
        choices=OUTPUT_CHOICES,
        default="table",
        help="Output format.",
    )

    show_parser = subparsers.add_parser(
        "show",
        help="Show one pending-review proposal by proposal_id.",
    )
    show_parser.add_argument("proposal_id")
    show_parser.add_argument(
        "--format",
        choices=OUTPUT_CHOICES,
        default="table",
        help="Output format.",
    )
    show_parser.add_argument(
        "--include-payload",
        action="store_true",
        help="Include the source proposal JSON payload in read-only output.",
    )

    args = parser.parse_args()
    queue = build_queue()

    if args.command == "list":
        if args.format == "json":
            emit_json(queue)
            return
        print(render_table(queue["entries"]))
        return

    if args.command == "show":
        entry = find_queue_entry(queue["entries"], args.proposal_id)
        if entry is None:
            raise SystemExit(
                f"proposal not pending human review: {args.proposal_id}"
            )

        payload = load_payload(entry) if args.include_payload else None

        if args.format == "json":
            result = {
                "queue_version": queue["queue_version"],
                "write": False,
                "entry": entry,
            }
            if payload is not None:
                result["payload"] = payload
            emit_json(result)
            return

        print(render_detail(entry, payload=payload))
        return


if __name__ == "__main__":
    main()
