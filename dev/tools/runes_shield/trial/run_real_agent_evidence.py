#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools" / "runes_shield"
RUNNER_VERSION = "m61.1-real-agent-evidence-runner-v1"
OUTPUT_CHOICES = ("json", "table")

COMMANDS = {
    "m59_onboarding_lock": [TOOLS / "runes_agent_onboarding_lock.py", "--format", "json"],
    "m60_external_agent_trial_lock": [TOOLS / "smoke_m60_external_agent_trial.py"],
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


def build_evidence(agent_profile_id, timeout):
    issues = []
    results = {}

    for name, command in COMMANDS.items():
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
            issues.append({
                "code": "command_not_pass",
                "command": name,
            })

        if payload.get("write") is not False:
            issues.append({
                "code": "command_write_not_false",
                "command": name,
            })

        if payload.get("issue_count") not in (0, None):
            issues.append({
                "code": "command_issue_count_nonzero",
                "command": name,
            })

    observed_status = "PASS" if not issues else "FAIL"

    return {
        "evidence_version": RUNNER_VERSION,
        "evidence_kind": "local-real-agent-invocation-evidence",
        "status": observed_status,
        "created_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "write": False,
        "agent_scope": "agent-agnostic",
        "agent_profile_id": agent_profile_id,
        "privacy_boundary": {
            "contains_secrets": False,
            "contains_private_user_data": False,
            "contains_full_chat_history": False,
            "contains_raw_prompt_dump": False,
            "contains_runtime_credentials": False,
            "public_safe": True,
        },
        "validated_commands": {
            name: {
                "status": payload.get("status"),
                "write": payload.get("write"),
                "issue_count": payload.get("issue_count"),
            }
            for name, payload in results.items()
        },
        "observed_status": observed_status,
        "observed_write": False,
        "observed_issue_count": len(issues),
        "governance_boundary": {
            "evidence_grants_permissions": False,
            "evidence_is_runtime_state": False,
            "evidence_is_memory_source": False,
            "direct_wiki_mutation": False,
            "direct_database_mutation": False,
            "automatic_apply": False,
            "automatic_promotion": False,
        },
        "storage_policy": {
            "default_persistence": "stdout_only",
            "commit_to_repository": False,
            "ingest_to_rag": False,
            "write_to_observation_log": False,
            "output_file_is_local_only": True,
        },
        "issue_count": len(issues),
        "issues": issues,
    }


def render_table(payload):
    lines = [
        f"evidence_version: {payload['evidence_version']}",
        f"status: {payload['status']}",
        f"agent_scope: {payload['agent_scope']}",
        f"agent_profile_id: {payload['agent_profile_id']}",
        f"write: {payload['write']}",
        f"observed_issue_count: {payload['observed_issue_count']}",
        "validated_commands:",
    ]
    for name, result in payload["validated_commands"].items():
        lines.append(
            f"  - {name}: status={result['status']} write={result['write']} issues={result['issue_count']}"
        )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="M61.1 local real-agent invocation evidence runner."
    )
    parser.add_argument("--agent-profile-id", default="generic-cli-agent")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--output", help="Optional local-only output JSON path. If omitted, evidence is printed only.")
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="json")

    args = parser.parse_args()
    payload = build_evidence(agent_profile_id=args.agent_profile_id, timeout=args.timeout)

    if args.output:
        output_path = Path(args.output).expanduser()
        if not output_path.is_absolute():
            output_path = ROOT / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        payload["local_output_path"] = str(output_path)

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(render_table(payload))

    if payload["issue_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
