#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path


IMPORTER = Path(__file__).resolve().parents[1]
ROOT = IMPORTER.parents[1]


def run_fts_recall():
    cmd = [
        str(ROOT / "bin/hermes-recall"),
        "sample project",
        "--project",
        "sample-project",
        "--mode",
        "fts",
        "--limit",
        "5",
        "--json",
    ]

    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
    )

    if proc.returncode != 0:
        return {
            "name": "sample_project_fts_recall",
            "status": "FAIL",
            "error": "fts_recall_failed",
            "stderr_tail": proc.stderr[-2000:],
            "stdout_tail": proc.stdout[-2000:],
        }

    data = json.loads(proc.stdout)
    results = data.get("results", [])
    paths = [item.get("path", "") for item in results]

    failures = []
    if data.get("status") != "pass":
        failures.append("status_not_pass")
    if not results:
        failures.append("no_results")
    if not any(path.startswith("wiki/sample-project/") for path in paths):
        failures.append("missing_sample_project_result")

    return {
        "name": "sample_project_fts_recall",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "result_count": len(results),
        "paths": paths,
    }


def main():
    results = [run_fts_recall()]
    failed = sum(1 for item in results if item["status"] != "PASS")
    output = {
        "suite": "Core FTS Smoke Test",
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
