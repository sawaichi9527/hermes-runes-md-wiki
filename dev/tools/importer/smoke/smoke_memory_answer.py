#!/usr/bin/env python3
"""
M8.2c Reversible Meta-tail Sanitizer smoke test.

Levels:
1. deterministic sanitizer regression tests
2. context-only smoke: no LLM required
3. optional LLM smoke: enabled with --llm
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


QUERY = "M8.0 Context Injection Risk Baseline 是什麼？"

LEAK_PATTERNS = [
    re.compile(r"(?i)here'?s a thinking process"),
    re.compile(r"(?i)analyze user query"),
    re.compile(r"(?i)scan memory context"),
    re.compile(r"(?i)extract key information"),
    re.compile(r"(?i)synthesize answer"),
    re.compile(r"(?i)chain[- ]of[- ]thought"),
    re.compile(r"(?i)let'?s verify"),
    re.compile(r"(?i)output matches schema"),
    re.compile(r"(?i)self-correction"),
]


def load_generator_module():
    path = Path.home() / "workspace/hermes-memory/tools/importer/memory_answer_generator.py"
    module_name = "memory_answer_generator"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)

    # Python 3.12 dataclasses expect sys.modules[cls.__module__] to exist
    # while the class decorator is being evaluated.
    sys.modules[module_name] = module

    spec.loader.exec_module(module)
    return module


def parse_json(stdout: str) -> dict:
    start = stdout.find("{")
    end = stdout.rfind("}")
    if start < 0 or end < start:
        raise ValueError("No JSON object found")
    return json.loads(stdout[start : end + 1])


def run_cmd(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(
        cmd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.returncode, proc.stdout


def has_reasoning_leak(answer: str) -> bool:
    return any(pattern.search(answer or "") for pattern in LEAK_PATTERNS)


def deterministic_sanitizer_checks() -> list[tuple[str, bool]]:
    mod = load_generator_module()

    normal_mixed_language = (
        "M8.2c 的 sanitizer 會檢查 JSON schema、Source Manifest、final_answer 欄位，"
        "但這些都是正常技術內容，不應該被切掉。"
    )

    tail_contaminated = (
        "M8.0 是 Hermes Memory 的安全基準，重點是把 retrieved memory 視為 untrusted reference。\n\n"
        "Let's verify the JSON schema.\n"
        "Output matches schema.\n"
        "Ready."
    )

    self_correction_tail = (
        "M8.0 Context Injection Risk Baseline 用來建立 context injection 前的安全邊界。\n\n"
        "Self-Correction/Verification during thought:\n"
        "- Check citations.\n"
        "- No extra text."
    )

    valid_json = {
        "final_answer": "M8.0 是 context injection 前的安全基準。",
        "memory_sufficiency": "sufficient",
        "citations": [{"source_index": 1, "ref": "ref-1"}],
    }

    parsed, strategy = mod.parse_structured_response(json.dumps(valid_json, ensure_ascii=False))
    normal = mod.sanitize_final_answer(normal_mixed_language, mode="auto", structured_output_valid=False)
    tail = mod.sanitize_final_answer(tail_contaminated, mode="auto", structured_output_valid=False)
    correction = mod.sanitize_final_answer(self_correction_tail, mode="auto", structured_output_valid=False)
    off = mod.sanitize_final_answer(tail_contaminated, mode="off", structured_output_valid=False)

    return [
        ("valid JSON parses", parsed is not None and strategy == "json_direct"),
        ("mixed-language technical answer not sanitized", normal.sanitized is False),
        ("meta tail sanitized", tail.sanitized is True and "Let's verify" not in tail.answer),
        ("self-correction tail sanitized", correction.sanitized is True and "Self-Correction" not in correction.answer),
        ("sanitize off preserves raw", off.sanitized is False and "Let's verify" in off.answer),
        ("sanitizer confidence present", tail.sanitizer_confidence in {"high", "medium", "low"}),
        ("review status present", tail.review_status in {"auto_pass", "auto_pass_with_warning", "needs_review", "blocked", "override_raw"}),
    ]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--llm", action="store_true", help="Also call the configured LLM endpoint")
    parser.add_argument("--model-profile", default="qwen-forced-thinking")
    args = parser.parse_args(argv)

    checks = deterministic_sanitizer_checks()

    hermes_answer = shutil.which("hermes-answer")
    if not hermes_answer:
        print("FAIL: hermes-answer not found in PATH", file=sys.stderr)
        return 1

    context_cmd = [
        hermes_answer,
        QUERY,
        "--project",
        "k6-freelancer",
        "--max-chunks",
        "4",
        "--context-only",
        "--json",
    ]

    rc, output = run_cmd(context_cmd)
    if rc != 0:
        print("FAIL: context-only command failed")
        print(output)
        return 1

    try:
        context_data = parse_json(output)
    except Exception as exc:
        print(f"FAIL: invalid context JSON: {exc}")
        print(output)
        return 1

    checks.extend([
        ("context status pass", context_data.get("status") == "pass"),
        ("context phase M8.1d", context_data.get("phase") == "M8.1d"),
        ("has memory_context", bool(context_data.get("memory_context"))),
        ("has sources", len(context_data.get("sources") or []) >= 1),
        ("has safe boundary", "=== Hermes Memory Context ===" in (context_data.get("memory_context") or "")),
    ])

    llm_result = None
    if args.llm:
        llm_cmd = [
            hermes_answer,
            QUERY,
            "--project",
            "k6-freelancer",
            "--max-chunks",
            "4",
            "--model-profile",
            args.model_profile,
            "--json",
            "--show-sanitizer-diff",
            "--debug-raw-preview",
        ]

        rc, output = run_cmd(llm_cmd)
        if rc != 0:
            checks.append(("llm command pass", False))
            llm_result = output
        else:
            try:
                data = parse_json(output)
                answer = data.get("answer") or ""
                llm_result = data
                checks.extend(
                    [
                        ("llm status acceptable", data.get("status") in {"pass", "needs_review"}),
                        ("llm phase M8.2c", data.get("phase") == "M8.2c"),
                        ("has answer", bool(answer)),
                        ("has answer sources", len(data.get("sources") or []) >= 1),
                        ("has extraction strategy", bool(data.get("extraction_strategy"))),
                        ("has memory sufficiency", data.get("memory_sufficiency") in {"sufficient", "partial", "insufficient"}),
                        ("has structured output validity flag", isinstance(data.get("structured_output_valid"), bool)),
                        ("has sanitizer metadata", "sanitizer_confidence" in data and "review_status" in data),
                        ("answer has no obvious reasoning leak", not has_reasoning_leak(answer)),
                    ]
                )
            except Exception as exc:
                checks.append((f"llm json parse: {exc}", False))
                llm_result = output

    failed = [name for name, ok in checks if not ok]

    result = {
        "suite": "M8.2c Reversible Meta-tail Sanitizer Smoke Test",
        "status": "PASS" if not failed else "FAIL",
        "failed": len(failed),
        "checks": [{"name": name, "status": "PASS" if ok else "FAIL"} for name, ok in checks],
        "context_used_count": context_data.get("used_count"),
        "context_recovered_count": context_data.get("recovered_count"),
        "llm_enabled": args.llm,
        "model_profile": args.model_profile,
        "llm_result_preview": llm_result if args.llm else None,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
