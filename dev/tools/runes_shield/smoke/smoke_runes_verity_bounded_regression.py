#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "runes_shield" / "runes_verity_bounded_regression.py"


def run(fmt="json"):
    return subprocess.run(
        [
            sys.executable,
            str(CLI),
            "--iterations",
            "3",
            "--max-events",
            "25",
            "--max-recent-days",
            "3",
            "--timeout",
            "15",
            "--format",
            fmt,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )


def main():
    print("== M56.2 Bounded Runtime Regression Smoke ==")

    payload = json.loads(run().stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if payload["regression_version"] != "m56.2-runes-verity-bounded-regression-v1":
        raise SystemExit("unexpected regression version")

    if payload["status"] != "PASS":
        raise SystemExit("bounded regression suite failed")

    if payload["mode"] != "bounded-runtime-regression":
        raise SystemExit("unexpected regression mode")

    if payload["scale"] != "personal-local":
        raise SystemExit("regression scale drift detected")

    if payload["write"] is not False:
        raise SystemExit("bounded regression must remain read-only")

    if payload["iterations"] != 3:
        raise SystemExit("unexpected iteration count")

    if payload["issue_count"] != 0:
        raise SystemExit("bounded regression must report zero issues")

    runs = payload["runs"]

    if len(runs) != 3:
        raise SystemExit("expected exactly 3 bounded regression runs")

    baseline_checks = None

    for run_data in runs:
        if run_data["status"] != "PASS":
            raise SystemExit(f"run failed: {run_data['run_index']}")

        if run_data["contract_status"] != "PASS":
            raise SystemExit(f"contract failed: {run_data['run_index']}")

        if run_data["contract_issue_count"] != 0:
            raise SystemExit(f"contract issue count drift: {run_data['run_index']}")

        if run_data["write"] is not False:
            raise SystemExit(f"write drift detected: {run_data['run_index']}")

        if run_data["forbidden_effect_violation_count"] != 0:
            raise SystemExit(f"forbidden effects detected: {run_data['run_index']}")

        checks = run_data["check_names"]

        if baseline_checks is None:
            baseline_checks = checks
        elif checks != baseline_checks:
            raise SystemExit("bounded regression check order drift detected")

        safety = run_data["load_safety"]

        if safety["bounded_execution"] is not True:
            raise SystemExit("bounded_execution drift detected")

        if safety["single_shot"] is not True:
            raise SystemExit("single_shot drift detected")

        for key in (
            "background_worker",
            "recursive_invocation",
            "unbounded_audit_scan",
            "automatic_remediation",
        ):
            if safety[key] is not False:
                raise SystemExit(f"load safety drift detected: {key}")

        if safety["max_events_checked"] != 25:
            raise SystemExit("max_events_checked drift detected")

        if safety["max_recent_days"] != 3:
            raise SystemExit("max_recent_days drift detected")

        if safety["timeout_sec_per_check"] != 15:
            raise SystemExit("timeout_sec_per_check drift detected")

    if payload["stability"]["status"] != "PASS":
        raise SystemExit("stability regression failed")

    if payload["side_effect_boundary"]["status"] != "PASS":
        raise SystemExit("side effect boundary regression failed")

    if payload["load_safety"]["status"] != "PASS":
        raise SystemExit("load safety regression failed")

    table_output = run(fmt="table").stdout

    if "bounded-runtime-regression" not in table_output:
        raise SystemExit("table output missing regression mode")

    if "load_safety: PASS" not in table_output:
        raise SystemExit("table output missing load safety PASS")

    print("PASS: bounded runtime regression validation completed")


if __name__ == "__main__":
    main()
