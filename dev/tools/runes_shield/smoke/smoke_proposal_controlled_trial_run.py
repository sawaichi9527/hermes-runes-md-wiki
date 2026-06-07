#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRIAL_RUN_CLI = ROOT / "tools" / "runes_shield" / "proposal_controlled_trial_run.py"

EXPECTED_EFFECT_KEYS = {
    "trusted_wiki_write",
    "markdown_mutation",
    "index_update",
    "automatic_apply",
    "automatic_promotion",
    "database_mutation",
}


def run(cmd, *args):
    return subprocess.run(
        [sys.executable, str(cmd), *args],
        capture_output=True,
        text=True,
        check=True,
    )


def main():
    print("== M50 Controlled Trial-run Smoke ==")

    result = run(TRIAL_RUN_CLI, "--profile", "p0", "--format", "json")

    payload = json.loads(result.stdout)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if payload["status"] != "PASS":
        raise SystemExit("controlled trial-run validation failed")

    if payload["integrity_status"] != "PASS":
        raise SystemExit("controlled trial-run requires integrity PASS")

    if payload["integrity_issue_count"] != 0:
        raise SystemExit("controlled trial-run requires zero integrity issues")

    if payload["write"] is not False:
        raise SystemExit("controlled trial-run must remain read-only")

    effects = payload["effects"]

    if set(effects) != EXPECTED_EFFECT_KEYS:
        raise SystemExit("unexpected controlled trial-run effect coverage")

    if any(value is not False for value in effects.values()):
        raise SystemExit("controlled trial-run effects must remain disabled")

    blocked_count = payload["execution_status_counts"].get("BLOCKED", 0)

    if blocked_count != payload["proposal_count"]:
        raise SystemExit("all apply execution requests must remain BLOCKED")

    if not payload["observations"]:
        raise SystemExit("expected controlled trial-run observations")

    for observation in payload["observations"]:
        if observation["write"] is not False:
            raise SystemExit("observation write flag must remain false")

        if observation["execution_status"] != "BLOCKED":
            raise SystemExit("observation execution status must remain BLOCKED")

    print("PASS: controlled trial-run governance validation completed")


if __name__ == "__main__":
    main()
