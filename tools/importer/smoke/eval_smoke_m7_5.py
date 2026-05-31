#!/usr/bin/env python3
import json
import subprocess
import sys

cmd = [
    "hermes-recall",
    "memory.check operation log status PASS",
    "--mode", "hybrid",
    "--project", "k6-freelancer",
    "--path", "wiki/k6-freelancer/operations.md",
    "--limit", "3",
    "--json",
]

p = subprocess.run(cmd, text=True, capture_output=True)

if p.returncode != 0:
    print(json.dumps({
        "suite": "M7.5 Tool Result Recall Smoke Test",
        "status": "FAIL",
        "reason": "hermes-recall command failed",
        "stderr": p.stderr,
    }, ensure_ascii=False, indent=2))
    sys.exit(1)

data = json.loads(p.stdout)
results = data.get("results", [])
top = results[0] if results else {}
content = top.get("content", "")

checks = {
    "has_results": bool(results),
    "top_is_operation_chunk": top.get("section_heading") == "O-20260531-035049 memory.check",
    "top_contains_memory_check": "memory.check" in content,
    "top_contains_status_pass": "Status: PASS" in content,
    "top_contains_summary": "Environment, commands, and database/schema probe completed" in content,
}

ok = all(checks.values())

print(json.dumps({
    "suite": "M7.5 Tool Result Recall Smoke Test",
    "status": "PASS" if ok else "FAIL",
    "checks": checks,
    "top_chunk_id": top.get("chunk_id"),
    "top_path": top.get("path"),
    "top_section_heading": top.get("section_heading"),
    "top_fts_rank": top.get("fts_rank"),
    "top_fts_score": top.get("fts_score"),
}, ensure_ascii=False, indent=2))

sys.exit(0 if ok else 1)
