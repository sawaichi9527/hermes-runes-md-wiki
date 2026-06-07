#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m65" / "wrapper-interpretation-regression.json"

EXPECTED_WRAPPERS = {
    "generic-cli-wrapper",
    "openclaw-style-agent",
    "openai-compatible-wrapper",
}

EXPECTED_FORBIDDEN_REGRESSION = {
    "wrapper-specific-trust-grant",
    "wrapper-specific-apply-permission",
    "wrapper-specific-promotion-permission",
    "wrapper-specific-runtime-escalation",
    "wrapper-profile-becomes-authority",
    "wrapper-runtime-becomes-dependency",
    "advanced-wrapper-bypasses-human-review",
    "agent-specific-adapter-changes-governance",
}

EXPECTED_FORBIDDEN_INFRA = {
    "wrapper-runtime-service",
    "adapter-daemon",
    "agent-specific-bridge",
    "websocket-bridge",
    "orchestration-daemon",
    "runtime-policy-engine",
    "wrapper-trust-score-system",
}

EXPECTED_INTERPRETATION = "review-only-non-authoritative"


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M65 wrapper interpretation regression fixture missing",
        })

        payload = {
            "smoke_version": "m65.3-wrapper-interpretation-regression-v1",
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

    if fixture.get("regression_principle") != "wrapper-regression-is-semantics-not-runtime":
        issues.append({
            "code": "regression_principle_drift",
            "actual": fixture.get("regression_principle"),
        })

    wrappers = set(fixture.get("supported_wrapper_profiles", []))

    if wrappers != EXPECTED_WRAPPERS:
        issues.append({
            "code": "wrapper_profile_drift",
            "expected": sorted(EXPECTED_WRAPPERS),
            "actual": sorted(wrappers),
        })

    canonical = fixture.get("canonical_expected_interpretation", {})

    expected_canonical = {
        "authoritative": False,
        "write": False,
        "apply_allowed": False,
        "promotion_allowed": False,
        "runtime_authority_escalation_allowed": False,
        "human_review_required": True,
        "runtime_dependency_required": False,
    }

    if canonical.get("interpretation") != EXPECTED_INTERPRETATION:
        issues.append({
            "code": "canonical_interpretation_drift",
            "actual": canonical.get("interpretation"),
        })

    for key, expected in expected_canonical.items():
        if canonical.get(key) != expected:
            issues.append({
                "code": "canonical_rule_violation",
                "field": key,
                "expected": expected,
                "actual": canonical.get(key),
            })

    regression_cases = fixture.get("regression_cases", [])

    for case in regression_cases:
        if case.get("expected_interpretation") != EXPECTED_INTERPRETATION:
            issues.append({
                "code": "interpretation_drift",
                "wrapper": case.get("wrapper_profile"),
                "actual": case.get("expected_interpretation"),
            })

        expected_case = {
            "authoritative": False,
            "write": False,
            "apply_allowed": False,
            "promotion_allowed": False,
            "runtime_authority_escalation_allowed": False,
            "human_review_required": True,
            "runtime_dependency_required": False,
        }

        for key, expected in expected_case.items():
            if case.get(key) != expected:
                issues.append({
                    "code": "regression_case_violation",
                    "wrapper": case.get("wrapper_profile"),
                    "field": key,
                    "expected": expected,
                    "actual": case.get(key),
                })

    forbidden_regression = set(fixture.get("forbidden_wrapper_regression", []))

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
        "wrapper_profile_count": 3,
        "regression_case_count": 3,
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
        "smoke_version": "m65.3-wrapper-interpretation-regression-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "wrapper-interpretation-regression",
        "scale": fixture.get("scale"),
        "write": False,
        "authoritative": False,
        "runtime_dependency_required": False,
        "consistent_interpretation": True,
        "wrapper_profile_count": len(regression_cases),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
