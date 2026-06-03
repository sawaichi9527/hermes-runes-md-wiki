#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DECISION_CLI = ROOT / "tools" / "runes_shield" / "proposal_attunement_decision.py"
HISTORY_CLI = ROOT / "tools" / "runes_shield" / "proposal_governance_history.py"
DECISION_PATH = (
    ROOT
    / "tools"
    / "runes_shield"
    / "decisions"
    / "m48_history_smoke.json"
)


def run(cmd, *args):
    return subprocess.run(
        [sys.executable, str(cmd), *args],
        capture_output=True,
        text=True,
        check=True,
    )


def main():
    print("== M48 Governance History Smoke ==")

    if DECISION_PATH.exists():
        DECISION_PATH.unlink()

    run(
        DECISION_CLI,
        "record",
        "proposal-m37.2-fixture-001",
        "--decision",
        "approved",
        "--note",
        "Governance history smoke.",
        "--output",
        str(DECISION_PATH.relative_to(ROOT)),
    )

    result = run(HISTORY_CLI, "--format", "json")

    payload = json.loads(result.stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if payload["proposal_count"] < 1:
        raise SystemExit("expected governance history entries")

    histories = payload["histories"]

    valid_entry = next(
        (
            item
            for item in histories
            if item["proposal_id"] == "proposal-m37.2-fixture-001"
        ),
        None,
    )

    if valid_entry is None:
        raise SystemExit("missing valid proposal history")

    if valid_entry["latest_event"] != "apply_execution_requested":
        raise SystemExit("unexpected latest governance event")

    if valid_entry["event_count"] < 5:
        raise SystemExit("governance timeline unexpectedly incomplete")

    if payload["write"] is not False:
        raise SystemExit("governance history must remain read-only")

    DECISION_PATH.unlink()

    print("PASS: governance history regression completed")


if __name__ == "__main__":
    main()
