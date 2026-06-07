#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools" / "runes_shield"

COMMANDS = {
    "m62_1_contract": [TOOLS / "smoke_m62_external_validation_contract.py"],
    "m62_2_session_evidence": [TOOLS / "smoke_m62_session_evidence.py"],
    "m62_3_minimal_integration": [TOOLS / "smoke_m62_minimal_integration.py"],
    "m62_4_first_real_agent_validation": [TOOLS / "run_m62_first_real_agent_validation.py"],
}

EXPECTED_MODE = "first-real-agent-validation"
EXPECTED_AGENT_KIND = "generic-cli-agent"


def run_json(command, timeout=300):
    completed = subprocess.run(
        [sys.executable, *[str(part) for part in command]],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=True,
    )
    return json.loads(completed.stdout)


def main():
    issues = []
    results = {}

    for name, command in COMMANDS.items():
        try:
            payload = run_json(command)
        except Exception as exc:
            issues.append({
                "code": "component_exception",
                "component": name,
                "message": str(exc),
            })
            results[name] = {"status": "FAIL", "write": None, "issue_count": None}
            continue

        results[name] = payload

        if payload.get("status") != "PASS":
            issues.append({
                "code": "component_not_pass",
                "component": name,
            })

        if payload.get("write") is not False:
            issues.append({
                "code": "component_write_not_false",
                "component": name,
            })

        if payload.get("issue_count") not in (0, None):
            issues.append({
                "code": "component_issue_count_nonzero",
                "component": name,
            })

    validation = results.get("m62_4_first_real_agent_validation", {})

    if validation.get("mode") != EXPECTED_MODE:
        issues.append({
            "code": "validation_mode_drift",
            "expected": EXPECTED_MODE,
            "actual": validation.get("mode"),
        })

    if validation.get("agent_kind") != EXPECTED_AGENT_KIND:
        issues.append({
            "code": "agent_kind_drift",
            "expected": EXPECTED_AGENT_KIND,
            "actual": validation.get("agent_kind"),
        })

    if validation.get("agent_scope") != "agent-agnostic":
        issues.append({
            "code": "agent_scope_drift",
        })

    if validation.get("scale") != "personal-local":
        issues.append({
            "code": "scale_drift",
        })

    evidence = validation.get("evidence_summary", {})
    if evidence.get("observed_status") != "PASS":
        issues.append({
            "code": "evidence_status_drift",
        })

    if evidence.get("observed_write") is not False:
        issues.append({
            "code": "evidence_write_violation",
        })

    boundary = validation.get("boundary_summary", {})
    required_boundary = {
        "runes_shield_required": True,
        "profile_metadata_only": True,
        "direct_wiki_mutation": False,
        "direct_database_mutation": False,
        "automatic_apply": False,
        "automatic_promotion": False,
        "orchestration_daemon": False,
    }

    for key, expected in required_boundary.items():
        if boundary.get(key) != expected:
            issues.append({
                "code": "boundary_summary_violation",
                "field": key,
                "expected": expected,
                "actual": boundary.get(key),
            })

    payload = {
        "smoke_version": "m62.5-external-agent-trial-freeze-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "external-agent-trial-freeze",
        "scale": "personal-local",
        "write": False,
        "freeze_target": "M62 Real External Agent Validation",
        "components": {
            name: {
                "status": result.get("status"),
                "write": result.get("write"),
                "issue_count": result.get("issue_count"),
            }
            for name, result in results.items()
        },
        "validation_summary": {
            "validation_version": validation.get("validation_version"),
            "mode": validation.get("mode"),
            "agent_kind": validation.get("agent_kind"),
            "agent_profile_id": validation.get("agent_profile_id"),
            "agent_scope": validation.get("agent_scope"),
            "evidence_kind": evidence.get("evidence_kind"),
            "observed_status": evidence.get("observed_status"),
            "observed_issue_count": evidence.get("observed_issue_count"),
        },
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
