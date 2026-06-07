#!/usr/bin/env python3
"""M70 Human Review / Machine Suggestion Boundary smoke."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m70" / "human-review-machine-suggestion-boundary.json"


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
        "machine_suggestion_is_not_human_approval",
        "model_output_is_not_trust_transition",
        "wrapper_output_is_not_approval",
        "evidence_summary_is_not_approval",
        "observation_report_is_not_approval",
        "human_review_required_for_apply",
        "human_review_required_for_promotion",
        "human_review_required_for_trust_transition",
    ]
    required_false = [
        "automatic_apply_from_machine_suggestion",
        "automatic_promotion_from_machine_suggestion",
        "automatic_trust_transition_from_machine_suggestion",
        "machine_suggestion_blocks_runtime",
    ]
    for key in required_true:
        if semantics.get(key) is not True:
            issues.append(f"required_semantics.{key} must be true")
    for key in required_false:
        if semantics.get(key) is not False:
            issues.append(f"required_semantics.{key} must be false")

    forbidden_infra = set(data.get("forbidden_infrastructure", []))
    for forbidden in [
        "automatic-approval-engine",
        "trust-scoring-system",
        "machine-review-replacement-system",
        "background-apply-worker",
        "automatic-promotion-worker",
        "approval-daemon",
        "policy-engine",
    ]:
        if forbidden not in forbidden_infra:
            issues.append(f"missing forbidden infrastructure: {forbidden}")

    result = {
        "smoke_version": "m70-human-review-machine-suggestion-boundary-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": data.get("mode"),
        "scale": data.get("scale"),
        "write": data.get("write"),
        "authoritative": data.get("authoritative"),
        "runtime_dependency_required": data.get("runtime_dependency_required"),
        "boundary_target_count": len(data.get("boundary_targets", [])),
        "issue_count": len(issues),
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
