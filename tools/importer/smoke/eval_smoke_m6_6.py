#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path.home() / "workspace/hermes-memory"
IMPORTER = ROOT / "tools/importer"

CASES = [
    {
        "name": "M6.1 sync entrypoint exists",
        "cmd": [
            "bash",
            "-lc",
            "command -v hermes-memory-sync || test -x ~/workspace/hermes-memory/bin/hermes-memory-sync",
        ],
        "expect_returncode": 0,
    },
    {
        "name": "M6.2 deletion handling safe not_found",
        "cmd": [
            "bash",
            "-lc",
            "python delete_source.py "
            "--project k6-freelancer "
            "--path __m6_2_delete_probe_not_exist__.md "
            "--json",
        ],
        "expect_returncode": 0,
        "expect_contains": [
            "\"status\": \"not_found\"",
            "\"documents_path\": \"source_path\"",
            "\"deleted_documents\": 0",
            "\"deleted_chunks\": 0",
        ],
    },
    {
        "name": "M6.3 security policy documented",
        "cmd": [
            "bash",
            "-lc",
            "grep -RIn "
            "--exclude-dir=.venv "
            "--exclude-dir=__pycache__ "
            "--exclude-dir=.pytest_cache "
            "'Real secrets must never\\|PostgreSQL database read/write passwords\\|Telegram bot tokens\\|API keys' "
            "~/workspace/hermes-memory/wiki/k6-freelancer "
            "| head -20",
        ],
        "expect_returncode": 0,
    },
    {
        "name": "M6.4 metadata filtering returns project scoped result",
        "cmd": [
            "bash",
            "-lc",
            "hermes-recall 'Telegram integration' "
            "--mode hybrid "
            "--project k6-freelancer "
            "--path services.md "
            "--limit 3 "
            "--json",
        ],
        "expect_returncode": 0,
        "expect_contains": ["k6-freelancer", "services.md"],
    },
    {
        "name": "M6.5 citation formatting answer contains source citation",
        "cmd": [
            "bash",
            "-lc",
            "python answer_generator.py "
            "'Telegram integration 是什麼？' "
            "--project k6-freelancer "
            "--path services.md "
            "--heading Telegram "
            "--max-tokens 512 "
            "--json",
        ],
        "expect_returncode": 0,
        "expect_contains": ["[Source 1]"],
    },
]


def run_case(case):
    proc = subprocess.run(
        case["cmd"],
        cwd=IMPORTER,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    combined = (proc.stdout or "") + "\n" + (proc.stderr or "")

    ok = proc.returncode == case.get("expect_returncode", 0)

    for needle in case.get("expect_contains", []):
        if needle not in combined:
            ok = False

    return {
        "name": case["name"],
        "status": "PASS" if ok else "FAIL",
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-1200:],
        "stderr_tail": proc.stderr[-1200:],
    }


def main():
    results = [run_case(case) for case in CASES]
    failed = sum(1 for r in results if r["status"] != "PASS")

    report = {
        "suite": "Phase3 M6.6 Expanded Evaluation",
        "status": "PASS" if failed == 0 else "FAIL",
        "failed": failed,
        "total": len(results),
        "results": results,
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
