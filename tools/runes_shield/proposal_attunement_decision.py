#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from proposal_review_queue import build_queue, find_queue_entry

ROOT = Path(__file__).resolve().parents[2]
DECISION_DIR = ROOT / "tools" / "runes_shield" / "decisions"
ALLOWED_DECISIONS = ("approved", "rejected", "quarantined")
OUTPUT_CHOICES = ("table", "json")


def build_decision(proposal_id, decision, reviewer, notes):
    queue = build_queue()
    entry = find_queue_entry(queue["entries"], proposal_id)
    if entry is None:
        raise SystemExit(f"proposal not pending human review: {proposal_id}")

    return {
        "decision_version": "m42-human-attunement-decision-v1",
        "proposal_id": proposal_id,
        "proposal_fixture": entry["proposal_fixture"],
        "decision": decision,
        "reviewer": reviewer,
        "notes": notes,
        "decided_at_utc": datetime.now(timezone.utc).isoformat(),
        "write": False,
        "effects": {
            "proposal_file_modified": False,
            "trusted_wiki_write": False,
            "automatic_approval": False,
            "automatic_promotion": False,
            "apply_execution": False,
            "database_mutation": False,
        },
    }


def decision_path(proposal_id, decision):
    safe_id = proposal_id.replace("/", "_")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return DECISION_DIR / f"{safe_id}-{decision}-{timestamp}.json"


def write_decision(decision_payload, output_path=None):
    if output_path is None:
        output_path = decision_path(
            decision_payload["proposal_id"],
            decision_payload["decision"],
        )
    else:
        output_path = Path(output_path)
        if not output_path.is_absolute():
            output_path = ROOT / output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(decision_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return output_path


def iter_decisions():
    if not DECISION_DIR.exists():
        return []
    return sorted(DECISION_DIR.glob("*.json"))


def load_decision(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        "decision_file": path.name,
        "decision_path": str(path.relative_to(ROOT)),
        "proposal_id": data.get("proposal_id"),
        "decision": data.get("decision"),
        "reviewer": data.get("reviewer"),
        "write": False,
    }


def list_decisions():
    return [load_decision(path) for path in iter_decisions()]


def render_table(entries):
    if not entries:
        return "No attunement decisions found."

    headers = ["decision", "proposal_id", "reviewer", "decision_file"]
    rows = [
        [
            entry["decision"],
            entry["proposal_id"],
            entry["reviewer"],
            entry["decision_file"],
        ]
        for entry in entries
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
        description="Record-only human attunement decision tool."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    record_parser = subparsers.add_parser(
        "record",
        help="Create a record-only human attunement decision artifact.",
    )
    record_parser.add_argument("proposal_id")
    record_parser.add_argument("--decision", choices=ALLOWED_DECISIONS, required=True)
    record_parser.add_argument("--reviewer", default="Human")
    record_parser.add_argument("--note", action="append", default=[])
    record_parser.add_argument("--output")
    record_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview decision artifact without writing it.",
    )

    list_parser = subparsers.add_parser(
        "list",
        help="List recorded attunement decisions.",
    )
    list_parser.add_argument("--format", choices=OUTPUT_CHOICES, default="table")

    args = parser.parse_args()

    if args.command == "record":
        decision = build_decision(
            proposal_id=args.proposal_id,
            decision=args.decision,
            reviewer=args.reviewer,
            notes=args.note,
        )

        result = {
            "status": "PASS",
            "mode": "dry-run" if args.dry_run else "record-only",
            "write": not args.dry_run,
            "decision": decision,
        }

        if not args.dry_run:
            output_path = write_decision(decision, args.output)
            result["output_path"] = str(output_path.relative_to(ROOT))

        emit_json(result)
        return

    if args.command == "list":
        entries = list_decisions()
        if args.format == "json":
            emit_json(
                {
                    "decision_store_version": "m42-human-attunement-decision-store-v1",
                    "entry_count": len(entries),
                    "write": False,
                    "entries": entries,
                }
            )
            return
        print(render_table(entries))
        return


if __name__ == "__main__":
    main()
