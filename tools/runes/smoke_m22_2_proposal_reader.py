#!/usr/bin/env python3
"""Smoke test for M22.2 read-only proposal list/show."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNES = ROOT / "bin" / "runes"
WORKSPACE = ROOT / "tmp" / "runes-trial" / "m22-2-proposal-reader"
EXPECTED_READER_SCHEMA = "m22.2.p0.v1"
EXPECTED_WRITER_SCHEMA = "m22.1.p0.v1"


def run_json(args: list[str], expect_rc: int = 0) -> dict:
    proc = subprocess.run(
        [str(RUNES), *args, "--json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != expect_rc:
        raise AssertionError(
            f"unexpected rc={proc.returncode}, expected={expect_rc}\nCMD: {' '.join(args)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"command did not emit valid JSON: {exc}\n{proc.stdout}") from exc


def assert_mutations_false(payload: dict) -> None:
    mutations = payload.get("mutations") or {}
    assert mutations.get("proposal_state_mutated") is False, payload
    assert mutations.get("trusted_memory_created") is False, payload
    assert mutations.get("curated_wiki_mutated") is False, payload
    assert mutations.get("database_mutated") is False, payload
    assert mutations.get("importer_mutated") is False, payload


def create_sandbox_proposal() -> dict:
    data = run_json(
        [
            "propose",
            "--title",
            "M22.2 read-only proposal reader smoke",
            "--text",
            "M22.2 proposal reader smoke PASS marker. This proposal must remain draft only.",
            "--source-context",
            "smoke_m22_2_proposal_reader",
            "--consent",
            "go",
            "--output-root",
            str(WORKSPACE),
        ]
    )
    assert data.get("schema_version") == EXPECTED_WRITER_SCHEMA, data
    assert data.get("status") == "PASS", data
    assert data.get("proposal_state") == "draft", data
    assert data.get("trusted_memory_created") is False, data
    assert data.get("database_mutated") is False, data
    return data


def assert_list(proposal_id: str) -> dict:
    data = run_json(
        [
            "proposal",
            "list",
            "--project",
            "k6-freelancer",
            "--state",
            "draft",
            "--output-root",
            str(WORKSPACE),
        ]
    )
    assert data.get("schema_version") == EXPECTED_READER_SCHEMA, data
    assert data.get("status") == "PASS", data
    assert data.get("mode") == "read_only", data
    assert data.get("count", 0) >= 1, data
    assert_mutations_false(data)
    ids = {item.get("proposal_id") for item in data.get("items", [])}
    assert proposal_id in ids, data
    return data


def assert_show(proposal_id: str) -> dict:
    data = run_json(
        [
            "proposal",
            "show",
            "--project",
            "k6-freelancer",
            "--id",
            proposal_id,
            "--output-root",
            str(WORKSPACE),
        ]
    )
    assert data.get("schema_version") == EXPECTED_READER_SCHEMA, data
    assert data.get("status") == "PASS", data
    assert data.get("mode") == "read_only", data
    assert_mutations_false(data)
    proposal = data.get("proposal", {})
    assert proposal.get("proposal_id") == proposal_id, data
    assert proposal.get("state") == "draft", data
    assert proposal.get("metadata_status") == "draft", data
    assert "M22.2 proposal reader smoke PASS marker" in data.get("body", ""), data
    return data


def main() -> int:
    if WORKSPACE.exists():
        shutil.rmtree(WORKSPACE)
    WORKSPACE.mkdir(parents=True, exist_ok=True)

    created = create_sandbox_proposal()
    proposal_id = created["proposal_id"]
    listed = assert_list(proposal_id)
    shown = assert_show(proposal_id)

    result = {
        "suite": "M22.2 Read-only proposal list/show smoke",
        "status": "PASS",
        "checked": [
            "sandbox draft proposal created by M22.1 writer",
            "runes proposal list finds draft proposal",
            "runes proposal show reads draft proposal body",
            "proposal reader is read-only",
            "proposal state not mutated",
            "trusted memory not created",
            "curated wiki not mutated",
            "database not mutated",
            "importer not mutated",
        ],
        "workspace": str(WORKSPACE),
        "proposal_id": proposal_id,
        "proposal_path": created.get("path"),
        "list_count": listed.get("count"),
        "show_path": shown.get("proposal", {}).get("path"),
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
                    "suite": "M22.2 Read-only proposal list/show smoke",
                    "status": "FAIL",
                    "error": str(exc),
                },
                ensure_ascii=False,
                indent=2,
            ),
        )
        raise SystemExit(1)
