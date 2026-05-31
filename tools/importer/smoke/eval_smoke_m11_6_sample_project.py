#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path


IMPORTER_PARENT = Path(__file__).resolve().parents[1]
if str(IMPORTER_PARENT) not in sys.path:
    sys.path.insert(0, str(IMPORTER_PARENT))

from root_resolver import resolve_importer_dir


IMPORTER = resolve_importer_dir()


CASES = [
    {
        "name": "sample_markdown_source_of_truth",
        "query": "Markdown source-of-truth",
        "project": "sample-project",
        "path": "wiki/sample-project/decisions.md",
        "must_contain": [
            "D-001: Use Markdown as Source-of-Truth",
            "durable human-readable source-of-truth",
            "database as an index and retrieval backend",
        ],
    },
    {
        "name": "sample_secret_policy",
        "query": "secrets API keys passwords",
        "project": "sample-project",
        "path": "wiki/sample-project/decisions.md",
        "must_contain": [
            "D-002: Keep Secrets Out of Markdown",
            "Do not store real API keys",
            "Secrets must remain in local `.env` files",
        ],
    },
]


def run_case(case):
    cmd = [
        sys.executable,
        "context_builder.py",
        case["query"],
        "--project",
        case["project"],
        "--path",
        case["path"],
        "--min-rerank-score",
        "1",
        "--json",
    ]

    try:
        proc = subprocess.run(
            cmd,
            cwd=IMPORTER,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=180,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "name": case["name"],
            "status": "FAIL",
            "failures": ["context_builder_timeout"],
            "stderr_tail": str(exc)[-2000:],
        }

    if proc.returncode != 0:
        return {
            "name": case["name"],
            "status": "FAIL",
            "failures": ["context_builder_failed"],
            "stderr_tail": proc.stderr[-2000:],
        }

    data = json.loads(proc.stdout)
    context = data.get("context", "")

    failures = []
    for text in case["must_contain"]:
        if text not in context:
            failures.append(f"missing required text: {text}")

    return {
        "name": case["name"],
        "status": "PASS" if not failures else "FAIL",
        "query": case["query"],
        "project": case["project"],
        "path": case["path"],
        "failures": failures,
        "debug": data.get("debug", {}),
    }


def main():
    results = [run_case(c) for c in CASES]
    failed = sum(1 for r in results if r["status"] != "PASS")

    output = {
        "suite": "M11.6 Sample Project Smoke Test",
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
