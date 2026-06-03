#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DECISION_CLI = ROOT / "tools" / "runes_shield" / "proposal_attunement_decision.py"
PLAN_CLI = ROOT / "tools" / "runes_shield" / "proposal_apply_plan.py"
DECISION_PATH = (
    ROOT
    / "tools"
    / "runes_shield"
    / "decisions"
    / "m44_apply_plan_smoke.json"
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
    print("== M44 Proposal Apply Planning Smoke ==")

    if DECISION_PATH.exists():
        DECISION_PATH.unlink()

    run(
        DECISION_CLI,
        "record",
        PROPOSAL_ID,
        "--decision",
        "approved",
        "--note",
        "Apply planning smoke decision.",
        "--output",
        str(DECISION_PATH.relative_to(ROOT)),
    )

    listing = run(PLAN_CLI, "list", "--format", "json")
    listing_payload = json.loads(listing.stdout)

    print(json.dumps(listing_payload, indent=2, ensure_ascii=False))

    if listing_payload["entry_count"] < 1:
        raise SystemExit("expected at least one apply plan")

    matching = [
        plan
        for plan in listing_payload["plans"]
        if plan["proposal_id"] == PROPOSAL_ID
    ]

    if not matching:
        raise SystemExit("missing proposal apply plan")

    plan = matching[0]

    if plan["effective_state"] != "approved_pending_apply":
        raise SystemExit("unexpected apply plan state")

    detail = run(
        PLAN_CLI,
        "show",
        PROPOSAL_ID,
        "--format",
        "json",
    )

    detail_payload = json.loads(detail.stdout)

    print(json.dumps(detail_payload, indent=2, ensure_ascii=False))

    if detail_payload["plan"]["effects"]["trusted_wiki_write"] is not False:
        raise SystemExit("apply planning layer must remain read-only")

    DECISION_PATH.unlink()

    print("PASS: proposal apply planning regression completed")


if __name__ == "__main__":
    main()
