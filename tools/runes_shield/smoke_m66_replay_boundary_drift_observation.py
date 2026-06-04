#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m66" / "replay-boundary-drift-observation.json"

EXPECTED_FORBIDDEN_DRIFT = {
    "review-replay-becomes-execution",
    "validation-replay-becomes-apply",
    "governance-replay-becomes-promotion",
    "replay-observation-becomes-authority",
    "replay-observation-grants-write",
    "replay-observation-triggers-background-worker",
    "replay-observation-becomes-automatic-correction",
    "summary-replay-becomes-workflow-replay",
}

EXPECTED_FORBIDDEN_INFRA = {
    "workflow-replay-engine",
    "execution-recovery-system",
    "background-worker",
    "event-bus",
    "orchestration-daemon",
    "distributed-replay-runner",
    "runtime-state-store",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M66 replay boundary drift observation fixture missing",
        })

        payload = {
            "smoke_version": "m66.3-replay-boundary-drift-observation-v1",
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

    if fixture.get("observation_principle") != "replay-observation-is-drift-detection-not-execution":
        issues.append({
            "code": "observation_principle_drift",
            "actual": fixture.get("observation_principle"),
        })

    semantics = fixture.get("protected_replay_observation_semantics", {})

    expected_semantics = {
        "replay_is_review_not_execution": True,
        "replay_is_not_apply": True,
        "replay_is_not_promotion": True,
        "replay_is_not_authority": True,
        "replay_observation_is_non_authoritative": True,
        "replay_observation_is_non_blocking": True,
        "replay_observation_is_human_review_support": True,
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

    targets = fixture.get("replay_drift_targets", [])

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

    forbidden_drift = set(fixture.get("forbidden_replay_drift", []))

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
        "replay_drift_target_count": 3,
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
        "smoke_version": "m66.3-replay-boundary-drift-observation-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "replay-boundary-drift-observation",
        "scale": fixture.get("scale"),
        "write": False,
        "authoritative": False,
        "runtime_dependency_required": False,
        "observation_only": True,
        "replay_drift_target_count": len(targets),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
