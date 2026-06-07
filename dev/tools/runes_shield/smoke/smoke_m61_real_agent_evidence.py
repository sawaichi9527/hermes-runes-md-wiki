#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m61" / "real-agent-invocation-evidence.json"

EXPECTED_COMMANDS = {
    "m59_onboarding_lock",
    "m60_external_agent_trial_lock",
}

REQUIRED_EVIDENCE_FIELDS = {
    "agent_profile_id",
    "agent_scope",
    "validated_commands",
    "privacy_boundary",
    "observed_status",
    "observed_write",
    "observed_issue_count",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M61 real agent evidence fixture missing",
        })
        payload = {
            "smoke_version": "m61-real-agent-evidence-smoke-v1",
            "status": "FAIL",
            "write": False,
            "issue_count": len(issues),
            "issues": issues,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        raise SystemExit(1)

    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    privacy = fixture.get("privacy_boundary", {})
    for key in (
        "contains_secrets",
        "contains_private_user_data",
        "contains_full_chat_history",
        "contains_raw_prompt_dump",
        "contains_runtime_credentials",
    ):
        if privacy.get(key) is not False:
            issues.append({
                "code": "privacy_boundary_violation",
                "field": key,
            })

    if privacy.get("public_safe") is not True:
        issues.append({
            "code": "public_safe_violation",
            "message": "M61 evidence fixture must remain public-safe",
        })

    commands = fixture.get("validated_commands", [])
    command_names = {command.get("name") for command in commands}
    if command_names != EXPECTED_COMMANDS:
        issues.append({
            "code": "validated_command_drift",
            "expected": sorted(EXPECTED_COMMANDS),
            "actual": sorted(command_names),
        })

    for command in commands:
        if command.get("expected_status") != "PASS":
            issues.append({
                "code": "expected_command_status_violation",
                "command": command.get("name"),
            })
        if command.get("expected_write") is not False:
            issues.append({
                "code": "expected_command_write_violation",
                "command": command.get("name"),
            })
        if command.get("expected_issue_count") != 0:
            issues.append({
                "code": "expected_command_issue_count_violation",
                "command": command.get("name"),
            })

    required_fields = set(fixture.get("required_evidence_fields", []))
    if required_fields != REQUIRED_EVIDENCE_FIELDS:
        issues.append({
            "code": "required_evidence_fields_drift",
            "expected": sorted(REQUIRED_EVIDENCE_FIELDS),
            "actual": sorted(required_fields),
        })

    if fixture.get("observed_status") != "PASS":
        issues.append({
            "code": "observed_status_violation",
            "message": "Observed status must remain PASS in public fixture",
        })

    if fixture.get("observed_write") is not False:
        issues.append({
            "code": "observed_write_violation",
            "message": "Observed write must remain false",
        })

    if fixture.get("observed_issue_count") != 0:
        issues.append({
            "code": "observed_issue_count_violation",
            "message": "Observed issue count must remain 0",
        })

    boundary = fixture.get("governance_boundary", {})
    for key in (
        "evidence_grants_permissions",
        "evidence_is_runtime_state",
        "evidence_is_memory_source",
        "direct_wiki_mutation",
        "direct_database_mutation",
        "automatic_apply",
        "automatic_promotion",
    ):
        if boundary.get(key) is not False:
            issues.append({
                "code": "governance_boundary_violation",
                "field": key,
            })

    payload = {
        "smoke_version": "m61-real-agent-evidence-smoke-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "real-agent-invocation-evidence-validation",
        "write": False,
        "fixture": str(FIXTURE.relative_to(ROOT)),
        "evidence_kind": fixture.get("evidence_kind"),
        "agent_scope": fixture.get("agent_scope"),
        "validated_command_count": len(commands),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
