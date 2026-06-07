#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERITY = ROOT / "tools" / "runes_shield" / "runes_verity.py"
VALIDATOR = ROOT / "tools" / "runes_shield" / "validate_runes_verity_contract.py"


def run_command(args, input_text=None):
    return subprocess.run(
        args,
        cwd=ROOT,
        input=input_text,
        capture_output=True,
        text=True,
        check=True,
    )


def main():
    print("== M56.1 Runes Verity Contract Smoke ==")

    verity_output = run_command(
        [sys.executable, str(VERITY), "--format", "json"]
    ).stdout

    payload = json.loads(verity_output)

    if payload["status"] != "PASS":
        raise SystemExit("live verity payload is not PASS")

    validator_output = run_command(
        [
            sys.executable,
            str(VALIDATOR),
            "--format",
            "json",
        ],
        input_text=verity_output,
    ).stdout

    result = json.loads(validator_output)

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result["contract_version"] != "m56.1-runes-verity-contract-v1":
        raise SystemExit("unexpected contract version")

    if result["status"] != "PASS":
        raise SystemExit("contract validation failed")

    if result["write"] is not False:
        raise SystemExit("contract validator must remain read-only")

    if result["issue_count"] != 0:
        raise SystemExit("contract validator must report zero issues")

    locked = result["locked_contract"]

    if locked["scale"] != "personal-local":
        raise SystemExit("scale contract drift detected")

    if locked["mode"] != "truth-gate-runtime-verification":
        raise SystemExit("mode contract drift detected")

    if "calamity_guard" not in locked["expected_checks"]:
        raise SystemExit("calamity_guard missing from locked contract")

    if locked["required_load_safety"]["background_worker"] is not False:
        raise SystemExit("background_worker contract drift detected")

    table_output = run_command(
        [
            sys.executable,
            str(VALIDATOR),
            "--run",
            "--format",
            "table",
        ]
    ).stdout

    if "status: PASS" not in table_output:
        raise SystemExit("table output missing PASS")

    print("PASS: Runes Verity contract validation completed")


if __name__ == "__main__":
    main()
