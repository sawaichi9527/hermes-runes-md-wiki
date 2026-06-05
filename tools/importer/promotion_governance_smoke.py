#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from observation_logger import write_observation

ROOT = Path(__file__).resolve().parents[2]
IMPORTER_DIR = ROOT / "tools" / "importer"
M94_TRIAL_FIXTURE_QUERY = "M94 trial promotion fixture real agent-proposed memory draft"


def workspace_slug() -> str:
    return (
        os.environ.get("HERMES_SMOKE_PROJECT")
        or os.environ.get("HERMES_PROJECT")
        or os.environ.get("HERMES_WORKSPACE_SLUG")
        or "k6-freelancer"
    ).strip()


def is_legacy_workspace() -> bool:
    return workspace_slug() in ("", "k6-freelancer")


def skip(reason: str, data: dict | None = None) -> dict:
    return {
        "id": "M20.4-SKIP",
        "status": "SKIP",
        "reason": reason,
        "data": data or {},
    }


def run_recall(query: str, project: str = "k6-freelancer", limit: int = 5) -> dict:
    cmd = [
        sys.executable,
        "hybrid_search.py",
        query,
        "--project",
        project,
        "--limit",
        str(limit),
        "--json",
    ]

    proc = subprocess.run(
        cmd,
        cwd=IMPORTER_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if proc.returncode != 0:
        return {
            "status": "FAIL",
            "error": "recall-command-failed",
            "query": query,
            "returncode": proc.returncode,
            "stderr": proc.stderr[-1200:],
            "stdout": proc.stdout[-1200:],
        }

    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        return {
            "status": "FAIL",
            "error": "invalid-json",
            "query": query,
            "exception": str(exc),
            "stdout": proc.stdout[-1200:],
            "stderr": proc.stderr[-1200:],
        }


def fail(case_id: str, reason: str, data: dict | None = None) -> dict:
    return {
        "id": case_id,
        "status": "FAIL",
        "reason": reason,
        "data": data or {},
    }


def passed(case_id: str, summary: str, data: dict | None = None) -> dict:
    return {
        "id": case_id,
        "status": "PASS",
        "summary": summary,
        "data": data or {},
    }


def first_result(data: dict) -> dict:
    results = data.get("results") or []
    return results[0] if results else {}


def forge_matches_reviewed_agent_memory(forge: dict) -> bool:
    return (
        forge.get("status") == "approved"
        and forge.get("trust_class") in {"reviewed", "human-reviewed"}
        and forge.get("proposal_type") == "agent_memory"
    )


def case_approved_agent_proposal_retrievable() -> dict:
    query = "real agent-proposed memory draft"
    data = run_recall(query)
    results = data.get("results") or []

    if not results:
        return fail("M20.4-A", "approved proposal was not retrieved", data)

    top = results[0]
    forge = top.get("forge") or {}

    expected = {
        "status": "approved",
        "trust_class": "reviewed",
        "proposal_type": "agent_memory",
    }

    for key, value in expected.items():
        if forge.get(key) != value:
            return fail(
                "M20.4-A",
                f"top result forge metadata mismatch: {key}",
                {"expected": value, "actual": forge.get(key), "top": top},
            )

    return passed(
        "M20.4-A",
        "approved reviewed agent proposal is retrieval-visible",
        {
            "path": top.get("path"),
            "trust_bias": top.get("trust_bias"),
            "forge": forge,
        },
    )


def case_trusted_telegram_ordering() -> dict:
    query = "Telegram integration"
    data = run_recall(query)
    top = first_result(data)

    if not top:
        return fail("M20.4-B", "no retrieval results for trusted wiki query", data)

    path = top.get("path", "")
    forge = top.get("forge") or {}

    if path != "wiki/k6-freelancer/services.md":
        return fail(
            "M20.4-B",
            "trusted Telegram wiki content did not rank first",
            {"top_path": path, "top": top},
        )

    if forge:
        return fail(
            "M20.4-B",
            "forge proposal unexpectedly ranked before trusted wiki content",
            {"top": top},
        )

    return passed(
        "M20.4-B",
        "trusted wiki content still outranks reviewed proposal",
        {
            "top_path": path,
            "section_heading": top.get("section_heading"),
            "trust_bias": top.get("trust_bias"),
        },
    )


def case_trial_promotion_fixture_retrievable(workspace: str) -> dict:
    data = run_recall(M94_TRIAL_FIXTURE_QUERY, project=workspace, limit=5)
    results = data.get("results") or []

    if not results:
        return skip(
            "promotion_governance_fixture_not_available_in_trial_workspace",
            {
                "profile": f"workspace-{workspace}",
                "workspace": workspace,
                "query": M94_TRIAL_FIXTURE_QUERY,
                "note": "Fresh trial workspace has no approved forge/proposal fixture imported yet.",
            },
        )

    expected_prefix = f"wiki/{workspace}/forge-inbox/"

    for item in results:
        path = item.get("path", "")
        forge = item.get("forge") or {}
        content = item.get("content") or ""

        if (
            path.startswith(expected_prefix)
            and forge_matches_reviewed_agent_memory(forge)
            and "M94 trial promotion fixture" in content
        ):
            return passed(
                "M20.4-TRIAL-A",
                "approved reviewed trial promotion fixture is retrieval-visible",
                {
                    "path": path,
                    "workspace": workspace,
                    "trust_bias": item.get("trust_bias"),
                    "forge": forge,
                },
            )

    return fail(
        "M20.4-TRIAL-A",
        "trial promotion fixture retrieval result did not match approved reviewed forge metadata",
        {
            "workspace": workspace,
            "expected_path_prefix": expected_prefix,
            "query": M94_TRIAL_FIXTURE_QUERY,
            "results": results,
        },
    )


def nonlegacy_workspace_cases(workspace: str) -> list[dict]:
    return [
        case_trial_promotion_fixture_retrievable(workspace),
    ]


def main() -> int:
    if not is_legacy_workspace():
        workspace = workspace_slug()
        cases = nonlegacy_workspace_cases(workspace)

        if all(c.get("status") == "SKIP" for c in cases):
            out = {
                "suite": "M20.4 Promotion Governance Smoke",
                "profile": f"workspace-{workspace}",
                "status": "SKIP",
                "failed": 0,
                "total": len(cases),
                "results": cases,
            }

            write_observation(
                {
                    "event": "promotion_governance_smoke",
                    "milestone": "M94",
                    "suite": out["suite"],
                    "status": out["status"],
                    "failed": out["failed"],
                    "total": out["total"],
                    "workspace": workspace,
                    "skip_reason": cases[0].get("reason"),
                    "trust_policy": "m20.5-personal-governance-v1",
                }
            )

            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 0

        failed = [c for c in cases if c["status"] != "PASS"]

        out = {
            "suite": "M20.4 Promotion Governance Smoke",
            "profile": f"workspace-{workspace}",
            "status": "FAIL" if failed else "PASS",
            "failed": len(failed),
            "total": len(cases),
            "results": cases,
        }

        case_a = next((c for c in cases if c.get("id") == "M20.4-TRIAL-A"), {})
        case_a_data = case_a.get("data") or {}
        forge = case_a_data.get("forge") or {}

        write_observation(
            {
                "event": "promotion_governance_smoke",
                "milestone": "M94",
                "suite": out["suite"],
                "status": out["status"],
                "failed": out["failed"],
                "total": out["total"],
                "workspace": workspace,
                "reviewed_proposal_visible": case_a.get("status") == "PASS",
                "reviewed_trust_bias": case_a_data.get("trust_bias"),
                "reviewed_proposal_path": case_a_data.get("path"),
                "trust_policy": forge.get("trust_policy") or "m20.5-personal-governance-v1",
            }
        )

        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 1 if failed else 0

    cases = [
        case_approved_agent_proposal_retrievable(),
        case_trusted_telegram_ordering(),
    ]

    failed = [c for c in cases if c["status"] != "PASS"]

    out = {
        "suite": "M20.4 Promotion Governance Smoke",
        "profile": "legacy-k6-freelancer",
        "status": "FAIL" if failed else "PASS",
        "failed": len(failed),
        "total": len(cases),
        "results": cases,
    }

    case_a = next((c for c in cases if c.get("id") == "M20.4-A"), {})
    case_b = next((c for c in cases if c.get("id") == "M20.4-B"), {})

    case_a_data = case_a.get("data") or {}
    case_b_data = case_b.get("data") or {}
    forge = case_a_data.get("forge") or {}

    write_observation(
        {
            "event": "promotion_governance_smoke",
            "milestone": "M20.6a",
            "suite": out["suite"],
            "status": out["status"],
            "failed": out["failed"],
            "total": out["total"],
            "reviewed_proposal_visible": case_a.get("status") == "PASS",
            "reviewed_trust_bias": case_a_data.get("trust_bias"),
            "trusted_wiki_outranks_reviewed": case_b.get("status") == "PASS",
            "trusted_top_path": case_b_data.get("top_path"),
            "reviewed_proposal_path": case_a_data.get("path"),
            "trust_policy": forge.get("trust_policy") or "m20.5-personal-governance-v1",
        }
    )

    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
