#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m65" / "replay-boundary-regression.json"

EXPECTED_FORBIDDEN_REPLAY_REGRESSION = {
    "replay-becomes-execution",
    "replay-becomes-apply",
    "replay-becomes-promotion",
    "replay-becomes-authority",
    "replay-grants-write",
    "replay-grants-database-mutation",
    "replay-grants-runtime-policy-override",
    "replay-grants-authority-escalation",
    "workflow-replay-engine-required",
    "background-worker-required",
    "orchestration-daemon-required",
}

EXPECTED_FORBIDDEN_INFRA = {
    "workflow-replay-engine",
    "orchestration-daemon",
    "background-worker",
    "event-bus",
    "execution-recovery-system",
    "distributed-replay-runner",
    "runtime-state-store",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M65 replay boundary regression fixture missing",
        })

        payload = {
            "smoke_version": "m65.2-replay-boundary-regression-v1",
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

    if fixture.get("regression_principle") != "replay-regression-is-semantic-boundary-check-only":
        issues.append({
            "code": "regression_principle_drift",
            "actual": fixture.get("regression_principle"),
        })

    semantics = fixture.get("protected_replay_semantics", {})

    expected_semantics = {
        "review_only_replay_allowed": True,
        "replay_is_review": True,
        "replay_is_execution": False,
        "replay_is_apply": False,
        "replay_is_promotion": False,
        "replay_is_authority": False,
        "replay_grants_write": False,
        "replay_grants_database_mutation": False,
        "replay_grants_runtime_policy_override": False,
        "replay_grants_authority_escalation": False,
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
            "execution": False,
            "apply_allowed": False,
            "promotion_allowed": False,
            "authoritative": False,
            "write": False,
        }

        for key, expected in expected_case.items():
            if case.get(key) != expected:
                issues.append({
                    "code": "regression_case_violation",
                    "case": case.get("id"),
                    "field": key,
                    "expected": expected,
                    "actual": case.get(key),
                })

    forbidden_regression = set(fixture.get("forbidden_replay_regression", []))

    if forbidden_regression != EXPECTED_FORBIDDEN_REPLAY_REGRESSION:
        issues.append({
            "code": "forbidden_regression_drift",
            "expected": sorted(EXPECTED_FORBIDDEN_REPLAY_REGRESSION),
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
        "smoke_version": "m65.2-replay-boundary-regression-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "replay-boundary-regression",
        "scale": fixture.get("scale"),
        "write": False,
        "authoritative": False,
        "runtime_dependency_required": False,
        "review_only_replay": True,
        "regression_case_count": len(regression_cases),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
