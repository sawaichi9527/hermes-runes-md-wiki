#!/usr/bin/env python3
"""M76 First Manual Apply Readiness Gate smoke."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m76" / "first-manual-apply-readiness-gate.json"


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

    if data.get("gate_mode") != "readiness-check-only":
        issues.append("gate_mode mismatch")

    semantics = data.get("required_semantics", {})

    required_true = [
        "gate_is_not_apply_executor",
        "one_candidate_required",
        "one_operation_required",
        "one_target_path_required",
        "source_reference_required",
        "diff_preview_required",
        "rollback_note_required",
        "human_approval_checkpoint_required",
        "pre_apply_smoke_list_required",
        "post_apply_smoke_list_required",
    ]

    required_false = [
        "real_write_performed_by_gate",
        "automatic_apply_allowed",
        "automatic_promotion_allowed",
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

    candidate = data.get("readiness_candidate", {})

    if candidate.get("candidate_count") != 1:
        issues.append("candidate_count must be 1")

    if candidate.get("operation_count") != 1:
        issues.append("operation_count must be 1")

    if candidate.get("target_path_count") != 1:
        issues.append("target_path_count must be 1")

    if candidate.get("real_write_status") != "not_performed_by_m76":
        issues.append("real_write_status mismatch")

    required_fields = set(data.get("required_gate_fields", []))

    for field in [
        "candidate_id",
        "operation_id",
        "target_path_preview",
        "source_reference",
        "diff_preview",
        "rollback_note",
        "human_approval_checkpoint",
        "pre_apply_smokes",
        "post_apply_smokes",
    ]:
        if field not in required_fields:
            issues.append(f"missing required gate field: {field}")

    pre_smokes = data.get("pre_apply_smokes", [])
    post_smokes = data.get("post_apply_smokes", [])

    if len(pre_smokes) < 3:
        issues.append("pre_apply_smokes must contain at least 3 entries")

    if len(post_smokes) < 4:
        issues.append("post_apply_smokes must contain at least 4 entries")

    result = {
        "smoke_version": "m76-first-manual-apply-readiness-gate-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": data.get("mode"),
        "scale": data.get("scale"),
        "write": data.get("write"),
        "authoritative": data.get("authoritative"),
        "runtime_dependency_required": data.get("runtime_dependency_required"),
        "gate_mode": data.get("gate_mode"),
        "required_gate_field_count": len(required_fields),
        "pre_apply_smoke_count": len(pre_smokes),
        "post_apply_smoke_count": len(post_smokes),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
