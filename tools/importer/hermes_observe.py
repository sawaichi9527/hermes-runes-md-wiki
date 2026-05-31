#!/usr/bin/env python3
"""
M8.3c hermes-observe

Lightweight local JSONL observation viewer/reporter.
Supports:
- tail
- stats
- report

No database required.
"""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any


DEFAULT_TZ = timezone(timedelta(hours=8))


def root_dir() -> Path:
    return Path(os.environ.get("HERMES_MEMORY_ROOT", str(Path.home() / "workspace/hermes-memory")))


def base_dir(args: argparse.Namespace) -> Path:
    return Path(args.observe_dir).expanduser() if args.observe_dir else root_dir() / "observations"


def iter_jsonl_files(base: Path, days: int | None = None) -> list[Path]:
    runs = base / "answer-runs"
    if not runs.exists():
        return []

    files = sorted(runs.glob("*/*.jsonl"))
    if days is None:
        return files

    cutoff = datetime.now(DEFAULT_TZ) - timedelta(days=days)
    selected = []
    for file in files:
        try:
            mtime = datetime.fromtimestamp(file.stat().st_mtime, DEFAULT_TZ)
            if mtime >= cutoff:
                selected.append(file)
        except Exception:
            continue
    return selected


def iter_records(base: Path, days: int | None = None):
    for file in iter_jsonl_files(base, days=days):
        with file.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except Exception:
                    continue


def pct(n: int, d: int) -> str:
    if d <= 0:
        return "0.0%"
    return f"{(n / d) * 100:.1f}%"


def top(counter: Counter, limit: int = 10) -> list[dict[str, Any]]:
    return [{"name": k, "count": v} for k, v in counter.most_common(limit)]


def summarize(records: list[dict[str, Any]], days: int) -> dict[str, Any]:
    total = len(records)

    by_profile = Counter()
    by_model = Counter()
    by_status = Counter()
    by_review = Counter()
    by_strategy = Counter()
    by_extraction = Counter()
    markers = Counter()
    source_paths = Counter()

    structured_true = 0
    sanitized_true = 0
    needs_review = 0
    total_prompt_tokens = 0
    total_completion_tokens = 0
    total_reasoning_tokens = 0
    total_tokens = 0
    token_records = 0

    for rec in records:
        gen = rec.get("generation") or {}
        san = rec.get("sanitizer") or {}
        model = rec.get("model") or {}
        content = rec.get("content_metrics") or {}
        usage = rec.get("usage") or {}
        context = rec.get("context") or {}

        by_profile[model.get("profile") or "unknown"] += 1
        by_model[model.get("name") or "unknown"] += 1
        by_status[gen.get("status") or "unknown"] += 1
        by_review[gen.get("review_status") or "unknown"] += 1
        by_strategy[san.get("strategy") or "none"] += 1
        by_extraction[gen.get("extraction_strategy") or "unknown"] += 1

        if gen.get("structured_output_valid") is True:
            structured_true += 1
        if san.get("sanitized") is True:
            sanitized_true += 1
        if gen.get("review_status") == "needs_review":
            needs_review += 1

        for marker in content.get("detected_markers") or []:
            markers[marker] += 1

        for path in context.get("source_paths") or []:
            source_paths[path] += 1

        prompt_tokens = usage.get("prompt_tokens")
        completion_tokens = usage.get("completion_tokens")
        reasoning_tokens = usage.get("reasoning_tokens")
        rec_total_tokens = usage.get("total_tokens")

        if isinstance(rec_total_tokens, int):
            total_tokens += rec_total_tokens
            token_records += 1
        if isinstance(prompt_tokens, int):
            total_prompt_tokens += prompt_tokens
        if isinstance(completion_tokens, int):
            total_completion_tokens += completion_tokens
        if isinstance(reasoning_tokens, int):
            total_reasoning_tokens += reasoning_tokens

    avg_total_tokens = round(total_tokens / token_records, 1) if token_records else 0

    return {
        "days": days,
        "total": total,
        "structured_output_valid": {
            "count": structured_true,
            "rate": pct(structured_true, total),
        },
        "sanitized": {
            "count": sanitized_true,
            "rate": pct(sanitized_true, total),
        },
        "needs_review": {
            "count": needs_review,
            "rate": pct(needs_review, total),
        },
        "by_model_profile": dict(by_profile),
        "by_model": dict(by_model),
        "by_status": dict(by_status),
        "by_review_status": dict(by_review),
        "top_sanitizer_strategy": top(by_strategy),
        "top_extraction_strategy": top(by_extraction),
        "top_detected_markers": top(markers),
        "top_source_paths": top(source_paths),
        "usage": {
            "records_with_tokens": token_records,
            "total_prompt_tokens": total_prompt_tokens,
            "total_completion_tokens": total_completion_tokens,
            "total_reasoning_tokens": total_reasoning_tokens,
            "total_tokens": total_tokens,
            "avg_total_tokens": avg_total_tokens,
        },
    }


