#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "runes_shield" / "runes_governance_compat_snapshot.py"


def run(fmt="json"):
    return subprocess.run(
        [
            sys.executable,
            str(CLI),
            "--timeout",
            "15",
            "--format",
            fmt,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )


def main():
    print("== M56.6 Governance Compatibility Snapshot Smoke ==")

    payload = json.loads(run().stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if payload["snapshot_version"] != "m56.6-governance-compatibility-snapshot-v1":
        raise SystemExit("unexpected snapshot version")

    if payload["status"] != "PASS":
        raise SystemExit("compatibility snapshot failed")

    if payload["mode"] != "governance-compatibility-snapshot":
        raise SystemExit("unexpected snapshot mode")

    if payload["scale"] != "personal-local":
        raise SystemExit("snapshot scale drift detected")

    if payload["write"] is not False:
        raise SystemExit("compatibility snapshot must remain read-only")

    if payload["issue_count"] != 0:
        raise SystemExit("compatibility snapshot must report zero issues")

    versions = payload["expected_versions"]

    required_versions = {
        "integrity_version",
        "trial_run_version",
        "shield_version",
        "adapter_version",
        "session_version",
        "persistence_version",
        "recall_version",
        "verity_version",
        "verity_contract_version",
        "bounded_regression_version",
        "audit_pressure_version",
        "replay_safety_version",
        "invocation_contract_version",
    }

    if set(versions) != required_versions:
        raise SystemExit("expected version surface drift detected")

    locked = payload["locked_surfaces"]

    if len(locked["verity_checks"]) != 10:
        raise SystemExit("verity check count drift detected")

    if len(locked["invocation_tools"]) != 8:
        raise SystemExit("invocation tool count drift detected")

    if len(locked["adapter_safe_intents"]) != 9:
        raise SystemExit("adapter safe intent count drift detected")

    if len(locked["adapter_blocked_intents"]) != 7:
        raise SystemExit("adapter blocked intent count drift detected")

    compatibility = payload["compatibility_matrix"]

    if compatibility["governance_core"]["m49_integrity"]["status"] != "PASS":
        raise SystemExit("m49 integrity compatibility drift")

    if compatibility["governance_core"]["m50_controlled_trial"]["status"] != "PASS":
        raise SystemExit("m50 controlled trial compatibility drift")

    runtime_boundary = compatibility["runtime_boundary"]

    if runtime_boundary["m51_invocation_tools"]["tool_count"] != 8:
        raise SystemExit("m51 invocation tool count drift")

    if len(runtime_boundary["m52_adapter_intents"]["safe_intents"]) != 9:
        raise SystemExit("m52 safe intent drift")

    observability = compatibility["runtime_observability"]

    for key in ("m53_session", "m54_persistence", "m55_recall_replay"):
        if observability[key]["status"] != "PASS":
            raise SystemExit(f"observability compatibility drift: {key}")

    hardening = compatibility["truth_gate_hardening"]

    for key in (
        "m56_verity",
        "m56_1_contract",
        "m56_2_bounded_regression",
        "m56_5_invocation_contract",
    ):
        if hardening[key]["status"] != "PASS":
            raise SystemExit(f"hardening compatibility drift: {key}")

    load_safety = payload["load_safety"]

    if load_safety["bounded_execution"] is not True:
        raise SystemExit("bounded_execution drift detected")

    if load_safety["single_shot"] is not True:
        raise SystemExit("single_shot drift detected")

    for key in (
        "background_worker",
        "recursive_invocation",
        "unbounded_audit_scan",
        "automatic_remediation",
    ):
        if load_safety[key] is not False:
            raise SystemExit(f"load safety drift detected: {key}")

    components = payload["component_statuses"]

    for name, status in components.items():
        if status["status"] != "PASS":
            raise SystemExit(f"component drift detected: {name}")
        if status["write"] is not False:
            raise SystemExit(f"component write drift detected: {name}")

    table_output = run(fmt="table").stdout

    if "governance-compatibility-snapshot" not in table_output:
        raise SystemExit("table output missing snapshot mode")

    if "invocation_tools: 8" not in table_output:
        raise SystemExit("table output missing invocation tool count")

    print("PASS: governance compatibility snapshot completed")


if __name__ == "__main__":
    main()
