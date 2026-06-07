#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "runes_shield" / "hermes_agent_adapter.py"

EXPECTED_EFFECT_KEYS = {
    "trusted_wiki_write",
    "markdown_mutation",
    "index_update",
    "automatic_apply",
    "automatic_promotion",
    "database_mutation",
    "observation_ingested_to_rag",
}

PROPOSAL_ID = "proposal-m37.2-fixture-001"


def run(request):
    return subprocess.run(
        [
            sys.executable,
            str(CLI),
            "--raw-json",
            json.dumps(request),
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )


def assert_effects_disabled(payload):
    if set(payload["effects"]) != EXPECTED_EFFECT_KEYS:
        raise SystemExit("unexpected adapter effect coverage")

    if any(value is not False for value in payload["effects"].values()):
        raise SystemExit("adapter effects must remain disabled")


def main():
    print("== M52 Hermes Agent Adapter Smoke ==")

    discover = json.loads(
        run(
            {
                "agent": "hermes-agent",
                "intent": "discover_tools",
            }
        ).stdout
    )

    print(json.dumps(discover, indent=2, ensure_ascii=False))

    if discover["status"] != "PASS":
        raise SystemExit("discover_tools request failed")

    if discover["write"] is not False:
        raise SystemExit("adapter must remain read-only")

    assert_effects_disabled(discover)

    if discover["payload"]["tool_count"] < 5:
        raise SystemExit("expected allowlisted tools")

    integrity = json.loads(
        run(
            {
                "agent": "hermes-agent",
                "intent": "check_integrity",
            }
        ).stdout
    )

    if integrity["status"] != "PASS":
        raise SystemExit("integrity adapter request failed")

    if integrity["payload"]["payload"]["status"] != "PASS":
        raise SystemExit("integrity payload status must be PASS")

    timeline = json.loads(
        run(
            {
                "agent": "hermes-agent",
                "intent": "show_timeline",
                "proposal_id": PROPOSAL_ID,
            }
        ).stdout
    )

    if timeline["status"] != "PASS":
        raise SystemExit("timeline adapter request failed")

    if timeline["payload"]["payload"]["event_count"] < 2:
        raise SystemExit("expected governance timeline events")

    blocked = json.loads(
        run(
            {
                "agent": "hermes-agent",
                "intent": "write_wiki",
            }
        ).stdout
    )

    print(json.dumps(blocked, indent=2, ensure_ascii=False))

    if blocked["status"] != "BLOCKED":
        raise SystemExit("blocked intent must remain BLOCKED")

    if blocked["reason_code"] != "intent_blocked":
        raise SystemExit("unexpected blocked intent reason")

    invalid = json.loads(
        run(
            {
                "agent": "hermes-agent",
            }
        ).stdout
    )

    if invalid["status"] != "BLOCKED":
        raise SystemExit("invalid request must remain blocked")

    if invalid["reason_code"] != "missing_intent":
        raise SystemExit("unexpected validation reason")

    assert_effects_disabled(invalid)

    print("PASS: Hermes-agent adapter validation completed")


if __name__ == "__main__":
    main()
