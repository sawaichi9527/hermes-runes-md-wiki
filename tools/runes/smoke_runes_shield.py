#!/usr/bin/env python3
"""Smoke test for M21.2 Runes Shield read-only CLI."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNES = ROOT / "bin" / "runes"
EXPECTED_SCHEMA = "m21.2.p0.v1"


def run_json(command: str) -> dict:
    proc = subprocess.run(
        [str(RUNES), command, "--json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise AssertionError(
            f"runes {command} failed: rc={proc.returncode}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"runes {command} did not emit valid JSON: {exc}\n{proc.stdout}") from exc


def assert_common(data: dict, command: str) -> None:
    assert data.get("schema_version") == EXPECTED_SCHEMA, data
    assert data.get("tool") == "runes", data
    assert data.get("command") == command, data
    assert data.get("status") == "PASS", data
    assert data.get("mode") == "read_only", data
    assert data.get("shield", {}).get("name") == "Runes Shield", data
    assert data.get("p0_boundary", {}).get("agent_direct_internal_mutation_allowed") is False, data
    assert data.get("p0_boundary", {}).get("human_approval_required_for_trusted_memory") is True, data

    files = data.get("canonical_p0_files") or []
    assert files, data
    missing = [item["path"] for item in files if not item.get("exists")]
    assert not missing, f"missing canonical files: {missing}"


def main() -> int:
    capabilities = run_json("capabilities")
    guidance = run_json("guidance")

    assert_common(capabilities, "capabilities")
    assert_common(guidance, "guidance")

    cap_names = {item.get("name") for item in capabilities.get("capabilities", [])}
    assert "capabilities" in cap_names, capabilities
    assert "guidance" in cap_names, capabilities
    assert "propose" in cap_names, capabilities

    agent_interaction = guidance.get("agent_interaction", {})
    assert agent_interaction.get("consent_required_before_propose") is True, guidance
    assert agent_interaction.get("recommended_prompt_zh"), guidance

    result = {
        "suite": "M21.2 Runes Shield CLI smoke",
        "status": "PASS",
        "checked": [
            "runes capabilities --json",
            "runes guidance --json",
            "canonical P0 file existence",
            "read-only boundary metadata",
            "consent guidance",
        ],
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
                    "suite": "M21.2 Runes Shield CLI smoke",
                    "status": "FAIL",
                    "error": str(exc),
                },
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        raise SystemExit(1)
