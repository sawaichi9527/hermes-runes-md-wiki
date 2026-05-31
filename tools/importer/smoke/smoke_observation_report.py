#!/usr/bin/env python3
"""
M8.3c Observation Report Layer smoke test.

Uses a temporary observation dir with synthetic JSONL records to avoid depending on live LLM.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path


def run_cmd(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(
        cmd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.returncode, proc.stdout


def write_record(path: Path, idx: int, *, sanitized: bool, structured: bool, marker: str, strategy: str) -> None:
    record = {
        "schema_version": "m8.3a-observation-v1",
        "trace_id": f"smoke-{idx}",
        "timestamp": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "duration_ms": 1000 + idx,
        "phase": "M8.3a",
        "project": "k6-freelancer",
        "query": {"hash": f"sha256:query-{idx}", "length": 32},
        "model": {
            "name": "Qwen3.6-35B-A3B",
            "profile": "qwen-forced-thinking",
            "base_url_hash": "sha256:base",
            "base_url_label": "local-or-lan",
            "disable_thinking_requested": False,
        },
        "context": {
            "phase": "M8.1d",
            "used_count": 4,
            "recovered_count": 1,
            "total_truncated": False,
            "max_chunks": 4,
            "max_context_chars": 7000,
            "source_refs": [
                "wiki/k6-freelancer/verification.md#v-20260531-m8-3a-default-on-jsonl-observation-logger:chunk-1"
            ],
            "source_paths": ["wiki/k6-freelancer/verification.md"],
        },
        "generation": {
            "status": "pass",
            "review_status": "auto_pass_with_warning" if sanitized else "auto_pass",
            "structured_output_valid": structured,
            "structured_mode_requested": False,
            "structured_mode_provider_enforced": False,
            "extraction_strategy": "json_embedded_object" if structured else "answer_marker",
            "memory_sufficiency": "sufficient",
            "citations_count": 2,
        },
        "sanitizer": {
            "mode": "auto",
            "sanitized": sanitized,
            "strategy": strategy,
            "confidence": "high" if sanitized else "none",
            "cut_position": 400 if sanitized else None,
            "removed_chars": 80 if sanitized else 0,
            "removed_ratio": 0.1 if sanitized else 0,
            "warnings": ["tail_meta_generation_removed"] if sanitized else [],
        },
        "content_metrics": {
            "raw_text_length": 1200,
            "answer_length": 420,
            "raw_preview_hash": "sha256:raw",
            "answer_preview_hash": "sha256:answer",
            "has_reasoning_markers_raw": bool(marker),
            "has_reasoning_markers_answer": False,
            "detected_markers": [marker] if marker else [],
        },
        "usage": {
            "prompt_tokens": 2000,
            "completion_tokens": 512,
            "reasoning_tokens": 500,
            "total_tokens": 2512,
        },
        "runtime": {"error": None},
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    hermes_observe = shutil.which("hermes-observe")
    if not hermes_observe:
        print("FAIL: hermes-observe not found", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory(prefix="hermes-report-smoke-") as tmp:
        observe_dir = Path(tmp) / "observations"
        log_path = observe_dir / "answer-runs" / "2026-05" / "20260531.jsonl"
        log_path.parent.mkdir(parents=True, exist_ok=True)

        write_record(log_path, 1, sanitized=True, structured=False, marker="Ready.", strategy="meta_tail_marker_cut:Ready.")
        write_record(log_path, 2, sanitized=False, structured=True, marker="", strategy="none")

        report_path = observe_dir / "reports" / "smoke-report.md"

        rc_stats, stats_out = run_cmd([hermes_observe, "--observe-dir", str(observe_dir), "stats", "--days", "7", "--json"])
        rc_report, report_out = run_cmd([hermes_observe, "--observe-dir", str(observe_dir), "report", "--days", "7", "--output", str(report_path)])
        rc_print, print_out = run_cmd([hermes_observe, "--observe-dir", str(observe_dir), "report", "--days", "7", "--print"])

        try:
            stats = json.loads(stats_out[stats_out.find("{"):stats_out.rfind("}")+1])
        except Exception:
            stats = {}

        report_text = report_path.read_text(encoding="utf-8") if report_path.exists() else ""

        checks = [
            ("stats command pass", rc_stats == 0),
            ("stats total 2", stats.get("total") == 2),
            ("report command pass", rc_report == 0),
            ("report file exists", report_path.exists()),
            ("report has title", "# Hermes Observation Report" in report_text),
            ("report has sanitizer section", "Top Sanitizer Strategies" in report_text),
            ("report has marker section", "Top Detected Markers" in report_text),
            ("report print pass", rc_print == 0 and "# Hermes Observation Report" in print_out),
        ]

        failed = [name for name, ok in checks if not ok]
        result = {
            "suite": "M8.3c Observation Report Layer Smoke Test",
            "status": "PASS" if not failed else "FAIL",
            "failed": len(failed),
            "checks": [{"name": name, "status": "PASS" if ok else "FAIL"} for name, ok in checks],
            "report_path": str(report_path),
            "report_preview": report_text[:1000],
            "stats": stats,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
