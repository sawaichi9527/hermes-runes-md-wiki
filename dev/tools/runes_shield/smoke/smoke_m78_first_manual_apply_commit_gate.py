#!/usr/bin/env python3
"""M78 First Manual Apply Commit Gate smoke."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m78" / "first-manual-apply-commit-gate.json"


def main() -> int:
    issues: list[str] = []

    data = json.loads(FIXTURE.read_text(encoding="utf-8")) if FIXTURE.exists() else {}
    if not data:
        issues.append(f"missing fixture: {FIXTURE}")

    for key in ["write", "authoritative", "runtime_dependency_required"]:
        if data.get(key) is not False:
            issues.append(f"{key} must be false")

    if data.get("gate_mode") != "final-pre-write-gate-only":
        issues.append("gate_mode mismatch")

    semantics = data.get("required_semantics", {})

    required_true = [
        "gate_is_not_commit_executor",
        "explicit_human_confirmation_required",
        "single_candidate_required",
        "single_operation_required",
        "single_target_path_required",
        "diff_preview_review_required",
        "rollback_note_review_required",
        "source_reference_review_required",
        "pre_apply_smokes_must_pass",
        "post_apply_smokes_must_be_defined",
    ]

    required_false = [
        "real_commit_performed",
        "real_write_performed",
        "automatic_commit_allowed",
        "automatic_apply_allowed",
        "batch_operation_allowed",
        "runtime_authority_escalation_allowed",
    ]

    for key in required_true:
        if semantics.get(key) is not True:
            issues.append(f"required_semantics.{key} must be true")

    for key in required_false:
        if semantics.get(key) is not False:
            issues.append(f"required_semantics.{key} must be false")

    required_fields = data.get("required_commit_gate_fields", [])

    if len(required_fields) < 9:
        issues.append("required_commit_gate_fields incomplete")

    review_sequence = data.get("gate_review_sequence", [])

    if len(review_sequence) < 8:
        issues.append("gate_review_sequence incomplete")

    result = {
        "smoke_version": "m78-first-manual-apply-commit-gate-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": data.get("mode"),
        "scale": data.get("scale"),
        "write": data.get("write"),
        "authoritative": data.get("authoritative"),
        "runtime_dependency_required": data.get("runtime_dependency_required"),
        "gate_mode": data.get("gate_mode"),
        "required_commit_gate_field_count": len(required_fields),
        "gate_review_sequence_count": len(review_sequence),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
