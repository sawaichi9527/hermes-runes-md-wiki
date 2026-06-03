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

    args = parser.parse_args()

    validation = args.validation
    if args.valid_only:
        validation = "valid"
    if args.invalid_only:
        validation = "invalid"

    manifest = build_manifest()
    entries = filter_entries(manifest["entries"], validation)

    if args.format == "json":
        payload = {
            "manifest_version": manifest["manifest_version"],
            "filter": validation,
            "entry_count": len(entries),
            "write": False,
            "entries": entries,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(render_table(entries))


if __name__ == "__main__":
    main()
