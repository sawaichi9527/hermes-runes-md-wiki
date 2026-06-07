#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "runes_shield" / "proposal_registry.py"

VALID_PROPOSAL_ID = "proposal-m37.2-fixture-001"
INVALID_PROPOSAL_ID = "proposal-m37.3-negative-wrong-role"


def run(*args, check=True):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        check=check,
    )


def main():
    print("== M38.2 Proposal Registry Show Smoke ==")

    valid = run(
        "show",
        VALID_PROPOSAL_ID,
        "--format",
        "json",
    )
    valid_payload = json.loads(valid.stdout)

    invalid = run(
        "show",
        INVALID_PROPOSAL_ID,
        "--format",
        "json",
    )
    invalid_payload = json.loads(invalid.stdout)

    print(json.dumps(valid_payload, indent=2, ensure_ascii=False))
    print(json.dumps(invalid_payload, indent=2, ensure_ascii=False))

    if valid_payload["entry"]["validation_status"] != "PASS":
        raise SystemExit("valid proposal lookup failed")

    if invalid_payload["entry"]["validation_status"] != "FAIL":
        raise SystemExit("invalid proposal lookup failed")

    missing = run(
        "show",
        "proposal-does-not-exist",
        check=False,
    )

    if missing.returncode == 0:
        raise SystemExit("missing proposal lookup unexpectedly passed")

    print("PASS: proposal registry show regression completed")


if __name__ == "__main__":
    main()
