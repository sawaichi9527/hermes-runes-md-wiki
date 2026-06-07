#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "runes_shield" / "proposal_attunement_decision.py"
DECISION_PATH = (
    ROOT
    / "tools"
    / "runes_shield"
    / "decisions"
    / "m42_1_decision_store_smoke.json"
)
PROPOSAL_ID = "proposal-m37.2-fixture-001"


def run(*args):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        check=True,
    )


def main():
    print("== M42.1 Attunement Decision Store Smoke ==")

    if DECISION_PATH.exists():
        DECISION_PATH.unlink()

    record = run(
        "record",
        PROPOSAL_ID,
        "--decision",
        "approved",
        "--note",
        "Decision store smoke validation.",
        "--output",
        str(DECISION_PATH.relative_to(ROOT)),
    )

    record_payload = json.loads(record.stdout)

    print(json.dumps(record_payload, indent=2, ensure_ascii=False))

    if not DECISION_PATH.exists():
        raise SystemExit("expected decision artifact in decision store")

    listing = run("list", "--format", "json")
    listing_payload = json.loads(listing.stdout)

    print(json.dumps(listing_payload, indent=2, ensure_ascii=False))

    if listing_payload["entry_count"] < 1:
        raise SystemExit("expected at least one decision entry")

    detail = run(
        "show",
        PROPOSAL_ID,
        "--format",
        "json",
    )

    detail_payload = json.loads(detail.stdout)

    print(json.dumps(detail_payload, indent=2, ensure_ascii=False))

    if detail_payload["entry_count"] < 1:
        raise SystemExit("decision show returned no entries")

    entry = detail_payload["entries"][0]

    if entry["payload"]["effects"]["trusted_wiki_write"] is not False:
        raise SystemExit("decision store must not enable trusted wiki write")

    DECISION_PATH.unlink()

    print("PASS: attunement decision store regression completed")


if __name__ == "__main__":
    main()
