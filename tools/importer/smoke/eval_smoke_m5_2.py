#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]


LEGACY_TESTS = [
    {
        "name": "telegram_context_recall",
        "query": "Telegram integration",
        "project": "k6-freelancer",
        "min_rerank_score": "8",
        "must_contain": [
            "# 4. Telegram Integration",
            "Telegram ingress channel",
            "Long polling",
            "not a memory backend",
        ],
        "must_not_contain": [
            "# 5. PostgreSQL Memory",
            "# 6. PostgreSQL FTS",
        ],
    },
    {
        "name": "secret_policy_recall",
        "query": "secret handling PostgreSQL password API key",
        "project": "k6-freelancer",
        "min_rerank_score": "1",
        "must_contain": [
            "# Secret Handling Rule",
            "PostgreSQL database read/write passwords",
            "LM Studio / OpenAI-compatible API keys",
            "Telegram bot tokens",
            "tools/importer/.env",
        ],
        "must_not_contain": [
            "OPENAI_API_KEY=sk-",
            "PGPASSWORD=change-this",
        ],
    },
    {
        "name": "phase3_m5_baseline_recall",
        "query": "M9.7 governed output baseline",
        "project": "k6-freelancer",
        "min_rerank_score": "1",
        "must_contain": [
            "V-012",
            "Governed Output Baseline",
            "PASS / FROZEN",
            "Response Sanitization",
        ],
        "must_not_contain": [
            "OPENAI_API_KEY=sk-",
            "PGPASSWORD=change-this",
        ],
    },
]


def workspace_slug() -> str:
    return (
        os.environ.get("HERMES_SMOKE_PROJECT")
        or os.environ.get("HERMES_PROJECT")
        or os.environ.get("HERMES_WORKSPACE_SLUG")
        or "k6-freelancer"
    ).strip()


def active_tests():
    workspace = workspace_slug()

    if workspace in ("", "k6-freelancer"):
        return "legacy-k6-freelancer", LEGACY_TESTS

    return f"workspace-{workspace}", [
        {
            "name": f"{workspace}_baseline_context_recall",
            "query": "Trial-run Workspace Baseline",
            "project": workspace,
            "min_rerank_score": "1",
            "must_contain": [
                "Trial-run Workspace Baseline",
                "ACTIVE / TRIAL-RUN",
                "fresh-user trial-run memory namespace",
            ],
            "must_not_contain": [
                "OPENAI_API_KEY=sk-",
                "PGPASSWORD=change-this",
            ],
        },
        {
            "name": "owner_runes_context_recall",
            "query": "owner preferences personal operating data",
            "project": "owner-runes",
            "min_rerank_score": "1",
            "must_contain": [
                "Owner Runes",
                "durable owner preferences",
                "agent-agnostic",
                "must not contain secrets",
            ],
            "must_not_contain": [
                "OPENAI_API_KEY=sk-",
                "PGPASSWORD=change-this",
            ],
        },
        {
            "name": "root_index_context_recall",
            "query": "Hermes Runes index memory wiki",
            "project": "default",
            "min_rerank_score": "1",
            "must_contain": [
                "Hermes",
                "Runes",
            ],
            "must_not_contain": [
                "OPENAI_API_KEY=sk-",
                "PGPASSWORD=change-this",
            ],
        },
    ]


def run_context_builder(test):
    cmd = [
        sys.executable,
        str(BASE_DIR / "context_builder.py"),
        test["query"],
        "--project",
        test["project"],
        "--limit",
        "5",
        "--max-chars",
        "8000",
        "--min-rerank-score",
        test["min_rerank_score"],
        "--json",
    ]

    proc = subprocess.run(
        cmd,
        cwd=str(BASE_DIR),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if proc.returncode != 0:
        return {
            "ok": False,
            "error": "context_builder_failed",
            "stderr": proc.stderr,
            "stdout": proc.stdout,
        }

    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {
            "ok": False,
            "error": "invalid_json",
            "stderr": proc.stderr,
            "stdout": proc.stdout,
        }

    return {
        "ok": True,
        "payload": payload,
    }


def evaluate(test, payload):
    context = payload.get("context", "")
    debug = payload.get("debug", {})

    failures = []

    if debug.get("selected_chunks", 0) < 1:
        failures.append("selected_chunks < 1")

    for item in test["must_contain"]:
        if item not in context:
            failures.append(f"missing required text: {item}")

    for item in test["must_not_contain"]:
        if item in context:
            failures.append(f"forbidden text found: {item}")

    return failures


def main():
    profile, tests = active_tests()
    all_results = []
    failed = 0

    for test in tests:
        result = run_context_builder(test)

        if not result["ok"]:
            failed += 1
            all_results.append({
                "name": test["name"],
                "status": "FAIL",
                "error": result,
            })
            continue

        payload = result["payload"]
        failures = evaluate(test, payload)

        if failures:
            failed += 1
            status = "FAIL"
        else:
            status = "PASS"

        all_results.append({
            "name": test["name"],
            "status": status,
            "query": test["query"],
            "project": test["project"],
            "debug": payload.get("debug", {}),
            "failures": failures,
        })

    print(json.dumps({
        "suite": "M5.2 Evaluation Smoke Test",
        "profile": profile,
        "status": "PASS" if failed == 0 else "FAIL",
        "failed": failed,
        "total": len(tests),
        "results": all_results,
    }, ensure_ascii=False, indent=2))

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
