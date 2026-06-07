#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DECISION_CLI = ROOT / "tools" / "runes_shield" / "proposal_attunement_decision.py"
PROJECTION_CLI = ROOT / "tools" / "runes_shield" / "proposal_state_projection.py"
DECISION_PATH = (
    ROOT
    / "tools"
    / "runes_shield"
    / "decisions"
    / "m43_projection_smoke.json"
)
PROPOSAL_ID = "proposal-m37.2-fixture-001"


def run(cmd, *args):
    return subprocess.run(
        [sys.executable, str(cmd), *args],
        capture_output=True,
        text=True,
        check=True,
    )


def main():
    print("== M43 Proposal State Projection Smoke ==")

    if DECISION_PATH.exists():
        DECISION_PATH.unlink()

    run(
        DECISION_CLI,
        "record",
        PROPOSAL_ID,
        "--decision",
        "approved",
        "--note",
        "Projection smoke decision.",
        "--output",
        str(DECISION_PATH.relative_to(ROOT)),
    )

    listing = run(PROJECTION_CLI, "list", "--format", "json")
    listing_payload = json.loads(listing.stdout)

    print(json.dumps(listing_payload, indent=2, ensure_ascii=False))

    matching = [
        state
        for state in listing_payload["states"]
        if state["proposal_id"] == PROPOSAL_ID
    ]

    if not matching:
        raise SystemExit("proposal state missing from projection")

    state = matching[0]

    if state["effective_state"] != "approved_pending_apply":
        raise SystemExit("unexpected effective state projection")

    detail = run(
        PROJECTION_CLI,
        "show",
        PROPOSAL_ID,
        "--format",
        "json",
    )

    detail_payload = json.loads(detail.stdout)

    print(json.dumps(detail_payload, indent=2, ensure_ascii=False))

    if detail_payload["state"]["write"] is not False:
        raise SystemExit("projection layer must remain read-only")

    DECISION_PATH.unlink()

    print("PASS: proposal state projection regression completed")


if __name__ == "__main__":
    main()
