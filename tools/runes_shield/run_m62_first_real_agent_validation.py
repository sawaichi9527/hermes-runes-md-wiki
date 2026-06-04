#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools" / "runes_shield"
CONTRACT = ROOT / "fixtures" / "m62" / "real-external-agent-validation-contract.json"
SESSION_FIXTURE = ROOT / "fixtures" / "m62" / "external-agent-session-evidence.json"
RUNNER_VERSION = "m62.4-first-real-agent-validation-v1"
OUTPUT_CHOICES = ("json", "table")

COMMANDS = {
    "m62_contract_smoke": [TOOLS / "smoke_m62_external_validation_contract.py"],
    "m62_session_evidence_smoke": [TOOLS / "smoke_m62_session_evidence.py"],
    "m61_real_agent_evidence_runner": [TOOLS / "run_real_agent_evidence.py", "--agent-profile-id", "generic-cli-agent"],
}


def run_json(command, timeout):
    completed = subprocess.run(
        [sys.executable, *[str(part) for part in command]],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=True,
    )
    return json.loads(completed.stdout)


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_validation(agent_profile_id, timeout):
    issues = []
    results = {}

    contract = load_json(CONTRACT)
    session = load_json(SESSION_FIXTURE)

    for name, command in COMMANDS.items():
        if name == "m61_real_agent_evidence_runner":
            command = [TOOLS / "run_real_agent_evidence.py", "--agent-profile-id", agent_profile_id]
        try:
            payload = run_json(command, timeout=timeout)
        except Exception as exc:
            issues.append({
                "code": "command_exception",
                "command": name,
                "message": str(exc),
            })
            results[name] = {"status": "FAIL", "write": None, "issue_count": None}
            continue

        results[name] = payload

        if payload.get("status") != "PASS":
            issues.append({"code": "command_not_pass", "command": name})

        if payload.get("write") is not False:
            issues.append({"code": "command_write_not_false", "command": name})

        if payload.get("issue_count") not in (0, None):
            issues.append({"code": "command_issue_count_nonzero", "command": name})

    if contract.get("agent_scope") != "agent-agnostic":
        issues.append({"code": "contract_agent_scope_drift"})

    if contract.get("scale") != "personal-local":
        issues.append({"code": "contract_scale_drift"})

    if session.get("agent_scope") != "agent-agnostic":
        issues.append({"code": "session_agent_scope_drift"})

    evidence = results.get("m61_real_agent_evidence_runner", {})

    if evidence.get("observed_status") != "PASS":
        issues.append({"code": "evidence_observed_status_not_pass"})

    if evidence.get("observed_write") is not False:
        issues.append({"code": "evidence_observed_write_not_false"})

    if evidence.get("observed_issue_count") != 0:
        issues.append({"code": "evidence_observed_issue_count_nonzero"})

    return {
        "validation_version": RUNNER_VERSION,
        "status": "PASS" if not issues else "FAIL",
        "mode": "first-real-agent-validation",
        "scale": "personal-local",
        "write": False,
        "created_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "agent_kind": "generic-cli-agent",
        "agent_profile_id": agent_profile_id,
        "agent_scope": "agent-agnostic",
        "validation_target": "Hermes Runes MD Wiki through Runes Shield",
        "contract_version": contract.get("contract_version"),
        "session_evidence_version": session.get("evidence_version"),
        "components": {
            name: {
                "status": payload.get("status"),
                "write": payload.get("write"),
                "issue_count": payload.get("issue_count"),
            }
            for name, payload in results.items()
        },
        "evidence_summary": {
            "evidence_version": evidence.get("evidence_version"),
            "evidence_kind": evidence.get("evidence_kind"),
            "observed_status": evidence.get("observed_status"),
            "observed_write": evidence.get("observed_write"),
            "observed_issue_count": evidence.get("observed_issue_count"),
            "validated_command_count": len(evidence.get("validated_commands", {})),
        },
        "boundary_summary": {
            "runes_shield_required": True,
            "profile_metadata_only": True,
            "direct_wiki_mutation": False,
            "direct_database_mutation": False,
            "automatic_apply": False,
            "automatic_promotion": False,
            "orchestration_daemon": False,
        },
        "issue_count": len(issues),
        "issues": issues,
    }


def render_table(payload):
    lines = [
        f"validation_version: {payload['validation_version']}",
        f"status: {payload['status']}",
        f"mode: {payload['mode']}",
        f"scale: {payload['scale']}",
        f"write: {payload['write']}",
        f"agent_kind: {payload['agent_kind']}",
        f"agent_profile_id: {payload['agent_profile_id']}",
        f"agent_scope: {payload['agent_scope']}",
        f"issue_count: {payload['issue_count']}",
        "components:",
    ]
    for name, component in payload["components"].items():
        lines.append(
            f"  - {name}: status={component['status']} write={component['write']} issues={component['issue_count']}"
        )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="M62.4 first real external agent validation runner.")
    parser.add_argument("--agent-profile-id", default="generic-cli-agent")
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="json")

    args = parser.parse_args()
    payload = build_validation(args.agent_profile_id, args.timeout)

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(render_table(payload))

    if payload["issue_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
