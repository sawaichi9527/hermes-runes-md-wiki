#!/usr/bin/env python3
"""Smoke test for M21.4 Runes Shield CLI, offer policy, and sandbox trial."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNES = ROOT / "bin" / "runes"
TRIAL_RUNNER = ROOT / "tools" / "runes" / "trial_run_m21_4.py"
EXPECTED_SCHEMA = "m21.3.p0.v1"
EXPECTED_TRIAL_SCHEMA = "m21.4.p0.v1"


def run_json(command: str, *args: str) -> dict:
    proc = subprocess.run(
        [str(RUNES), command, *args, "--json"],
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


def run_trial_json() -> dict:
    proc = subprocess.run(
        [sys.executable, str(TRIAL_RUNNER), "--json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise AssertionError(
            f"M21.4 trial runner failed: rc={proc.returncode}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"M21.4 trial runner did not emit valid JSON: {exc}\n{proc.stdout}") from exc


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


def assert_offer(text: str, expected: bool, reason: str) -> dict:
    data = run_json("offer", "--text", text)
    assert_common(data, "offer")
    decision = data.get("decision", {})
    assert decision.get("should_offer") is expected, {
        "reason": reason,
        "text": text,
        "decision": decision,
    }
    assert decision.get("proposal_created") is False, decision
    assert decision.get("write") is False, decision
    return data


def assert_trial(data: dict) -> None:
    assert data.get("schema_version") == EXPECTED_TRIAL_SCHEMA, data
    assert data.get("status") == "PASS", data
    assert data.get("mode") == "sandbox_write_only", data
    assert data.get("trusted_wiki_mutated") is False, data
    assert data.get("database_mutated") is False, data
    assert data.get("proposal_created_in_real_forge_inbox") is False, data

    checks = data.get("checks", {})
    assert checks.get("created_three_proposals") is True, data
    assert checks.get("approved_imported_visible") is True, data
    assert checks.get("rejected_not_trusted_visible") is True, data
    assert checks.get("draft_not_trusted_visible") is True, data
    assert checks.get("trusted_index_contains_only_approved") is True, data

    recall = data.get("recall_result", {})
    assert recall.get("approved_visible") is True, data
    assert recall.get("rejected_visible") is False, data
    assert recall.get("draft_visible") is False, data


def main() -> int:
    capabilities = run_json("capabilities")
    guidance = run_json("guidance")

    assert_common(capabilities, "capabilities")
    assert_common(guidance, "guidance")

    cap_names = {item.get("name") for item in capabilities.get("capabilities", [])}
    assert "capabilities" in cap_names, capabilities
    assert "guidance" in cap_names, capabilities
    assert "offer" in cap_names, capabilities
    assert "propose" in cap_names, capabilities

    agent_interaction = guidance.get("agent_interaction", {})
    assert agent_interaction.get("consent_required_before_propose") is True, guidance
    assert agent_interaction.get("recommended_prompt_zh"), guidance

    offer_positive = assert_offer(
        "M21.2 Runes Shield capabilities/guidance CLI PASS. This is a frozen baseline and should be tracked as a project decision.",
        True,
        "project decision / baseline / PASS marker should offer Runes proposal",
    )
    assert offer_positive.get("decision", {}).get("recommended_prompt_zh"), offer_positive

    assert_offer(
        "哈哈，這名字很帥氣",
        False,
        "casual short acknowledgement should not offer Runes proposal",
    )

    assert_offer(
        "DATABASE_URL=postgres://user:password@example/db and API_KEY=secret-token",
        False,
        "secret-bearing content should not offer Runes proposal",
    )

    assert_offer(
        "Maybe this architecture might be useful, but it is still unverified speculation.",
        False,
        "unverified speculation should not offer Runes proposal",
    )

    trial = run_trial_json()
    assert_trial(trial)

    result = {
        "suite": "M21.4 Runes Shield CLI, offer-policy, and multi-proposal sandbox smoke",
        "status": "PASS",
        "checked": [
            "runes capabilities --json",
            "runes guidance --json",
            "runes offer --text <positive durable knowledge> --json",
            "runes offer --text <casual chat> --json",
            "runes offer --text <secret-bearing content> --json",
            "runes offer --text <unverified speculation> --json",
            "M21.4 sandbox create proposal A/B/C",
            "M21.4 sandbox approve A",
            "M21.4 sandbox reject B",
            "M21.4 sandbox leave C draft",
            "M21.4 sandbox approved-only trusted visibility",
            "canonical P0 file existence",
            "read-only boundary metadata",
            "consent guidance",
        ],
        "trial_workspace": trial.get("workspace"),
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
                    "suite": "M21.4 Runes Shield CLI, offer-policy, and multi-proposal sandbox smoke",
                    "status": "FAIL",
                    "error": str(exc),
                },
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        raise SystemExit(1)
