#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m62" / "external-agent-session-evidence.json"

EXPECTED_COMMANDS = {
    "m59_onboarding_lock",
    "m60_external_agent_trial_lock",
    "m61_real_agent_evidence_runner",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M62 session evidence fixture missing",
        })
        payload = {
            "smoke_version": "m62.2-session-evidence-smoke-v1",
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
            "message": "Session evidence must remain agent-agnostic",
        })

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
            "message": "Session evidence must remain public-safe",
        })

    commands = fixture.get("commands_run", [])
    command_names = {command.get("name") for command in commands}

    if command_names != EXPECTED_COMMANDS:
        issues.append({
            "code": "command_set_drift",
            "expected": sorted(EXPECTED_COMMANDS),
            "actual": sorted(command_names),
        })

    for command in commands:
        if command.get("expected_status") != "PASS":
            issues.append({
                "code": "expected_status_violation",
                "command": command.get("name"),
            })

        if command.get("expected_write") is not False:
            issues.append({
                "code": "expected_write_violation",
                "command": command.get("name"),
            })

        if command.get("expected_issue_count") != 0:
            issues.append({
                "code": "expected_issue_count_violation",
                "command": command.get("name"),
            })

    summary = fixture.get("pass_fail_summary", {})

    if summary.get("status") != "PASS":
        issues.append({
            "code": "summary_status_violation",
        })

    if summary.get("ready_for_governed_access") is not True:
        issues.append({
            "code": "summary_readiness_violation",
        })

    if summary.get("write") is not False:
        issues.append({
            "code": "summary_write_violation",
        })

    if summary.get("issue_count") != 0:
        issues.append({
            "code": "summary_issue_count_violation",
        })

    boundary = fixture.get("boundary_result", {})

    required_boundary = {
        "runes_shield_required": True,
        "profile_grants_permissions": False,
        "direct_wiki_mutation": False,
        "direct_database_mutation": False,
        "automatic_apply": False,
        "automatic_promotion": False,
        "background_worker": False,
        "orchestration_daemon": False,
    }

    for key, expected in required_boundary.items():
        if boundary.get(key) != expected:
            issues.append({
                "code": "boundary_result_violation",
                "field": key,
                "expected": expected,
                "actual": boundary.get(key),
            })

    policy = fixture.get("evidence_policy", {})

    required_policy = {
        "summarized_only": True,
        "full_transcript_required": False,
        "commit_local_evidence_to_repo": False,
        "ingest_evidence_to_rag": False,
        "write_to_observation_log": False,
        "local_output_allowed": True,
    }

    for key, expected in required_policy.items():
        if policy.get(key) != expected:
            issues.append({
                "code": "evidence_policy_violation",
                "field": key,
                "expected": expected,
                "actual": policy.get(key),
            })

    payload = {
        "smoke_version": "m62.2-session-evidence-smoke-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "external-agent-session-evidence-validation",
        "write": False,
        "fixture": str(FIXTURE.relative_to(ROOT)),
        "command_count": len(commands),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
