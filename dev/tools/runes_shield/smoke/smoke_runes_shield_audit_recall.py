#!/usr/bin/env python3

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PERSIST_CLI = ROOT / "tools" / "runes_shield" / "runes_shield_audit_persistence.py"
RECALL_CLI = ROOT / "tools" / "runes_shield" / "runes_shield_audit_recall.py"
TEMP_ROOT = ROOT / "tmp" / "m55-smoke-audit"

REQUEST = {
    "agent": "hermes-agent",
    "conversation_id": "conv-m55-smoke",
    "request": {
        "intent": "check_integrity",
    },
}

EXPECTED_EFFECT_KEYS = {
    "trusted_wiki_write",
    "markdown_mutation",
    "index_update",
    "automatic_apply",
    "automatic_promotion",
    "database_mutation",
    "observation_ingested_to_rag",
    "audit_log_written",
    "session_reexecuted",
    "adapter_reinvoked",
}


def persist():
    return subprocess.run(
        [
            sys.executable,
            str(PERSIST_CLI),
            "--raw-json",
            json.dumps(REQUEST),
            "--audit-root",
            str(TEMP_ROOT.relative_to(ROOT)),
            "--write",
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )


def recall(*args):
    return subprocess.run(
        [
            sys.executable,
            str(RECALL_CLI),
            *args,
        ],
        capture_output=True,
        text=True,
        check=True,
    )


def assert_effects(payload):
    if set(payload["effects"]) != EXPECTED_EFFECT_KEYS:
        raise SystemExit("unexpected recall effect coverage")

    if any(value is not False for value in payload["effects"].values()):
        raise SystemExit("recall/replay effects must remain disabled")


def main():
    print("== M55 Governance Audit Recall Smoke ==")

    if TEMP_ROOT.exists():
        shutil.rmtree(TEMP_ROOT)

    persisted = json.loads(persist().stdout)

    session_id = persisted["session_id"]

    summary = json.loads(
        recall(
            "summary",
            "--audit-root",
            str(TEMP_ROOT.relative_to(ROOT)),
            "--format",
            "json",
        ).stdout
    )

    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if summary["status"] != "PASS":
        raise SystemExit("summary recall failed")

    assert_effects(summary)

    if summary["event_count"] < 2:
        raise SystemExit("expected recalled events")

    replay = json.loads(
        recall(
            "replay",
            "--audit-root",
            str(TEMP_ROOT.relative_to(ROOT)),
            "--session-id",
            session_id,
            "--format",
            "json",
        ).stdout
    )

    print(json.dumps(replay, indent=2, ensure_ascii=False))

    if replay["status"] != "PASS":
        raise SystemExit("replay reconstruction failed")

    assert_effects(replay)

    if replay["chain_count"] < 2:
        raise SystemExit("expected reconstructed replay chain")

    recall_payload = json.loads(
        recall(
            "recall",
            "--audit-root",
            str(TEMP_ROOT.relative_to(ROOT)),
            "--session-id",
            session_id,
            "--format",
            "json",
        ).stdout
    )

    if recall_payload["event_count"] != replay["event_count"]:
        raise SystemExit("recall/replay event mismatch")

    jsonl_output = recall(
        "recall",
        "--audit-root",
        str(TEMP_ROOT.relative_to(ROOT)),
        "--format",
        "jsonl",
    ).stdout

    lines = [line for line in jsonl_output.splitlines() if line.strip()]

    if len(lines) < 2:
        raise SystemExit("expected recall jsonl rows")

    for line in lines:
        row = json.loads(line)

        if row["event_type"] != "runtime_audit_persistence":
            raise SystemExit("unexpected recalled event type")

    shutil.rmtree(TEMP_ROOT)

    print("PASS: governance audit recall validation completed")


if __name__ == "__main__":
    main()
