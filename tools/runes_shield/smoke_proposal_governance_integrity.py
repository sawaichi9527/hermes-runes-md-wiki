#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DECISION_CLI = ROOT / "tools" / "runes_shield" / "proposal_attunement_decision.py"
INTEGRITY_CLI = ROOT / "tools" / "runes_shield" / "proposal_governance_integrity.py"
DECISION_PATH = (
    ROOT
    / "tools"
    / "runes_shield"
    / "decisions"
    / "m49_integrity_smoke.json"
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
    print("== M49 Governance Integrity Smoke ==")

    if DECISION_PATH.exists():
        DECISION_PATH.unlink()

    run(
        DECISION_CLI,
        "record",
        PROPOSAL_ID,
        "--decision",
        "approved",
        "--note",
        "Governance integrity smoke.",
        "--output",
        str(DECISION_PATH.relative_to(ROOT)),
    )

    result = run(INTEGRITY_CLI, "--format", "json")

    payload = json.loads(result.stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if payload["status"] != "PASS":
        raise SystemExit("governance integrity validation failed")

    if payload["issue_count"] != 0:
        raise SystemExit("expected zero governance integrity issues")

    if payload["write"] is not False:
        raise SystemExit("governance integrity validator must remain read-only")

    if payload["proposal_count"] < 1:
        raise SystemExit("expected at least one proposal")

    required_layers = {
        "manifest",
        "review_queue",
        "state_projection",
        "apply_preview",
        "apply_execution_boundary",
        "governance_timeline",
        "governance_history",
    }

    if set(payload["checked_layers"]) != required_layers:
        raise SystemExit("unexpected governance integrity layer coverage")

    DECISION_PATH.unlink()

    print("PASS: governance integrity validation completed")


if __name__ == "__main__":
    main()
