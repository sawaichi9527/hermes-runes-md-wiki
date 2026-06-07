#!/usr/bin/env python3

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "runes_shield" / "runes_shield_audit_persistence.py"
TEMP_ROOT = ROOT / "tmp" / "m54-smoke-audit"

EXPECTED_EFFECT_KEYS = {
    "trusted_wiki_write",
    "markdown_mutation",
    "index_update",
    "automatic_apply",
    "automatic_promotion",
    "database_mutation",
    "observation_ingested_to_rag",
    "audit_log_written",
    "session_persisted",
}

REQUEST = {
    "agent": "hermes-agent",
    "conversation_id": "conv-m54-smoke",
    "request": {
        "intent": "check_integrity",
    },
}


def run(extra_args=None, fmt="json"):
    args = [
        sys.executable,
        str(CLI),
        "--raw-json",
        json.dumps(REQUEST),
        "--audit-root",
        str(TEMP_ROOT.relative_to(ROOT)),
        "--format",
        fmt,
    ]

    if extra_args:
        args.extend(extra_args)

    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        check=True,
    )


def assert_effects(payload, expected_write):
    if set(payload["effects"]) != EXPECTED_EFFECT_KEYS:
        raise SystemExit("unexpected audit persistence effect coverage")

    if payload["effects"]["audit_log_written"] != expected_write:
        raise SystemExit("unexpected audit_log_written state")

    if payload["effects"]["session_persisted"] != expected_write:
        raise SystemExit("unexpected session_persisted state")

    for key, value in payload["effects"].items():
        if key in {"audit_log_written", "session_persisted"}:
            continue
        if value is not False:
            raise SystemExit(f"unexpected enabled effect: {key}")


def main():
    print("== M54 Runtime Audit Persistence Smoke ==")

    if TEMP_ROOT.exists():
        shutil.rmtree(TEMP_ROOT)

    dry_run = json.loads(run().stdout)

    print(json.dumps(dry_run, indent=2, ensure_ascii=False))

    if dry_run["status"] != "PASS":
        raise SystemExit("dry-run persistence failed")

    if dry_run["mode"] != "dry-run":
        raise SystemExit("expected dry-run mode")

    if dry_run["write"] is not False:
        raise SystemExit("dry-run write flag must remain false")

    assert_effects(dry_run, expected_write=False)

    output_path = ROOT / dry_run["output_path"]

    if output_path.exists():
        raise SystemExit("dry-run must not create audit file")

    persisted = json.loads(run(extra_args=["--write"]).stdout)

    print(json.dumps(persisted, indent=2, ensure_ascii=False))

    if persisted["status"] != "PASS":
        raise SystemExit("write persistence failed")

    if persisted["mode"] != "write":
        raise SystemExit("expected write mode")

    if persisted["write"] is not True:
        raise SystemExit("write mode flag must be true")

    assert_effects(persisted, expected_write=True)

    persisted_path = ROOT / persisted["output_path"]

    if not persisted_path.exists():
        raise SystemExit("expected persisted audit file")

    lines = [line for line in persisted_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    if len(lines) != persisted["event_count"]:
        raise SystemExit("persisted audit event count mismatch")

    for line in lines:
        event = json.loads(line)

        if event["event_type"] != "runtime_audit_persistence":
            raise SystemExit("unexpected persisted event type")

        if event["write"] is not False:
            raise SystemExit("persisted audit event must remain read-only")

    jsonl_output = run(fmt="jsonl").stdout

    if len([line for line in jsonl_output.splitlines() if line.strip()]) < 2:
        raise SystemExit("expected jsonl audit persistence export")

    shutil.rmtree(TEMP_ROOT)

    print("PASS: runtime audit persistence validation completed")


if __name__ == "__main__":
    main()
