#!/usr/bin/env python3
import json
import re
import subprocess
import sys
from pathlib import Path

IMPORTER_PARENT = Path(__file__).resolve().parents[1]
if str(IMPORTER_PARENT) not in sys.path:
    sys.path.insert(0, str(IMPORTER_PARENT))

from root_resolver import resolve_root, resolve_importer_dir


ROOT = resolve_root()
IMPORTER = resolve_importer_dir()


def source_count(answer: str) -> int:
    citations = set()
    for m in re.finditer(r"\[Source\s+(\d+)\]", answer or ""):
        citations.add(int(m.group(1)))
    return len(citations)


def main():
    cmd = [
        sys.executable,
        "answer_generator.py",
        "Telegram integration 是什麼？",
        "--project", "k6-freelancer",
        "--path", "services.md",
        "--heading", "Telegram",
        "--max-tokens", "512",
        "--json",
    ]

    proc = subprocess.run(
        cmd,
        cwd=IMPORTER,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
    )

    if proc.returncode != 0:
        print(json.dumps({
            "suite": "M10 Observation Log Smoke Test",
            "status": "FAIL",
            "step": "answer_generator",
            "returncode": proc.returncode,
            "stderr_tail": proc.stderr[-2000:],
        }, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    data = json.loads(proc.stdout)
    answer = data.get("answer") or ""
    expected_citations = source_count(answer)

    issues = []

    if not answer.strip():
        issues.append("answer_empty")

    if data.get("answer_chars") != len(answer):
        issues.append("answer_chars_mismatch")

    if data.get("citation_count") != expected_citations:
        issues.append("citation_count_mismatch_final_answer")

    if expected_citations > 0 and data.get("citation_integrity_ok") is not True:
        citation_issues = data.get("citation_issues") or []
        if "invalid_citation_reference" in citation_issues:
            issues.append("invalid_citation_reference")
        elif "missing_citation" in citation_issues:
            issues.append("missing_citation_despite_sources")
        else:
            issues.append("citation_integrity_false_with_sources")

    if data.get("retry_executed") and data.get("retry_success"):
        if data.get("answer_chars") != len(answer):
            issues.append("retry_final_answer_chars_mismatch")

    output = {
        "suite": "M10 Observation Log Smoke Test",
        "status": "FAIL" if issues else "PASS",
        "issues": issues,
        "summary": {
            "answer_chars": data.get("answer_chars"),
            "actual_chars": len(answer),
            "citation_count": data.get("citation_count"),
            "expected_citations": expected_citations,
            "citation_integrity_ok": data.get("citation_integrity_ok"),
            "retry_executed": data.get("retry_executed"),
            "retry_success": data.get("retry_success"),
            "selected_model_profile": data.get("selected_model_profile"),
            "extraction_path": data.get("extraction_path"),
        },
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
