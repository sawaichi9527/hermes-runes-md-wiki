#!/usr/bin/env python3
"""M67 Observation Stability Boundary smoke.

This smoke is intentionally small and deterministic. It verifies that the
observation layer remains observation-only and cannot drift into authority,
enforcement, policy evaluation, trust scoring, or automatic remediation.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m67" / "observation-stability-boundary.json"


def main() -> int:
    issues: list[str] = []

    if not FIXTURE.exists():
        issues.append(f"missing fixture: {FIXTURE}")
        data = {}
    else:
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    required_false = [
        "write",
        "authoritative",
        "runtime_dependency_required",
    ]
    for key in required_false:
        if data.get(key) is not False:
            issues.append(f"{key} must be false")

    if data.get("scale") != "personal-local":
        issues.append("scale must be personal-local")
    if data.get("observation_only") is not True:
        issues.append("observation_only must be true")

    semantics = data.get("required_semantics", {})
    required_true_semantics = [
        "observation_is_drift_detection_support",
        "observation_is_not_authority",
        "observation_is_not_enforcement",
        "observation_is_not_policy_engine",
        "observation_is_not_trust_scoring",
        "observation_is_non_blocking",
        "observation_is_human_review_support",
        "observation_is_runtime_lightweight",
    ]
    required_false_semantics = [
        "automatic_correction",
        "automatic_policy_mutation",
        "automatic_remediation",
    ]
    for key in required_true_semantics:
        if semantics.get(key) is not True:
            issues.append(f"required_semantics.{key} must be true")
    for key in required_false_semantics:
        if semantics.get(key) is not False:
            issues.append(f"required_semantics.{key} must be false")

    forbidden_infra = set(data.get("forbidden_infrastructure", []))
    for forbidden in [
        "governance-enforcement-daemon",
        "policy-engine",
        "trust-scoring-system",
        "telemetry-analytics-platform",
        "runtime-governance-mesh",
        "automatic-remediation-service",
    ]:
        if forbidden not in forbidden_infra:
            issues.append(f"missing forbidden infrastructure: {forbidden}")

    result = {
        "smoke_version": "m67-observation-stability-boundary-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": data.get("mode"),
        "scale": data.get("scale"),
        "write": data.get("write"),
        "authoritative": data.get("authoritative"),
        "runtime_dependency_required": data.get("runtime_dependency_required"),
        "observation_only": data.get("observation_only"),
        "stability_target_count": len(data.get("stability_targets", [])),
        "issue_count": len(issues),
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
