#!/usr/bin/env python3

import json
from pathlib import Path

from validate_proposal_fixture import validate_fixture

ROOT = Path(__file__).resolve().parents[2]
RUNE_SHIELD_DIR = ROOT / "tools" / "runes_shield"
FIXTURE_DIR = RUNE_SHIELD_DIR / "fixtures"
DRAFT_DIR = RUNE_SHIELD_DIR / "drafts"

SOURCES = [
    ("fixture", FIXTURE_DIR, "proposal_draft_*.json"),
    ("draft", DRAFT_DIR, "*.json"),
]


def iter_proposal_sources():
    for source_type, source_dir, pattern in SOURCES:
        if not source_dir.exists():
            continue
        for path in sorted(source_dir.glob(pattern)):
            yield source_type, path


def build_manifest():
    entries = []

    for source_type, proposal_path in iter_proposal_sources():
        validation = validate_fixture(proposal_path)
        entries.append(
            {
                "proposal_fixture": proposal_path.name,
                "proposal_source": source_type,
                "proposal_path": str(proposal_path.relative_to(ROOT)),
                "proposal_id": _read_proposal_id(proposal_path),
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
        "source": "tools/runes_shield/fixtures + tools/runes_shield/drafts",
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
