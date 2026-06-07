#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DECISION_CLI = ROOT / "tools" / "runes_shield" / "proposal_attunement_decision.py"
PREVIEW_CLI = ROOT / "tools" / "runes_shield" / "proposal_apply_preview.py"

APPROVED_PATH = (
    ROOT
    / "tools"
    / "runes_shield"
    / "decisions"
    / "m45_1_approved_preview_smoke.json"
)

REJECTED_PATH = (
    ROOT
    / "tools"
    / "runes_shield"
    / "decisions"
    / "m45_1_rejected_preview_smoke.json"
)

QUARANTINED_PATH = (
    ROOT
    / "tools"
    / "runes_shield"
    / "decisions"
    / "m45_1_quarantined_preview_smoke.json"
)

VALID_PROPOSAL = "proposal-m37.2-fixture-001"
INVALID_PROPOSAL = "proposal-m37.3-negative-wrong-role"


def run(cmd, *args):
    return subprocess.run(
        [sys.executable, str(cmd), *args],
        capture_output=True,
        text=True,
        check=True,
    )


def load_previews():
    result = run(PREVIEW_CLI, "list", "--format", "json")
    payload = json.loads(result.stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    return payload


def find_preview(payload, proposal_id):
    for preview in payload["previews"]:
        if preview["proposal_id"] == proposal_id:
            return preview
    return None


def main():
    print("== M45.1 Proposal Apply Preview Variant Smoke ==")

    for path in [APPROVED_PATH, REJECTED_PATH, QUARANTINED_PATH]:
        if path.exists():
            path.unlink()

    run(
        DECISION_CLI,
        "record",
        VALID_PROPOSAL,
        "--decision",
        "approved",
        "--note",
        "Approved apply preview smoke.",
        "--output",
        str(APPROVED_PATH.relative_to(ROOT)),
    )

    approved_payload = load_previews()
    approved_preview = find_preview(approved_payload, VALID_PROPOSAL)

    if approved_preview is None:
        raise SystemExit("approved proposal should generate apply preview")

    if "markdown_preview" not in approved_preview:
        raise SystemExit("approved preview missing markdown_preview")

    APPROVED_PATH.unlink()

    run(
        DECISION_CLI,
        "record",
        VALID_PROPOSAL,
        "--decision",
        "rejected",
        "--note",
        "Rejected apply preview smoke.",
        "--output",
        str(REJECTED_PATH.relative_to(ROOT)),
    )

    rejected_payload = load_previews()

    if find_preview(rejected_payload, VALID_PROPOSAL) is not None:
        raise SystemExit("rejected proposal must not generate apply preview")

    REJECTED_PATH.unlink()

    run(
        DECISION_CLI,
        "record",
        VALID_PROPOSAL,
        "--decision",
        "quarantined",
        "--note",
        "Quarantined apply preview smoke.",
        "--output",
        str(QUARANTINED_PATH.relative_to(ROOT)),
    )

    quarantined_payload = load_previews()

    if find_preview(quarantined_payload, VALID_PROPOSAL) is not None:
        raise SystemExit("quarantined proposal must not generate apply preview")

    if find_preview(quarantined_payload, INVALID_PROPOSAL) is not None:
        raise SystemExit("invalid proposal must not generate apply preview")

    QUARANTINED_PATH.unlink()

    print("PASS: proposal apply preview variant regression completed")


if __name__ == "__main__":
    main()
