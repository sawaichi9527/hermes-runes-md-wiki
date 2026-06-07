#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DECISION_CLI = ROOT / "tools" / "runes_shield" / "proposal_attunement_decision.py"
PROJECTION_CLI = ROOT / "tools" / "runes_shield" / "proposal_state_projection.py"

REJECTED_PATH = (
    ROOT
    / "tools"
    / "runes_shield"
    / "decisions"
    / "m43_1_rejected_projection_smoke.json"
)

QUARANTINED_PATH = (
    ROOT
    / "tools"
    / "runes_shield"
    / "decisions"
    / "m43_1_quarantined_projection_smoke.json"
)

VALID_PROPOSAL = "proposal-m37.2-fixture-001"
PENDING_PROPOSAL = "proposal-m37.3-negative-wrong-role"


def run(cmd, *args):
    return subprocess.run(
        [sys.executable, str(cmd), *args],
        capture_output=True,
        text=True,
        check=True,
    )


def load_projection():
    result = run(PROJECTION_CLI, "list", "--format", "json")
    payload = json.loads(result.stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    return payload


def find_state(payload, proposal_id):
    for state in payload["states"]:
        if state["proposal_id"] == proposal_id:
            return state
    raise SystemExit(f"missing projected state: {proposal_id}")


def main():
    print("== M43.1 Proposal State Projection Variant Smoke ==")

    for path in [REJECTED_PATH, QUARANTINED_PATH]:
        if path.exists():
            path.unlink()

    run(
        DECISION_CLI,
        "record",
        VALID_PROPOSAL,
        "--decision",
        "rejected",
        "--note",
        "Rejected projection smoke.",
        "--output",
        str(REJECTED_PATH.relative_to(ROOT)),
    )

    rejected_projection = load_projection()
    rejected_state = find_state(rejected_projection, VALID_PROPOSAL)

    if rejected_state["effective_state"] != "rejected":
        raise SystemExit("rejected projection mismatch")

    REJECTED_PATH.unlink()

    run(
        DECISION_CLI,
        "record",
        VALID_PROPOSAL,
        "--decision",
        "quarantined",
        "--note",
        "Quarantined projection smoke.",
        "--output",
        str(QUARANTINED_PATH.relative_to(ROOT)),
    )

    quarantined_projection = load_projection()
    quarantined_state = find_state(quarantined_projection, VALID_PROPOSAL)

    if quarantined_state["effective_state"] != "quarantined":
        raise SystemExit("quarantined projection mismatch")

    pending_state = find_state(quarantined_projection, PENDING_PROPOSAL)

    if pending_state["effective_state"] != "invalid":
        raise SystemExit("unexpected invalid projection state")

    QUARANTINED_PATH.unlink()

    print("PASS: proposal state projection variant regression completed")


if __name__ == "__main__":
    main()
