#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m65" / "provenance-regression.json"

EXPECTED_FORBIDDEN_REGRESSION = {
    "source-becomes-authority",
    "timestamp-becomes-freshness-guarantee",
    "wrapper-profile-becomes-trust-grant",
    "validation-pass-becomes-apply-permission",
    "validation-pass-becomes-promotion-permission",
    "commit-presence-becomes-runtime-authorization",
    "provenance-record-grants-write",
    "provenance-record-grants-database-mutation",
    "provenance-record-grants-runtime-policy-override",
}

EXPECTED_FORBIDDEN_INFRA = {
    "pki-chain",
    "timestamp-authority",
    "signed-audit-mesh",
    "distributed-ledger",
    "enterprise-provenance-graph",
    "authority-token-system",
    "runtime-attestation-service",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M65 provenance regression fixture missing",
        })

        payload = {
            "smoke_version": "m65.4-provenance-regression-v1",
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

    if fixture.get("regression_principle") != "provenance-regression-is-traceability-not-authority":
        issues.append({
            "code": "regression_principle_drift",
            "actual": fixture.get("regression_principle"),
        })

    semantics = fixture.get("protected_provenance_semantics", {})

    expected_semantics = {
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
        "runtime_dependency_required": False,
    }

    for key, expected in expected_semantics.items():
        if semantics.get(key) != expected:
            issues.append({
                "code": "protected_semantic_violation",
                "field": key,
                "expected": expected,
                "actual": semantics.get(key),
            })

    regression_cases = fixture.get("regression_cases", [])

    for case in regression_cases:
        expected_case = {
            "authority": False,
            "apply_allowed": False,
            "promotion_allowed": False,
            "write": False,
        }

        for key, expected in expected_case.items():
            if key in case and case.get(key) != expected:
                issues.append({
                    "code": "regression_case_violation",
                    "case": case.get("id"),
                    "field": key,
                    "expected": expected,
                    "actual": case.get(key),
                })

    forbidden_regression = set(fixture.get("forbidden_provenance_regression", []))

    if forbidden_regression != EXPECTED_FORBIDDEN_REGRESSION:
        issues.append({
            "code": "forbidden_regression_drift",
            "expected": sorted(EXPECTED_FORBIDDEN_REGRESSION),
            "actual": sorted(forbidden_regression),
        })

    forbidden_infra = set(fixture.get("forbidden_infrastructure", []))

    if forbidden_infra != EXPECTED_FORBIDDEN_INFRA:
        issues.append({
            "code": "forbidden_infrastructure_drift",
            "expected": sorted(EXPECTED_FORBIDDEN_INFRA),
            "actual": sorted(forbidden_infra),
        })

    expected_result = fixture.get("expected_result", {})

    expected_result_rules = {
        "status": "PASS",
        "regression_case_count": 5,
        "authoritative": False,
        "write": False,
        "runtime_dependency_required": False,
        "issue_count": 0,
    }

    for key, expected in expected_result_rules.items():
        if expected_result.get(key) != expected:
            issues.append({
                "code": "expected_result_violation",
                "field": key,
                "expected": expected,
                "actual": expected_result.get(key),
            })

    payload = {
        "smoke_version": "m65.4-provenance-regression-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "provenance-regression",
        "scale": fixture.get("scale"),
        "write": False,
        "authoritative": False,
        "runtime_dependency_required": False,
        "traceability_only": True,
        "regression_case_count": len(regression_cases),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
