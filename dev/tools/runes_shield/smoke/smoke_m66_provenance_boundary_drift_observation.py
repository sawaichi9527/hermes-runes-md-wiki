#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m66" / "provenance-boundary-drift-observation.json"

EXPECTED_FORBIDDEN_DRIFT = {
    "source-becomes-authority",
    "timestamp-becomes-freshness-guarantee",
    "validation-pass-becomes-apply-permission",
    "validation-pass-becomes-promotion-permission",
    "commit-presence-becomes-runtime-authorization",
    "wrapper-profile-becomes-trust-grant",
    "provenance-observation-becomes-authority",
    "provenance-observation-becomes-automatic-correction",
}

EXPECTED_FORBIDDEN_INFRA = {
    "pki-chain",
    "signature-chain",
    "timestamp-authority",
    "runtime-attestation-service",
    "signed-audit-mesh",
    "enterprise-provenance-graph",
    "authority-token-system",
    "distributed-ledger",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M66 provenance boundary drift observation fixture missing",
        })

        payload = {
            "smoke_version": "m66.4-provenance-boundary-drift-observation-v1",
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

    if fixture.get("observation_principle") != "provenance-observation-is-traceability-drift-detection-not-authority":
        issues.append({
            "code": "observation_principle_drift",
            "actual": fixture.get("observation_principle"),
        })

    semantics = fixture.get("protected_provenance_observation_semantics", {})

    expected_semantics = {
        "source_is_traceability_not_authority": True,
        "timestamp_is_metadata_not_freshness_guarantee": True,
        "validation_pass_is_evidence_not_apply_permission": True,
        "commit_presence_is_record_not_runtime_authorization": True,
        "wrapper_profile_is_metadata_not_trust_grant": True,
        "provenance_observation_is_non_authoritative": True,
        "provenance_observation_is_non_blocking": True,
        "provenance_observation_is_human_review_support": True,
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

    targets = fixture.get("provenance_drift_targets", [])

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

    forbidden_drift = set(fixture.get("forbidden_provenance_drift", []))

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
        "provenance_drift_target_count": 4,
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
        "smoke_version": "m66.4-provenance-boundary-drift-observation-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "provenance-boundary-drift-observation",
        "scale": fixture.get("scale"),
        "write": False,
        "authoritative": False,
        "runtime_dependency_required": False,
        "observation_only": True,
        "provenance_drift_target_count": len(targets),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
