#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools" / "runes_shield"
LOCK_VERSION = "m59-agent-onboarding-lock-v1"
OUTPUT_CHOICES = ("table", "json")

COMMANDS = {
    "m57_baseline": [TOOLS / "runes_shield_baseline.py", "--format", "json"],
    "m58_workflow": [TOOLS / "runes_governed_agent_workflow.py", "--format", "json"],
    "m58_docs": [TOOLS / "smoke_m58_docs.py"],
    "m58_integration": [TOOLS / "smoke_m58_integration.py"],
}

EXPECTED_LOCKED_SURFACES = {
    "verity_checks": 10,
    "invocation_tools": 8,
    "adapter_safe_intents": 9,
    "adapter_blocked_intents": 7,
}

FORBIDDEN_TRUE_EFFECTS = {
    "trusted_wiki_write",
    "markdown_mutation",
    "index_update",
    "automatic_apply",
    "automatic_promotion",
    "database_mutation",
    "observation_ingested_to_rag",
    "session_reexecuted",
    "adapter_reinvoked",
    "audit_log_written",
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


def collect_forbidden_effects(value, path, issues):
    if isinstance(value, dict):
        effects = value.get("effects")
        if isinstance(effects, dict):
            for key in FORBIDDEN_TRUE_EFFECTS:
                if effects.get(key) is True:
                    issues.append({
                        "code": "forbidden_effect_true",
                        "path": f"{path}.effects.{key}",
                        "message": f"Forbidden effect became true: {key}",
                    })
        for key, child in value.items():
            if key == "payload":
                continue
            collect_forbidden_effects(child, f"{path}.{key}", issues)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            collect_forbidden_effects(child, f"{path}[{index}]", issues)


def build_lock(timeout=90):
    issues = []
    results = {}

    for name, command in COMMANDS.items():
        try:
            payload = run_json(command, timeout=timeout)
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
                "code": "component_failed",
                "component": name,
                "message": f"{name} did not report PASS.",
            })

        if payload.get("write") is not False:
            issues.append({
                "code": "component_write_not_false",
                "component": name,
                "message": f"{name} write must remain false.",
            })

        if payload.get("issue_count") not in (0, None):
            issues.append({
                "code": "component_issue_count_nonzero",
                "component": name,
                "message": f"{name} reported non-zero issues.",
            })

        collect_forbidden_effects(payload, name, issues)

    baseline = results.get("m57_baseline", {})
    workflow = results.get("m58_workflow", {})
    docs = results.get("m58_docs", {})
    integration = results.get("m58_integration", {})

    baseline_locked = baseline.get("locked_surface_counts", {})
    workflow_locked = workflow.get("post_workflow_verification", {}).get("locked_surface_counts", {})
    integration_workflow_locked = integration.get("workflow_summary", {}).get("locked_surface_counts", {})
    integration_baseline_locked = integration.get("baseline_summary", {}).get("locked_surface_counts", {})

    locked_sets = {
        "baseline": baseline_locked,
        "workflow": workflow_locked,
        "integration_workflow": integration_workflow_locked,
        "integration_baseline": integration_baseline_locked,
    }

    for label, locked in locked_sets.items():
        if locked != EXPECTED_LOCKED_SURFACES:
            issues.append({
                "code": "locked_surface_drift",
                "surface": label,
                "message": f"Locked surface drifted for {label}.",
            })

    if workflow.get("agent_scope") != "agent-agnostic":
        issues.append({
            "code": "agent_scope_drift",
            "message": "M58 workflow must remain agent-agnostic.",
        })

    if workflow.get("workflow_version") != "m58-governed-agent-workflow-v1":
        issues.append({
            "code": "workflow_version_drift",
            "message": "Unexpected M58 workflow version.",
        })

    if docs.get("checked_file_count") != 3:
        issues.append({
            "code": "docs_checked_file_count_drift",
            "message": "M58 docs smoke must check exactly 3 files.",
        })

    return {
        "lock_version": LOCK_VERSION,
        "status": "PASS" if not issues else "FAIL",
        "mode": "generic-agent-onboarding-lock",
        "scale": "personal-local",
        "write": False,
        "onboarding_target": "Generic Agent Onboarding Path",
        "agent_scope": workflow.get("agent_scope"),
        "readiness": {
            "runtime_workflow": workflow.get("status"),
            "baseline": baseline.get("status"),
            "docs": docs.get("status"),
            "integration": integration.get("status"),
            "ready_for_governed_access": not issues,
        },
        "components": {
            name: {
                "status": payload.get("status"),
                "write": payload.get("write"),
                "issue_count": payload.get("issue_count"),
            }
            for name, payload in results.items()
        },
        "locked_surface_counts": locked_sets,
        "expected_locked_surfaces": EXPECTED_LOCKED_SURFACES,
        "safety_boundary": {
            "trusted_wiki_write": False,
            "markdown_mutation": False,
            "database_mutation": False,
            "automatic_apply": False,
            "automatic_promotion": False,
            "background_worker": False,
            "recursive_invocation": False,
            "unbounded_audit_scan": False,
            "automatic_remediation": False,
            "forbidden_true_effects": sorted(FORBIDDEN_TRUE_EFFECTS),
        },
        "issue_count": len(issues),
        "issues": issues,
    }


def render_table(payload):
    lines = [
        f"lock_version: {payload['lock_version']}",
        f"status: {payload['status']}",
        f"mode: {payload['mode']}",
        f"scale: {payload['scale']}",
        f"write: {payload['write']}",
        f"onboarding_target: {payload['onboarding_target']}",
        f"agent_scope: {payload['agent_scope']}",
        f"ready_for_governed_access: {payload['readiness']['ready_for_governed_access']}",
        f"issue_count: {payload['issue_count']}",
        "components:",
    ]
    for name, component in payload["components"].items():
        lines.append(
            f"  - {name}: status={component['status']} write={component['write']} issues={component['issue_count']}"
        )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="M59 Generic Agent Onboarding Lock: verify M57 + M58 readiness path."
    )
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="json")

    args = parser.parse_args()
    payload = build_lock(timeout=args.timeout)

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(render_table(payload))


if __name__ == "__main__":
    main()
