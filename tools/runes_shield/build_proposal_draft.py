#!/usr/bin/env python3

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from validate_proposal_fixture import validate_fixture

ROOT = Path(__file__).resolve().parents[2]
DRAFT_OUTPUT_DIR = ROOT / "tools" / "runes_shield" / "drafts"


def stable_proposal_id(source_summary, claims):
    seed = "\n".join([source_summary, *claims]).encode("utf-8")
    digest = hashlib.sha256(seed).hexdigest()[:12]
    return f"proposal-m41-dry-run-{digest}"


def build_proposal(source_summary, claims):
    return {
        "proposal_id": stable_proposal_id(source_summary, claims),
        "status": "pending_human_review",
        "author_role": "Hermes-agent",
        "assessment_role": "Runes Shield",
        "reviewer_role": "Human",
        "source_summary": source_summary,
        "candidate_claims": claims,
        "assessment": {
            "credibility_level": "medium",
            "risk_level": "low",
            "source_evidence": [
                "user-provided input",
                "M41 dry-run proposal builder",
            ],
            "policy_notes": [
                "Dry-run proposal only; no trusted memory write performed.",
                "Requires human review before any trusted memory promotion.",
                "Runes Shield blocks apply, approval, promotion, wiki write, and database mutation.",
            ],
            "quarantine_recommendation": False,
        },
        "human_review": {
            "status": "pending",
            "notes": [],
        },
    }


def write_draft(proposal, output_path=None):
    if output_path is None:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_path = DRAFT_OUTPUT_DIR / f"{proposal['proposal_id']}-{timestamp}.json"
    else:
        output_path = Path(output_path)
        if not output_path.is_absolute():
            output_path = ROOT / output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(proposal, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return output_path


def validate_written_draft(path):
    return validate_fixture(path)


def main():
    parser = argparse.ArgumentParser(
        description="Build a governed proposal draft. Dry-run by default."
    )
    parser.add_argument(
        "--source-summary",
        required=True,
        help="Short summary of the source material to turn into a proposal.",
    )
    parser.add_argument(
        "--claim",
        action="append",
        required=True,
        help="Candidate claim. Repeat this flag for multiple claims.",
    )
    parser.add_argument(
        "--output",
        help="Optional output path. Only used with --write-draft.",
    )
    parser.add_argument(
        "--write-draft",
        action="store_true",
        help="Write proposal draft JSON under tools/runes_shield/drafts or --output path.",
    )

    args = parser.parse_args()

    proposal = build_proposal(args.source_summary, args.claim)

    result = {
        "status": "PASS",
        "mode": "dry-run" if not args.write_draft else "write-draft",
        "write": bool(args.write_draft),
        "proposal": proposal,
        "blocked_capabilities": {
            "trusted_wiki_write": False,
            "automatic_approval": False,
            "automatic_promotion": False,
            "apply_execution": False,
            "database_mutation": False,
        },
    }

    if args.write_draft:
        output_path = write_draft(proposal, args.output)
        validation = validate_written_draft(output_path)
        result["output_path"] = str(output_path.relative_to(ROOT))
        result["validation"] = validation
        if validation["status"] != "PASS":
            result["status"] = "FAIL"

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result["status"] != "PASS":
        raise SystemExit("proposal draft build failed")


if __name__ == "__main__":
    main()
