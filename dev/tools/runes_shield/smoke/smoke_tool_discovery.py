#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "runes_shield" / "runes_shield_tool_index.py"

SAFE_TOOL = "proposal_review_queue.show_payload"
BLOCKED_TOOL = "proposal.apply"


def run(*args, check=True):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        check=check,
    )


def main():
    print("== M40.1 Tool Discovery Smoke ==")

    listing = run("list", "--format", "json")
    listing_payload = json.loads(listing.stdout)

    print(json.dumps(listing_payload, indent=2, ensure_ascii=False))

    if listing_payload["tool_count"] < 1:
        raise SystemExit("expected at least one safe tool")

    detail = run("show", SAFE_TOOL, "--format", "json")
    detail_payload = json.loads(detail.stdout)

    print(json.dumps(detail_payload, indent=2, ensure_ascii=False))

    if detail_payload["tool"]["write"] is not False:
        raise SystemExit("unsafe write tool exposed")

    blocked = run("blocked", "--format", "json")
    blocked_payload = json.loads(blocked.stdout)

    print(json.dumps(blocked_payload, indent=2, ensure_ascii=False))

    if BLOCKED_TOOL not in blocked_payload["blocked_tool_names"]:
        raise SystemExit("blocked tool missing from discovery output")

    missing = run("show", BLOCKED_TOOL, check=False)

    if missing.returncode == 0:
        raise SystemExit("blocked tool unexpectedly exposed")

    print("PASS: Runes Shield tool discovery regression completed")


if __name__ == "__main__":
    main()
