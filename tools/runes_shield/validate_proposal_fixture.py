#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "tools" / "runes_shield" / "proposal_schema.json"
FIXTURE_PATH = (
    ROOT
    / "tools"
    / "runes_shield"
    / "fixtures"
    / "proposal_draft_m37_2_valid.json"
)


def load_schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def load_fixture():
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def validate_fixture():
    schema = load_schema()
    proposal = load_fixture()

    missing = [
        field
        for field in schema["required_fields"]
        if field not in proposal
    ]

    blocked_status = (
        proposal["status"] in schema["blocked_status"]
    )

    allowed_status = (
        proposal["status"] in schema["allowed_status"]
    )

    role_ok = (
        proposal["author_role"]
        == schema["required_roles"]["author_role"]
        and proposal["assessment_role"]
        == schema["required_roles"]["assessment_role"]
        and proposal["reviewer_role"]
        == schema["required_roles"]["reviewer_role"]
    )

    assessment_missing = [
        field
        for field in schema["required_assessment_fields"]
        if field not in proposal["assessment"]
    ]

    passed = (
        not missing
        and not blocked_status
        and allowed_status
        and role_ok
        and not assessment_missing
    )

    return {
        "status": "PASS" if passed else "FAIL",
        "schema_version": schema["schema_version"],
        "fixture": FIXTURE_PATH.name,
        "missing_fields": missing,
        "assessment_missing_fields": assessment_missing,
        "blocked_status_detected": blocked_status,
        "allowed_status_validation": allowed_status,
        "role_validation": role_ok,
        "write": False,
        "sample_status": proposal["status"],
        "blocked_capabilities": schema["blocked_capabilities"],
    }


def main():
    print(json.dumps(validate_fixture(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
