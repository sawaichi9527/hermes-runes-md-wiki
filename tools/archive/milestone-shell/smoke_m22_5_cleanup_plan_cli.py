#!/usr/bin/env python3
"""Smoke test for M22.5 cleanup-plan CLI wiring."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNES = ROOT / "bin" / "runes"
WORKSPACE = ROOT / "tmp" / "runes-trial" / "m22-5-cleanup-plan-cli"
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
""",
    )


def run_cli() -> dict:
    proc = subprocess.run(
        [
            str(RUNES),
            "proposal",
            "cleanup-plan",
            "--project",
            PROJECT,
            "--output-root",
            str(WORKSPACE),
            "--json",
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise AssertionError(f"unexpected rc={proc.returncode}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
    return json.loads(proc.stdout)


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
    data = run_cli()

    assert data.get("schema_version") == EXPECTED_SCHEMA, data
    assert data.get("suite") == "M22.4 Human cleanup plan dry-run", data
    assert data.get("status") == "PASS", data
    assert data.get("mode") == "dry_run_only", data
    assert data.get("execution_allowed") is False, data
    assert data.get("agent_may_execute_cleanup") is False, data
    assert data.get("planned_action_count") == 1, data
    assert_mutations_false(data)

    result = {
        "suite": "M22.5 Cleanup-plan CLI smoke",
        "status": "PASS",
        "checked": [
            "bin/runes proposal cleanup-plan --json works",
            "cleanup-plan CLI produces dry-run plan",
            "cleanup-plan CLI is non-executable",
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
        "planned_action_count": data.get("planned_action_count"),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(json.dumps({"suite": "M22.5 Cleanup-plan CLI smoke", "status": "FAIL", "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
