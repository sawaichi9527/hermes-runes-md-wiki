#!/usr/bin/env python3
"""Smoke test for M22.4 human cleanup plan dry-run."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

try:
    from cleanup_plan_m22_4 import cleanup_plan
except ImportError:  # pragma: no cover
    from tools.runes.cleanup_plan_m22_4 import cleanup_plan

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "tmp" / "runes-trial" / "m22-4-cleanup-plan"
PROJECT = "k6-freelancer"
EXPECTED_SCHEMA = "m22.4.p0.v1"


def write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def seed_workspace() -> None:
    if WORKSPACE.exists():
        shutil.rmtree(WORKSPACE)

    base = WORKSPACE / PROJECT / "forge-inbox"
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


def assert_mutations_false(payload: dict) -> None:
    mutations = payload.get("mutations") or {}
    assert mutations.get("files_moved") is False, payload
    assert mutations.get("metadata_mutated") is False, payload
    assert mutations.get("proposal_state_mutated") is False, payload
    assert mutations.get("trusted_memory_created") is False, payload
    assert mutations.get("curated_wiki_mutated") is False, payload
    assert mutations.get("database_mutated") is False, payload
    assert mutations.get("importer_mutated") is False, payload


def main() -> int:
    seed_workspace()
    data = cleanup_plan(ROOT, PROJECT, str(WORKSPACE))

    assert data.get("schema_version") == EXPECTED_SCHEMA, data
    assert data.get("suite") == "M22.4 Human cleanup plan dry-run", data
    assert data.get("status") == "PASS", data
    assert data.get("mode") == "dry_run_only", data
    assert data.get("issue_count") == 1, data
    assert data.get("planned_action_count") == 1, data
    assert data.get("execution_allowed") is False, data
    assert data.get("human_approval_required_before_any_cleanup") is True, data
    assert data.get("agent_may_execute_cleanup") is False, data
    assert_mutations_false(data)

    action = data.get("planned_actions", [])[0]
    assert action.get("action_type") == "review_state_mismatch", data
    assert action.get("dry_run_only") is True, data
    assert action.get("recommended_human_decision") == "choose_directory_state_or_metadata_status_as_source_of_truth", data
    options = action.get("candidate_manual_resolutions", [])
    assert len(options) >= 2, data
    assert all(option.get("human_only") is True for option in options), data

    result = {
        "suite": "M22.4 Human cleanup plan dry-run smoke",
        "status": "PASS",
        "checked": [
            "hygiene mismatch converted into cleanup plan action",
            "cleanup plan is dry-run only",
            "execution is not allowed",
            "human approval is required before any cleanup",
            "agent may not execute cleanup",
            "files not moved",
            "metadata not mutated",
            "proposal state not mutated",
            "trusted memory not created",
            "curated wiki not mutated",
            "database not mutated",
            "importer not mutated",
        ],
        "workspace": str(WORKSPACE),
        "issue_count": data.get("issue_count"),
        "planned_action_count": data.get("planned_action_count"),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(json.dumps({"suite": "M22.4 Human cleanup plan dry-run smoke", "status": "FAIL", "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
