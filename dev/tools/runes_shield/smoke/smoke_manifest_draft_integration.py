#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUILD_CLI = ROOT / "tools" / "runes_shield" / "build_proposal_draft.py"
MANIFEST_CLI = ROOT / "tools" / "runes_shield" / "build_proposal_manifest.py"
QUEUE_CLI = ROOT / "tools" / "runes_shield" / "proposal_review_queue.py"
DRAFT_PATH = ROOT / "tools" / "runes_shield" / "drafts" / "m41_2_manifest_integration.json"


PROPOSAL_SUMMARY = "M41.2 manifest integration smoke proposal."


def run(cmd, *args):
    return subprocess.run(
        [sys.executable, str(cmd), *args],
        capture_output=True,
        text=True,
        check=True,
    )


def main():
    print("== M41.2 Manifest Draft Integration Smoke ==")

    if DRAFT_PATH.exists():
        DRAFT_PATH.unlink()

    build = run(
        BUILD_CLI,
        "--source-summary",
        PROPOSAL_SUMMARY,
        "--claim",
        "External drafts may appear in the proposal manifest.",
        "--claim",
        "Pending-review drafts may enter the attunement queue.",
        "--write-draft",
        "--output",
        str(DRAFT_PATH.relative_to(ROOT)),
    )

    build_payload = json.loads(build.stdout)
    proposal_id = build_payload["proposal"]["proposal_id"]

    manifest = run(MANIFEST_CLI)
    manifest_payload = json.loads(manifest.stdout)

    print(json.dumps(manifest_payload, indent=2, ensure_ascii=False))

    matching_entries = [
        entry
        for entry in manifest_payload["entries"]
        if entry["proposal_id"] == proposal_id
    ]

    if not matching_entries:
        raise SystemExit("draft proposal missing from manifest")

    manifest_entry = matching_entries[0]

    if manifest_entry["proposal_source"] != "draft":
        raise SystemExit("manifest did not classify proposal as draft")

    queue = run(QUEUE_CLI, "list", "--format", "json")
    queue_payload = json.loads(queue.stdout)

    print(json.dumps(queue_payload, indent=2, ensure_ascii=False))

    queue_matches = [
        entry
        for entry in queue_payload["entries"]
        if entry["proposal_id"] == proposal_id
    ]

    if not queue_matches:
        raise SystemExit("draft proposal missing from review queue")

    DRAFT_PATH.unlink()

    print("PASS: manifest draft integration regression completed")


if __name__ == "__main__":
    main()
