#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "runes_shield" / "proposal_attunement_decision.py"
OUTPUT = ROOT / "tmp" / "m42_attunement_decision_smoke.json"
PROPOSAL_ID = "proposal-m37.2-fixture-001"


def run(*args):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        check=True,
    )


def main():
    print("== M42 Human Attunement Decision Smoke ==")

    if OUTPUT.exists():
        OUTPUT.unlink()

    dry_run = run(
        "record",
        PROPOSAL_ID,
        "--decision",
        "approved",
        "--note",
        "Smoke validation decision artifact.",
        "--dry-run",
    )

    dry_payload = json.loads(dry_run.stdout)

    print(json.dumps(dry_payload, indent=2, ensure_ascii=False))

    if dry_payload["mode"] != "dry-run":
        raise SystemExit("unexpected dry-run mode")

    if dry_payload["write"] is not False:
        raise SystemExit("dry-run unexpectedly enabled write")

    record = run(
        "record",
        PROPOSAL_ID,
        "--decision",
        "approved",
        "--note",
        "Smoke validation decision artifact.",
        "--output",
        str(OUTPUT.relative_to(ROOT)),
    )

    record_payload = json.loads(record.stdout)

    print(json.dumps(record_payload, indent=2, ensure_ascii=False))

    if record_payload["mode"] != "record-only":
        raise SystemExit("unexpected record mode")

    if record_payload["write"] is not True:
        raise SystemExit("record-only mode must report write true")

    if not OUTPUT.exists():
        raise SystemExit("expected decision artifact output")

    decision = json.loads(OUTPUT.read_text(encoding="utf-8"))

    if decision["decision"] != "approved":
        raise SystemExit("unexpected decision outcome")

    if decision["effects"]["trusted_wiki_write"] is not False:
        raise SystemExit("decision artifact must not enable wiki write")

    listing = run("list", "--format", "json")
    listing_payload = json.loads(listing.stdout)

    print(json.dumps(listing_payload, indent=2, ensure_ascii=False))

    OUTPUT.unlink()

    print("PASS: human attunement decision regression completed")


if __name__ == "__main__":
    main()
