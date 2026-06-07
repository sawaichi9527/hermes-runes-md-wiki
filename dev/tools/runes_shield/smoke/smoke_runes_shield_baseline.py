#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "runes_shield" / "runes_shield_baseline.py"


def run(fmt="json"):
    return subprocess.run(
        [
            sys.executable,
            str(CLI),
            "--timeout",
            "30",
            "--format",
            fmt,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )


def main():
    print("== M57 Runes Shield Baseline Smoke ==")

    payload = json.loads(run().stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if payload["baseline_version"] != "m57-runes-shield-baseline-lock-v1":
        raise SystemExit("unexpected baseline version")

    if payload["status"] != "PASS":
        raise SystemExit("baseline lock failed")

    if payload["mode"] != "runes-shield-baseline-lock":
        raise SystemExit("unexpected baseline mode")

    if payload["scale"] != "personal-local":
        raise SystemExit("baseline scale drift detected")

    if payload["write"] is not False:
        raise SystemExit("baseline runner must remain read-only")

    if payload["component_count"] != 9:
        raise SystemExit("unexpected baseline component count")

    if payload["issue_count"] != 0:
        raise SystemExit("baseline runner must report zero issues")

    components = payload["components"]

    if len(components) != 9:
        raise SystemExit("component list length drift detected")

    required_components = {
        "m49_integrity",
        "m50_controlled_trial",
        "m56_verity",
        "m56_1_verity_contract",
        "m56_2_bounded_regression",
        "m56_3_audit_pressure",
        "m56_4_replay_safety",
        "m56_5_invocation_contract",
        "m56_6_compat_snapshot",
    }

    names = {component["component"] for component in components}

    if names != required_components:
        raise SystemExit("baseline component surface drift detected")

    for component in components:
        if component["status"] != "PASS":
            raise SystemExit(f"component failed: {component['component']}")

        if component["write"] is not False:
            raise SystemExit(f"component write drift detected: {component['component']}")

        if component["error"] is not None:
            raise SystemExit(f"component error detected: {component['component']}")

    locked = payload["locked_surface_counts"]

    expected_locked = {
        "verity_checks": 10,
        "invocation_tools": 8,
        "adapter_safe_intents": 9,
        "adapter_blocked_intents": 7,
    }

    if locked != expected_locked:
        raise SystemExit("locked surface counts drift detected")

    load_safety = payload["load_safety"]

    if load_safety["bounded_execution"] is not True:
        raise SystemExit("bounded_execution drift detected")

    if load_safety["single_shot"] is not True:
        raise SystemExit("single_shot drift detected")

    for key in (
        "background_worker",
        "recursive_invocation",
        "unbounded_audit_scan",
        "automatic_remediation",
    ):
        if load_safety[key] is not False:
            raise SystemExit(f"load safety drift detected: {key}")

    side_effects = payload["side_effect_boundary"]

    if side_effects["status"] != "PASS":
        raise SystemExit("side effect boundary failed")

    if len(side_effects["forbidden_true_effects"]) != 9:
        raise SystemExit("forbidden effect surface drift detected")

    table_output = run(fmt="table").stdout

    if "runes-shield-baseline-lock" not in table_output:
        raise SystemExit("table output missing baseline mode")

    if "component_count: 9" not in table_output:
        raise SystemExit("table output missing component count")

    print("PASS: Runes Shield baseline validation completed")


if __name__ == "__main__":
    main()
