#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESOLVER = ROOT / "resolve_route.py"

EXPECTED = {
    "MATCH": "observe",
    "CONFIRM": "confirm",
    "CONFIRM_MATCH": "observe",
    "NO_MATCH": "none",
}


def run_state(state):
    result = subprocess.run(
        [sys.executable, str(RESOLVER), state],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    return json.loads(result.stdout)


def main():
    print("== M35.2 Route Resolver Smoke ==")

    for state, expected_tool in EXPECTED.items():
        data = run_state(state)

        print(json.dumps(data, indent=2, ensure_ascii=False))

        if data["tool"] != expected_tool:
            raise SystemExit(
                f"unexpected tool for {state}: {data['tool']}"
            )

        if data["write"] is not False:
            raise SystemExit(
                f"write flag must remain false: {state}"
            )

    unknown = run_state("UNKNOWN_STATE")

    print(json.dumps(unknown, indent=2, ensure_ascii=False))

    if unknown["status"] != "BLOCKED":
        raise SystemExit("unknown states must remain blocked")

    print("PASS: route resolver validation completed")


if __name__ == "__main__":
    main()
