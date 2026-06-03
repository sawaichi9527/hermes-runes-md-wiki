#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "runes_shield" / "build_proposal_draft.py"


def run(*args):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        check=True,
    )


def main():
    print("== M41 Governed Proposal Draft Builder Smoke ==")

    result = run(
        "--source-summary",
        "M41 smoke validates governed proposal draft generation.",
        "--claim",
        "Hermes-agent may generate governed proposal drafts.",
        "--claim",
        "Runes Shield keeps proposal drafts outside trusted wiki write boundaries.",
    )

    payload = json.loads(result.stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if payload["status"] != "PASS":
        raise SystemExit("proposal draft build did not pass")

    if payload["write"] is not False:
        raise SystemExit("dry-run builder unexpectedly enabled write")

    proposal = payload["proposal"]

    if proposal["status"] != "pending_human_review":
        raise SystemExit("unexpected proposal review status")

    if proposal["author_role"] != "Hermes-agent":
        raise SystemExit("unexpected proposal author role")

    if proposal["reviewer_role"] != "Human":
        raise SystemExit("unexpected proposal reviewer role")

    print("PASS: governed proposal draft regression completed")


if __name__ == "__main__":
    main()
