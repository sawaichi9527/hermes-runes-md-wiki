#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

from validate_proposal_fixture import validate_fixture

ROOT = Path(__file__).resolve().parents[2]
DRAFT_DIR = ROOT / "tools" / "runes_shield" / "drafts"
OUTPUT_CHOICES = ("table", "json")


def iter_drafts():
    if not DRAFT_DIR.exists():
        return []
    return sorted(DRAFT_DIR.glob("*.json"))


def build_entries():
    entries = []
    for path in iter_drafts():
        data = json.loads(path.read_text(encoding="utf-8"))
        validation = validate_fixture(path)
        entries.append(
            {
                "proposal_id": data.get("proposal_id"),
                "draft_file": path.name,
                "draft_path": str(path.relative_to(ROOT)),
                "sample_status": validation["sample_status"],
                "validation_status": validation["status"],
                "write": False,
            }
        )
    return entries


def find_entry(entries, proposal_id):
    for entry in entries:
        if entry["proposal_id"] == proposal_id:
            return entry
    return None


def load_payload(entry):
    return json.loads((ROOT / entry["draft_path"]).read_text(encoding="utf-8"))


def render_table(entries):
    if not entries:
        return "No proposal drafts found."

    headers = ["validation", "status", "proposal_id", "draft_file"]
    rows = [
        [
            entry["validation_status"],
            entry["sample_status"],
            entry["proposal_id"] or "-",
            entry["draft_file"],
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
        description="Read-only external proposal draft store CLI."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List external proposal drafts.")
    list_parser.add_argument("--format", choices=OUTPUT_CHOICES, default="table")

    show_parser = subparsers.add_parser("show", help="Show an external proposal draft by proposal_id.")
    show_parser.add_argument("proposal_id")
    show_parser.add_argument("--format", choices=OUTPUT_CHOICES, default="table")
    show_parser.add_argument("--include-payload", action="store_true")

    args = parser.parse_args()
    entries = build_entries()

    if args.command == "list":
        if args.format == "json":
            emit_json(
                {
                    "store_version": "m41.3-proposal-draft-store-v1",
                    "draft_dir": str(DRAFT_DIR.relative_to(ROOT)),
                    "entry_count": len(entries),
                    "write": False,
                    "entries": entries,
                }
            )
            return
        print(render_table(entries))
        return

    if args.command == "show":
        entry = find_entry(entries, args.proposal_id)
        if entry is None:
            raise SystemExit(f"draft not found: {args.proposal_id}")

        if args.format == "json":
            payload = {
                "store_version": "m41.3-proposal-draft-store-v1",
                "write": False,
                "entry": entry,
            }
            if args.include_payload:
                payload["payload"] = load_payload(entry)
            emit_json(payload)
            return

        print(f"proposal_id: {entry['proposal_id']}")
        print(f"draft_file: {entry['draft_file']}")
        print(f"draft_path: {entry['draft_path']}")
        print(f"sample_status: {entry['sample_status']}")
        print(f"validation_status: {entry['validation_status']}")
        print(f"write: {entry['write']}")
        if args.include_payload:
            print("payload:")
            print(json.dumps(load_payload(entry), indent=2, ensure_ascii=False))
        return


if __name__ == "__main__":
    main()
