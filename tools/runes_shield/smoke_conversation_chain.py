#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "tools" / "runes_shield"

SMOKES = [
    ("observe_handler", "smoke_observe_handler.py"),
    ("formatter", "smoke_formatter.py"),
    ("integration", "smoke_integration.py"),
    ("conversation_adapter", "smoke_conversation_adapter.py"),
    ("response_renderer", "smoke_response_renderer.py"),
    ("boundary_regression", "smoke_boundary_regression.py"),
]


def run_smoke(name, script):
    path = TOOL_DIR / script
    proc = subprocess.run(
        [sys.executable, str(path)],
        cwd=str(TOOL_DIR),
        text=True,
        capture_output=True,
        check=False,
    )

    stdout_lines = proc.stdout.strip().splitlines()
    stderr_lines = proc.stderr.strip().splitlines()

    return {
        "name": name,
        "path": str(path.relative_to(ROOT)),
        "returncode": proc.returncode,
        "stdout_tail": stdout_lines[-8:],
        "stderr_tail": stderr_lines[-8:],
        "status": "PASS" if proc.returncode == 0 else "FAIL",
    }


def main():
    print("== M36.5 Conversation Chain Regression Smoke ==")

    results = []
    failed = 0

    for name, script in SMOKES:
        result = run_smoke(name, script)
        results.append(result)
        print(json.dumps(result, indent=2, ensure_ascii=False))

        if result["status"] != "PASS":
            failed += 1

    summary = {
        "suite": "M36.5 Conversation Chain Regression Smoke",
        "status": "PASS" if failed == 0 else "FAIL",
        "total": len(results),
        "failed": failed,
        "checked": [name for name, _ in SMOKES],
        "runtime_chain": [
            "conversation_adapter",
            "integration_runtime",
            "dispatcher",
            "observe_or_confirm_or_none",
            "formatter",
            "response_renderer",
        ],
        "boundary": {
            "write": False,
            "autonomous_apply": False,
            "hidden_escalation": False,
            "trusted_memory_mutation": False,
        },
    }

    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if failed:
        raise SystemExit(1)

    print("PASS: conversation chain regression completed")


if __name__ == "__main__":
    main()
