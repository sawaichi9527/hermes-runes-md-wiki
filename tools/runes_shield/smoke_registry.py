#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOADER = ROOT / "load_registry.py"


def main():
    result = subprocess.run(
        [sys.executable, str(LOADER)],
        capture_output=True,
        text=True,
    )

    print("== M35 Registry Smoke ==")
    print(result.stdout.strip())

    if result.returncode != 0:
        print(result.stderr.strip())
        sys.exit(result.returncode)

    print("PASS: runtime registry validation completed")


if __name__ == "__main__":
    main()
