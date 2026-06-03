#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DECISION_CLI = ROOT / "tools" / "runes_shield" / "proposal_attunement_decision.py"
PLAN_CLI = ROOT / "tools" / "runes_shield" / "proposal_apply_plan.py"

APPROVED_PATH = (
    ROOT
    / "tools"
    / "runes_shield"
    / "decisions"
    / "m44_1_approved_plan_smoke.json"
)

REJECTED_PATH = (
    ROOT
    / "tools"
    / "runes_shield"
    / "decisions"
    / "m44_1_rejected_plan_smoke.json"
)

QUARANTINED_PATH = (
    ROOT
    / "tools"
    / "runes_shield"
    / "decisions"
    / "m44_1_quarantined_plan_smoke.json"
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


def load_plans():
    result = run(PLAN_CLI, "list", "--format", "json")
    payload = json.loads(result.stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    return payload


def find_plan(payload, proposal_id):
    for plan in payload["plans"]:
        if plan["proposal_id"] == proposal_id:
            return plan
    return None


def main():
    print("== M44.1 Proposal Apply Planning Variant Smoke ==")

    for path in [APPROVED_PATH, REJECTED_PATH, QUARANTINED_PATH]:
        if path.exists():
            path.unlink()

    run(
        DECISION_CLI,
        "record",
        VALID_PROPOSAL,
        "--decision",
        "approved",
        "--note",
        "Approved apply plan smoke.",
        "--output",
        str(APPROVED_PATH.relative_to(ROOT)),
    )

    approved_payload = load_plans()
    approved_plan = find_plan(approved_payload, VALID_PROPOSAL)

    if approved_plan is None:
        raise SystemExit("approved proposal should generate apply plan")

    if approved_plan["effective_state"] != "approved_pending_apply":
        raise SystemExit("approved proposal projection mismatch")

    APPROVED_PATH.unlink()

    run(
        DECISION_CLI,
        "record",
        VALID_PROPOSAL,
        "--decision",
        "rejected",
        "--note",
        "Rejected apply plan smoke.",
        "--output",
        str(REJECTED_PATH.relative_to(ROOT)),
    )

    rejected_payload = load_plans()

    if find_plan(rejected_payload, VALID_PROPOSAL) is not None:
        raise SystemExit("rejected proposal must not generate apply plan")

    REJECTED_PATH.unlink()

    run(
        DECISION_CLI,
        "record",
        VALID_PROPOSAL,
        "--decision",
        "quarantined",
        "--note",
        "Quarantined apply plan smoke.",
        "--output",
        str(QUARANTINED_PATH.relative_to(ROOT)),
    )

    quarantined_payload = load_plans()

    if find_plan(quarantined_payload, VALID_PROPOSAL) is not None:
        raise SystemExit("quarantined proposal must not generate apply plan")

    if find_plan(quarantined_payload, INVALID_PROPOSAL) is not None:
        raise SystemExit("invalid proposal must not generate apply plan")

    QUARANTINED_PATH.unlink()

    print("PASS: proposal apply planning variant regression completed")


if __name__ == "__main__":
    main()
