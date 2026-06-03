#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "runes_shield" / "build_proposal_draft.py"
OUTPUT = ROOT / "tmp" / "m41_1_write_draft_smoke.json"


def run(*args):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        check=True,
    )


def main():
    print("== M41.1 Governed Proposal Draft Write Smoke ==")

    if OUTPUT.exists():
        OUTPUT.unlink()

    result = run(
        "--source-summary",
        "M41.1 smoke validates external draft writing only.",
        "--claim",
        "Runes Shield may write external proposal draft JSON files.",
        "--claim",
        "External proposal drafts do not write trusted wiki memory.",
        "--write-draft",
        "--output",
        str(OUTPUT.relative_to(ROOT)),
    )

    payload = json.loads(result.stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if payload["status"] != "PASS":
        raise SystemExit("write-draft build did not pass")

    if payload["mode"] != "write-draft":
        raise SystemExit("unexpected builder mode")

    if payload["write"] is not True:
        raise SystemExit("write-draft mode must report write true")

    if not OUTPUT.exists():
        raise SystemExit("expected proposal draft output file")

    validation = payload.get("validation", {})
    if validation.get("status") != "PASS":
        raise SystemExit("written draft did not validate")

    proposal = json.loads(OUTPUT.read_text(encoding="utf-8"))
    if proposal["status"] != "pending_human_review":
        raise SystemExit("written draft has unexpected status")

    OUTPUT.unlink()

    print("PASS: governed proposal draft write regression completed")


if __name__ == "__main__":
    main()
