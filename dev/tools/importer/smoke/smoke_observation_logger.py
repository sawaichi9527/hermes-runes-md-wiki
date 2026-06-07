#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

QUERY = "M8.0 Context Injection Risk Baseline 是什麼？"

def parse_json(stdout: str) -> dict:
    start = stdout.find("{")
    end = stdout.rfind("}")
    if start < 0 or end < start:
        raise ValueError("No JSON object found")
    return json.loads(stdout[start:end+1])

def run_cmd(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    return proc.returncode, proc.stdout

def main() -> int:
    hermes_answer = shutil.which("hermes-answer")
    hermes_observe = shutil.which("hermes-observe")
    if not hermes_answer:
        print("FAIL: hermes-answer not found", file=sys.stderr)
        return 1
    if not hermes_observe:
        print("FAIL: hermes-observe not found", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory(prefix="hermes-observe-smoke-") as tmp:
        observe_dir = Path(tmp) / "observations"
        cmd = [
            hermes_answer, QUERY,
            "--project", "k6-freelancer",
            "--max-chunks", "4",
            "--model-profile", "qwen-forced-thinking",
            "--observe-dir", str(observe_dir),
            "--json",
            "--show-sanitizer-diff",
        ]
        rc, out = run_cmd(cmd)
        if rc != 0:
            print("FAIL: hermes-answer failed")
            print(out)
            return 1
        data = parse_json(out)
        files = list((observe_dir / "answer-runs").glob("*/*.jsonl"))
        records = []
        for file in files:
            for line in file.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    records.append(json.loads(line))
        record = records[-1] if records else {}

        forbidden = {"raw_model_output", "full_prompt", "memory_context", "full_answer", "retrieved_chunk_content"}
        rc_tail, tail_out = run_cmd([hermes_observe, "--observe-dir", str(observe_dir), "tail", "--limit", "5"])
        rc_stats, stats_out = run_cmd([hermes_observe, "--observe-dir", str(observe_dir), "stats", "--json"])
        try:
            stats_data = parse_json(stats_out)
        except Exception:
            stats_data = {}

        checks = [
            ("answer status acceptable", data.get("status") in {"pass", "needs_review"}),
            ("phase M8.3a", data.get("phase") == "M8.3a"),
            ("has trace id", bool(data.get("trace_id"))),
            ("observation warnings present", bool(data.get("observation_warnings"))),
            ("jsonl written", bool(files) and bool(records)),
            ("record schema version", record.get("schema_version") == "m8.3a-observation-v1"),
            ("record has sanitizer", bool(record.get("sanitizer"))),
            ("record has content_metrics", bool(record.get("content_metrics"))),
            ("record avoids forbidden keys", not any(k in record for k in forbidden)),
            ("tail command pass", rc_tail == 0 and data.get("trace_id") in tail_out),
            ("stats command pass", rc_stats == 0 and stats_data.get("total", 0) >= 1),
        ]
        failed = [name for name, ok in checks if not ok]
        result = {
            "suite": "M8.3a Default-on JSONL Observation Logger Smoke Test",
            "status": "PASS" if not failed else "FAIL",
            "failed": len(failed),
            "checks": [{"name": name, "status": "PASS" if ok else "FAIL"} for name, ok in checks],
            "trace_id": data.get("trace_id"),
            "observation_files": [str(f) for f in files],
            "tail_preview": tail_out[:1000],
            "stats": stats_data,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if not failed else 1

if __name__ == "__main__":
    raise SystemExit(main())
