#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "runes_shield" / "runes_shield_invocation.py"

EXPECTED_BLOCKED_CAPABILITIES = {
    "automatic_apply",
    "automatic_promotion",
    "background_worker",
    "direct_database_mutation",
    "direct_markdown_mutation",
    "trusted_wiki_write",
    "unmediated_decision_write",
}


PROPOSAL_ID = "proposal-m37.2-fixture-001"


def run(*args):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        check=True,
    )


def main():
    print("== M51 Runes Shield Invocation Smoke ==")

    discover = json.loads(run("discover", "--format", "json").stdout)

    print(json.dumps(discover, indent=2, ensure_ascii=False))

    if discover["write"] is not False:
        raise SystemExit("discover must remain read-only")

    if set(discover["blocked_capabilities"]) != EXPECTED_BLOCKED_CAPABILITIES:
        raise SystemExit("unexpected blocked capability coverage")

    if discover["tool_count"] < 5:
        raise SystemExit("expected multiple allowlisted tools")

    integrity = json.loads(
        run(
            "invoke",
            "governance.integrity",
            "--format",
            "json",
        ).stdout
    )

    if integrity["status"] != "PASS":
        raise SystemExit("integrity invocation failed")

    if integrity["write"] is not False:
        raise SystemExit("integrity invocation must remain read-only")

    if integrity["payload"]["status"] != "PASS":
        raise SystemExit("integrity payload status must be PASS")

    timeline = json.loads(
        run(
            "invoke",
            "governance.timeline",
            "--proposal-id",
            PROPOSAL_ID,
            "--format",
            "json",
        ).stdout
    )

    if timeline["status"] != "PASS":
        raise SystemExit("timeline invocation failed")

    if timeline["payload"]["event_count"] < 2:
        raise SystemExit("expected governance timeline events")

    blocked = json.loads(
        run(
            "invoke",
            "wiki.apply",
            "--format",
            "json",
        ).stdout
    )

    print(json.dumps(blocked, indent=2, ensure_ascii=False))

    if blocked["status"] != "BLOCKED":
        raise SystemExit("non-allowlisted tool must remain BLOCKED")

    if blocked["write"] is not False:
        raise SystemExit("blocked invocation must remain read-only")

    if blocked["reason_code"] != "tool_not_allowlisted":
        raise SystemExit("unexpected blocked reason code")

    print("PASS: Runes Shield governed invocation validation completed")


if __name__ == "__main__":
    main()
