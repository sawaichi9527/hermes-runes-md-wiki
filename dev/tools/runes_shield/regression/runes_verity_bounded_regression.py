#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERITY = ROOT / "tools" / "runes_shield" / "runes_verity.py"
CONTRACT = ROOT / "tools" / "runes_shield" / "validate_runes_verity_contract.py"
REGRESSION_VERSION = "m56.2-runes-verity-bounded-regression-v1"
OUTPUT_CHOICES = ("table", "json")

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


def run_process(args, timeout, input_text=None):
    return subprocess.run(
        [sys.executable, *[str(arg) for arg in args]],
        cwd=ROOT,
        input=input_text,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=True,
    )


def load_verity_payload(max_events, max_recent_days, timeout):
    completed = run_process(
        [
            VERITY,
            "--format",
            "json",
            "--max-events",
            str(max_events),
            "--max-recent-days",
            str(max_recent_days),
            "--timeout",
            str(timeout),
        ],
        timeout=timeout + 10,
    )
    return json.loads(completed.stdout)


def validate_contract(payload, timeout):
    completed = run_process(
        [
            CONTRACT,
            "--format",
            "json",
        ],
        timeout=timeout + 10,
        input_text=json.dumps(payload),
    )
    return json.loads(completed.stdout)


def build_regression(iterations=3, max_events=25, max_recent_days=3, timeout=15):
    runs = []
    issues = []

    if iterations <= 0 or iterations > 5:
        issues.append(
            _issue(
                "invalid_iterations",
                "iterations must be bounded in range 1..5 for personal-local regression.",
            )
        )
        iterations = min(max(iterations, 1), 5)

    for index in range(iterations):
        payload = load_verity_payload(max_events=max_events, max_recent_days=max_recent_days, timeout=timeout)
        contract = validate_contract(payload, timeout=timeout)
        run = summarize_run(index + 1, payload, contract)
        runs.append(run)

        if run["status"] != "PASS":
            issues.append(_issue("run_failed", f"Run {index + 1} failed bounded regression."))

    stability = evaluate_stability(runs)
    if stability["status"] != "PASS":
        issues.extend(stability["issues"])

    side_effects = evaluate_side_effects(runs)
    if side_effects["status"] != "PASS":
        issues.extend(side_effects["issues"])

    load_safety = evaluate_load_safety(runs, max_events=max_events, max_recent_days=max_recent_days, timeout=timeout)
    if load_safety["status"] != "PASS":
        issues.extend(load_safety["issues"])

    return {
        "regression_version": REGRESSION_VERSION,
        "status": "PASS" if not issues else "FAIL",
        "mode": "bounded-runtime-regression",
        "scale": "personal-local",
        "write": False,
        "iterations": iterations,
        "runs": runs,
        "stability": stability,
        "side_effect_boundary": side_effects,
        "load_safety": load_safety,
        "issue_count": len(issues),
        "issues": issues,
    }


def summarize_run(run_index, payload, contract):
    checks = payload.get("checks", [])
    check_names = [check.get("check") for check in checks]
    statuses = {check.get("check"): check.get("status") for check in checks}
    load_safety = payload.get("load_safety", {})
    violations = []
    collect_forbidden_effects(payload, "$", violations)

    status = "PASS"
    if payload.get("status") != "PASS":
        status = "FAIL"
    if contract.get("status") != "PASS":
        status = "FAIL"
    if payload.get("write") is not False:
        status = "FAIL"
    if violations:
        status = "FAIL"

    return {
        "run_index": run_index,
        "status": status,
        "verity_status": payload.get("status"),
        "contract_status": contract.get("status"),
        "contract_issue_count": contract.get("issue_count"),
        "write": payload.get("write"),
        "check_count": len(checks),
        "check_names": check_names,
        "check_statuses": statuses,
        "load_safety": load_safety,
        "summary": payload.get("summary"),
        "forbidden_effect_violation_count": len(violations),
        "forbidden_effect_violations": violations[:10],
    }