def cmd_tail(args: argparse.Namespace) -> int:
    records = list(iter_records(base_dir(args), days=args.days))
    records = records[-args.limit:]

    for rec in records:
        gen = rec.get("generation") or {}
        san = rec.get("sanitizer") or {}
        model = rec.get("model") or {}
        ctx = rec.get("context") or {}
        usage = rec.get("usage") or {}
        markers = (rec.get("content_metrics") or {}).get("detected_markers") or []

        print(
            f"{rec.get('timestamp')} | "
            f"{rec.get('trace_id')} | "
            f"profile={model.get('profile')} | "
            f"status={gen.get('status')} | "
            f"review={gen.get('review_status')} | "
            f"structured={gen.get('structured_output_valid')} | "
            f"sanitized={san.get('sanitized')} | "
            f"strategy={san.get('strategy')} | "
            f"markers={','.join(markers[:5])} | "
            f"ctx={ctx.get('used_count')} | "
            f"tok={usage.get('total_tokens')}"
        )

    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    records = list(iter_records(base_dir(args), days=args.days))
    result = summarize(records, args.days)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Days: {args.days}")
        print(f"Total runs: {result['total']}")
        print(f"Structured valid: {result['structured_output_valid']['count']} ({result['structured_output_valid']['rate']})")
        print(f"Sanitized: {result['sanitized']['count']} ({result['sanitized']['rate']})")
        print(f"Needs review: {result['needs_review']['count']} ({result['needs_review']['rate']})")
        print(f"Avg total tokens: {result['usage']['avg_total_tokens']}")

        print("\nBy model profile:")
        for k, v in Counter(result["by_model_profile"]).most_common():
            print(f"- {k}: {v}")

        print("\nTop sanitizer strategies:")
        for item in result["top_sanitizer_strategy"]:
            print(f"- {item['name']}: {item['count']}")

        print("\nTop detected markers:")
        for item in result["top_detected_markers"]:
            print(f"- {item['name']}: {item['count']}")

    return 0


def markdown_table(items: list[dict[str, Any]], name_header: str = "Name") -> str:
    if not items:
        return "_No data._\n"

    lines = [f"| {name_header} | Count |", "|---|---:|"]
    for item in items:
        lines.append(f"| `{item['name']}` | {item['count']} |")
    return "\n".join(lines) + "\n"


def format_dict_table(data: dict[str, int], name_header: str = "Name") -> str:
    if not data:
        return "_No data._\n"
    items = [{"name": k, "count": v} for k, v in Counter(data).most_common()]
    return markdown_table(items, name_header)


def build_report(summary: dict[str, Any], generated_at: datetime) -> str:
    usage = summary["usage"]

    return f"""# Hermes Observation Report

Generated at: {generated_at.isoformat()}
Window: last {summary['days']} day(s)

## Executive Summary

- Total runs: {summary['total']}
- Structured output valid: {summary['structured_output_valid']['count']} ({summary['structured_output_valid']['rate']})
- Sanitized: {summary['sanitized']['count']} ({summary['sanitized']['rate']})
- Needs review: {summary['needs_review']['count']} ({summary['needs_review']['rate']})
- Average total tokens: {usage['avg_total_tokens']}

## Model Profiles

{format_dict_table(summary['by_model_profile'], 'Model Profile')}

## Models

{format_dict_table(summary['by_model'], 'Model')}

## Status Breakdown

{format_dict_table(summary['by_status'], 'Status')}

## Review Status Breakdown

{format_dict_table(summary['by_review_status'], 'Review Status')}

## Top Sanitizer Strategies

{markdown_table(summary['top_sanitizer_strategy'], 'Strategy')}

## Top Extraction Strategies

{markdown_table(summary['top_extraction_strategy'], 'Strategy')}

## Top Detected Markers

{markdown_table(summary['top_detected_markers'], 'Marker')}

## Top Source Paths

{markdown_table(summary['top_source_paths'], 'Source Path')}

## Token Usage

| Metric | Value |
|---|---:|
| Records with token usage | {usage['records_with_tokens']} |
| Prompt tokens | {usage['total_prompt_tokens']} |
| Completion tokens | {usage['total_completion_tokens']} |
| Reasoning tokens | {usage['total_reasoning_tokens']} |
| Total tokens | {usage['total_tokens']} |
| Average total tokens | {usage['avg_total_tokens']} |

## Governance Notes

- Observation analysis is automated.
- Heuristic modification is not automated.
- Human review remains required before sanitizer rule changes.
- Observation logs are local JSONL records and should not be imported into RAG memory.
- Missing or sparse data is expected early in the observation period.

## Suggested Follow-up

- Review `needs_review` and `auto_pass_with_warning` traces.
- Compare structured output validity by model profile.
- Check recurring sanitizer strategies before adding hardcoded heuristics.
- Prefer observe-first, tune-later changes.
"""


def cmd_report(args: argparse.Namespace) -> int:
    base = base_dir(args)
    records = list(iter_records(base, days=args.days))
    summary = summarize(records, args.days)
    generated_at = datetime.now(DEFAULT_TZ)
    report = build_report(summary, generated_at)

    if args.output:
        output = Path(args.output).expanduser()
    else:
        report_dir = base / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        output = report_dir / f"{generated_at.strftime('%Y%m%d')}-observation-report.md"

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")

    if args.print:
        print(report)
    else:
        print(str(output))

    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Hermes observation JSONL viewer")
    parser.add_argument("--observe-dir", default=None)

    sub = parser.add_subparsers(dest="cmd", required=True)

    tail = sub.add_parser("tail")
    tail.add_argument("--limit", type=int, default=10)
    tail.add_argument("--days", type=int, default=7)
    tail.set_defaults(func=cmd_tail)

    stats = sub.add_parser("stats")
    stats.add_argument("--days", type=int, default=7)
    stats.add_argument("--json", action="store_true")
    stats.set_defaults(func=cmd_stats)

    report = sub.add_parser("report")
    report.add_argument("--days", type=int, default=7)
    report.add_argument("--output", default=None)
    report.add_argument("--print", action="store_true")
    report.set_defaults(func=cmd_report)

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
