#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DISCOVERY = ROOT / "discover_registry.py"


def main():
    result = subprocess.run(
        [sys.executable, str(DISCOVERY)],
        capture_output=True,
        text=True,
    )

    print("== M35.1 Discovery Smoke ==")

    if result.returncode != 0:
        print(result.stderr.strip())
        sys.exit(result.returncode)

    print(result.stdout.strip())

    data = json.loads(result.stdout)

    if data["write_default"] is not False:
        raise SystemExit("write_default must remain false")

    for tool in data["tools"]:
        if tool["write"] is not False:
            raise SystemExit(
                f"tool write flag must remain false: {tool['name']}"
            )

    print("PASS: discovery output validation completed")


if __name__ == "__main__":
    main()
