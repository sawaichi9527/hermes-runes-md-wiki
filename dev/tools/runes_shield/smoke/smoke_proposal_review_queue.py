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
    print("== M39 Proposal Review Queue Smoke ==")

    listing = run("list", "--format", "json")
    listing_payload = json.loads(listing.stdout)

    print(json.dumps(listing_payload, indent=2, ensure_ascii=False))

    if listing_payload["entry_count"] < 1:
        raise SystemExit("expected at least one pending-review proposal")

    if listing_payload["write"] is not False:
        raise SystemExit("review queue must remain read-only")

    detail = run(
        "show",
        VALID_PROPOSAL_ID,
        "--format",
        "json",
    )
    detail_payload = json.loads(detail.stdout)

    print(json.dumps(detail_payload, indent=2, ensure_ascii=False))

    if detail_payload["entry"]["proposal_id"] != VALID_PROPOSAL_ID:
        raise SystemExit("unexpected review queue proposal_id")

    invalid = run(
        "show",
        INVALID_PROPOSAL_ID,
        check=False,
    )

    if invalid.returncode == 0:
        raise SystemExit(
            "invalid proposal unexpectedly appeared in review queue"
        )

    print("PASS: proposal review queue regression completed")


if __name__ == "__main__":
    main()
