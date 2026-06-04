#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m62" / "real-external-agent-validation-contract.json"

EXPECTED_REQUIRED_PASSES = {
    "m59_onboarding_lock",
    "m60_external_agent_trial_lock",
    "m61_real_agent_evidence",
}

EXPECTED_AGENT_KINDS = {
    "generic-cli-agent",
    "generic-openai-agent",
    "generic-mcp-agent",
    "openclaw-reference-agent",
    "future-agent-framework",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M62 external validation contract fixture missing",
        })
        payload = {
            "smoke_version": "m62.1-external-validation-contract-smoke-v1",
            "status": "FAIL",
            "write": False,
            "issue_count": len(issues),
            "issues": issues,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        raise SystemExit(1)

    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    if fixture.get("agent_scope") != "agent-agnostic":
        issues.append({
            "code": "agent_scope_drift",
            "message": "M62 contract must remain agent-agnostic",
        })

    if fixture.get("scale") != "personal-local":
        issues.append({
            "code": "scale_drift",
            "message": "M62 contract must remain personal-local",
        })

    passes = set(fixture.get("required_passes", []))
    if passes != EXPECTED_REQUIRED_PASSES:
        issues.append({
            "code": "required_passes_drift",
            "expected": sorted(EXPECTED_REQUIRED_PASSES),
            "actual": sorted(passes),
        })

    boundaries = fixture.get("required_boundaries", {})
    for key, value in boundaries.items():
        if value is not True:
            issues.append({
                "code": "boundary_violation",
                "boundary": key,
            })

    kinds = set(fixture.get("external_agent_kinds", []))
    if kinds != EXPECTED_AGENT_KINDS:
        issues.append({
            "code": "external_agent_kind_drift",
            "expected": sorted(EXPECTED_AGENT_KINDS),
            "actual": sorted(kinds),
        })

    evidence_policy = fixture.get("evidence_policy", {})

    required_policy = {
        "summarized_only": True,
        "public_safe_fixture_allowed": True,
        "full_transcript_required": False,
        "contains_secrets": False,
        "contains_private_user_data": False,
        "commit_local_evidence_to_repo": False,
        "ingest_evidence_to_rag": False,
        "write_to_observation_log": False,
    }

    for key, expected in required_policy.items():
        if evidence_policy.get(key) != expected:
            issues.append({
                "code": "evidence_policy_violation",
                "field": key,
                "expected": expected,
                "actual": evidence_policy.get(key),
            })

    expected_result = fixture.get("expected_result", {})

    if expected_result.get("status") != "PASS":
        issues.append({
            "code": "expected_status_violation",
            "message": "Expected result status must remain PASS",
        })

    if expected_result.get("write") is not False:
        issues.append({
            "code": "expected_write_violation",
            "message": "Expected write must remain false",
        })

    if expected_result.get("issue_count") != 0:
        issues.append({
            "code": "expected_issue_count_violation",
            "message": "Expected issue count must remain 0",
        })

    if expected_result.get("ready_for_governed_access") is not True:
        issues.append({
            "code": "governed_access_violation",
            "message": "ready_for_governed_access must remain true",
        })

    payload = {
        "smoke_version": "m62.1-external-validation-contract-smoke-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "real-external-agent-validation-contract",
        "write": False,
        "fixture": str(FIXTURE.relative_to(ROOT)),
        "required_pass_count": len(passes),
        "external_agent_kind_count": len(kinds),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
