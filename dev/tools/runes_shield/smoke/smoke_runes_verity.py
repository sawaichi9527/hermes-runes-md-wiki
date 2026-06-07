#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "runes_shield" / "runes_verity.py"

REQUIRED_CHECKS = {
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
}


def run(fmt="json"):
    return subprocess.run(
        [
            sys.executable,
            str(CLI),
            "--max-events",
            "100",
            "--max-recent-days",
            "7",
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
    print("== M56 Runes Mouth of Verity Smoke ==")

    payload = json.loads(run().stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if payload["verity_version"] != "m56-runes-mouth-of-verity-v1":
        raise SystemExit("unexpected verity version")

    if payload["name"] != "Runes Mouth of Verity":
        raise SystemExit("unexpected verity formal name")

    if payload["status"] != "PASS":
        raise SystemExit("Runes Mouth of Verity did not pass")

    if payload["write"] is not False:
        raise SystemExit("Runes Mouth of Verity must remain read-only")

    if payload["scale"] != "personal-local":
        raise SystemExit("M56 must remain personal-local scale")

    check_names = {check["check"] for check in payload["checks"]}

    if check_names != REQUIRED_CHECKS:
        missing = sorted(REQUIRED_CHECKS - check_names)
        extra = sorted(check_names - REQUIRED_CHECKS)
        raise SystemExit(f"unexpected check set missing={missing} extra={extra}")

    for check in payload["checks"]:
        if check["status"] != "PASS":
            raise SystemExit(f"check failed: {check['check']}")
        if check["write"] is not False:
            raise SystemExit(f"check must remain read-only: {check['check']}")
        if check["bounded"] is not True:
            raise SystemExit(f"check must remain bounded: {check['check']}")

    load_safety = payload["load_safety"]

    if load_safety["bounded_execution"] is not True:
        raise SystemExit("bounded_execution must be true")

    if load_safety["single_shot"] is not True:
        raise SystemExit("single_shot must be true")

    for key in (
        "background_worker",
        "recursive_invocation",
        "unbounded_audit_scan",
        "automatic_remediation",
    ):
        if load_safety[key] is not False:
            raise SystemExit(f"load safety flag must remain false: {key}")

    if load_safety["max_events_checked"] > 100:
        raise SystemExit("max_events_checked must remain bounded")

    table_output = run(fmt="table").stdout

    if "Runes Mouth of Verity" not in table_output:
        raise SystemExit("table output missing formal name")

    if "calamity_guard: PASS" not in table_output:
        raise SystemExit("table output missing calamity guard")

    print("PASS: Runes Mouth of Verity validation completed")


if __name__ == "__main__":
    main()
