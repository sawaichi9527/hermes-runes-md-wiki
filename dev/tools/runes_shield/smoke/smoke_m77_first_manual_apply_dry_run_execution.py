#!/usr/bin/env python3
"""M77 First Manual Apply Dry-run Execution smoke."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m77" / "first-manual-apply-dry-run-execution.json"


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

    if data.get("execution_mode") != "dry-run-execution-only":
        issues.append("execution_mode mismatch")

    semantics = data.get("required_semantics", {})

    required_true = [
        "dry_run_execution_only",
        "human_approval_required",
        "one_candidate_required",
        "one_operation_required",
        "one_target_path_required",
        "diff_preview_required",
        "rollback_note_required",
        "pre_apply_smokes_must_pass",
        "post_apply_smokes_must_pass",
    ]

    required_false = [
        "real_write_allowed",
        "automatic_apply_allowed",
        "batch_apply_allowed",
        "runtime_authority_escalation_allowed",
        "enterprise_workflow_required",
    ]

    for key in required_true:
        if semantics.get(key) is not True:
            issues.append(f"required_semantics.{key} must be true")

    for key in required_false:
        if semantics.get(key) is not False:
            issues.append(f"required_semantics.{key} must be false")

    steps = data.get("dry_run_execution_steps", [])

    if len(steps) < 8:
        issues.append("dry_run_execution_steps must contain at least 8 steps")

    expected_steps = [
        "load_single_candidate",
        "verify_source_reference",
        "verify_target_path_preview",
        "render_diff_preview",
        "run_pre_apply_smokes",
        "simulate_apply_execution",
        "run_post_apply_smokes",
        "record_dry_run_result",
    ]

    for step in expected_steps:
        if step not in steps:
            issues.append(f"missing execution step: {step}")

    execution_expectation = data.get("execution_result_expectation", {})

    for key in [
        "real_write_performed",
        "target_path_mutated",
        "index_mutated",
        "runtime_state_changed",
        "database_side_effect",
    ]:
        if execution_expectation.get(key) is not False:
            issues.append(f"execution_result_expectation.{key} must be false")

    result = {
        "smoke_version": "m77-first-manual-apply-dry-run-execution-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": data.get("mode"),
        "scale": data.get("scale"),
        "write": data.get("write"),
        "authoritative": data.get("authoritative"),
        "runtime_dependency_required": data.get("runtime_dependency_required"),
        "execution_mode": data.get("execution_mode"),
        "dry_run_execution_step_count": len(steps),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
