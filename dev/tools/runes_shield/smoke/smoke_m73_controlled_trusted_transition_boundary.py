#!/usr/bin/env python3
"""M73 Controlled Trusted Transition Boundary smoke."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m73" / "controlled-trusted-transition-boundary.json"


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
    if data.get("transition_mode") != "human-approved-transition-rehearsal":
        issues.append("transition_mode mismatch")

    semantics = data.get("required_semantics", {})
    required_true = [
        "reviewed_is_not_trusted",
        "trusted_transition_must_be_explicit",
        "human_approval_required",
        "source_check_required",
        "boundary_regression_required",
    ]
    required_false = [
        "automatic_trust_escalation_allowed",
        "automatic_promotion_allowed",
        "automatic_apply_allowed",
        "direct_wiki_mutation_allowed",
        "runtime_authority_escalation_allowed",
        "trust_scoring_required",
        "enterprise_workflow_required",
    ]
    for key in required_true:
        if semantics.get(key) is not True:
            issues.append(f"required_semantics.{key} must be true")
    for key in required_false:
        if semantics.get(key) is not False:
            issues.append(f"required_semantics.{key} must be false")

    transition_cases = data.get("transition_cases", [])
    if len(transition_cases) < 3:
        issues.append("transition_cases must contain at least 3 cases")
    for case in transition_cases:
        if case.get("trusted_memory") is not False:
            issues.append(f"transition case must not become trusted memory: {case.get('id')}")

    expected_to_states = {"reviewed_not_trusted", "trusted_candidate", "rejected_or_quarantined"}
    seen_to_states = {case.get("to_state") for case in transition_cases}
    for state in sorted(expected_to_states - seen_to_states):
        issues.append(f"missing transition to_state: {state}")

    forbidden_infra = set(data.get("forbidden_infrastructure", []))
    for forbidden in [
        "automatic-trust-scoring-system",
        "automatic-promotion-worker",
        "automatic-apply-worker",
        "trusted-write-daemon",
        "runtime-policy-engine",
    ]:
        if forbidden not in forbidden_infra:
            issues.append(f"missing forbidden infrastructure: {forbidden}")

    result = {
        "smoke_version": "m73-controlled-trusted-transition-boundary-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": data.get("mode"),
        "scale": data.get("scale"),
        "write": data.get("write"),
        "authoritative": data.get("authoritative"),
        "runtime_dependency_required": data.get("runtime_dependency_required"),
        "transition_mode": data.get("transition_mode"),
        "transition_case_count": len(transition_cases),
        "issue_count": len(issues),
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
