#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m65" / "governance-regression-baseline.json"

EXPECTED_FORBIDDEN_INFRASTRUCTURE = {
    "ci-orchestration-mesh",
    "distributed-runner",
    "telemetry-aggregation-service",
    "regression-database",
    "policy-engine",
    "trust-scoring-system",
    "runtime-monitoring-daemon",
    "siem-platform",
    "distributed-tracing",
    "workflow-replay-engine",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M65 governance regression baseline fixture missing",
        })

        payload = {
            "smoke_version": "m65.1-governance-regression-baseline-v1",
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

    if fixture.get("regression_principle") != "simple-semantic-contract-regression":
        issues.append({
            "code": "regression_principle_drift",
            "actual": fixture.get("regression_principle"),
        })

    protected_semantics = fixture.get("protected_semantics", {})

    expected_semantics = {
        "evidence_is_review_material_not_authority": True,
        "provenance_is_traceability_not_authority": True,
        "replay_is_review_not_execution": True,
        "wrapper_is_interface_not_governance_authority": True,
        "retention_is_not_runtime_dependency": True,
        "same_evidence_same_boundary_same_interpretation": True,
        "human_review_remains_required": True,
        "authoritative": False,
        "write": False,
    }

    for key, expected in expected_semantics.items():
        if protected_semantics.get(key) != expected:
            issues.append({
                "code": "protected_semantic_violation",
                "field": key,
                "expected": expected,
                "actual": protected_semantics.get(key),
            })

    regression_targets = fixture.get("regression_targets", [])

    for target in regression_targets:
        for field in ["authoritative", "write"]:
            if field in target and target.get(field) is not False:
                issues.append({
                    "code": "target_boundary_violation",
                    "target": target.get("id"),
                    "field": field,
                })

    forbidden_infra = set(fixture.get("forbidden_regression_infrastructure", []))

    if forbidden_infra != EXPECTED_FORBIDDEN_INFRASTRUCTURE:
        issues.append({
            "code": "forbidden_infrastructure_drift",
            "expected": sorted(EXPECTED_FORBIDDEN_INFRASTRUCTURE),
            "actual": sorted(forbidden_infra),
        })

    expected_result = fixture.get("expected_result", {})

    expected_result_rules = {
        "status": "PASS",
        "regression_target_count": 6,
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
        "smoke_version": "m65.1-governance-regression-baseline-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "governance-regression-baseline",
        "scale": fixture.get("scale"),
        "write": False,
        "authoritative": False,
        "runtime_dependency_required": False,
        "regression_target_count": len(regression_targets),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
