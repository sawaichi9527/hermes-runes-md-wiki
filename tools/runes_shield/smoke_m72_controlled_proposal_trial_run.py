#!/usr/bin/env python3
"""M72 Controlled Proposal Trial-run smoke."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m72" / "controlled-proposal-trial-run.json"


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

    if data.get("trial_run_mode") != "governed-proposal-lifecycle-rehearsal":
        issues.append("trial_run_mode mismatch")

    semantics = data.get("required_semantics", {})

    required_true = [
        "proposal_lifecycle_is_rehearsal",
        "proposal_draft_is_not_trusted_memory",
        "human_review_required",
        "source_check_required",
        "boundary_regression_required",
    ]

    required_false = [
        "trusted_write_allowed",
        "automatic_promotion_allowed",
        "automatic_apply_allowed",
        "direct_wiki_mutation_allowed",
        "runtime_authority_escalation_allowed",
        "enterprise_workflow_required",
    ]

    for key in required_true:
        if semantics.get(key) is not True:
            issues.append(f"required_semantics.{key} must be true")

    for key in required_false:
        if semantics.get(key) is not False:
            issues.append(f"required_semantics.{key} must be false")

    proposal_cases = data.get("proposal_cases", [])

    if len(proposal_cases) < 3:
        issues.append("proposal_cases must contain at least 3 cases")

    expected_decisions = {
        "accept_ready_after_human_review",
        "reject",
        "quarantine",
    }

    seen_decisions = set()

    for case in proposal_cases:
        seen_decisions.add(case.get("expected_decision"))

        if case.get("proposal_status") != "pending_human_review":
            issues.append(f"proposal_status invalid for {case.get('id')}")

        if case.get("write") is not False:
            issues.append(f"proposal case write must be false: {case.get('id')}")

    missing_decisions = expected_decisions - seen_decisions

    for decision in sorted(missing_decisions):
        issues.append(f"missing proposal decision path: {decision}")

    pre_trial_smokes = set(data.get("pre_trial_smokes", []))

    required_smokes = [
        "smoke_m71_controlled_trial_run_preparation.py",
        "smoke_m67_observation_stability_boundary.py",
        "smoke_m68_runtime_verification_separation_boundary.py",
        "smoke_m69_documentation_runtime_interface_boundary.py",
        "smoke_m70_human_review_machine_suggestion_boundary.py",
    ]

    for smoke in required_smokes:
        if smoke not in pre_trial_smokes:
            issues.append(f"missing pre-trial smoke: {smoke}")

        if not (ROOT / "tools" / "runes_shield" / smoke).exists():
            issues.append(f"missing smoke file: {smoke}")

    result = {
        "smoke_version": "m72-controlled-proposal-trial-run-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": data.get("mode"),
        "scale": data.get("scale"),
        "write": data.get("write"),
        "authoritative": data.get("authoritative"),
        "runtime_dependency_required": data.get("runtime_dependency_required"),
        "trial_run_mode": data.get("trial_run_mode"),
        "proposal_case_count": len(proposal_cases),
        "pre_trial_smoke_count": len(pre_trial_smokes),
        "post_trial_check_count": len(data.get("post_trial_checks", [])),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
