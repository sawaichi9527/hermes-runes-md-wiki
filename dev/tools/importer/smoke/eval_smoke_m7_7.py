#!/usr/bin/env python3
import json
import subprocess
import sys

cmd = [
    "hermes-recall",
    "memory.audit multi operation recall validation marker PASS",
    "--mode", "hybrid",
    "--project", "k6-freelancer",
    "--path", "wiki/k6-freelancer/operations.md",
    "--limit", "5",
    "--json",
]

p = subprocess.run(cmd, text=True, capture_output=True)

if p.returncode != 0:
    print(json.dumps({
        "suite": "M7.7 Operations Recall Smoke Expansion",
        "status": "FAIL",
        "reason": "hermes-recall command failed",
        "stderr": p.stderr,
    }, ensure_ascii=False, indent=2))
    sys.exit(1)

data = json.loads(p.stdout)
results = data.get("results", [])
top = results[0] if results else {}
content = top.get("content", "")
headings = [r.get("section_heading") for r in results]

checks = {
    "has_results": bool(results),
    "top_is_memory_audit": top.get("section_heading") == "O-20260531-041500 memory.audit",
    "top_contains_audit_marker": "Multi-operation recall validation marker completed" in content,
    "top_contains_status_pass": "Status: PASS" in content,
    "memory_check_not_before_audit": headings.index("O-20260531-035049 memory.check") > headings.index("O-20260531-041500 memory.audit") if "O-20260531-035049 memory.check" in headings and "O-20260531-041500 memory.audit" in headings else False,
    "generic_header_not_top": top.get("section_heading") != "Operations Log",
}

ok = all(checks.values())

print(json.dumps({
    "suite": "M7.7 Operations Recall Smoke Expansion",
    "status": "PASS" if ok else "FAIL",
    "checks": checks,
    "top_chunk_id": top.get("chunk_id"),
    "top_path": top.get("path"),
    "top_section_heading": top.get("section_heading"),
    "top_fts_rank": top.get("fts_rank"),
    "top_fts_score": top.get("fts_score"),
    "headings": headings,
}, ensure_ascii=False, indent=2))

sys.exit(0 if ok else 1)
