#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m64" / "governance-interpretation-consistency.json"

EXPECTED_WRAPPERS = {
    "generic-cli-wrapper",
    "openclaw-style-agent",
    "openai-compatible-wrapper",
}

EXPECTED_INTERPRETATION = "review-only-non-authoritative"

EXPECTED_FORBIDDEN_DRIFT = {
    "wrapper-specific trust grant",
    "wrapper-specific apply permission",
    "wrapper-specific promotion permission",
    "profile metadata becoming authority",
    "PASS evidence becoming trusted memory",
    "provenance becoming authorization",
    "timestamp becoming freshness guarantee",
    "validation result becoming automatic apply permission",
    "runtime capability becoming governance authority",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M64 governance interpretation consistency fixture missing",
        })

        payload = {
            "smoke_version": "m64.5-governance-interpretation-consistency-v1",
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

    if fixture.get("governance_principle") != "same-evidence-same-boundary-same-interpretation":
        issues.append({
            "code": "governance_principle_drift",
            "actual": fixture.get("governance_principle"),
        })

    wrappers = set(fixture.get("supported_wrapper_profiles", []))

    if wrappers != EXPECTED_WRAPPERS:
        issues.append({
            "code": "wrapper_profile_drift",
            "expected": sorted(EXPECTED_WRAPPERS),
            "actual": sorted(wrappers),
        })

    canonical = fixture.get("canonical_interpretation", {})

    canonical_expected = {
        "authoritative": False,
        "write": False,
        "apply_allowed": False,
        "promotion_allowed": False,
        "direct_wiki_mutation_allowed": False,
        "direct_database_mutation_allowed": False,
        "runtime_authority_escalation_allowed": False,
        "human_review_required": True,
    }

    if canonical.get("interpretation") != EXPECTED_INTERPRETATION:
        issues.append({
            "code": "canonical_interpretation_drift",
            "actual": canonical.get("interpretation"),
        })

    for key, expected in canonical_expected.items():
        if canonical.get(key) != expected:
            issues.append({
                "code": "canonical_rule_violation",
                "field": key,
                "expected": expected,
                "actual": canonical.get(key),
            })

    wrapper_interpretations = fixture.get("wrapper_interpretations", [])

    for wrapper in wrapper_interpretations:
        if wrapper.get("interpretation") != EXPECTED_INTERPRETATION:
            issues.append({
                "code": "wrapper_interpretation_drift",
                "wrapper": wrapper.get("wrapper_profile"),
                "actual": wrapper.get("interpretation"),
            })

        if wrapper.get("authoritative") is not False:
            issues.append({
                "code": "wrapper_authoritative_violation",
                "wrapper": wrapper.get("wrapper_profile"),
            })

        if wrapper.get("write") is not False:
            issues.append({
                "code": "wrapper_write_violation",
                "wrapper": wrapper.get("wrapper_profile"),
            })

        if wrapper.get("apply_allowed") is not False:
            issues.append({
                "code": "wrapper_apply_violation",
                "wrapper": wrapper.get("wrapper_profile"),
            })

        if wrapper.get("promotion_allowed") is not False:
            issues.append({
                "code": "wrapper_promotion_violation",
                "wrapper": wrapper.get("wrapper_profile"),
            })

        if wrapper.get("human_review_required") is not True:
            issues.append({
                "code": "wrapper_review_requirement_violation",
                "wrapper": wrapper.get("wrapper_profile"),
            })

    forbidden_drift = set(fixture.get("forbidden_interpretation_drift", []))

    if forbidden_drift != EXPECTED_FORBIDDEN_DRIFT:
        issues.append({
            "code": "forbidden_drift_mismatch",
            "expected": sorted(EXPECTED_FORBIDDEN_DRIFT),
            "actual": sorted(forbidden_drift),
        })

    consistency_rules = fixture.get("consistency_rules", {})

    expected_rules = {
        "same_evidence_same_boundary_same_interpretation": True,
        "wrapper_profile_must_not_change_authority": True,
        "wrapper_profile_must_not_change_write": True,
        "wrapper_profile_must_not_change_apply": True,
        "wrapper_profile_must_not_change_promotion": True,
        "human_review_remains_required": True,
        "authoritative": False,
        "write": False,
    }

    for key, expected in expected_rules.items():
        if consistency_rules.get(key) != expected:
            issues.append({
                "code": "consistency_rule_violation",
                "field": key,
                "expected": expected,
                "actual": consistency_rules.get(key),
            })

    expected_result = fixture.get("expected_result", {})

    if expected_result.get("status") != "PASS":
        issues.append({
            "code": "expected_status_violation",
            "actual": expected_result.get("status"),
        })

    if expected_result.get("wrapper_profile_count") != 3:
        issues.append({
            "code": "wrapper_profile_count_violation",
            "actual": expected_result.get("wrapper_profile_count"),
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
        "smoke_version": "m64.5-governance-interpretation-consistency-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "governance-interpretation-consistency",
        "scale": fixture.get("scale"),
        "write": False,
        "authoritative": False,
        "consistent": not issues,
        "wrapper_profile_count": len(wrapper_interpretations),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
