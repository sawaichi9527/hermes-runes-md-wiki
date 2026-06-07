#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "tools" / "runes_shield" / "proposal_schema.json"
DEFAULT_FIXTURE_PATH = ROOT / "tools" / "runes_shield" / "fixtures" / "proposal_draft_m37_2_valid.json"


def load_schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def resolve_fixture_path(path=None):
    if path is None:
        return DEFAULT_FIXTURE_PATH
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate


def load_fixture(path=None):
    fixture_path = resolve_fixture_path(path)
    proposal = json.loads(fixture_path.read_text(encoding="utf-8"))
    return proposal, fixture_path


def validate_fixture(path=None):
    schema = load_schema()
    proposal, fixture_path = load_fixture(path)

    missing = [
        field
        for field in schema["required_fields"]
        if field not in proposal
    ]

    sample_status = proposal.get("status")
    blocked_status_detected = sample_status in schema["blocked_status"]
    allowed_status_validation = sample_status in schema["allowed_status"]

    role_mismatches = [
        field
        for field, expected in schema["required_roles"].items()
        if proposal.get(field) != expected
    ]
    role_validation = not role_mismatches

    assessment = proposal.get("assessment")
    if isinstance(assessment, dict):
        assessment_missing = [
            field
            for field in schema["required_assessment_fields"]
            if field not in assessment
        ]
    else:
        assessment_missing = list(schema["required_assessment_fields"])

    passed = (
        not missing
        and not assessment_missing
        and not blocked_status_detected
        and allowed_status_validation
        and role_validation
    )

    return {
        "status": "PASS" if passed else "FAIL",
        "schema_version": schema["schema_version"],
        "fixture": fixture_path.name,
        "missing_fields": missing,
        "assessment_missing_fields": assessment_missing,
        "blocked_status_detected": blocked_status_detected,
        "allowed_status_validation": allowed_status_validation,
        "role_validation": role_validation,
        "role_mismatches": role_mismatches,
        "write": False,
        "sample_status": sample_status,
        "blocked_capabilities": schema["blocked_capabilities"],
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate a Runes Shield proposal fixture."
    )
    parser.add_argument(
        "fixture",
        nargs="?",
        help="Optional fixture path. Defaults to the M37.2 valid fixture.",
    )
    args = parser.parse_args()
    print(json.dumps(validate_fixture(args.fixture), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
