#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "runes_shield" / "runes_audit_volume_pressure.py"


def run(fmt="json"):
    return subprocess.run(
        [
            sys.executable,
            str(CLI),
            "--sessions",
            "12",
            "--max-events",
            "10",
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
    print("== M56.3 Audit Volume Pressure Smoke ==")

    payload = json.loads(run().stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if payload["pressure_version"] != "m56.3-audit-volume-pressure-v1":
        raise SystemExit("unexpected pressure version")

    if payload["status"] != "PASS":
        raise SystemExit("audit volume pressure test failed")

    if payload["mode"] != "audit-volume-pressure-test":
        raise SystemExit("unexpected pressure mode")

    if payload["scale"] != "personal-local":
        raise SystemExit("pressure test scale drift detected")

    if payload["write"] is not False:
        raise SystemExit("pressure test must remain read-only")

    if payload["sessions_generated"] != 12:
        raise SystemExit("unexpected generated session count")

    if payload["expected_event_count"] != 24:
        raise SystemExit("unexpected expected event count")

    summary = payload["summary"]

    if summary["status"] != "PASS":
        raise SystemExit("recall summary failed under pressure")

    if summary["event_count"] != 24:
        raise SystemExit("summary event count mismatch")

    if summary["session_count"] != 12:
        raise SystemExit("summary session count mismatch")

    if summary["write"] is not False:
        raise SystemExit("summary must remain read-only")

    verity = payload["verity"]

    if verity["status"] != "PASS":
        raise SystemExit("verity failed under audit pressure")

    if verity["write"] is not False:
        raise SystemExit("verity must remain read-only")

    bounded = verity["bounded_sample"]

    if bounded["events_checked"] > 10:
        raise SystemExit("bounded sample exceeded max_events")

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

    if load_safety["max_events_checked"] != 10:
        raise SystemExit("max_events_checked drift detected")

    if load_safety["max_recent_days"] != 3:
        raise SystemExit("max_recent_days drift detected")

    if payload["side_effect_boundary"]["status"] != "PASS":
        raise SystemExit("side effect boundary failed under pressure")

    if payload["side_effect_boundary"]["violation_count"] != 0:
        raise SystemExit("side effect violations detected under pressure")

    if payload["issue_count"] != 0:
        raise SystemExit("pressure test must report zero issues")

    table_output = run(fmt="table").stdout

    if "audit-volume-pressure-test" not in table_output:
        raise SystemExit("table output missing pressure mode")

    if "side_effect_boundary: PASS" not in table_output:
        raise SystemExit("table output missing side effect boundary PASS")

    print("PASS: audit volume pressure validation completed")


if __name__ == "__main__":
    main()
