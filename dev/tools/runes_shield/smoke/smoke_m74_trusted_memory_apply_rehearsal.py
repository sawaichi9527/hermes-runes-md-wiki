#!/usr/bin/env python3
"""M74 Trusted Memory Apply Rehearsal smoke."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m74" / "trusted-memory-apply-rehearsal.json"


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
    if data.get("apply_mode") != "dry-run-plan-only":
        issues.append("apply_mode must be dry-run-plan-only")

    semantics = data.get("required_semantics", {})
    required_true = [
        "apply_rehearsal_is_plan_only",
        "apply_plan_is_reviewable",
        "human_approval_required",
        "path_preview_required",
        "diff_preview_required",
        "rollback_note_required",
    ]
    required_false = [
        "real_write_allowed",
        "direct_wiki_mutation_allowed",
        "automatic_apply_allowed",
        "automatic_promotion_allowed",
        "runtime_authority_escalation_allowed",
        "enterprise_workflow_required",
    ]
    for key in required_true:
        if semantics.get(key) is not True:
            issues.append(f"required_semantics.{key} must be true")
    for key in required_false:
        if semantics.get(key) is not False:
            issues.append(f"required_semantics.{key} must be false")

    apply_cases = data.get("apply_plan_cases", [])
    if len(apply_cases) < 3:
        issues.append("apply_plan_cases must contain at least 3 cases")
    for case in apply_cases:
        if case.get("plan_only") is not True:
            issues.append(f"apply case must be plan_only: {case.get('id')}")
        if case.get("write") is not False:
            issues.append(f"apply case write must be false: {case.get('id')}")

    required_fields = set(data.get("required_apply_plan_fields", []))
    for field in [
        "operation_id",
        "target_path_preview",
        "diff_preview",
        "source_reference",
        "human_decision_required",
        "rollback_note",
    ]:
        if field not in required_fields:
            issues.append(f"missing required apply plan field: {field}")

    result = {
        "smoke_version": "m74-trusted-memory-apply-rehearsal-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": data.get("mode"),
        "scale": data.get("scale"),
        "write": data.get("write"),
        "authoritative": data.get("authoritative"),
        "runtime_dependency_required": data.get("runtime_dependency_required"),
        "apply_mode": data.get("apply_mode"),
        "apply_plan_case_count": len(apply_cases),
        "required_apply_plan_field_count": len(required_fields),
        "issue_count": len(issues),
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
