#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools" / "runes_shield"
BASELINE_VERSION = "m57-runes-shield-baseline-lock-v1"
OUTPUT_CHOICES = ("table", "json")

BASELINE_COMPONENTS = {
    "m49_integrity": [TOOLS / "proposal_governance_integrity.py", "--format", "json"],
    "m50_controlled_trial": [TOOLS / "proposal_controlled_trial_run.py", "--format", "json"],
    "m56_verity": [TOOLS / "runes_verity.py", "--format", "json", "--max-events", "25", "--max-recent-days", "3"],
    "m56_1_verity_contract": [TOOLS / "validate_runes_verity_contract.py", "--run", "--format", "json"],
    "m56_2_bounded_regression": [TOOLS / "runes_verity_bounded_regression.py", "--iterations", "2", "--max-events", "25", "--max-recent-days", "3", "--format", "json"],
    "m56_3_audit_pressure": [TOOLS / "runes_audit_volume_pressure.py", "--sessions", "6", "--max-events", "5", "--max-recent-days", "3", "--format", "json"],
    "m56_4_replay_safety": [TOOLS / "runes_replay_safety_regression.py", "--iterations", "3", "--format", "json"],
    "m56_5_invocation_contract": [TOOLS / "validate_invocation_contract.py", "--format", "json"],
    "m56_6_compat_snapshot": [TOOLS / "runes_governance_compat_snapshot.py", "--format", "json"],
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
}


def run_component(name, command, timeout):
    try:
        completed = subprocess.run(
            [sys.executable, *[str(part) for part in command]],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True,
        )
        payload = json.loads(completed.stdout)
        return {
            "component": name,
            "status": "PASS" if payload.get("status") == "PASS" else "FAIL",
            "returncode": completed.returncode,
            "payload": payload,
            "error": None,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "component": name,
            "status": "FAIL",
            "returncode": None,
            "payload": None,
            "error": {
                "type": "timeout",
                "message": f"component timed out after {timeout}s",
                "stdout_tail": (exc.stdout or "")[-800:] if isinstance(exc.stdout, str) else "",
                "stderr_tail": (exc.stderr or "")[-800:] if isinstance(exc.stderr, str) else "",
            },
        }
    except Exception as exc:
        return {
            "component": name,
            "status": "FAIL",
            "returncode": None,
            "payload": None,
            "error": {
                "type": exc.__class__.__name__,
                "message": str(exc),
            },
        }


def build_baseline(timeout=30):
    issues = []
    component_results = []

    for name, command in BASELINE_COMPONENTS.items():
        result = run_component(name, command, timeout=timeout)
        component_results.append(summarize_component(result))
        payload = result.get("payload")

        if result["status"] != "PASS":
            issues.append(_issue("component_failed", f"{name} did not pass."))

        if isinstance(payload, dict):
            if payload.get("write") is not False:
                issues.append(_issue("component_write_not_false", f"{name} write was not false."))
            collect_forbidden_effects(payload, name, issues)

    compat = _payload_for(component_results, "m56_6_compat_snapshot") or {}
    locked = compat.get("locked_surfaces", {}) if isinstance(compat, dict) else {}

    locked_counts = {
        "verity_checks": len(locked.get("verity_checks", [])),
        "invocation_tools": len(locked.get("invocation_tools", [])),
        "adapter_safe_intents": len(locked.get("adapter_safe_intents", [])),
        "adapter_blocked_intents": len(locked.get("adapter_blocked_intents", [])),
    }

    for key, expected in EXPECTED_LOCKED_SURFACES.items():
        if locked_counts.get(key) != expected:
            issues.append(_issue("locked_surface_drift", f"{key} expected {expected}, got {locked_counts.get(key)}."))

    verity = _payload_for(component_results, "m56_verity") or {}
    load_safety = verity.get("load_safety", {}) if isinstance(verity, dict) else {}
    for key in ("background_worker", "recursive_invocation", "unbounded_audit_scan", "automatic_remediation"):
        if load_safety.get(key) is not False:
            issues.append(_issue("load_safety_drift", f"{key} must remain false."))

    if load_safety.get("bounded_execution") is not True:
        issues.append(_issue("load_safety_drift", "bounded_execution must remain true."))
    if load_safety.get("single_shot") is not True:
        issues.append(_issue("load_safety_drift", "single_shot must remain true."))

    return {
        "baseline_version": BASELINE_VERSION,
        "status": "PASS" if not issues else "FAIL",
        "mode": "runes-shield-baseline-lock",
        "scale": "personal-local",
        "write": False,
        "baseline_target": "Runes Shield P0/P1 Transitional Runtime Baseline",
        "component_count": len(BASELINE_COMPONENTS),
        "components": component_results,
        "locked_surface_counts": locked_counts,
        "expected_locked_surfaces": EXPECTED_LOCKED_SURFACES,
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
        "side_effect_boundary": {
            "forbidden_true_effects": sorted(FORBIDDEN_TRUE_EFFECTS),
            "status": "PASS" if not any(issue["code"] == "forbidden_effect_true" for issue in issues) else "FAIL",
        },
        "issue_count": len(issues),
        "issues": issues,
    }


