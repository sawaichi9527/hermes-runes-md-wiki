#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools" / "runes_shield"
SNAPSHOT_VERSION = "m56.6-governance-compatibility-snapshot-v1"
OUTPUT_CHOICES = ("table", "json")

COMMANDS = {
    "integrity": [TOOLS / "proposal_governance_integrity.py", "--format", "json"],
    "controlled_trial": [TOOLS / "proposal_controlled_trial_run.py", "--format", "json"],
    "verity": [TOOLS / "runes_verity.py", "--format", "json", "--max-events", "25", "--max-recent-days", "3"],
    "verity_contract": [TOOLS / "validate_runes_verity_contract.py", "--run", "--format", "json"],
    "bounded_regression": [TOOLS / "runes_verity_bounded_regression.py", "--iterations", "2", "--max-events", "25", "--max-recent-days", "3", "--format", "json"],
    "invocation_contract": [TOOLS / "validate_invocation_contract.py", "--format", "json"],
}

EXPECTED_VERSIONS = {
    "integrity_version": "m49-governance-integrity-v1",
    "trial_run_version": "m50-controlled-trial-run-v1",
    "shield_version": "m51-runes-shield-invocation-v1",
    "adapter_version": "m52-hermes-agent-adapter-v1",
    "session_version": "m53-runtime-invocation-session-v1",
    "persistence_version": "m54-runtime-audit-persistence-v1",
    "recall_version": "m55-governance-audit-recall-v1",
    "verity_version": "m56-runes-mouth-of-verity-v1",
    "verity_contract_version": "m56.1-runes-verity-contract-v1",
    "bounded_regression_version": "m56.2-runes-verity-bounded-regression-v1",
    "audit_pressure_version": "m56.3-audit-volume-pressure-v1",
    "replay_safety_version": "m56.4-replay-safety-regression-v1",
    "invocation_contract_version": "m56.5-invocation-contract-v1",
}

EXPECTED_CHECKS = [
    "integrity_oath",
    "trial_run_oath",
    "invocation_oath",
    "adapter_oath",
    "session_oath",
    "persistence_oath",
    "recall_replay_oath",
    "side_effect_oath",
    "abyss_guard",
    "calamity_guard",
]

EXPECTED_TOOLS = [
    "governance.history",
    "governance.integrity",
    "governance.timeline",
    "manifest.list",
    "observation.export",
    "review_queue.list",
    "state_projection.list",
    "trial_run.controlled",
]

EXPECTED_SAFE_INTENTS = [
    "discover_tools",
    "list_manifest",
    "list_review_queue",
    "list_state_projection",
    "show_timeline",
    "show_history",
    "check_integrity",
    "run_controlled_trial",
    "export_observations",
]

EXPECTED_BLOCKED_INTENTS = [
    "apply_wiki",
    "auto_approve",
    "mutate_database",
    "promote_memory",
    "spawn_background_worker",
    "write_decision",
    "write_wiki",
]

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


