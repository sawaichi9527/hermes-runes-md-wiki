#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m66" / "lightweight-governance-drift-observation.json"

EXPECTED_FORBIDDEN_INFRA = {
    "governance-enforcement-daemon",
    "policy-engine",
    "semantic-scoring-engine",
    "telemetry-analytics-platform",
    "drift-ai-analyzer",
    "automatic-remediation-service",
    "runtime-governance-mesh",
    "distributed-observation-platform",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M66 governance drift observation fixture missing",
        })

        payload = {
            "smoke_version": "m66.1-lightweight-governance-drift-observation-v1",
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

    if fixture.get("observation_principle") != "observe-first-dont-over-automate":
        issues.append({
            "code": "observation_principle_drift",
            "actual": fixture.get("observation_principle"),
        })

    semantics = fixture.get("protected_observation_semantics", {})

    expected_semantics = {
        "observation_is_non_authoritative": True,
        "observation_is_non_blocking": True,
        "observation_is_human_review_support": True,
        "observation_is_runtime_lightweight": True,
        "automatic_governance_correction": False,
        "automatic_policy_mutation": False,
        "automatic_authority_escalation": False,
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

    observation_targets = fixture.get("drift_observation_targets", [])

    for target in observation_targets:
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

    forbidden_infra = set(fixture.get("forbidden_observation_infrastructure", []))

    if forbidden_infra != EXPECTED_FORBIDDEN_INFRA:
        issues.append({
            "code": "forbidden_infrastructure_drift",
            "expected": sorted(EXPECTED_FORBIDDEN_INFRA),
            "actual": sorted(forbidden_infra),
        })

    expected_result = fixture.get("expected_result", {})

    expected_result_rules = {
        "status": "PASS",
        "observation_target_count": 4,
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
        "smoke_version": "m66.1-lightweight-governance-drift-observation-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "lightweight-governance-drift-observation",
        "scale": fixture.get("scale"),
        "write": False,
        "authoritative": False,
        "runtime_dependency_required": False,
        "observation_only": True,
        "observation_target_count": len(observation_targets),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
