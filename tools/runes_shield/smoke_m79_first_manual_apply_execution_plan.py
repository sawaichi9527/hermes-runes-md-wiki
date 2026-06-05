#!/usr/bin/env python3
"""M79 First Manual Apply Execution Plan smoke."""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m79" / "first-manual-apply-execution-plan.json"

def main() -> int:
    issues: list[str] = []
    data = json.loads(FIXTURE.read_text(encoding="utf-8")) if FIXTURE.exists() else {}
    if not data:
        issues.append(f"missing fixture: {FIXTURE}")
    for key in ["write", "authoritative", "runtime_dependency_required"]:
        if data.get(key) is not False:
            issues.append(f"{key} must be false")
    if data.get("plan_mode") != "manual-command-checklist-only":
        issues.append("plan_mode mismatch")
    semantics = data.get("required_semantics", {})
    for key in ["plan_is_not_executor", "human_confirmation_required", "single_candidate_required", "single_operation_required", "single_target_path_required", "pre_apply_smokes_required", "post_apply_smokes_required", "rollback_note_required"]:
        if semantics.get(key) is not True:
            issues.append(f"required_semantics.{key} must be true")
    for key in ["real_write_performed_by_m79", "automatic_apply_allowed", "automatic_commit_allowed", "batch_operation_allowed", "runtime_authority_escalation_allowed"]:
        if semantics.get(key) is not False:
            issues.append(f"required_semantics.{key} must be false")
    steps = data.get("execution_plan_steps", [])
    if len(steps) < 8:
        issues.append("execution_plan_steps incomplete")
    result = {
        "smoke_version": "m79-first-manual-apply-execution-plan-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": data.get("mode"),
        "scale": data.get("scale"),
        "write": data.get("write"),
        "authoritative": data.get("authoritative"),
        "runtime_dependency_required": data.get("runtime_dependency_required"),
        "plan_mode": data.get("plan_mode"),
        "execution_plan_step_count": len(steps),
        "issue_count": len(issues),
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1
if __name__ == "__main__":
    raise SystemExit(main())
