#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m64" / "evidence-provenance-verification.json"

EXPECTED_FORBIDDEN_FIELDS = {
    "authority_token",
    "permission_grant",
    "runtime_policy_override",
    "apply_permission",
    "promotion_permission",
    "secret",
    "token",
    "password",
    "database_password",
    "api_key",
    "private_user_data",
    "full_transcript",
    "raw_prompt",
    "raw_answer",
    "runtime_state",
}

EXPECTED_FORBIDDEN_INTERPRETATIONS = {
    "source implies authority",
    "timestamp implies freshness guarantee",
    "wrapper profile implies trust grant",
    "validation PASS implies apply permission",
    "validation PASS implies automatic promotion",
    "commit presence implies runtime authorization",
    "provenance record implies direct wiki write permission",
    "provenance record implies database mutation permission",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M64 provenance verification fixture missing",
        })

        payload = {
            "smoke_version": "m64.4-evidence-provenance-verification-v1",
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
            "actual": fixture.get("scale"),
        })

    if fixture.get("governance_principle") != "provenance-is-traceability-not-authority":
        issues.append({
            "code": "governance_principle_drift",
            "actual": fixture.get("governance_principle"),
        })

    provenance_rules = fixture.get("provenance_rules", {})

    expected_rules = {
        "source_trace_required": True,
        "source_is_authority": False,
        "timestamp_is_freshness_guarantee": False,
        "wrapper_profile_is_trust_grant": False,
        "validation_result_is_apply_permission": False,
        "validation_result_is_promotion_permission": False,
        "commit_presence_is_authority": False,
        "human_review_remains_required": True,
        "authoritative": False,
        "write": False,
        "public_safe": True,
        "summarized_only": True,
    }

    for key, expected in expected_rules.items():
        if provenance_rules.get(key) != expected:
            issues.append({
                "code": "provenance_rule_violation",
                "field": key,
                "expected": expected,
                "actual": provenance_rules.get(key),
            })

    forbidden_fields = set(fixture.get("forbidden_provenance_fields", []))

    if forbidden_fields != EXPECTED_FORBIDDEN_FIELDS:
        issues.append({
            "code": "forbidden_fields_drift",
            "expected": sorted(EXPECTED_FORBIDDEN_FIELDS),
            "actual": sorted(forbidden_fields),
        })

    forbidden_interpretations = set(fixture.get("forbidden_interpretations", []))

    if forbidden_interpretations != EXPECTED_FORBIDDEN_INTERPRETATIONS:
        issues.append({
            "code": "forbidden_interpretations_drift",
            "expected": sorted(EXPECTED_FORBIDDEN_INTERPRETATIONS),
            "actual": sorted(forbidden_interpretations),
        })

    provenance_classes = fixture.get("provenance_classes", [])

    for provenance_class in provenance_classes:
        if provenance_class.get("traceable") is not True:
            issues.append({
                "code": "traceability_violation",
                "class": provenance_class.get("id"),
            })

        if provenance_class.get("authoritative") is not False:
            issues.append({
                "code": "authoritative_violation",
                "class": provenance_class.get("id"),
            })

        if provenance_class.get("write") is not False:
            issues.append({
                "code": "write_violation",
                "class": provenance_class.get("id"),
            })

        if provenance_class.get("trust_grant") is not False:
            issues.append({
                "code": "trust_grant_violation",
                "class": provenance_class.get("id"),
            })

    expected_result = fixture.get("expected_result", {})

    if expected_result.get("status") != "PASS":
        issues.append({
            "code": "expected_status_violation",
            "actual": expected_result.get("status"),
        })

    if expected_result.get("provenance_class_count") != 5:
        issues.append({
            "code": "provenance_class_count_violation",
            "actual": expected_result.get("provenance_class_count"),
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
        "smoke_version": "m64.4-evidence-provenance-verification-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "evidence-provenance-verification",
        "scale": fixture.get("scale"),
        "write": False,
        "authoritative": False,
        "traceable": True,
        "provenance_class_count": len(provenance_classes),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
