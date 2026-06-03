#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "runes_shield" / "runes_replay_safety_regression.py"


def run(fmt="json"):
    return subprocess.run(
        [
            sys.executable,
            str(CLI),
            "--iterations",
            "5",
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
    print("== M56.4 Replay Safety Regression Smoke ==")

    payload = json.loads(run().stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if payload["regression_version"] != "m56.4-replay-safety-regression-v1":
        raise SystemExit("unexpected regression version")

    if payload["status"] != "PASS":
        raise SystemExit("replay safety regression failed")

    if payload["mode"] != "replay-safety-regression":
        raise SystemExit("unexpected replay regression mode")

    if payload["scale"] != "personal-local":
        raise SystemExit("replay regression scale drift detected")

    if payload["write"] is not False:
        raise SystemExit("replay regression must remain read-only")

    if payload["iterations"] != 5:
        raise SystemExit("unexpected replay iteration count")

    if payload["issue_count"] != 0:
        raise SystemExit("replay regression must report zero issues")

    seed = payload["seed"]

    if seed["status"] != "PASS":
        raise SystemExit("seed persistence failed")

    if seed["write"] is not True:
        raise SystemExit("seed persistence must perform explicit write")

    before = payload["audit_before"]
    after = payload["audit_after"]

    if before["line_count"] != after["line_count"]:
        raise SystemExit("replay changed audit line count")

    if before["line_count"] != 2:
        raise SystemExit("unexpected audit line count")

    summary = payload["summary"]

    if summary["status"] != "PASS":
        raise SystemExit("summary failed after replay regression")

    if summary["event_count"] != before["line_count"]:
        raise SystemExit("summary event count mismatch")

    if summary["write"] is not False:
        raise SystemExit("summary must remain read-only")

    replays = payload["replays"]

    if len(replays) != 5:
        raise SystemExit("expected exactly 5 replay runs")

    baseline_chain = None

    for replay in replays:
        if replay["status"] != "PASS":
            raise SystemExit(f"replay run failed: {replay['run_index']}")

        if replay["replay_status"] != "PASS":
            raise SystemExit(f"replay status drift: {replay['run_index']}")

        if replay["mode"] != "read-only-reconstruction":
            raise SystemExit(f"replay mode drift: {replay['run_index']}")

        if replay["write"] is not False:
            raise SystemExit(f"replay write drift: {replay['run_index']}")

        if replay["session_reexecuted"] is not False:
            raise SystemExit(f"session re-executed: {replay['run_index']}")

        if replay["adapter_reinvoked"] is not False:
            raise SystemExit(f"adapter reinvoked: {replay['run_index']}")

        if replay["audit_log_written"] is not False:
            raise SystemExit(f"audit log written during replay: {replay['run_index']}")

        if replay["forbidden_effect_violation_count"] != 0:
            raise SystemExit(f"forbidden effects during replay: {replay['run_index']}")

        if replay["audit_lines_after"] != before["line_count"]:
            raise SystemExit(f"audit line count drift during replay: {replay['run_index']}")

        chain = replay["chain_signature"]

        if baseline_chain is None:
            baseline_chain = chain
        elif chain != baseline_chain:
            raise SystemExit("replay chain drift detected")

    contract = payload["safety_contract"]

    if contract["replay_mode"] != "read-only-reconstruction":
        raise SystemExit("safety contract replay mode drift")

    for key in (
        "session_reexecuted",
        "adapter_reinvoked",
        "audit_log_written",
        "background_worker",
        "automatic_remediation",
    ):
        if contract[key] is not False:
            raise SystemExit(f"safety contract drift detected: {key}")

    if contract["audit_line_count_unchanged"] is not True:
        raise SystemExit("audit_line_count_unchanged drift detected")

    table_output = run(fmt="table").stdout

    if "replay-safety-regression" not in table_output:
        raise SystemExit("table output missing replay regression mode")

    if "audit_lines_after" not in table_output:
        raise SystemExit("table output missing audit line count")

    print("PASS: replay safety regression validation completed")


if __name__ == "__main__":
    main()
