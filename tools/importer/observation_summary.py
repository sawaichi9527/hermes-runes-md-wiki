#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

from root_resolver import resolve_observation_log_dir


OBS_ROOT = resolve_observation_log_dir()


def iter_log_files(days: int):
    today = datetime.now().date()
    for i in range(days):
        d = today - timedelta(days=i)
        yield OBS_ROOT / d.strftime("%Y-%m") / f"{d.strftime('%Y%m%d')}.jsonl"


def read_records(days: int):
    for path in iter_log_files(days):
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except Exception as exc:
                    yield {
                        "_parse_error": True,
                        "path": str(path),
                        "line": line_no,
                        "error": str(exc),
                    }


def pct(n, d):
    if d <= 0:
        return 0.0
    return round((n / d) * 100, 2)


def build_tuning_candidates(summary):
    candidates = []

    quality = dict(summary.get("top_quality_issues", []))
    risks = dict(summary.get("top_risk_signals", []))
    citations = dict(summary.get("top_citation_issues", []))
    extraction_paths = dict(summary.get("extraction_paths", []))
    rates = summary.get("rates", {})

    if quality.get("answer_empty", 0) > 0 or extraction_paths.get("empty", 0) > 0:
        candidates.append({
            "bucket": "empty_extraction",
            "severity": "high",
            "evidence": {
                "answer_empty": quality.get("answer_empty", 0),
                "extraction_path_empty": extraction_paths.get("empty", 0),
            },
            "recommendation": "Investigate extraction path fallback for qwen forced-thinking responses. Prefer improving structured extraction before adding more regex cleanup.",
            "auto_patch": False,
        })

    if risks.get("finish_reason_length", 0) > 0:
        candidates.append({
            "bucket": "finish_reason_length",
            "severity": "medium",
            "evidence": {
                "finish_reason_length": risks.get("finish_reason_length", 0),
            },
            "recommendation": "Consider compact prompts, lower context budget, or larger max_tokens for affected answer paths. Keep retry conservative.",
            "auto_patch": False,
        })

    if quality.get("ends_mid_sentence", 0) > 0:
        candidates.append({
            "bucket": "incomplete_tail",
            "severity": "medium",
            "evidence": {
                "ends_mid_sentence": quality.get("ends_mid_sentence", 0),
            },
            "recommendation": "Review trim_incomplete_answer_tail and retry validation behavior. Add targeted smoke case before changing sanitizer.",
            "auto_patch": False,
        })

    if citations.get("missing_citation", 0) > 0:
        candidates.append({
            "bucket": "citation_missing",
            "severity": "medium",
            "evidence": {
                "missing_citation": citations.get("missing_citation", 0),
            },
            "recommendation": "Check whether final retry answer lost citation or citation checker ran against stale answer. Prefer final-answer consistency checks.",
            "auto_patch": False,
        })

    retry_rate = rates.get("retry_success_when_executed_pct", 0)
    if retry_rate and retry_rate < 90:
        candidates.append({
            "bucket": "retry_effectiveness",
            "severity": "medium",
            "evidence": {
                "retry_success_when_executed_pct": retry_rate,
            },
            "recommendation": "Inspect failed retry samples. Improve compact retry prompt only if failures are repeated and classifiable.",
            "auto_patch": False,
        })

    return candidates


def main():
    ap = argparse.ArgumentParser(description="Summarize Hermes Memory observation JSONL logs.")
    ap.add_argument("--days", type=int, default=1)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    records = list(read_records(args.days))
    total = len(records)
    parse_errors = [r for r in records if r.get("_parse_error")]
    valid = [r for r in records if not r.get("_parse_error")]

    quality_issues = Counter()
    risk_signals = Counter()
    citation_issues = Counter()
    model_profiles = Counter()
    extraction_paths = Counter()
    finish_reasons = Counter()

    retry_executed = 0
    retry_success = 0
    citation_ok = 0
    extraction_ok = 0
    completeness_ok = 0

    for r in valid:
        for x in r.get("quality_issues") or []:
            quality_issues[x] += 1
        for x in r.get("risk_signals") or []:
            risk_signals[x] += 1
        for x in r.get("citation_issues") or []:
            citation_issues[x] += 1

        if r.get("selected_model_profile"):
            model_profiles[r["selected_model_profile"]] += 1
        if r.get("extraction_path"):
            extraction_paths[r["extraction_path"]] += 1
        if r.get("finish_reason"):
            finish_reasons[r["finish_reason"]] += 1

        if r.get("retry_executed"):
            retry_executed += 1
        if r.get("retry_success"):
            retry_success += 1
        if r.get("citation_integrity_ok"):
            citation_ok += 1
        if r.get("extraction_quality_ok"):
            extraction_ok += 1
        if r.get("completeness_ok"):
            completeness_ok += 1

    summary = {
        "suite": "M11 Observation Summary",
        "days": args.days,
        "records_total": total,
        "records_valid": len(valid),
        "parse_errors": len(parse_errors),
        "rates": {
            "extraction_quality_ok_pct": pct(extraction_ok, len(valid)),
            "completeness_ok_pct": pct(completeness_ok, len(valid)),
            "citation_integrity_ok_pct": pct(citation_ok, len(valid)),
            "retry_executed_pct": pct(retry_executed, len(valid)),
            "retry_success_when_executed_pct": pct(retry_success, retry_executed),
        },
        "top_quality_issues": quality_issues.most_common(10),
        "top_risk_signals": risk_signals.most_common(10),
        "top_citation_issues": citation_issues.most_common(10),
        "model_profiles": model_profiles.most_common(),
        "extraction_paths": extraction_paths.most_common(),
        "finish_reasons": finish_reasons.most_common(),
    }

    summary["tuning_candidates"] = build_tuning_candidates(summary)

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
