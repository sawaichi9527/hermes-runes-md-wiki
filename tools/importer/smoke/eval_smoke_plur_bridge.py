#!/usr/bin/env python3
"""Core smoke for v0.7.4-dev PLUR runtime memory bridge.

This smoke is intentionally lightweight and dependency-free. It verifies the
S7-S9 bridge helper stays read-only, keeps Noop available, and exposes the
expected schema roles without requiring PLUR to be installed.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


IMPORTER = Path(__file__).resolve().parents[1]
SCRIPT = IMPORTER / "plur_runtime_bridge.py"


def run_json(*args: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args, "--json"],
        cwd=IMPORTER,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
    )
    if proc.returncode != 0:
        return {
            "status": "FAIL",
            "error": "command_failed",
            "args": list(args),
            "returncode": proc.returncode,
            "stdout_tail": proc.stdout[-2000:],
            "stderr_tail": proc.stderr[-2000:],
        }
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        return {
            "status": "FAIL",
            "error": "json_decode_failed",
            "args": list(args),
            "exception": str(exc),
            "stdout_tail": proc.stdout[-2000:],
            "stderr_tail": proc.stderr[-2000:],
        }


def check_status() -> dict:
    payload = run_json("status", "--provider", "auto")
    failures = []

    if payload.get("status") != "pass":
        failures.append("status_not_pass")
    if payload.get("provider_selected") != "noop":
        failures.append("auto_did_not_select_noop")
    if payload.get("read_only") is not True:
        failures.append("not_read_only")
    if payload.get("memory_read") is not False:
        failures.append("memory_read_not_false")
    if payload.get("memory_write") is not False:
        failures.append("memory_write_not_false")
    if payload.get("writes_performed") is not False:
        failures.append("writes_performed_not_false")

    providers = payload.get("providers", {})
    noop = providers.get("noop", {})
    if noop.get("available") is not True:
        failures.append("noop_not_available")
    if noop.get("selected") is not True:
        failures.append("noop_not_selected")

    return {
        "name": "plur_bridge_status_auto_noop",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "provider_selected": payload.get("provider_selected"),
        "read_only": payload.get("read_only"),
        "memory_read": payload.get("memory_read"),
        "memory_write": payload.get("memory_write"),
        "writes_performed": payload.get("writes_performed"),
    }


def check_schema() -> dict:
    payload = run_json("schema")
    failures = []

    expected_roles = {"engram", "episode", "checkpoint", "candidate"}
    roles = set((payload.get("roles") or {}).keys())

    if payload.get("status") != "pass":
        failures.append("status_not_pass")
    if payload.get("read_only") is not True:
        failures.append("schema_not_read_only")
    if payload.get("writes_performed") is not False:
        failures.append("schema_writes_performed_not_false")
    if not expected_roles.issubset(roles):
        failures.append("missing_expected_roles")

    candidate = (payload.get("roles") or {}).get("candidate", {})
    if candidate.get("auto_promote_to_runes_wiki") is not False:
        failures.append("candidate_auto_promote_not_false")

    episode = (payload.get("roles") or {}).get("episode", {})
    if episode.get("default_prompt_injection") != "disabled":
        failures.append("episode_injection_not_disabled")

    return {
        "name": "plur_bridge_schema_mapping",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "roles": sorted(roles),
    }


def main() -> None:
    results = [check_status(), check_schema()]
    failed = sum(1 for item in results if item["status"] != "PASS")
    output = {
        "suite": "PLUR Runtime Bridge Smoke Test",
        "profile": "core",
        "status": "PASS" if failed == 0 else "FAIL",
        "failed": failed,
        "total": len(results),
        "results": results,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