def summarize_component(result):
    payload = result.get("payload")
    summary = {
        "component": result["component"],
        "status": result["status"],
        "returncode": result.get("returncode"),
        "write": payload.get("write") if isinstance(payload, dict) else None,
        "version": _extract_version(payload) if isinstance(payload, dict) else None,
        "issue_count": payload.get("issue_count") if isinstance(payload, dict) else None,
        "error": result.get("error"),
        "payload": payload,
    }
    return summary


def _extract_version(payload):
    for key in (
        "baseline_version",
        "snapshot_version",
        "pressure_version",
        "regression_version",
        "contract_version",
        "verity_version",
        "integrity_version",
        "trial_run_version",
    ):
        if key in payload:
            return payload[key]
    return None


def _payload_for(components, name):
    for component in components:
        if component.get("component") == name:
            return component.get("payload")
    return None


def collect_forbidden_effects(value, path, issues):
    if isinstance(value, dict):
        effects = value.get("effects")
        if isinstance(effects, dict):
            for key in FORBIDDEN_TRUE_EFFECTS:
                if effects.get(key) is True:
                    issues.append(_issue("forbidden_effect_true", f"{path}.effects.{key} became true."))
        for key, child in value.items():
            if key == "payload":
                continue
            collect_forbidden_effects(child, f"{path}.{key}", issues)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            collect_forbidden_effects(child, f"{path}[{index}]", issues)


def _issue(code, message):
    return {"code": code, "message": message}


def render_table(payload):
    lines = [
        f"baseline_version: {payload['baseline_version']}",
        f"status: {payload['status']}",
        f"mode: {payload['mode']}",
        f"scale: {payload['scale']}",
        f"write: {payload['write']}",
        f"baseline_target: {payload['baseline_target']}",
        f"component_count: {payload['component_count']}",
        f"issue_count: {payload['issue_count']}",
        "components:",
    ]
    for component in payload["components"]:
        lines.append(
            f"  - {component['component']}: status={component['status']} "
            f"write={component['write']} version={component['version']} issues={component['issue_count']}"
        )
    lines.append("locked_surface_counts:")
    for key, value in payload["locked_surface_counts"].items():
        lines.append(f"  {key}: {value}")
    lines.append("load_safety:")
    for key, value in payload["load_safety"].items():
        lines.append(f"  {key}: {value}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Runes Shield baseline lock runner for P0/P1 transitional runtime baseline."
    )
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="json")

    args = parser.parse_args()
    payload = build_baseline(timeout=args.timeout)

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(render_table(payload))


if __name__ == "__main__":
    main()
