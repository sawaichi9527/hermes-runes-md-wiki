#!/usr/bin/env python3

import json
from pathlib import Path

from validate_proposal_fixture import validate_fixture

ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = ROOT / "tools" / "runes_shield" / "fixtures"

NEGATIVE_FIXTURES = [
    "proposal_draft_m37_3_negative_blocked_status.json",
    "proposal_draft_m37_3_negative_missing_field.json",
    "proposal_draft_m37_3_negative_wrong_role.json",
]


def main():
    print("== M37.3 Negative Proposal Fixture Smoke ==")

    failures = []

    for fixture in NEGATIVE_FIXTURES:
        path = FIXTURE_DIR / fixture

        result = validate_fixture(path)

        print(json.dumps(result, indent=2, ensure_ascii=False))

        if result["status"] != "FAIL":
            failures.append(fixture)

    if failures:
        raise SystemExit(
            f"negative fixtures unexpectedly passed: {failures}"
        )

    print("PASS: negative proposal fixture regression completed")


if __name__ == "__main__":
    main()
