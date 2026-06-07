#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = {
    "registry": ROOT / "smoke_registry.py",
    "discovery": ROOT / "smoke_discovery.py",
    "route_resolver": ROOT / "smoke_route_resolver.py",
    "dispatcher": ROOT / "smoke_dispatcher.py",
}


def run_script(name, path):
    result = subprocess.run(
        [sys.executable, str(path)],
        capture_output=True,
        text=True,
    )

    return {
        "name": name,
        "path": str(path),
        "returncode": result.returncode,
        "stdout_tail": result.stdout.strip().splitlines()[-8:],
        "stderr_tail": result.stderr.strip().splitlines()[-8:],
        "status": "PASS" if result.returncode == 0 else "FAIL",
    }


def main():
    print("== M35.4 Runtime Boundary Regression Smoke ==")

    results = []

    for name, path in SCRIPTS.items():
        result = run_script(name, path)
        results.append(result)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    failed = [item for item in results if item["status"] != "PASS"]

    summary = {
        "suite": "M35.4 Runtime Boundary Regression Smoke",
        "status": "PASS" if not failed else "FAIL",
        "total": len(results),
        "failed": len(failed),
        "checked": [item["name"] for item in results],
        "governance_boundary": {
            "write_default": False,
            "autonomous_apply": False,
            "hidden_escalation": False,
            "trusted_memory_mutation": False,
        },
    }

    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if failed:
        sys.exit(1)

    print("PASS: runtime boundary regression completed")


if __name__ == "__main__":
    main()
