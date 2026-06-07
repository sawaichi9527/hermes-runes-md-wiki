#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools" / "runes_shield"

COMMANDS = {
    "m58_governed_agent_workflow": [
        TOOLS / "runes_governed_agent_workflow.py",
        "--format",
        "json",
    ],
    "m57_baseline": [
        TOOLS / "runes_shield_baseline.py",
        "--format",
        "json",
    ],
    "m58_docs_smoke": [
        TOOLS / "smoke_m58_docs.py",
    ],
}

EXPECTED_LOCKED_SURFACES = {
    "verity_checks": 10,
    "invocation_tools": 8,
    "adapter_safe_intents": 9,
    "adapter_blocked_intents": 7,
}


def run_json(command, timeout=60):
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
        payload = run_json(command)
        results[name] = payload
        if payload.get("status") != "PASS":
            issues.append({
                "code": "component_failed",
                "component": name,
                "message": f"{name} did not report PASS",
            })
        if payload.get("write") is not False:
            issues.append({
                "code": "component_write_not_false",
                "component": name,
                "message": f"{name} write must remain false",
            })

    workflow = results.get("m58_governed_agent_workflow", {})
    baseline = results.get("m57_baseline", {})
    docs = results.get("m58_docs_smoke", {})

    if workflow.get("workflow_version") != "m58-governed-agent-workflow-v1":
        issues.append({"code": "workflow_version_drift", "message": "Unexpected M58 workflow version"})

    if workflow.get("agent_scope") != "agent-agnostic":
        issues.append({"code": "agent_scope_drift", "message": "M58 workflow must remain agent-agnostic"})

    if workflow.get("issue_count") != 0:
        issues.append({"code": "workflow_issues", "message": "M58 workflow reported issues"})

    if len(workflow.get("steps", [])) != 8:
        issues.append({"code": "workflow_step_count_drift", "message": "M58 workflow must keep 8 governed steps"})

    if len(workflow.get("blocked_probes", [])) != 5:
        issues.append({"code": "blocked_probe_count_drift", "message": "M58 workflow must keep 5 blocked probes"})

    workflow_locked = workflow.get("post_workflow_verification", {}).get("locked_surface_counts", {})
    baseline_locked = baseline.get("locked_surface_counts", {})

    if workflow_locked != EXPECTED_LOCKED_SURFACES:
        issues.append({"code": "workflow_locked_surface_drift", "message": "M58 workflow locked surface counts drifted"})

    if baseline_locked != EXPECTED_LOCKED_SURFACES:
        issues.append({"code": "baseline_locked_surface_drift", "message": "M57 baseline locked surface counts drifted"})

    if workflow_locked != baseline_locked:
        issues.append({"code": "workflow_baseline_mismatch", "message": "M58 workflow and M57 baseline locked surfaces differ"})

    if docs.get("checked_file_count") != 3:
        issues.append({"code": "docs_checked_file_count_drift", "message": "M58 docs smoke must check 3 files"})

    payload = {
        "smoke_version": "m58.5-integration-smoke-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "m58-runtime-docs-integration",
        "write": False,
        "components": {
            name: {
                "status": result.get("status"),
                "write": result.get("write"),
                "issue_count": result.get("issue_count"),
            }
            for name, result in results.items()
        },
        "workflow_summary": {
            "workflow_version": workflow.get("workflow_version"),
            "agent_scope": workflow.get("agent_scope"),
            "step_count": len(workflow.get("steps", [])),
            "blocked_probe_count": len(workflow.get("blocked_probes", [])),
            "locked_surface_counts": workflow_locked,
        },
        "baseline_summary": {
            "baseline_version": baseline.get("baseline_version"),
            "locked_surface_counts": baseline_locked,
        },
        "docs_summary": {
            "smoke_version": docs.get("smoke_version"),
            "checked_file_count": docs.get("checked_file_count"),
            "checked_files": docs.get("checked_files"),
        },
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
