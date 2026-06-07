#!/usr/bin/env python3
"""M75 Minimal Human-approved Apply Path smoke."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m75" / "minimal-human-approved-apply-path.json"


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
    if data.get("apply_path_mode") != "bounded-human-approved-dry-run":
        issues.append("apply_path_mode must be bounded-human-approved-dry-run")

    semantics = data.get("required_semantics", {})
    required_true = [
        "human_approval_required",
        "single_operation_scope_required",
        "explicit_target_path_required",
        "explicit_source_reference_required",
        "pre_apply_smoke_required",
        "post_apply_smoke_required",
        "manual_review_checkpoint_required",
    ]
    required_false = [
        "real_write_enabled_in_this_pack",
        "automatic_apply_allowed",
        "automatic_promotion_allowed",
        "multi_file_batch_apply_allowed",
        "runtime_authority_escalation_allowed",
        "enterprise_workflow_required",
    ]
    for key in required_true:
        if semantics.get(key) is not True:
            issues.append(f"required_semantics.{key} must be true")
    for key in required_false:
        if semantics.get(key) is not False:
            issues.append(f"required_semantics.{key} must be false")

    required_steps = [
        "select_one_human_approved_candidate",
        "confirm_source_reference",
        "confirm_target_path_preview",
        "confirm_diff_preview",
        "run_pre_apply_smokes",
        "record_manual_review_checkpoint",
        "prepare_single_operation_apply_plan",
        "run_post_apply_smokes",
    ]
    steps = set(data.get("minimal_apply_steps", []))
    for step in required_steps:
        if step not in steps:
            issues.append(f"missing minimal apply step: {step}")

    guardrails = set(data.get("apply_guardrails", []))
    for guardrail in [
        "one_candidate_per_operation",
        "one_target_path_per_operation",
        "explicit_human_decision_required",
        "no_background_worker",
        "no_runtime_policy_change",
    ]:
        if guardrail not in guardrails:
            issues.append(f"missing apply guardrail: {guardrail}")

    result = {
        "smoke_version": "m75-minimal-human-approved-apply-path-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": data.get("mode"),
        "scale": data.get("scale"),
        "write": data.get("write"),
        "authoritative": data.get("authoritative"),
        "runtime_dependency_required": data.get("runtime_dependency_required"),
        "apply_path_mode": data.get("apply_path_mode"),
        "minimal_apply_step_count": len(data.get("minimal_apply_steps", [])),
        "apply_guardrail_count": len(data.get("apply_guardrails", [])),
        "issue_count": len(issues),
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
