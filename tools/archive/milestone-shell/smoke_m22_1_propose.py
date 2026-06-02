#!/usr/bin/env python3
"""Smoke test for M22.1 governed draft proposal writer."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNES = ROOT / "bin" / "runes"
WORKSPACE = ROOT / "tmp" / "runes-trial" / "m22-1-propose"
EXPECTED_SCHEMA = "m22.1.p0.v1"


def run_propose(*args: str, expect_rc: int = 0) -> dict:
    proc = subprocess.run(
        [str(RUNES), "propose", *args, "--json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != expect_rc:
        raise AssertionError(
            f"unexpected rc={proc.returncode}, expected={expect_rc}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"runes propose did not emit valid JSON: {exc}\n{proc.stdout}") from exc


def assert_refused_without_consent() -> None:
    data = run_propose(
        "--title",
        "M22.1 missing consent should refuse",
        "--text",
        "M22.1 proposal writer smoke PASS marker should be draft only.",
        "--output-root",
        str(WORKSPACE),
        expect_rc=2,
    )
    assert data.get("schema_version") == EXPECTED_SCHEMA, data
    assert data.get("status") == "REFUSED", data
    assert data.get("proposal_created") is False, data
    assert data.get("trusted_memory_created") is False, data
    assert data.get("database_mutated") is False, data
    assert data.get("reason") == "missing_or_invalid_user_consent_marker", data


def assert_created_with_consent() -> dict:
    data = run_propose(
        "--title",
        "M22.1 governed draft proposal smoke",
        "--text",
        "M22.1 proposal writer smoke PASS marker. This creates a governed draft proposal only.",
        "--source-context",
        "smoke_m22_1_propose",
        "--consent",
        "go",
        "--output-root",
        str(WORKSPACE),
        expect_rc=0,
    )
    assert data.get("schema_version") == EXPECTED_SCHEMA, data
    assert data.get("status") == "PASS", data
    assert data.get("mode") == "draft_write_only", data
    assert data.get("proposal_created") is True, data
    assert data.get("proposal_state") == "draft", data
    assert data.get("trusted_memory_created") is False, data
    assert data.get("approved") is False, data
    assert data.get("promoted") is False, data
    assert data.get("database_mutated") is False, data
    assert data.get("importer_mutated") is False, data

    path = Path(data["path"])
    assert path.exists(), data
    body = path.read_text(encoding="utf-8")
    assert "status: draft" in body, body
    assert "trusted_memory: false" in body, body
    assert "Human approval required: true" in body, body
    assert "Agent may approve: false" in body, body
    assert "Agent may promote: false" in body, body

    checks = data.get("checks", {})
    assert checks.get("proposal_file_exists") is True, data
    assert checks.get("proposal_state_is_draft") is True, data
    assert checks.get("trusted_memory_created") is False, data
    assert checks.get("approved") is False, data
    assert checks.get("promoted") is False, data
    assert checks.get("database_mutated") is False, data
    assert checks.get("importer_mutated") is False, data
    assert checks.get("consent_recorded") is True, data
    return data


def main() -> int:
    if WORKSPACE.exists():
        shutil.rmtree(WORKSPACE)
    WORKSPACE.mkdir(parents=True, exist_ok=True)

    assert_refused_without_consent()
    created = assert_created_with_consent()

    result = {
        "suite": "M22.1 Governed draft proposal writer smoke",
        "status": "PASS",
        "checked": [
            "runes propose without consent refuses",
            "runes propose with consent creates draft proposal",
            "proposal status remains draft",
            "trusted memory not created",
            "approval not performed",
            "promotion not performed",
            "database not mutated",
            "importer not mutated",
        ],
        "workspace": str(WORKSPACE),
        "proposal_path": created.get("path"),
        "proposal_id": created.get("proposal_id"),
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
                    "suite": "M22.1 Governed draft proposal writer smoke",
                    "status": "FAIL",
                    "error": str(exc),
                },
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        raise SystemExit(1)
