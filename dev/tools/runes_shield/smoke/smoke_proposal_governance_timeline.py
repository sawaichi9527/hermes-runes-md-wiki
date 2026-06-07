#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DECISION_CLI = ROOT / "tools" / "runes_shield" / "proposal_attunement_decision.py"
TIMELINE_CLI = ROOT / "tools" / "runes_shield" / "proposal_governance_timeline.py"
DECISION_PATH = (
    ROOT
    / "tools"
    / "runes_shield"
    / "decisions"
    / "m47_timeline_smoke.json"
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
    print("== M47 Governance Timeline Smoke ==")

    if DECISION_PATH.exists():
        DECISION_PATH.unlink()

    run(
        DECISION_CLI,
        "record",
        PROPOSAL_ID,
        "--decision",
        "approved",
        "--note",
        "Governance timeline smoke.",
        "--output",
        str(DECISION_PATH.relative_to(ROOT)),
    )

    result = run(
        TIMELINE_CLI,
        PROPOSAL_ID,
        "--format",
        "json",
    )

    payload = json.loads(result.stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    events = [event["event"] for event in payload["events"]]

    required_events = [
        "proposal_queued",
        "human_attunement_decision",
        "state_projected",
        "apply_preview_generated",
        "apply_execution_requested",
    ]

    for required in required_events:
        if required not in events:
            raise SystemExit(f"missing governance event: {required}")

    if payload["write"] is not False:
        raise SystemExit("timeline layer must remain read-only")

    DECISION_PATH.unlink()

    print("PASS: governance timeline regression completed")


if __name__ == "__main__":
    main()
