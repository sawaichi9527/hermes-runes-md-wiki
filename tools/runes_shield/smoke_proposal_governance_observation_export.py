#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPORT_CLI = ROOT / "tools" / "runes_shield" / "proposal_governance_observation_export.py"

EXPECTED_EFFECT_KEYS = {
    "trusted_wiki_write",
    "markdown_mutation",
    "index_update",
    "automatic_apply",
    "automatic_promotion",
    "database_mutation",
    "observation_ingested_to_rag",
}


def run(cmd, *args):
    return subprocess.run(
        [sys.executable, str(cmd), *args],
        capture_output=True,
        text=True,
        check=True,
    )


def main():
    print("== M50.1 Governance Observation Export Smoke ==")

    result = run(EXPORT_CLI, "--format", "json")
    payload = json.loads(result.stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if payload["status"] != "PASS":
        raise SystemExit("governance observation export failed")

    if payload["trial_run_status"] != "PASS":
        raise SystemExit("governance observation export requires PASS trial-run")

    if payload["integrity_status"] != "PASS":
        raise SystemExit("governance observation export requires integrity PASS")

    if payload["integrity_issue_count"] != 0:
        raise SystemExit("governance observation export requires zero integrity issues")

    if payload["write"] is not False:
        raise SystemExit("governance observation export must remain read-only")

    if set(payload["effects"]) != EXPECTED_EFFECT_KEYS:
        raise SystemExit("unexpected governance observation export effect coverage")

    if any(value is not False for value in payload["effects"].values()):
        raise SystemExit("governance observation export effects must remain disabled")

    if payload["event_count"] != payload["proposal_count"]:
        raise SystemExit("expected one exported event per proposal")

    if not payload["events"]:
        raise SystemExit("expected exported governance observation events")

    for event in payload["events"]:
        if event["write"] is not False:
            raise SystemExit("exported governance observation event must remain read-only")

        if event["execution_status"] != "BLOCKED":
            raise SystemExit("exported governance observation execution must remain BLOCKED")

        if any(value is not False for value in event["effects"].values()):
            raise SystemExit("exported governance observation event effects must remain disabled")

    jsonl_result = run(EXPORT_CLI, "--format", "jsonl")
    jsonl_lines = [line for line in jsonl_result.stdout.splitlines() if line.strip()]

    if len(jsonl_lines) != payload["event_count"]:
        raise SystemExit("jsonl export line count mismatch")

    for line in jsonl_lines:
        event = json.loads(line)

        if event["event_type"] != "governance_trial_observation":
            raise SystemExit("unexpected governance observation event type")

    print("PASS: governance observation export validation completed")


if __name__ == "__main__":
    main()
