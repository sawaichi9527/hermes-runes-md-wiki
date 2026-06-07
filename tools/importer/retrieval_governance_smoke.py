#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BUG_ID_RETRIEVAL_GOVERNANCE_FIXTURE_GATE = "TB-M19810-RG001"


APPROVED_PATH = (
    "wiki/freelancer/forge-inbox/"
    "m18-4-p0-trial-write-forge-20260601-213005-75d858f8.md"
)

REJECTED_PATH = (
    "wiki/freelancer/forge-inbox/"
    "first-p0-governed-write-forge-20260601-212653-0e522ebc.md"
)


def workspace_slug() -> str:
    return (
        os.environ.get("HERMES_SMOKE_PROJECT")
        or os.environ.get("HERMES_PROJECT")
        or os.environ.get("HERMES_WORKSPACE_SLUG")
        or "freelancer"
    ).strip()


def fixture_skip(check_id: str, reason: str, data: dict | None = None) -> dict:
    return {
        "id": check_id,
        "status": "SKIP",
        "reason": reason,
        "bug_id": BUG_ID_RETRIEVAL_GOVERNANCE_FIXTURE_GATE,
        "data": data or {},
    }


def run_recall(query: str, path: str, project: str) -> dict:
    cmd = [
        str(ROOT / "bin" / "hermes-recall"),
        query,
        "--project",
        project,
        "--path",
        path,
        "--mode",
        "hybrid",
        "--limit",
        "5",
        "--json",
    ]

    proc = subprocess.run(
        cmd,
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if proc.returncode != 0:
        return {
            "status": "FAIL",
            "error": "recall command failed",
            "returncode": proc.returncode,
            "stderr": proc.stderr,
            "stdout": proc.stdout,
        }

    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        return {
            "status": "FAIL",
            "error": f"invalid json: {exc}",
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }


def check_approved(project: str) -> dict:
    data = run_recall(
        "M18.4 P0 trial run controlled forge write",
        APPROVED_PATH,
        project,
    )

    if data.get("status") != "pass":
        return {
            "id": "approved_recall_status",
            "status": "FAIL",
            "data": data,
        }

    results = data.get("results") or []

    if not results:
        return fixture_skip(
            "approved_forge_fixture_missing",
            "approved forge governance fixture is not present in this runtime workspace",
            {
                "project": project,
                "path": APPROVED_PATH,
                "query": "M18.4 P0 trial run controlled forge write",
            },
        )

    top = results[0]
    forge = top.get("forge") or {}

    checks = {
        "path_match": top.get("path") == APPROVED_PATH,
        "forge_is_forge": forge.get("is_forge") is True,
        "forge_status_approved": forge.get("status") == "approved",
        "trust_bias_present": isinstance(top.get("trust_bias"), int),
        "trust_policy_present": top.get("trust_policy")
        == "m19.2c-soft-bias-v1",
        "trust_bias_positive": top.get("trust_bias", 0) > 0,
    }

    return {
        "id": "approved_forge_trust_metadata",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "top": {
            "path": top.get("path"),
            "chunk_index": top.get("chunk_index"),
            "trust_bias": top.get("trust_bias"),
            "trust_policy": top.get("trust_policy"),
            "forge": forge,
        },
    }


def check_rejected_isolation(project: str) -> dict:
    data = run_recall(
        "First P0 governed write controlled forge write",
        REJECTED_PATH,
        project,
    )

    if data.get("status") != "pass":
        return {
            "id": "rejected_recall_status",
            "status": "FAIL",
            "data": data,
        }

    results = data.get("results") or []

    return {
        "id": "rejected_forge_isolation",
        "status": "PASS" if len(results) == 0 else "FAIL",
        "result_count": len(results),
        "results": [
            {
                "path": item.get("path"),
                "trust_bias": item.get("trust_bias"),
                "forge": item.get("forge"),
            }
            for item in results[:3]
        ],
    }


def main() -> int:
    project = workspace_slug()
    checks = [
        check_approved(project),
        check_rejected_isolation(project),
    ]

    if all(item.get("status") in {"PASS", "SKIP"} for item in checks) and any(
        item.get("status") == "SKIP" for item in checks
    ):
        result = {
            "suite": "M19.3 Retrieval Governance Regression Smoke",
            "status": "SKIP",
            "reason": "retrieval_governance_fixtures_not_available_in_runtime_workspace",
            "bug_id": BUG_ID_RETRIEVAL_GOVERNANCE_FIXTURE_GATE,
            "failed": 0,
            "total": len(checks),
            "project": project,
            "checks": checks,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    failed = [item for item in checks if item.get("status") != "PASS"]

    result = {
        "suite": "M19.3 Retrieval Governance Regression Smoke",
        "status": "PASS" if not failed else "FAIL",
        "failed": len(failed),
        "total": len(checks),
        "project": project,
        "checks": checks,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
