#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from proposal_apply_preview import build_previews, find_preview

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_CHOICES = ("table", "json")


def build_blocked_result(proposal_id, reason):
    return {
        "execution_boundary_version": "m46-apply-execution-boundary-v1",
        "proposal_id": proposal_id,
        "status": "BLOCKED",
        "reason": reason,
        "requested_at_utc": datetime.now(timezone.utc).isoformat(),
        "write": False,
        "effects": {
            "trusted_wiki_write": False,
            "markdown_mutation": False,
            "index_update": False,
            "automatic_apply": False,
            "automatic_promotion": False,
            "database_mutation": False,
        },
    }


def request_apply(proposal_id):
    previews = build_previews()
    preview = find_preview(previews["previews"], proposal_id)

    if preview is None:
        return build_blocked_result(
            proposal_id,
            "No approved apply preview is available for this proposal.",
        )

    result = build_blocked_result(
        proposal_id,
        "P0 governance boundary blocks apply execution. Human-approved preview is not sufficient for trusted wiki mutation.",
    )
    result["preview_available"] = True
    result["candidate_target_path"] = preview["candidate_target_path"]
    result["candidate_index_hint"] = preview["candidate_index_hint"]
    return result


def render_table(result):
    return "\n".join(
        [
            f"proposal_id: {result['proposal_id']}",
            f"status: {result['status']}",
            f"reason: {result['reason']}",
            f"write: {result['write']}",
            "effects:",
            *[
                f"  {key}: {value}"
                for key, value in result["effects"].items()
            ],
        ]
    )


def emit_json(payload):
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="Explicit apply execution boundary. Always blocks trusted write in P0."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    request_parser = subparsers.add_parser(
        "request",
        help="Request apply execution for a proposal. P0 always blocks execution.",
    )
    request_parser.add_argument("proposal_id")
    request_parser.add_argument("--format", choices=OUTPUT_CHOICES, default="table")

    args = parser.parse_args()

    if args.command == "request":
        result = request_apply(args.proposal_id)
        if args.format == "json":
            emit_json(result)
            return
        print(render_table(result))
        return


if __name__ == "__main__":
    main()
