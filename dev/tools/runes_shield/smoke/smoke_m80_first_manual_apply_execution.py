#!/usr/bin/env python3
"""M80 first manual apply record-template smoke.

This smoke validates only the record template and safety flags.
It does not perform any repository mutation.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m80" / "first-manual-apply-execution-record.json"

def main() -> int:
    issues: list[str] = []
    data = json.loads(FIXTURE.read_text(encoding="utf-8")) if FIXTURE.exists() else {}
    if not data:
        issues.append(f"missing fixture: {FIXTURE}")
    for key in ["write", "authoritative", "runtime_dependency_required"]:
        if data.get(key) is not False:
            issues.append(f"{key} must be false")
    if data.get("record_mode") != "manual-execution-record-template":
        issues.append("record_mode mismatch")
    semantics = data.get("required_semantics", {})
    required_true = [
        "manual_apply_must_be_human_executed",
        "one_candidate_required",
        "one_operation_required",
        "one_target_path_required",
        "source_reference_required",
        "post_apply_verification_required",
        "rollback_note_required",
    ]
    required_false = [
        "tool_performs_real_write",
        "automatic_apply_allowed",
        "automatic_commit_allowed",
        "batch_operation_allowed",
        "runtime_authority_escalation_allowed",
    ]
    for key in required_true:
        if semantics.get(key) is not True:
            issues.append(f"required_semantics.{key} must be true")
    for key in required_false:
        if semantics.get(key) is not False:
            issues.append(f"required_semantics.{key} must be false")
    fields = data.get("manual_execution_record_fields", [])
    if len(fields) < 9:
        issues.append("manual_execution_record_fields incomplete")
    result = {
        "smoke_version": "m80-first-manual-apply-record-template-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": data.get("mode"),
        "scale": data.get("scale"),
        "write": data.get("write"),
        "authoritative": data.get("authoritative"),
        "runtime_dependency_required": data.get("runtime_dependency_required"),
        "record_mode": data.get("record_mode"),
        "manual_execution_record_field_count": len(fields),
        "issue_count": len(issues),
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1
if __name__ == "__main__":
    raise SystemExit(main())
