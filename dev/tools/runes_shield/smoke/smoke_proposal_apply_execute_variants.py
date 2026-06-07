#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DECISION_CLI = ROOT / "tools" / "runes_shield" / "proposal_attunement_decision.py"
EXECUTE_CLI = ROOT / "tools" / "runes_shield" / "proposal_apply_execute.py"

APPROVED_PATH = (
    ROOT
    / "tools"
    / "runes_shield"
    / "decisions"
    / "m46_1_approved_execute_smoke.json"
)

REJECTED_PATH = (
    ROOT
    / "tools"
    / "runes_shield"
    / "decisions"
    / "m46_1_rejected_execute_smoke.json"
)

VALID_PROPOSAL = "proposal-m37.2-fixture-001"
INVALID_PROPOSAL = "proposal-m37.3-negative-wrong-role"


def run(cmd, *args):
    return subprocess.run(
        [sys.executable, str(cmd), *args],
        capture_output=True,
        text=True,
        check=True,
    )


def request(proposal_id):
    result = run(
        EXECUTE_CLI,
        "request",
        proposal_id,
        "--format",
        "json",
    )

    payload = json.loads(result.stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    return payload


def main():
    print("== M46.1 Apply Execution Boundary Variant Smoke ==")

    for path in [APPROVED_PATH, REJECTED_PATH]:
        if path.exists():
            path.unlink()

    run(
        DECISION_CLI,
        "record",
        VALID_PROPOSAL,
        "--decision",
        "approved",
        "--note",
        "Approved execution boundary smoke.",
        "--output",
        str(APPROVED_PATH.relative_to(ROOT)),
    )

    approved_payload = request(VALID_PROPOSAL)

    if approved_payload["status"] != "BLOCKED":
        raise SystemExit("approved proposal must remain blocked")

    if approved_payload.get("preview_available") is not True:
        raise SystemExit("approved proposal should expose preview_available")

    APPROVED_PATH.unlink()

    run(
        DECISION_CLI,
        "record",
        VALID_PROPOSAL,
        "--decision",
        "rejected",
        "--note",
        "Rejected execution boundary smoke.",
        "--output",
        str(REJECTED_PATH.relative_to(ROOT)),
    )

    rejected_payload = request(VALID_PROPOSAL)

    if rejected_payload["status"] != "BLOCKED":
        raise SystemExit("rejected proposal must remain blocked")

    if rejected_payload.get("preview_available") is True:
        raise SystemExit("rejected proposal must not expose preview_available")

    REJECTED_PATH.unlink()

    invalid_payload = request(INVALID_PROPOSAL)

    if invalid_payload["status"] != "BLOCKED":
        raise SystemExit("invalid proposal must remain blocked")

    if invalid_payload.get("preview_available") is True:
        raise SystemExit("invalid proposal must not expose preview_available")

    if invalid_payload["effects"]["trusted_wiki_write"] is not False:
        raise SystemExit("trusted wiki write must remain disabled")

    print("PASS: apply execution boundary variant regression completed")


if __name__ == "__main__":
    main()
