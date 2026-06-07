#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "tools" / "runes_shield" / "build_proposal_draft.py"
STORE = ROOT / "tools" / "runes_shield" / "proposal_draft_store.py"
TEMP_DRAFT = ROOT / "tools" / "runes_shield" / "drafts" / "m41_3_store_smoke.json"


def run(cmd, *args, check=True):
    return subprocess.run(
        [sys.executable, str(cmd), *args],
        capture_output=True,
        text=True,
        check=check,
    )


def main():
    print("== M41.3 Proposal Draft Store Smoke ==")

    if TEMP_DRAFT.exists():
        TEMP_DRAFT.unlink()

    build = run(
        BUILD,
        "--source-summary",
        "M41.3 draft store smoke proposal.",
        "--claim",
        "Proposal draft store may enumerate external drafts.",
        "--claim",
        "Draft store remains read-only.",
        "--write-draft",
        "--output",
        str(TEMP_DRAFT.relative_to(ROOT)),
    )

    build_payload = json.loads(build.stdout)
    proposal_id = build_payload["proposal"]["proposal_id"]

    listing = run(STORE, "list", "--format", "json")
    listing_payload = json.loads(listing.stdout)

    print(json.dumps(listing_payload, indent=2, ensure_ascii=False))

    matches = [
        entry
        for entry in listing_payload["entries"]
        if entry["proposal_id"] == proposal_id
    ]

    if not matches:
        raise SystemExit("draft proposal missing from store listing")

    detail = run(
        STORE,
        "show",
        proposal_id,
        "--include-payload",
        "--format",
        "json",
    )

    detail_payload = json.loads(detail.stdout)

    print(json.dumps(detail_payload, indent=2, ensure_ascii=False))

    if detail_payload["entry"]["validation_status"] != "PASS":
        raise SystemExit("draft store detail validation failed")

    if detail_payload["write"] is not False:
        raise SystemExit("draft store must remain read-only")

    TEMP_DRAFT.unlink()

    print("PASS: proposal draft store regression completed")


if __name__ == "__main__":
    main()
