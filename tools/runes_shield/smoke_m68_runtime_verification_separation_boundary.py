#!/usr/bin/env python3
"""M68 Runtime / Verification Separation Boundary smoke."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m68" / "runtime-verification-separation-boundary.json"


def main() -> int:
    issues: list[str] = []
    data = json.loads(FIXTURE.read_text(encoding="utf-8")) if FIXTURE.exists() else {}
    if not data:
        issues.append(f"missing fixture: {FIXTURE}")

    for key in ["write", "authoritative", "runtime_dependency_required"]:
        if data.get(key) is not False:
            issues.append(f"{key} must be false")
    if data.get("scale") != "personal-local":
        issues.append("scale must be personal-local")

    semantics = data.get("required_semantics", {})
    required_true = [
        "smoke_pass_is_not_apply_permission",
        "smoke_pass_is_not_promotion_permission",
        "verification_doc_is_not_runtime_policy",
        "fixture_is_not_runtime_state",
        "validation_result_is_not_trust_grant",
        "test_success_is_not_authority",
        "runtime_does_not_depend_on_verification_docs",
        "human_review_required_for_trust_transition",
    ]
    required_false = [
        "automatic_apply_from_verification",
        "automatic_promotion_from_verification",
        "automatic_runtime_policy_mutation",
    ]
    for key in required_true:
        if semantics.get(key) is not True:
            issues.append(f"required_semantics.{key} must be true")
    for key in required_false:
        if semantics.get(key) is not False:
            issues.append(f"required_semantics.{key} must be false")

    forbidden_infra = set(data.get("forbidden_infrastructure", []))
    for forbidden in [
        "runtime-policy-engine",
        "verification-driven-apply-worker",
        "automatic-promotion-worker",
        "verification-daemon",
        "runtime-state-store",
    ]:
        if forbidden not in forbidden_infra:
            issues.append(f"missing forbidden infrastructure: {forbidden}")

    result = {
        "smoke_version": "m68-runtime-verification-separation-boundary-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": data.get("mode"),
        "scale": data.get("scale"),
        "write": data.get("write"),
        "authoritative": data.get("authoritative"),
        "runtime_dependency_required": data.get("runtime_dependency_required"),
        "separation_target_count": len(data.get("separation_targets", [])),
        "issue_count": len(issues),
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
