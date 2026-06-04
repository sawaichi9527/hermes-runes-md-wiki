#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m66" / "wrapper-drift-observation.json"

EXPECTED_WRAPPERS = {
    "generic-cli-wrapper",
    "openclaw-style-agent",
    "openai-compatible-wrapper",
}

EXPECTED_FORBIDDEN_DRIFT = {
    "wrapper-interface-becomes-authority",
    "wrapper-profile-becomes-trust-grant",
    "runtime-capability-becomes-apply-permission",
    "tool-call-becomes-authority-grant",
    "advanced-wrapper-bypasses-human-review",
    "wrapper-observation-becomes-trust-scoring",
    "wrapper-observation-becomes-automatic-correction",
}

EXPECTED_FORBIDDEN_INFRA = {
    "wrapper-runtime-service",
    "adapter-daemon",
    "agent-specific-bridge",
    "websocket-bridge",
    "orchestration-daemon",
    "wrapper-trust-score-system",
    "wrapper-monitoring-daemon",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M66 wrapper drift observation fixture missing",
        })

        payload = {
            "smoke_version": "m66.2-wrapper-drift-observation-v1",
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

    if fixture.get("observation_principle") != "wrapper-observation-is-drift-detection-not-trust-scoring":
        issues.append({
            "code": "observation_principle_drift",
            "actual": fixture.get("observation_principle"),
        })

    wrappers = set(fixture.get("supported_wrapper_profiles", []))

    if wrappers != EXPECTED_WRAPPERS:
        issues.append({
            "code": "wrapper_profile_drift",
            "expected": sorted(EXPECTED_WRAPPERS),
            "actual": sorted(wrappers),
        })

    semantics = fixture.get("protected_wrapper_observation_semantics", {})

    expected_semantics = {
        "wrapper_is_interface_not_authority": True,
        "profile_is_metadata_not_permission": True,
        "runtime_capability_is_not_trust_grant": True,
        "tool_call_is_not_authority_grant": True,
        "observation_is_non_authoritative": True,
        "observation_is_non_blocking": True,
        "observation_is_human_review_support": True,
        "automatic_correction": False,
        "automatic_policy_mutation": False,
        "runtime_dependency_required": False,
        "write": False,
        "authoritative": False,
    }

    for key, expected in expected_semantics.items():
        if semantics.get(key) != expected:
            issues.append({
                "code": "protected_semantic_violation",
                "field": key,
                "expected": expected,
                "actual": semantics.get(key),
            })

    targets = fixture.get("wrapper_drift_targets", [])

    for target in targets:
        if target.get("drift_detection_only") is not True:
            issues.append({
                "code": "drift_detection_boundary_violation",
                "target": target.get("id"),
            })

        if target.get("automatic_correction") is not False:
            issues.append({
                "code": "automatic_correction_violation",
                "target": target.get("id"),
            })

    forbidden_drift = set(fixture.get("forbidden_wrapper_drift", []))

    if forbidden_drift != EXPECTED_FORBIDDEN_DRIFT:
        issues.append({
            "code": "forbidden_drift_mismatch",
            "expected": sorted(EXPECTED_FORBIDDEN_DRIFT),
            "actual": sorted(forbidden_drift),
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
        "wrapper_drift_target_count": 3,
        "runtime_dependency_required": False,
        "authoritative": False,
        "write": False,
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
        "smoke_version": "m66.2-wrapper-drift-observation-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "wrapper-drift-observation",
        "scale": fixture.get("scale"),
        "write": False,
        "authoritative": False,
        "runtime_dependency_required": False,
        "observation_only": True,
        "wrapper_drift_target_count": len(targets),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
