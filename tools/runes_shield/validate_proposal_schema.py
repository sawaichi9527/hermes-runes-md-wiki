#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "tools" / "runes_shield" / "proposal_schema.json"


SAMPLE_PROPOSAL = {
    "proposal_id": "proposal-m37-demo-001",
    "status": "pending_human_review",
    "author_role": "Hermes-agent",
    "assessment_role": "Runes Shield",
    "reviewer_role": "Human",
    "source_summary": "User provided a technical architecture discussion.",
    "candidate_claims": [
        "Hermes-agent may suggest candidate memory proposals.",
        "Human remains the final decision authority."
    ],
    "assessment": {
        "credibility_level": "medium",
        "risk_level": "low",
        "source_evidence": [
            "conversation history"
        ],
        "policy_notes": [
            "Requires human review before trusted memory promotion."
        ],
        "quarantine_recommendation": false
    },
    "human_review": {
        "status": "pending",
        "notes": []
    }
}


def load_schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def validate():
    schema = load_schema()

    missing = [
        field
        for field in schema["required_fields"]
        if field not in SAMPLE_PROPOSAL
    ]

    blocked_status = (
        SAMPLE_PROPOSAL["status"] in schema["blocked_status"]
    )

    role_ok = (
        SAMPLE_PROPOSAL["author_role"]
        == schema["required_roles"]["author_role"]
        and SAMPLE_PROPOSAL["assessment_role"]
        == schema["required_roles"]["assessment_role"]
        and SAMPLE_PROPOSAL["reviewer_role"]
        == schema["required_roles"]["reviewer_role"]
    )

    assessment_missing = [
        field
        for field in schema["required_assessment_fields"]
        if field not in SAMPLE_PROPOSAL["assessment"]
    ]

    passed = (
        not missing
        and not blocked_status
        and role_ok
        and not assessment_missing
    )

    return {
        "status": "PASS" if passed else "FAIL",
        "schema_version": schema["schema_version"],
        "missing_fields": missing,
        "assessment_missing_fields": assessment_missing,
        "blocked_status_detected": blocked_status,
        "role_validation": role_ok,
        "write": False,
        "sample_status": SAMPLE_PROPOSAL["status"],
        "blocked_capabilities": schema["blocked_capabilities"],
    }


def main():
    print(json.dumps(validate(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
