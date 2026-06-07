#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DECISION_CLI = ROOT / "tools" / "runes_shield" / "proposal_attunement_decision.py"
EXECUTE_CLI = ROOT / "tools" / "runes_shield" / "proposal_apply_execute.py"
DECISION_PATH = (
    ROOT
    / "tools"
    / "runes_shield"
    / "decisions"
    / "m46_apply_execute_smoke.json"
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
    print("== M46 Apply Execution Boundary Smoke ==")

    if DECISION_PATH.exists():
        DECISION_PATH.unlink()

    run(
        DECISION_CLI,
        "record",
        PROPOSAL_ID,
        "--decision",
        "approved",
        "--note",
        "Apply execution boundary smoke.",
        "--output",
        str(DECISION_PATH.relative_to(ROOT)),
    )

    result = run(
        EXECUTE_CLI,
        "request",
        PROPOSAL_ID,
        "--format",
        "json",
    )

    payload = json.loads(result.stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if payload["status"] != "BLOCKED":
        raise SystemExit("apply execution must remain blocked")

    if payload["effects"]["trusted_wiki_write"] is not False:
        raise SystemExit("trusted wiki write must remain disabled")

    if payload["effects"]["markdown_mutation"] is not False:
        raise SystemExit("markdown mutation must remain disabled")

    DECISION_PATH.unlink()

    print("PASS: apply execution boundary regression completed")


if __name__ == "__main__":
    main()
