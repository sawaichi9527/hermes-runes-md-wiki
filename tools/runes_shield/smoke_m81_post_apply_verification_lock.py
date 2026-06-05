#!/usr/bin/env python3
"""M81 Post-Apply Verification Lock smoke."""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m81" / "post-apply-verification-lock.json"

def main() -> int:
    issues: list[str] = []
    data = json.loads(FIXTURE.read_text(encoding="utf-8")) if FIXTURE.exists() else {}
    if not data:
        issues.append(f"missing fixture: {FIXTURE}")
    for key in ["write", "authoritative", "runtime_dependency_required"]:
        if data.get(key) is not False:
            issues.append(f"{key} must be false")
    if data.get("verification_mode") != "post-apply-checklist-only":
        issues.append("verification_mode mismatch")
    semantics = data.get("required_semantics", {})
    for key in ["post_apply_verification_required", "smoke_verification_required", "diff_review_required", "recall_check_required", "source_check_required", "rollback_note_required", "verification_is_not_runtime_policy"]:
        if semantics.get(key) is not True:
            issues.append(f"required_semantics.{key} must be true")
    for key in ["automatic_remediation_allowed", "automatic_rollback_allowed", "background_monitoring_required", "enterprise_workflow_required"]:
        if semantics.get(key) is not False:
            issues.append(f"required_semantics.{key} must be false")
    checks = data.get("verification_checks", [])
    if len(checks) < 7:
        issues.append("verification_checks incomplete")
    result = {
        "smoke_version": "m81-post-apply-verification-lock-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": data.get("mode"),
        "scale": data.get("scale"),
        "write": data.get("write"),
        "authoritative": data.get("authoritative"),
        "runtime_dependency_required": data.get("runtime_dependency_required"),
        "verification_mode": data.get("verification_mode"),
        "verification_check_count": len(checks),
        "issue_count": len(issues),
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1
if __name__ == "__main__":
    raise SystemExit(main())
