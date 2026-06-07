#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "runes_shield" / "runes_shield_session.py"

EXPECTED_EFFECT_KEYS = {
    "trusted_wiki_write",
    "markdown_mutation",
    "index_update",
    "automatic_apply",
    "automatic_promotion",
    "database_mutation",
    "observation_ingested_to_rag",
    "session_persisted",
    "audit_log_written",
}


def run(payload, fmt="json"):
    return subprocess.run(
        [
            sys.executable,
            str(CLI),
            "--raw-json",
            json.dumps(payload),
            "--format",
            fmt,
        ],
        capture_output=True,
        text=True,
        check=True,
    )


def assert_effects_disabled(payload):
    if set(payload["effects"]) != EXPECTED_EFFECT_KEYS:
        raise SystemExit("unexpected runtime session effect coverage")

    if any(value is not False for value in payload["effects"].values()):
        raise SystemExit("runtime session effects must remain disabled")


def main():
    print("== M53 Runtime Invocation Session Smoke ==")

    valid = json.loads(
        run(
            {
                "agent": "hermes-agent",
                "conversation_id": "conv-test-001",
                "request": {
                    "intent": "check_integrity",
                },
            }
        ).stdout
    )

    print(json.dumps(valid, indent=2, ensure_ascii=False))

    if valid["status"] != "PASS":
        raise SystemExit("runtime session request failed")

    if valid["write"] is not False:
        raise SystemExit("runtime session must remain read-only")

    assert_effects_disabled(valid)

    if len(valid["audit_chain"]) < 2:
        raise SystemExit("expected runtime + adapter audit chain")

    adapter = valid["adapter_response"]

    if adapter["status"] != "PASS":
        raise SystemExit("adapter response must be PASS")

    if adapter["payload"]["payload"]["status"] != "PASS":
        raise SystemExit("nested integrity payload must be PASS")

    blocked = json.loads(
        run(
            {
                "agent": "hermes-agent",
                "request": {
                    "intent": "write_wiki",
                },
            }
        ).stdout
    )

    print(json.dumps(blocked, indent=2, ensure_ascii=False))

    if blocked["status"] != "BLOCKED":
        raise SystemExit("blocked runtime session intent must remain BLOCKED")

    if blocked["adapter_response"]["reason_code"] != "intent_blocked":
        raise SystemExit("unexpected blocked adapter reason")

    invalid = json.loads(run({}).stdout)

    if invalid["status"] != "BLOCKED":
        raise SystemExit("invalid runtime session request must remain BLOCKED")

    if invalid["reason_code"] != "missing_request":
        raise SystemExit("unexpected runtime validation reason")

    jsonl_output = run(
        {
            "agent": "hermes-agent",
            "request": {
                "intent": "discover_tools",
            },
        },
        fmt="jsonl",
    ).stdout

    lines = [line for line in jsonl_output.splitlines() if line.strip()]

    if len(lines) < 2:
        raise SystemExit("expected runtime invocation audit events")

    for line in lines:
        event = json.loads(line)

        if event["event_type"] != "runtime_invocation_audit":
            raise SystemExit("unexpected runtime audit event type")

        if event["write"] is not False:
            raise SystemExit("runtime audit events must remain read-only")

    print("PASS: runtime invocation session validation completed")


if __name__ == "__main__":
    main()
