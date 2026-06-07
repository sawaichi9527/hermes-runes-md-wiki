#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "runes_shield" / "validate_invocation_contract.py"


def run(fmt="json"):
    return subprocess.run(
        [
            sys.executable,
            str(CLI),
            "--timeout",
            "15",
            "--format",
            fmt,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )


def main():
    print("== M56.5 Invocation Contract Smoke ==")

    payload = json.loads(run().stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if payload["contract_version"] != "m56.5-invocation-contract-v1":
        raise SystemExit("unexpected invocation contract version")

    if payload["status"] != "PASS":
        raise SystemExit("invocation contract validation failed")

    if payload["mode"] != "invocation-contract-freeze":
        raise SystemExit("unexpected invocation contract mode")

    if payload["scale"] != "personal-local":
        raise SystemExit("invocation contract scale drift detected")

    if payload["write"] is not False:
        raise SystemExit("invocation contract validator must remain read-only")

    if payload["issue_count"] != 0:
        raise SystemExit("invocation contract validator must report zero issues")

    discovery = payload["discovery"]

    if discovery["shield_version"] != "m51-runes-shield-invocation-v1":
        raise SystemExit("shield version drift detected")

    if discovery["tool_count"] != 8:
        raise SystemExit("tool count drift detected")

    if discovery["write"] is not False:
        raise SystemExit("discovery write drift detected")

    safe_invocations = payload["safe_invocations"]

    if len(safe_invocations) != 8:
        raise SystemExit("unexpected safe invocation count")

    for item in safe_invocations:
        if item["status"] != "PASS":
            raise SystemExit(f"safe invocation failed: {item['tool']}")
        if item["write"] is not False:
            raise SystemExit(f"safe invocation write drift: {item['tool']}")

    blocked_invocations = payload["blocked_invocations"]

    if len(blocked_invocations) != 3:
        raise SystemExit("unexpected blocked invocation count")

    for item in blocked_invocations:
        if item["status"] != "BLOCKED":
            raise SystemExit(f"blocked invocation drift: {item['tool']}")
        if item["reason_code"] != "tool_not_allowlisted":
            raise SystemExit(f"blocked invocation reason drift: {item['tool']}")
        if item["write"] is not False:
            raise SystemExit(f"blocked invocation write drift: {item['tool']}")

    adapter_safe = payload["adapter_safe_intents"]

    if len(adapter_safe) != 9:
        raise SystemExit("unexpected adapter safe intent count")

    for item in adapter_safe:
        if item["status"] != "PASS":
            raise SystemExit(f"adapter safe intent failed: {item['intent']}")
        if item["write"] is not False:
            raise SystemExit(f"adapter safe intent write drift: {item['intent']}")

    adapter_blocked = payload["adapter_blocked_intents"]

    if len(adapter_blocked) != 7:
        raise SystemExit("unexpected adapter blocked intent count")

    for item in adapter_blocked:
        if item["status"] != "BLOCKED":
            raise SystemExit(f"adapter blocked intent drift: {item['intent']}")
        if item["reason_code"] != "intent_blocked":
            raise SystemExit(f"adapter blocked reason drift: {item['intent']}")
        if item["write"] is not False:
            raise SystemExit(f"adapter blocked write drift: {item['intent']}")

    argument_validation = payload["argument_validation"]

    invocation_missing = argument_validation["invocation_missing_proposal_id"]
    if invocation_missing["status"] != "BLOCKED":
        raise SystemExit("invocation missing proposal_id drift")
    if invocation_missing["reason_code"] != "missing_required_argument":
        raise SystemExit("invocation missing proposal_id reason drift")

    adapter_missing = argument_validation["adapter_missing_proposal_id"]
    if adapter_missing["status"] != "BLOCKED":
        raise SystemExit("adapter missing proposal_id drift")
    if adapter_missing["reason_code"] != "missing_proposal_id":
        raise SystemExit("adapter missing proposal_id reason drift")

    table_output = run(fmt="table").stdout

    if "invocation-contract-freeze" not in table_output:
        raise SystemExit("table output missing invocation contract mode")

    if "tool_count: 8" not in table_output:
        raise SystemExit("table output missing tool count")

    print("PASS: invocation contract validation completed")


if __name__ == "__main__":
    main()
