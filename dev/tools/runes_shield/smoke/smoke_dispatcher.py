#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DISPATCHER = ROOT / "dispatch_invocation.py"

EXPECTED = {
    "MATCH": "observe",
    "CONFIRM": "confirm",
    "CONFIRM_MATCH": "observe",
    "NO_MATCH": "none",
}

EXPECTED_STATUS = {
    "MATCH": "PASS",
    "CONFIRM": "CONFIRM_REQUIRED",
    "CONFIRM_MATCH": "PASS",
    "NO_MATCH": "BYPASS",
}


def run_state(state):
    result = subprocess.run(
        [sys.executable, str(DISPATCHER), state],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    return json.loads(result.stdout)


def main():
    print("== M35.3 Dispatcher Smoke ==")

    for state, expected_handler in EXPECTED.items():
        data = run_state(state)

        print(json.dumps(data, indent=2, ensure_ascii=False))

        if data["handler"] != expected_handler:
            raise SystemExit(
                f"unexpected handler for {state}: {data['handler']}"
            )

        if data["status"] != EXPECTED_STATUS[state]:
            raise SystemExit(
                f"unexpected status for {state}: {data['status']}"
            )

        if data["write"] is not False:
            raise SystemExit(
                f"write flag must remain false: {state}"
            )

    print("PASS: dispatcher validation completed")


if __name__ == "__main__":
    main()
