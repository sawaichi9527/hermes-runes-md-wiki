#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m63" / "generic-cli-wrapper-validation.json"

EXPECTED_REQUIRED_FIELDS = {
    "status",
    "mode",
    "scale",
    "write",
    "agent_scope",
    "wrapper_profile_id",
    "issue_count",
}

EXPECTED_FORBIDDEN_FIELDS = {
    "raw_prompt",
    "full_transcript",
    "secret",
    "token",
    "password",
    "database_password",
    "api_key",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M63 generic CLI wrapper fixture missing",
        })

        payload = {
            "smoke_version": "m63.1-generic-cli-wrapper-validation-v1",
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
            "message": "M63 wrapper validation must remain agent-agnostic",
        })

    if fixture.get("scale") != "personal-local":
        issues.append({
            "code": "scale_drift",
            "message": "M63 wrapper validation must remain personal-local",
        })

    wrapper_profile = fixture.get("wrapper_profile", {})

    if wrapper_profile.get("profile_id") != "generic-cli-wrapper":
        issues.append({
            "code": "wrapper_profile_drift",
            "message": "wrapper profile id drift detected",
        })

    if wrapper_profile.get("transport") != "local-process":
        issues.append({
            "code": "transport_drift",
            "message": "transport must remain local-process",
        })

    boundaries = fixture.get("required_boundaries", {})

    for key, value in boundaries.items():
        if value is not True:
            issues.append({
                "code": "boundary_violation",
                "boundary": key,
            })

    cli_contract = fixture.get("expected_cli_contract", {})

    required_fields = set(cli_contract.get("required_stdout_fields", []))

    if required_fields != EXPECTED_REQUIRED_FIELDS:
        issues.append({
            "code": "required_stdout_fields_drift",
            "expected": sorted(EXPECTED_REQUIRED_FIELDS),
            "actual": sorted(required_fields),
        })

    forbidden_fields = set(cli_contract.get("forbidden_stdout_fields", []))

    if forbidden_fields != EXPECTED_FORBIDDEN_FIELDS:
        issues.append({
            "code": "forbidden_stdout_fields_drift",
            "expected": sorted(EXPECTED_FORBIDDEN_FIELDS),
            "actual": sorted(forbidden_fields),
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

    payload = {
        "smoke_version": "m63.1-generic-cli-wrapper-validation-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "generic-cli-wrapper-validation",
        "scale": fixture.get("scale"),
        "write": False,
        "agent_scope": fixture.get("agent_scope"),
        "wrapper_profile_id": wrapper_profile.get("profile_id"),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
