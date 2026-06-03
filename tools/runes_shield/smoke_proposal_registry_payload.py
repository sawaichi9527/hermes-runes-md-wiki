#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "runes_shield" / "proposal_registry.py"

PROPOSAL_ID = "proposal-m37.2-fixture-001"


def run(*args):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        check=True,
    )


def main():
    print("== M38.3 Proposal Registry Payload Smoke ==")

    result = run(
        "show",
        PROPOSAL_ID,
        "--include-payload",
        "--format",
        "json",
    )

    payload = json.loads(result.stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if payload["write"] is not False:
        raise SystemExit("registry payload view must remain read-only")

    if "payload" not in payload:
        raise SystemExit("payload output missing")

    proposal_payload = payload["payload"]

    if proposal_payload["proposal_id"] != PROPOSAL_ID:
        raise SystemExit("payload proposal_id mismatch")

    if proposal_payload["status"] != "pending_human_review":
        raise SystemExit("unexpected payload status")

    print("PASS: proposal registry payload regression completed")


if __name__ == "__main__":
    main()
