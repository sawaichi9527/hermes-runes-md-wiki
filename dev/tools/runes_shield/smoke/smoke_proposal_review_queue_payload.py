#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "runes_shield" / "proposal_review_queue.py"

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
    print("== M39.1 Proposal Review Queue Payload Smoke ==")

    result = run(
        "show",
        VALID_PROPOSAL_ID,
        "--include-payload",
        "--format",
        "json",
    )

    payload = json.loads(result.stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if payload["write"] is not False:
        raise SystemExit("review queue payload view must remain read-only")

    if payload["entry"]["proposal_id"] != VALID_PROPOSAL_ID:
        raise SystemExit("unexpected queue proposal_id")

    if "payload" not in payload:
        raise SystemExit("queue payload output missing")

    invalid = run(
        "show",
        INVALID_PROPOSAL_ID,
        "--include-payload",
        check=False,
    )

    if invalid.returncode == 0:
        raise SystemExit(
            "invalid proposal unexpectedly exposed through queue payload view"
        )

    print("PASS: proposal review queue payload regression completed")


if __name__ == "__main__":
    main()
