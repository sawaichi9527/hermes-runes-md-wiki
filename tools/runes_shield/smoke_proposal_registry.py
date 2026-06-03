#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "runes_shield" / "proposal_registry.py"


def run(*args):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        check=True,
    )


def main():
    print("== M38.1 Proposal Registry Smoke ==")

    valid = run("list", "--valid-only", "--format", "json")
    valid_payload = json.loads(valid.stdout)

    invalid = run("list", "--invalid-only", "--format", "json")
    invalid_payload = json.loads(invalid.stdout)

    print(json.dumps(valid_payload, indent=2, ensure_ascii=False))
    print(json.dumps(invalid_payload, indent=2, ensure_ascii=False))

    if valid_payload["entry_count"] < 1:
        raise SystemExit("expected at least one valid proposal fixture")

    if invalid_payload["entry_count"] < 3:
        raise SystemExit("expected at least three invalid proposal fixtures")

    if valid_payload["write"] is not False:
        raise SystemExit("registry must remain read-only")

    if invalid_payload["write"] is not False:
        raise SystemExit("registry must remain read-only")

    print("PASS: proposal registry regression completed")


if __name__ == "__main__":
    main()
