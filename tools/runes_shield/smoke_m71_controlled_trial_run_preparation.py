#!/usr/bin/env python3
"""M71 Controlled Trial-run Preparation Pack smoke."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m71" / "controlled-trial-run-preparation.json"


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
    if data.get("trial_run_mode") != "governed-proposal-only":
        issues.append("trial_run_mode must be governed-proposal-only")

    semantics = data.get("required_semantics", {})
    required_true = [
        "trial_run_is_preparation_not_production",
        "proposal_draft_is_not_trusted_memory",
        "human_review_required",
    ]
    required_false = [
        "trusted_write_allowed",
        "automatic_promotion_allowed",
        "automatic_apply_allowed",
        "direct_wiki_mutation_allowed",
        "runtime_authority_escalation_allowed",
        "hermes_agent_runtime_burden_added",
        "enterprise_workflow_required",
    ]
    for key in required_true:
        if semantics.get(key) is not True:
            issues.append(f"required_semantics.{key} must be true")
    for key in required_false:
        if semantics.get(key) is not False:
            issues.append(f"required_semantics.{key} must be false")

    required_smokes = [
        "smoke_m67_observation_stability_boundary.py",
        "smoke_m68_runtime_verification_separation_boundary.py",
        "smoke_m69_documentation_runtime_interface_boundary.py",
        "smoke_m70_human_review_machine_suggestion_boundary.py",
    ]
    pre_trial_smokes = set(data.get("pre_trial_smokes", []))
    for smoke in required_smokes:
        if smoke not in pre_trial_smokes:
            issues.append(f"missing pre-trial smoke: {smoke}")
        if not (ROOT / "tools" / "runes_shield" / smoke).exists():
            issues.append(f"pre-trial smoke file not found: {smoke}")

    checklist = set(data.get("review_checklist", []))
    for item in [
        "source_is_identified",
        "proposal_intent_is_clear",
        "human_decision_is_explicit",
        "trusted_memory_transition_is_explicit",
    ]:
        if item not in checklist:
            issues.append(f"missing review checklist item: {item}")

    forbidden_infra = set(data.get("forbidden_infrastructure", []))
    for forbidden in [
        "automatic-apply-worker",
        "automatic-promotion-worker",
        "trusted-write-daemon",
        "proposal-orchestration-daemon",
        "enterprise-workflow-engine",
        "runtime-policy-engine",
    ]:
        if forbidden not in forbidden_infra:
            issues.append(f"missing forbidden infrastructure: {forbidden}")

    result = {
        "smoke_version": "m71-controlled-trial-run-preparation-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": data.get("mode"),
        "scale": data.get("scale"),
        "write": data.get("write"),
        "authoritative": data.get("authoritative"),
        "runtime_dependency_required": data.get("runtime_dependency_required"),
        "trial_run_mode": data.get("trial_run_mode"),
        "allowed_scope_count": len(data.get("allowed_scope", [])),
        "pre_trial_smoke_count": len(data.get("pre_trial_smokes", [])),
        "review_checklist_count": len(data.get("review_checklist", [])),
        "issue_count": len(issues),
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
