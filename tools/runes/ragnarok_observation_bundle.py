#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT_ROOT = ROOT / "bundles/ragnarok-observation"


def run_cmd(args: list[str]) -> dict[str, Any]:
    proc = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return {
        "cmd": args,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def safe_copy(src: Path, dst: Path) -> None:
    if not src.is_file():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def collect_git(bundle: Path) -> None:
    git_dir = bundle / "repository-state"

    for name, cmd in {
        "status-short.txt": ["git", "status", "--short"],
        "status-branch.txt": ["git", "status", "--short", "--branch"],
        "log-oneline-20.txt": ["git", "log", "--oneline", "-20"],
        "tracked-files.txt": ["git", "ls-files"],
        "ignored-local-evidence.txt": ["git", "status", "--ignored", "--short", "operations", "logs", "bundles"],
    }.items():
        result = run_cmd(cmd)
        write_text(git_dir / name, result["stdout"] if result["stdout"] else result["stderr"])

    head = run_cmd(["git", "rev-parse", "HEAD"])
    branch = run_cmd(["git", "branch", "--show-current"])
    write_json(
        git_dir / "repository-summary.json",
        {
            "head": head["stdout"].strip(),
            "branch": branch["stdout"].strip(),
            "git_available": head["returncode"] == 0,
        },
    )


def collect_smoke_inventory(bundle: Path) -> None:
    smoke_dir = ROOT / "smoke"
    items = []
    if smoke_dir.is_dir():
        for p in sorted(smoke_dir.glob("*.sh")):
            st = p.stat()
            items.append(
                {
                    "path": p.relative_to(ROOT).as_posix(),
                    "size_bytes": st.st_size,
                    "executable": os.access(p, os.X_OK),
                }
            )
    write_json(bundle / "smoke-verification" / "smoke-script-inventory.json", items)

    known_smokes = [
        "dev/smoke/m31_7_final_verification_lock.sh",
        "dev/smoke/m32_7_p0_trial_run_lock.sh",
        "dev/smoke/m33_0_runes_markdown_source_health_concept_smoke.sh",
        "dev/smoke/m33_1_ragnarok_observation_bundle_policy_smoke.sh",
        "dev/smoke/m33_2b_markdown_source_granularity_audit_smoke.sh",
        "dev/smoke/m33_3_forge_readiness_check_smoke.sh",
        "dev/smoke/m33_4_growth_aware_forge_proposal_trial_smoke.sh",
        "dev/smoke/m33_5_ragnarok_observation_evidence_inventory_smoke.sh",
    ]
    write_json(
        bundle / "smoke-verification" / "known-lock-smokes.json",
        [{"path": s, "exists": (ROOT / s).is_file()} for s in known_smokes],
    )


def collect_reports(bundle: Path) -> None:
    reports_dir = ROOT / "reports"
    report_inventory = []
    if reports_dir.is_dir():
        for p in sorted(reports_dir.rglob("*")):
            if p.is_file():
                report_inventory.append(
                    {
                        "path": p.relative_to(ROOT).as_posix(),
                        "size_bytes": p.stat().st_size,
                    }
                )
    write_json(bundle / "reports" / "reports-inventory.json", report_inventory)

    # Selected curated report copies. These are already non-secret governance reports.
    selected = [
        "reports/m33-markdown-source-health/latest.json",
        "reports/m33-markdown-source-health/latest.md",
    ]
    for rel in selected:
        src = ROOT / rel
        if src.is_file():
            safe_copy(src, bundle / rel)


def collect_operations_summary(bundle: Path) -> None:
    operations_dir = ROOT / "operations"
    summary: dict[str, Any] = {
        "operations_dir_exists": operations_dir.is_dir(),
        "total_json_files": 0,
        "by_operation_type": {},
        "status_counts": {},
        "returncode_counts": {},
        "write_counts": {},
        "risk_counts": {},
        "parse_errors": 0,
        "note": "metadata summary only; raw operations logs are not copied",
    }

    by_type: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    returncode_counts: Counter[str] = Counter()
    write_counts: Counter[str] = Counter()
    risk_counts: Counter[str] = Counter()

    if operations_dir.is_dir():
        for p in sorted(operations_dir.rglob("*.json")):
            summary["total_json_files"] += 1
            op_type = p.parent.name
            by_type[op_type] += 1
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                summary["parse_errors"] += 1
                continue

            status_counts[str(data.get("status", "unknown"))] += 1
            returncode_counts[str(data.get("returncode", "unknown"))] += 1
            write_counts[str(data.get("write", "unknown"))] += 1
            risk_counts[str(data.get("risk", "unknown"))] += 1

    summary["by_operation_type"] = dict(by_type)
    summary["status_counts"] = dict(status_counts)
    summary["returncode_counts"] = dict(returncode_counts)
    summary["write_counts"] = dict(write_counts)
    summary["risk_counts"] = dict(risk_counts)

    write_json(bundle / "operations-summary" / "operations-summary.json", summary)


def collect_observation_summary(bundle: Path) -> None:
    logs_dir = ROOT / "logs/observations"
    summary: dict[str, Any] = {
        "observations_dir_exists": logs_dir.is_dir(),
        "jsonl_files": 0,
        "records_total": 0,
        "records_valid": 0,
        "parse_errors": 0,
        "event_counts": {},
        "status_counts": {},
        "selected_model_profile_counts": {},
        "note": "summary only; raw full prompts, answers, and context are not copied",
    }

    event_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    model_counts: Counter[str] = Counter()

    if logs_dir.is_dir():
        for p in sorted(logs_dir.rglob("*.jsonl")):
            summary["jsonl_files"] += 1
            for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
                if not line.strip():
                    continue
                summary["records_total"] += 1
                try:
                    data = json.loads(line)
                except Exception:
                    summary["parse_errors"] += 1
                    continue
                summary["records_valid"] += 1
                event_counts[str(data.get("event", "answer_observation"))] += 1
                status_counts[str(data.get("status", "unknown"))] += 1
                profile = data.get("selected_model_profile")
                if profile:
                    model_counts[str(profile)] += 1

    summary["event_counts"] = dict(event_counts)
    summary["status_counts"] = dict(status_counts)
    summary["selected_model_profile_counts"] = dict(model_counts)

    write_json(bundle / "observation-summary" / "observation-summary.json", summary)


def collect_tool_inventory(bundle: Path) -> None:
    runes_dir = ROOT / "tools/runes"
    tools = []
    if runes_dir.is_dir():
        for p in sorted(runes_dir.glob("*.py")):
            tools.append(
                {
                    "path": p.relative_to(ROOT).as_posix(),
                    "size_bytes": p.stat().st_size,
                    "executable": os.access(p, os.X_OK),
                }
            )

    write_json(
        bundle / "tool-runtime-inventory" / "tool-runtime-inventory.json",
        {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "tools_runes": tools,
        },
    )


def collect_bundle_metadata(bundle: Path, bundle_id: str) -> None:
    write_json(
        bundle / "bundle-metadata.json",
        {
            "schema": "m33_ragnarok_observation_bundle_mvp_v1",
            "bundle_id": bundle_id,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "profile": "ragnarok-observation-mvp",
            "output_path": bundle.relative_to(ROOT).as_posix(),
            "included_categories": [
                "repository_state",
                "smoke_verification_inventory",
                "operations_metadata_summary",
                "observation_summary",
                "reports_inventory_and_selected_reports",
                "markdown_source_health_reports",
                "tool_runtime_inventory",
                "bundle_metadata",
            ],
            "excluded_by_policy": [
                ".env",
                "API keys",
                "PostgreSQL passwords",
                "Telegram bot tokens",
                "raw full prompts",
                "raw full answers",
                "raw full memory context",
                "database dumps",
                "vector embeddings",
                "shell history",
                "unrestricted raw logs",
            ],
            "local_only": True,
            "secret_exclusion_required": True,
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate local-only Ragnarok observation bundle MVP.")
    parser.add_argument("--out-root", default=str(DEFAULT_OUT_ROOT))
    parser.add_argument("--bundle-id", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    bundle_id = args.bundle_id or timestamp
    out_root = Path(args.out_root)
    if not out_root.is_absolute():
        out_root = ROOT / out_root

    bundle = out_root / bundle_id
    bundle.mkdir(parents=True, exist_ok=True)

    collect_bundle_metadata(bundle, bundle_id)
    collect_git(bundle)
    collect_smoke_inventory(bundle)
    collect_reports(bundle)
    collect_operations_summary(bundle)
    collect_observation_summary(bundle)
    collect_tool_inventory(bundle)

    result = {
        "status": "PASS",
        "bundle_id": bundle_id,
        "path": bundle.relative_to(ROOT).as_posix() if bundle.is_relative_to(ROOT) else str(bundle),
        "local_only": True,
        "profile": "ragnarok-observation-mvp",
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"PASS Ragnarok Observation Bundle MVP: {result['path']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
