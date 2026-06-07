#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m63" / "openclaw-compatibility-validation.json"

EXPECTED_AGENT_TRAITS = {
    "local-agent-runtime",
    "tool-oriented-invocation",
    "shell-capable-agent-style",
    "file-access-capable-agent-style",
    "plugin-or-skill-capable-agent-style",
    "persistent-state-capable-agent-style",
}

EXPECTED_RISK_ACKS = {
    "local_file_access_risk_acknowledged",
    "shell_execution_risk_acknowledged",
    "plugin_skill_risk_acknowledged",
    "persistent_state_poisoning_risk_acknowledged",
    "prompt_injection_risk_acknowledged",
    "human_governance_boundary_required",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M63.2 OpenClaw compatibility fixture missing",
        })

        payload = {
            "smoke_version": "m63.2-openclaw-compatibility-validation-v1",
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
            "message": "M63.2 must remain agent-agnostic",
        })

    if fixture.get("scale") != "personal-local":
        issues.append({
            "code": "scale_drift",
            "message": "M63.2 must remain personal-local",
        })

    compatibility_profile = fixture.get("compatibility_profile", {})

    if compatibility_profile.get("profile_id") != "openclaw-style-agent":
        issues.append({
            "code": "compatibility_profile_drift",
            "message": "compatibility profile id drift detected",
        })

    if compatibility_profile.get("runtime_dependency_required") is not False:
        issues.append({
            "code": "runtime_dependency_violation",
            "message": "M63.2 must not require OpenClaw runtime installation",
        })

    traits = set(compatibility_profile.get("expected_agent_traits", []))

    if traits != EXPECTED_AGENT_TRAITS:
        issues.append({
            "code": "agent_traits_drift",
            "expected": sorted(EXPECTED_AGENT_TRAITS),
            "actual": sorted(traits),
        })

    boundaries = fixture.get("required_boundaries", {})

    for key, value in boundaries.items():
        if value is not True:
            issues.append({
                "code": "boundary_violation",
                "boundary": key,
            })

    risk_alignment = fixture.get("risk_alignment", {})

    for key in EXPECTED_RISK_ACKS:
        if risk_alignment.get(key) is not True:
            issues.append({
                "code": "risk_acknowledgement_missing",
                "field": key,
            })

    expected_surface = fixture.get("expected_wrapper_surface", {})
    forbidden_surface = set(expected_surface.get("forbidden_invocation_surface", []))

    required_forbidden_terms = {
        "direct wiki path write",
        "direct database connection write",
        "automatic proposal apply",
        "automatic memory promotion",
        "runtime policy modification",
        "background sync loop",
        "continuous filesystem watcher",
        "websocket control bridge",
        "enterprise telemetry exporter",
    }

    if forbidden_surface != required_forbidden_terms:
        issues.append({
            "code": "forbidden_surface_drift",
            "expected": sorted(required_forbidden_terms),
            "actual": sorted(forbidden_surface),
        })

    expected_result = fixture.get("expected_result", {})

    if expected_result.get("status") != "PASS":
        issues.append({
            "code": "expected_status_violation",
            "message": "Expected result status must remain PASS",
        })

    if expected_result.get("runtime_dependency_required") is not False:
        issues.append({
            "code": "expected_runtime_dependency_violation",
            "message": "Expected runtime dependency must remain false",
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

    payload = {
        "smoke_version": "m63.2-openclaw-compatibility-validation-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "openclaw-style-compatibility-validation",
        "scale": fixture.get("scale"),
        "write": False,
        "agent_scope": fixture.get("agent_scope"),
        "compatibility_profile_id": compatibility_profile.get("profile_id"),
        "runtime_dependency_required": compatibility_profile.get("runtime_dependency_required"),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
