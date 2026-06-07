#!/usr/bin/env python3
"""M82 P0 Governed Memory Operating Baseline smoke."""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m82" / "p0-governed-memory-operating-baseline.json"

def main() -> int:
    issues: list[str] = []
    data = json.loads(FIXTURE.read_text(encoding="utf-8")) if FIXTURE.exists() else {}
    if not data:
        issues.append(f"missing fixture: {FIXTURE}")
    for key in ["write", "authoritative", "runtime_dependency_required"]:
        if data.get(key) is not False:
            issues.append(f"{key} must be false")
    if data.get("baseline_mode") != "freeze-readiness-check":
        issues.append("baseline_mode mismatch")
    semantics = data.get("required_semantics", {})
    for key in ["proposal_generation_governed", "human_review_required", "trusted_transition_explicit", "manual_apply_path_defined", "post_apply_verification_defined"]:
        if semantics.get(key) is not True:
            issues.append(f"required_semantics.{key} must be true")
    for key in ["agent_runtime_burden_added", "enterprise_workflow_required", "automatic_apply_allowed", "automatic_promotion_allowed", "background_worker_required"]:
        if semantics.get(key) is not False:
            issues.append(f"required_semantics.{key} must be false")
    components = data.get("baseline_components", [])
    if len(components) < 10:
        issues.append("baseline_components incomplete")
    result = {
        "smoke_version": "m82-p0-governed-memory-operating-baseline-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": data.get("mode"),
        "scale": data.get("scale"),
        "write": data.get("write"),
        "authoritative": data.get("authoritative"),
        "runtime_dependency_required": data.get("runtime_dependency_required"),
        "baseline_mode": data.get("baseline_mode"),
        "baseline_component_count": len(components),
        "issue_count": len(issues),
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1
if __name__ == "__main__":
    raise SystemExit(main())
