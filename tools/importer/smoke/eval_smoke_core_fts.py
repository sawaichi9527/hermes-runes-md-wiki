#!/usr/bin/env python3
import json
import os
import subprocess
from pathlib import Path


IMPORTER = Path(__file__).resolve().parents[1]
ROOT = IMPORTER.parents[1]


def workspace_config() -> tuple[str, str, str, str]:
    project = (
        os.environ.get("HERMES_SMOKE_PROJECT")
        or os.environ.get("HERMES_PROJECT")
        or os.environ.get("HERMES_WORKSPACE_SLUG")
        or "freelancer"
    )
    path = os.environ.get("HERMES_SMOKE_PATH") or f"wiki/{project}"
    query = os.environ.get("HERMES_SMOKE_QUERY") or "forge inbox boundary"
    expected_prefix = os.environ.get("HERMES_SMOKE_EXPECTED_PREFIX") or f"wiki/{project}/"

    return project, path, query, expected_prefix


def run_fts_recall():
    project, path, query, expected_prefix = workspace_config()
    cmd = [
        str(ROOT / "bin/hermes-recall"),
        query,
        "--project",
        project,
        "--mode",
        "fts",
        "--path",
        path,
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

    test_name = f"{project}_fts_recall"

    if proc.returncode != 0:
        return {
            "name": test_name,
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
    if not any(path.startswith(expected_prefix) for path in paths):
        failures.append("missing_expected_project_result")

    return {
        "name": test_name,
        "status": "PASS" if not failures else "FAIL",
        "project": project,
        "path": path,
        "query": query,
        "expected_prefix": expected_prefix,
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
