#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m63" / "openai-compatible-wrapper-validation.json"

EXPECTED_AGENT_TRAITS = {
    "chat-completions-compatible",
    "role-message-mapping",
    "tool-call-capable",
    "json-schema-capable",
    "function-argument-serialization",
    "model-output-untrusted",
}

EXPECTED_REQUIRED_RESPONSE_FIELDS = {
    "status",
    "mode",
    "scale",
    "write",
    "agent_scope",
    "compatibility_profile_id",
    "issue_count",
}

EXPECTED_FORBIDDEN_REQUEST_FIELDS = {
    "direct_wiki_path_write",
    "direct_database_write",
    "apply_proposal",
    "promote_memory",
    "runtime_policy_override",
    "authority_escalation",
}

EXPECTED_FORBIDDEN_RESPONSE_FIELDS = {
    "raw_prompt",
    "full_transcript",
    "secret",
    "token",
    "password",
    "database_password",
    "api_key",
}

EXPECTED_RISK_ACKS = {
    "tool_call_confusion_risk_acknowledged",
    "role_confusion_risk_acknowledged",
    "json_schema_overtrust_risk_acknowledged",
    "function_argument_injection_risk_acknowledged",
    "model_output_injection_risk_acknowledged",
    "human_governance_boundary_required",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M63.3 OpenAI-compatible wrapper fixture missing",
        })

        payload = {
            "smoke_version": "m63.3-openai-compatible-wrapper-validation-v1",
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
            "message": "M63.3 must remain agent-agnostic",
        })

    if fixture.get("scale") != "personal-local":
        issues.append({
            "code": "scale_drift",
            "message": "M63.3 must remain personal-local",
        })

    compatibility_profile = fixture.get("compatibility_profile", {})

    if compatibility_profile.get("profile_id") != "openai-compatible-wrapper":
        issues.append({
            "code": "compatibility_profile_drift",
            "message": "compatibility profile id drift detected",
        })

    if compatibility_profile.get("runtime_dependency_required") is not False:
        issues.append({
            "code": "runtime_dependency_violation",
            "message": "M63.3 must not require cloud/OpenAI runtime dependency",
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

    schema_surface = fixture.get("schema_surface", {})

    required_response_fields = set(schema_surface.get("required_response_fields", []))

    if required_response_fields != EXPECTED_REQUIRED_RESPONSE_FIELDS:
        issues.append({
            "code": "required_response_fields_drift",
            "expected": sorted(EXPECTED_REQUIRED_RESPONSE_FIELDS),
            "actual": sorted(required_response_fields),
        })

    forbidden_request_fields = set(schema_surface.get("forbidden_request_fields", []))

    if forbidden_request_fields != EXPECTED_FORBIDDEN_REQUEST_FIELDS:
        issues.append({
            "code": "forbidden_request_fields_drift",
            "expected": sorted(EXPECTED_FORBIDDEN_REQUEST_FIELDS),
            "actual": sorted(forbidden_request_fields),
        })

    forbidden_response_fields = set(schema_surface.get("forbidden_response_fields", []))

    if forbidden_response_fields != EXPECTED_FORBIDDEN_RESPONSE_FIELDS:
        issues.append({
            "code": "forbidden_response_fields_drift",
            "expected": sorted(EXPECTED_FORBIDDEN_RESPONSE_FIELDS),
            "actual": sorted(forbidden_response_fields),
        })

    risk_alignment = fixture.get("risk_alignment", {})

    for key in EXPECTED_RISK_ACKS:
        if risk_alignment.get(key) is not True:
            issues.append({
                "code": "risk_acknowledgement_missing",
                "field": key,
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
        "smoke_version": "m63.3-openai-compatible-wrapper-validation-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "openai-compatible-wrapper-validation",
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
