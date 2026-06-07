#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m64" / "evidence-classification.json"

EXPECTED_CLASSES = {
    "smoke_evidence",
    "validation_evidence",
    "runtime_summary",
    "wrapper_profile_evidence",
    "replay_evidence",
    "governance_interpretation",
}

EXPECTED_FORBIDDEN_FIELDS = {
    "raw_prompt",
    "full_transcript",
    "secret",
    "token",
    "password",
    "api_key",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M64 evidence classification fixture missing",
        })

        payload = {
            "smoke_version": "m64.1-evidence-classification-v1",
            "status": "FAIL",
            "write": False,
            "issue_count": len(issues),
            "issues": issues,
        }

        print(json.dumps(payload, indent=2, ensure_ascii=False))
        raise SystemExit(1)

    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    if fixture.get("scale") != "personal-local":
        issues.append({
            "code": "scale_drift",
            "expected": "personal-local",
            "actual": fixture.get("scale"),
        })

    if fixture.get("governance_principle") != "evidence-is-review-material-not-authority":
        issues.append({
            "code": "governance_principle_drift",
            "actual": fixture.get("governance_principle"),
        })

    system_boundary = fixture.get("system_boundary", {})

    for key, value in system_boundary.items():
        if value is not True:
            issues.append({
                "code": "system_boundary_violation",
                "boundary": key,
            })

    global_rules = fixture.get("global_evidence_rules", {})

    expected_global_rules = {
        "authoritative": False,
        "write": False,
        "summarized_only": True,
        "public_safe": True,
        "contains_secrets": False,
        "contains_private_user_data": False,
        "full_transcript_allowed": False,
        "rag_ingestion_allowed": False,
        "runtime_state_allowed": False,
        "authority_escalation_allowed": False,
    }

    for key, expected in expected_global_rules.items():
        if global_rules.get(key) != expected:
            issues.append({
                "code": "global_rule_violation",
                "field": key,
                "expected": expected,
                "actual": global_rules.get(key),
            })

    evidence_classes = fixture.get("evidence_classes", [])
    class_ids = {item.get("id") for item in evidence_classes}

    if class_ids != EXPECTED_CLASSES:
        issues.append({
            "code": "evidence_class_drift",
            "expected": sorted(EXPECTED_CLASSES),
            "actual": sorted(class_ids),
        })

    for evidence_class in evidence_classes:
        if evidence_class.get("authoritative") is not False:
            issues.append({
                "code": "authoritative_violation",
                "class": evidence_class.get("id"),
            })

        if evidence_class.get("write") is not False:
            issues.append({
                "code": "write_violation",
                "class": evidence_class.get("id"),
            })

        if evidence_class.get("summarized_only") is not True:
            issues.append({
                "code": "summarized_only_violation",
                "class": evidence_class.get("id"),
            })

        if evidence_class.get("public_safe") is not True:
            issues.append({
                "code": "public_safe_violation",
                "class": evidence_class.get("id"),
            })

        forbidden_fields = set(evidence_class.get("forbidden_fields", []))

        if forbidden_fields != EXPECTED_FORBIDDEN_FIELDS:
            issues.append({
                "code": "forbidden_fields_drift",
                "class": evidence_class.get("id"),
                "expected": sorted(EXPECTED_FORBIDDEN_FIELDS),
                "actual": sorted(forbidden_fields),
            })

    expected_result = fixture.get("expected_result", {})

    if expected_result.get("status") != "PASS":
        issues.append({
            "code": "expected_status_violation",
            "actual": expected_result.get("status"),
        })

    if expected_result.get("evidence_class_count") != 6:
        issues.append({
            "code": "evidence_class_count_violation",
            "actual": expected_result.get("evidence_class_count"),
        })

    if expected_result.get("authoritative") is not False:
        issues.append({
            "code": "expected_authoritative_violation",
            "actual": expected_result.get("authoritative"),
        })

    if expected_result.get("write") is not False:
        issues.append({
            "code": "expected_write_violation",
            "actual": expected_result.get("write"),
        })

    if expected_result.get("issue_count") != 0:
        issues.append({
            "code": "expected_issue_count_violation",
            "actual": expected_result.get("issue_count"),
        })

    payload = {
        "smoke_version": "m64.1-evidence-classification-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "evidence-classification",
        "scale": fixture.get("scale"),
        "write": False,
        "authoritative": False,
        "evidence_class_count": len(evidence_classes),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
