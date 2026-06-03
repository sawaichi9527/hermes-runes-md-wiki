#!/usr/bin/env python3

import argparse
import json

from build_proposal_manifest import build_manifest


VALIDATION_CHOICES = ("all", "valid", "invalid")
OUTPUT_CHOICES = ("table", "json")


def filter_entries(entries, validation):
    if validation == "valid":
        return [
            entry
            for entry in entries
            if entry["validation_status"] == "PASS"
        ]

    if validation == "invalid":
        return [
            entry
            for entry in entries
            if entry["validation_status"] == "FAIL"
        ]

    return entries


def find_entry(entries, proposal_id):
    for entry in entries:
        if entry["proposal_id"] == proposal_id:
            return entry
    return None


def render_table(entries):
    headers = [
        "validation",
        "status",
        "proposal_id",
        "fixture",
    ]

    rows = [
        [
            entry["validation_status"],
            entry["sample_status"],
            entry["proposal_id"] or "-",
            entry["proposal_fixture"],
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


def render_detail(entry):
    lines = [
        f"proposal_id: {entry['proposal_id']}",
        f"fixture: {entry['proposal_fixture']}",
        f"sample_status: {entry['sample_status']}",
        f"validation_status: {entry['validation_status']}",
        f"blocked_status_detected: {entry['blocked_status_detected']}",
        f"allowed_status_validation: {entry['allowed_status_validation']}",
        f"role_validation: {entry['role_validation']}",
        f"role_mismatches: {entry['role_mismatches']}",
        f"missing_fields: {entry['missing_fields']}",
        f"assessment_missing_fields: {entry['assessment_missing_fields']}",
        f"write: {entry['write']}",
    ]
    return "\n".join(lines)


def emit_json(payload):
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="Read-only proposal registry CLI."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser(
        "list",
        help="List proposal fixtures from the read-only manifest.",
    )
    list_parser.add_argument(
        "--validation",
        choices=VALIDATION_CHOICES,
        default="all",
        help="Filter by validation result.",
    )
    list_parser.add_argument(
        "--valid-only",
        action="store_true",
        help="Shortcut for --validation valid.",
    )
    list_parser.add_argument(
        "--invalid-only",
        action="store_true",
        help="Shortcut for --validation invalid.",
    )
    list_parser.add_argument(
        "--format",
        choices=OUTPUT_CHOICES,
        default="table",
        help="Output format.",
    )

    show_parser = subparsers.add_parser(
        "show",
        help="Show one proposal by proposal_id from the read-only manifest.",
    )
    show_parser.add_argument("proposal_id")
    show_parser.add_argument(
        "--format",
        choices=OUTPUT_CHOICES,
        default="table",
        help="Output format.",
    )

    args = parser.parse_args()

    manifest = build_manifest()

    if args.command == "list":
        validation = args.validation
        if args.valid_only:
            validation = "valid"
        if args.invalid_only:
            validation = "invalid"

        entries = filter_entries(manifest["entries"], validation)

        if args.format == "json":
            emit_json(
                {
                    "manifest_version": manifest["manifest_version"],
                    "filter": validation,
                    "entry_count": len(entries),
                    "write": False,
                    "entries": entries,
                }
            )
            return

        print(render_table(entries))
        return

    if args.command == "show":
        entry = find_entry(manifest["entries"], args.proposal_id)
        if entry is None:
            raise SystemExit(f"proposal not found: {args.proposal_id}")

        if args.format == "json":
            emit_json(
                {
                    "manifest_version": manifest["manifest_version"],
                    "write": False,
                    "entry": entry,
                }
            )
            return

        print(render_detail(entry))
        return


if __name__ == "__main__":
    main()