def evaluate_stability(runs):
    issues = []
    if not runs:
        return {"status": "FAIL", "issues": [_issue("no_runs", "No regression runs were executed.")]}

    baseline_checks = runs[0]["check_names"]
    for run in runs:
        if run["check_names"] != baseline_checks:
            issues.append(_issue("check_set_drift", f"Run {run['run_index']} check set/order drifted."))
        if run["contract_status"] != "PASS":
            issues.append(_issue("contract_failed", f"Run {run['run_index']} contract failed."))
        if run["contract_issue_count"] != 0:
            issues.append(_issue("contract_issues", f"Run {run['run_index']} had contract issues."))

    return {
        "status": "PASS" if not issues else "FAIL",
        "stable_check_order": not issues,
        "baseline_checks": baseline_checks,
        "issues": issues,
    }


def evaluate_side_effects(runs):
    issues = []
    for run in runs:
        if run["write"] is not False:
            issues.append(_issue("write_not_false", f"Run {run['run_index']} write flag was not false."))
        if run["forbidden_effect_violation_count"]:
            issues.append(
                _issue(
                    "forbidden_effects",
                    f"Run {run['run_index']} reported forbidden effects.",
                )
            )

    return {
        "status": "PASS" if not issues else "FAIL",
        "write": False,
        "forbidden_true_effects": sorted(FORBIDDEN_TRUE_EFFECTS),
        "issues": issues,
    }


def evaluate_load_safety(runs, max_events, max_recent_days, timeout):
    issues = []
    for run in runs:
        safety = run.get("load_safety") or {}
        expected = {
            "bounded_execution": True,
            "single_shot": True,
            "background_worker": False,
            "recursive_invocation": False,
            "unbounded_audit_scan": False,
            "automatic_remediation": False,
        }
        for key, value in expected.items():
            if safety.get(key) != value:
                issues.append(_issue("load_safety_drift", f"Run {run['run_index']} {key} drifted."))
        if safety.get("max_events_checked") != max_events:
            issues.append(_issue("max_events_drift", f"Run {run['run_index']} max_events_checked drifted."))
        if safety.get("max_recent_days") != max_recent_days:
            issues.append(_issue("max_recent_days_drift", f"Run {run['run_index']} max_recent_days drifted."))
        if safety.get("timeout_sec_per_check") != timeout:
            issues.append(_issue("timeout_drift", f"Run {run['run_index']} timeout_sec_per_check drifted."))

    return {
        "status": "PASS" if not issues else "FAIL",
        "bounded_execution": True,
        "single_shot": True,
        "background_worker": False,
        "recursive_invocation": False,
        "unbounded_audit_scan": False,
        "automatic_remediation": False,
        "max_events_checked": max_events,
        "max_recent_days": max_recent_days,
        "timeout_sec_per_check": timeout,
        "issues": issues,
    }


def collect_forbidden_effects(value, path, violations):
    if isinstance(value, dict):
        effects = value.get("effects")
        if isinstance(effects, dict):
            for key in FORBIDDEN_TRUE_EFFECTS:
                if effects.get(key) is True:
                    violations.append({"path": f"{path}.effects.{key}", "effect": key})
        for key, child in value.items():
            collect_forbidden_effects(child, f"{path}.{key}", violations)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            collect_forbidden_effects(child, f"{path}[{index}]", violations)


def _issue(code, message):
    return {"code": code, "message": message}


def render_table(payload):
    lines = [
        f"regression_version: {payload['regression_version']}",
        f"status: {payload['status']}",
        f"mode: {payload['mode']}",
        f"scale: {payload['scale']}",
        f"write: {payload['write']}",
        f"iterations: {payload['iterations']}",
        f"issue_count: {payload['issue_count']}",
        "runs:",
    ]
    for run in payload["runs"]:
        lines.append(
            f"  - run={run['run_index']} status={run['status']} "
            f"contract={run['contract_status']} checks={run['check_count']}"
        )
    lines.append(f"stability: {payload['stability']['status']}")
    lines.append(f"side_effect_boundary: {payload['side_effect_boundary']['status']}")
    lines.append(f"load_safety: {payload['load_safety']['status']}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Bounded-runtime regression runner for Runes Mouth of Verity."
    )
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--max-events", type=int, default=25)
    parser.add_argument("--max-recent-days", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=15)
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="json")

    args = parser.parse_args()
    payload = build_regression(
        iterations=args.iterations,
        max_events=args.max_events,
        max_recent_days=args.max_recent_days,
        timeout=args.timeout,
    )

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(render_table(payload))


if __name__ == "__main__":
    main()
