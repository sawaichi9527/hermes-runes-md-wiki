#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

from proposal_apply_plan import build_apply_plans
from proposal_registry import find_entry, load_payload
from build_proposal_manifest import build_manifest

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_CHOICES = ("markdown", "json")


def load_proposal_payload(proposal_id):
    manifest = build_manifest()
    entry = find_entry(manifest["entries"], proposal_id)
    if entry is None:
        raise SystemExit(f"proposal not found: {proposal_id}")
    return load_payload(entry)


def render_metadata_block(plan):
    metadata = plan["candidate_metadata"]
    lines = ["---"]
    for key, value in metadata.items():
        lines.append(f"{key}: {value}")
    lines.extend(
        [
            "trusted_write: false",
            "apply_preview_only: true",
            "---",
        ]
    )
    return "\n".join(lines)


def render_claims(payload):
    claims = payload.get("candidate_claims", [])
    if not claims:
        return "- No candidate claims supplied."
    return "\n".join(f"- {claim}" for claim in claims)


def render_markdown_preview(plan, payload):
    return "\n\n".join(
        [
            render_metadata_block(plan),
            f"# {plan['candidate_heading']}",
            "## Source Summary",
            payload.get("source_summary", ""),
            "## Candidate Claims",
            render_claims(payload),
            "## Governance Notes",
            "- This is an apply preview only.",
            "- No trusted wiki write has been performed.",
            "- Human attunement remains required before any future apply step.",
        ]
    ) + "\n"


def render_index_preview(plan):
    return (
        f"- [{plan['proposal_id']}]"
        f"({plan['candidate_target_path']})"
        f" — {plan['effective_state']}"
    )


def build_previews():
    apply_plans = build_apply_plans()
    previews = []

    for plan in apply_plans["plans"]:
        payload = load_proposal_payload(plan["proposal_id"])
        previews.append(
            {
                "proposal_id": plan["proposal_id"],
                "candidate_target_path": plan["candidate_target_path"],
                "candidate_index_hint": plan["candidate_index_hint"],
                "markdown_preview": render_markdown_preview(plan, payload),
                "index_insertion_preview": render_index_preview(plan),
                "write": False,
                "effects": {
                    "trusted_wiki_write": False,
                    "index_update": False,
                    "automatic_apply": False,
                    "automatic_promotion": False,
                    "database_mutation": False,
                },
            }
        )

    return {
        "apply_preview_version": "m45-apply-preview-v1",
        "source_apply_plan": apply_plans["apply_plan_version"],
        "entry_count": len(previews),
        "write": False,
        "previews": previews,
    }


def find_preview(previews, proposal_id):
    for preview in previews:
        if preview["proposal_id"] == proposal_id:
            return preview
    return None


def emit_json(payload):
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="Dry-run markdown apply preview renderer."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List apply previews.")
    list_parser.add_argument("--format", choices=OUTPUT_CHOICES, default="markdown")

    show_parser = subparsers.add_parser("show", help="Show one apply preview.")
    show_parser.add_argument("proposal_id")
    show_parser.add_argument("--format", choices=OUTPUT_CHOICES, default="markdown")

    args = parser.parse_args()
    previews = build_previews()

    if args.command == "list":
        if args.format == "json":
            emit_json(previews)
            return
        if not previews["previews"]:
            print("No apply previews found.")
            return
        for preview in previews["previews"]:
            print(preview["index_insertion_preview"])
        return

    if args.command == "show":
        preview = find_preview(previews["previews"], args.proposal_id)
        if preview is None:
            raise SystemExit(f"apply preview not found: {args.proposal_id}")

        if args.format == "json":
            emit_json(
                {
                    "apply_preview_version": previews["apply_preview_version"],
                    "write": False,
                    "preview": preview,
                }
            )
            return

        print(preview["markdown_preview"])
        print("<!-- index insertion preview -->")
        print(preview["index_insertion_preview"])
        return


if __name__ == "__main__":
    main()