def build_snapshot(timeout=15):
    issues = []
    results = {}

    for name, command in COMMANDS.items():
        payload = run_json(command, timeout=timeout + 10)
        results[name] = payload
        if payload.get("status") != "PASS":
            issues.append(_issue("component_not_pass", f"{name} did not report PASS."))
        if payload.get("write") is not False:
            issues.append(_issue("component_write_not_false", f"{name} write was not false."))
        collect_forbidden_effects(payload, name, issues)

    verity = results["verity"]
    invocation_contract = results["invocation_contract"]
    verity_contract = results["verity_contract"]
    bounded_regression = results["bounded_regression"]

    checks = [check.get("check") for check in verity.get("checks", [])]
    if checks != EXPECTED_CHECKS:
        issues.append(_issue("verity_check_set_drift", "Runes Verity check set/order drifted."))

    locked_checks = verity_contract.get("locked_contract", {}).get("expected_checks")
    if locked_checks != EXPECTED_CHECKS:
        issues.append(_issue("verity_contract_check_drift", "Runes Verity contract expected checks drifted."))

    expected_tools = sorted(invocation_contract.get("locked_contract", {}).get("expected_tools", {}).keys())
    if expected_tools != sorted(EXPECTED_TOOLS):
        issues.append(_issue("invocation_tool_surface_drift", "Invocation tool surface drifted."))

    safe_intents = sorted(invocation_contract.get("locked_contract", {}).get("expected_intent_tool_map", {}).keys())
    if safe_intents != sorted(EXPECTED_SAFE_INTENTS):
        issues.append(_issue("safe_intent_surface_drift", "Adapter safe intent surface drifted."))

    blocked_intents = sorted(invocation_contract.get("locked_contract", {}).get("expected_blocked_intents", []))
    if blocked_intents != sorted(EXPECTED_BLOCKED_INTENTS):
        issues.append(_issue("blocked_intent_surface_drift", "Adapter blocked intent surface drifted."))

    load_safety = verity.get("load_safety", {})
    if load_safety.get("background_worker") is not False:
        issues.append(_issue("background_worker_enabled", "background_worker must remain false."))
    if load_safety.get("recursive_invocation") is not False:
        issues.append(_issue("recursive_invocation_enabled", "recursive_invocation must remain false."))
    if load_safety.get("unbounded_audit_scan") is not False:
        issues.append(_issue("unbounded_audit_scan_enabled", "unbounded_audit_scan must remain false."))
    if load_safety.get("automatic_remediation") is not False:
        issues.append(_issue("automatic_remediation_enabled", "automatic_remediation must remain false."))

    if bounded_regression.get("stability", {}).get("status") != "PASS":
        issues.append(_issue("bounded_regression_stability_failed", "Bounded regression stability failed."))
    if bounded_regression.get("side_effect_boundary", {}).get("status") != "PASS":
        issues.append(_issue("bounded_regression_side_effect_failed", "Bounded regression side-effect boundary failed."))
    if bounded_regression.get("load_safety", {}).get("status") != "PASS":
        issues.append(_issue("bounded_regression_load_safety_failed", "Bounded regression load safety failed."))

    compatibility_matrix = {
        "governance_core": {
            "m49_integrity": _status(results["integrity"]),
            "m50_controlled_trial": _status(results["controlled_trial"]),
        },
        "runtime_boundary": {
            "m51_invocation_tools": {
                "status": invocation_contract.get("status"),
                "tool_count": invocation_contract.get("discovery", {}).get("tool_count"),
                "tools": EXPECTED_TOOLS,
            },
            "m52_adapter_intents": {
                "status": invocation_contract.get("status"),
                "safe_intents": EXPECTED_SAFE_INTENTS,
                "blocked_intents": EXPECTED_BLOCKED_INTENTS,
            },
        },
        "runtime_observability": {
            "m53_session": _check_status(verity, "session_oath"),
            "m54_persistence": _check_status(verity, "persistence_oath"),
            "m55_recall_replay": _check_status(verity, "recall_replay_oath"),
        },
        "truth_gate_hardening": {
            "m56_verity": _status(verity),
            "m56_1_contract": _status(verity_contract),
            "m56_2_bounded_regression": _status(bounded_regression),
            "m56_5_invocation_contract": _status(invocation_contract),
        },
    }

    return {
        "snapshot_version": SNAPSHOT_VERSION,
        "status": "PASS" if not issues else "FAIL",
        "mode": "governance-compatibility-snapshot",
        "scale": "personal-local",
        "write": False,
        "compatibility_target": "Runes Shield P0/P1 transitional governed runtime baseline",
        "expected_versions": EXPECTED_VERSIONS,
        "compatibility_matrix": compatibility_matrix,
        "locked_surfaces": {
            "verity_checks": EXPECTED_CHECKS,
            "invocation_tools": EXPECTED_TOOLS,
            "adapter_safe_intents": EXPECTED_SAFE_INTENTS,
            "adapter_blocked_intents": EXPECTED_BLOCKED_INTENTS,
            "forbidden_true_effects": sorted(FORBIDDEN_TRUE_EFFECTS),
        },
        "load_safety": {
            "bounded_execution": load_safety.get("bounded_execution"),
            "single_shot": load_safety.get("single_shot"),
            "background_worker": load_safety.get("background_worker"),
            "recursive_invocation": load_safety.get("recursive_invocation"),
            "unbounded_audit_scan": load_safety.get("unbounded_audit_scan"),
            "automatic_remediation": load_safety.get("automatic_remediation"),
            "max_events_checked": load_safety.get("max_events_checked"),
            "max_recent_days": load_safety.get("max_recent_days"),
        },
        "component_statuses": {name: _status(payload) for name, payload in results.items()},
        "issue_count": len(issues),
        "issues": issues,
    }


def _status(payload):
    return {
        "status": payload.get("status"),
        "write": payload.get("write"),
        "issue_count": payload.get("issue_count"),
    }


def _check_status(verity, check_name):
    for check in verity.get("checks", []):
        if check.get("check") == check_name:
            evidence = check.get("evidence", {}) if isinstance(check.get("evidence"), dict) else {}
            return {
                "status": check.get("status"),
                "write": check.get("write"),
                "evidence_status": evidence.get("status"),
            }
    return {"status": "MISSING", "write": None, "evidence_status": None}


def collect_forbidden_effects(value, path, issues):
    if isinstance(value, dict):
        effects = value.get("effects")
        if isinstance(effects, dict):
            for key in FORBIDDEN_TRUE_EFFECTS:
                if effects.get(key) is True:
                    issues.append(_issue("forbidden_effect_true", f"{path}.effects.{key} became true."))
        for key, child in value.items():
            collect_forbidden_effects(child, f"{path}.{key}", issues)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            collect_forbidden_effects(child, f"{path}[{index}]", issues)


def _issue(code, message):
    return {"code": code, "message": message}


def render_table(payload):
    lines = [
        f"snapshot_version: {payload['snapshot_version']}",
        f"status: {payload['status']}",
        f"mode: {payload['mode']}",
        f"scale: {payload['scale']}",
        f"write: {payload['write']}",
        f"compatibility_target: {payload['compatibility_target']}",
        f"issue_count: {payload['issue_count']}",
        "components:",
    ]
    for name, status in payload["component_statuses"].items():
        lines.append(f"  - {name}: status={status['status']} write={status['write']} issues={status['issue_count']}")
    lines.append("locked_surfaces:")
    lines.append(f"  verity_checks: {len(payload['locked_surfaces']['verity_checks'])}")
    lines.append(f"  invocation_tools: {len(payload['locked_surfaces']['invocation_tools'])}")
    lines.append(f"  adapter_safe_intents: {len(payload['locked_surfaces']['adapter_safe_intents'])}")
    lines.append(f"  adapter_blocked_intents: {len(payload['locked_surfaces']['adapter_blocked_intents'])}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Create a read-only governance compatibility snapshot for Runes Shield baseline."
    )
    parser.add_argument("--timeout", type=int, default=15)
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="json")

    args = parser.parse_args()
    payload = build_snapshot(timeout=args.timeout)

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(render_table(payload))


if __name__ == "__main__":
    main()
