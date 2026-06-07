#!/usr/bin/env python3
"""Smoke test for M22.3 read-only proposal status hygiene report."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

try:
    from proposal_hygiene_m22_3 import hygiene_report
except ImportError:  # pragma: no cover
    from tools.runes.proposal_hygiene_m22_3 import hygiene_report

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "tmp" / "runes-trial" / "m22-3-proposal-hygiene"
PROJECT = "k6-freelancer"
EXPECTED_SCHEMA = "m22.3.p0.v1"


def write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def seed_workspace() -> None:
    if WORKSPACE.exists():
        shutil.rmtree(WORKSPACE)

    base = WORKSPACE / PROJECT / "forge-inbox"

    write_file(
        base / "clean-draft.md",
        """---
proposal_id: clean-draft
title: Clean draft
project: k6-freelancer
status: draft
trusted_memory: false
---

# Clean draft

This is a normal draft.
""",
    )

    write_file(
        base / "mismatch-approved-in-draft.md",
        """---
proposal_id: mismatch-approved-in-draft
title: Mismatch approved in draft
project: k6-freelancer
status: approved
trusted_memory: false
---

# Mismatch approved in draft

Directory says draft, metadata says approved.
""",
    )

    write_file(
        base / "missing-status.md",
        """---
proposal_id: missing-status
title: Missing status
project: k6-freelancer
trusted_memory: false
---

# Missing status

No frontmatter status.
""",
    )


def assert_mutations_false(payload: dict) -> None:
    mutations = payload.get("mutations") or {}
    assert mutations.get("proposal_state_mutated") is False, payload
    assert mutations.get("metadata_mutated") is False, payload
    assert mutations.get("trusted_memory_created") is False, payload
    assert mutations.get("curated_wiki_mutated") is False, payload
    assert mutations.get("database_mutated") is False, payload
    assert mutations.get("importer_mutated") is False, payload


def main() -> int:
    seed_workspace()
    report = hygiene_report(ROOT, PROJECT, str(WORKSPACE))

    assert report.get("schema_version") == EXPECTED_SCHEMA, report
    assert report.get("suite") == "M22.3 Read-only proposal status hygiene report", report
    assert report.get("status") == "PASS", report
    assert report.get("mode") == "read_only", report
    assert report.get("proposal_count") == 3, report
    assert report.get("issue_count") == 2, report
    assert_mutations_false(report)

    issue_types = {issue.get("type") for issue in report.get("issues", [])}
    assert "directory_state_metadata_status_mismatch" in issue_types, report
    assert "missing_metadata_status" in issue_types, report

    result = {
        "suite": "M22.3 Read-only proposal status hygiene smoke",
        "status": "PASS",
        "checked": [
            "clean draft has no issue",
            "draft directory with approved metadata is reported",
            "missing metadata status is reported",
            "hygiene report is read-only",
            "proposal state not mutated",
            "metadata not mutated",
            "trusted memory not created",
            "curated wiki not mutated",
            "database not mutated",
            "importer not mutated",
        ],
        "workspace": str(WORKSPACE),
        "issue_count": report.get("issue_count"),
        "issue_counts": report.get("issue_counts"),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(
            json.dumps(
                {
                    "suite": "M22.3 Read-only proposal status hygiene smoke",
                    "status": "FAIL",
                    "error": str(exc),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1)
