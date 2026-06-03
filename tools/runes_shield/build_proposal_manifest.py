#!/usr/bin/env python3

import json
from pathlib import Path

from validate_proposal_fixture import validate_fixture

ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = ROOT / "tools" / "runes_shield" / "fixtures"


def iter_proposal_fixtures():
    return sorted(FIXTURE_DIR.glob("proposal_draft_*.json"))


def build_manifest():
    entries = []

    for fixture_path in iter_proposal_fixtures():
        validation = validate_fixture(fixture_path)
        entries.append(
            {
                "proposal_fixture": fixture_path.name,
                "proposal_id": _read_proposal_id(fixture_path),
                "sample_status": validation["sample_status"],
                "validation_status": validation["status"],
                "blocked_status_detected": validation["blocked_status_detected"],
                "allowed_status_validation": validation["allowed_status_validation"],
                "role_validation": validation["role_validation"],
                "role_mismatches": validation["role_mismatches"],
                "missing_fields": validation["missing_fields"],
                "assessment_missing_fields": validation[
                    "assessment_missing_fields"
                ],
                "write": False,
            }
        )

    return {
        "manifest_version": "m38-proposal-registry-v1",
        "source": "tools/runes_shield/fixtures",
        "entry_count": len(entries),
        "write": False,
        "capabilities": {
            "trusted_wiki_write": False,
            "automatic_approval": False,
            "automatic_promotion": False,
            "apply_execution": False,
            "database_mutation": False,
        },
        "entries": entries,
    }


def _read_proposal_id(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("proposal_id")


def main():
    print(json.dumps(build_manifest(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
