#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DECISION_CLI = ROOT / "tools" / "runes_shield" / "proposal_attunement_decision.py"
PREVIEW_CLI = ROOT / "tools" / "runes_shield" / "proposal_apply_preview.py"
DECISION_PATH = (
    ROOT
    / "tools"
    / "runes_shield"
    / "decisions"
    / "m45_apply_preview_smoke.json"
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
    print("== M45 Proposal Apply Preview Smoke ==")

    if DECISION_PATH.exists():
        DECISION_PATH.unlink()

    run(
        DECISION_CLI,
        "record",
        PROPOSAL_ID,
        "--decision",
        "approved",
        "--note",
        "Apply preview smoke decision.",
        "--output",
        str(DECISION_PATH.relative_to(ROOT)),
    )

    listing = run(PREVIEW_CLI, "list", "--format", "json")
    listing_payload = json.loads(listing.stdout)

    print(json.dumps(listing_payload, indent=2, ensure_ascii=False))

    if listing_payload["entry_count"] < 1:
        raise SystemExit("expected at least one apply preview")

    detail = run(
        PREVIEW_CLI,
        "show",
        PROPOSAL_ID,
        "--format",
        "json",
    )

    detail_payload = json.loads(detail.stdout)

    print(json.dumps(detail_payload, indent=2, ensure_ascii=False))

    preview = detail_payload["preview"]

    if "# Proposal Apply Candidate:" not in preview["markdown_preview"]:
        raise SystemExit("missing markdown preview heading")

    if preview["effects"]["trusted_wiki_write"] is not False:
        raise SystemExit("apply preview layer must remain read-only")

    DECISION_PATH.unlink()

    print("PASS: proposal apply preview regression completed")


if __name__ == "__main__":
    main()
