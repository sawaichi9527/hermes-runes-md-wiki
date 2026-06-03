#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]

DEFAULT_SCAN_ROOT = "wiki"
DEFAULT_OUT_DIR = "reports/m33-markdown-source-health"

HEADING_RE = re.compile(r"^(#{1,6})\s+.+$", re.MULTILINE)
CJK_RE = re.compile(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]")


def estimate_tokens(text: str) -> dict[str, int]:
    chars = len(text)
    cjk_chars = len(CJK_RE.findall(text))
    non_cjk_chars = max(chars - cjk_chars, 0)

    # Conservative estimates:
    # - English-ish text: ~4 chars/token
    # - CJK-heavy text: ~1 to 1.6 chars/token; use 1.2 chars/token as pressure estimate
    estimated_en = math.ceil(chars / 4) if chars else 0
    estimated_cjk = math.ceil((cjk_chars / 1.2) + (non_cjk_chars / 4)) if chars else 0

    return {
        "chars": chars,
        "cjk_chars": cjk_chars,
        "estimated_tokens_en": estimated_en,
        "estimated_tokens_cjk": estimated_cjk,
        "estimated_tokens_pressure": max(estimated_en, estimated_cjk),
    }


def count_headings(text: str) -> int:
    return len(HEADING_RE.findall(text))


def largest_heading_span_lines(text: str) -> int:
    lines = text.splitlines()
    heading_indexes = [idx for idx, line in enumerate(lines) if HEADING_RE.match(line)]
    if not heading_indexes:
        return len(lines)

    spans: list[int] = []
    for pos, start in enumerate(heading_indexes):
        end = heading_indexes[pos + 1] if pos + 1 < len(heading_indexes) else len(lines)
        spans.append(max(end - start, 0))
    return max(spans) if spans else len(lines)


def estimate_chunk_count(text: str, chunk_chars: int = 1200) -> int:
    if not text:
        return 0
    return max(1, math.ceil(len(text) / chunk_chars))


def level_from_size(size_kb: float) -> int:
    if size_kb <= 10:
        return 0
    if size_kb <= 25:
        return 1
    if size_kb <= 50:
        return 2
    if size_kb <= 80:
        return 4
    if size_kb <= 120:
        return 5
    if size_kb <= 200:
        return 6
    if size_kb <= 350:
        return 7
    if size_kb <= 500:
        return 8
    return 9


def level_from_tokens(tokens: int) -> int:
    if tokens <= 5_000:
        return 0
    if tokens <= 10_000:
        return 1
    if tokens <= 20_000:
        return 2
    if tokens <= 35_000:
        return 4
    if tokens <= 50_000:
        return 5
    if tokens <= 80_000:
        return 6
    if tokens <= 120_000:
        return 7
    if tokens <= 180_000:
        return 8
    return 9


def level_from_headings(heading_count: int) -> int:
    if heading_count <= 15:
        return 0
    if heading_count <= 30:
        return 1
    if heading_count <= 40:
        return 2
    if heading_count <= 70:
        return 4
    if heading_count <= 100:
        return 5
    if heading_count <= 120:
        return 6
    if heading_count <= 180:
        return 7
    if heading_count <= 240:
        return 8
    return 9


def level_from_chunks(chunk_count: int) -> int:
    if chunk_count <= 15:
        return 0
    if chunk_count <= 30:
        return 1
    if chunk_count <= 40:
        return 2
    if chunk_count <= 70:
        return 4
    if chunk_count <= 100:
        return 5
    if chunk_count <= 150:
        return 6
    if chunk_count <= 250:
        return 7
    if chunk_count <= 400:
        return 8
    return 9


def zone_from_level(level: int) -> tuple[str, str, str, str]:
    if level <= 3:
        return (
            "green",
            f"+{level}",
            "stable",
            "section_patch_ok_small_append_ok",
        )
    if level <= 6:
        return (
            "yellow",
            f"+{level}",
            "heated",
            "avoid_broad_append_prefer_new_topic_file_or_targeted_section_patch",
        )
    return (
        "red",
        f"+{level}",
        "overloaded",
        "do_not_direct_append_prefer_split_proposal_or_new_topic_file",
    )


def analyze_file(path: Path) -> dict[str, Any]:
    rel = path.relative_to(ROOT).as_posix()
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    size_bytes = len(raw)
    size_kb = round(size_bytes / 1024, 2)

    token_info = estimate_tokens(text)
    heading_count = count_headings(text)
    chunk_count = estimate_chunk_count(text)
    largest_span = largest_heading_span_lines(text)

    largest_span_est_tokens = math.ceil((largest_span * 80) / 4)

    levels = {
        "size": level_from_size(size_kb),
        "tokens": level_from_tokens(token_info["estimated_tokens_pressure"]),
        "headings": level_from_headings(heading_count),
        "chunks": level_from_chunks(chunk_count),
    }
    level = max(levels.values())
    growth_zone, refinement_level, rune_state, recommended_action = zone_from_level(level)

    return {
        "path": rel,
        "size_bytes": size_bytes,
        "size_kb": size_kb,
        **token_info,
        "heading_count": heading_count,
        "chunk_estimate": chunk_count,
        "largest_heading_span_lines": largest_span,
        "largest_heading_span_est_tokens": largest_span_est_tokens,
        "level_components": levels,
        "growth_zone": growth_zone,
        "refinement_level": refinement_level,
        "rune_state": rune_state,
        "recommended_action": recommended_action,
    }


def write_markdown_report(report: dict[str, Any], path: Path) -> None:
    rows = sorted(report["files"], key=lambda item: (item["growth_zone"], item["size_bytes"]), reverse=True)
    lines = [
        "# M33 Markdown Source Health Audit",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "## Summary",
        "",
        f"- files_scanned: {report['summary']['files_scanned']}",
        f"- green: {report['summary']['green']}",
        f"- yellow: {report['summary']['yellow']}",
        f"- red: {report['summary']['red']}",
        f"- max_size_kb: {report['summary']['max_size_kb']}",
        f"- max_refinement_level: {report['summary']['max_refinement_level']}",
        "",
        "## Largest / Highest Pressure Files",
        "",
        "| zone | level | state | size KB | tokens pressure | headings | chunks | path | recommendation |",
        "|---|---:|---|---:|---:|---:|---:|---|---|",
    ]

    def zone_rank(item: dict[str, Any]) -> tuple[int, int, int]:
        rank = {"red": 3, "yellow": 2, "green": 1}.get(item["growth_zone"], 0)
        level = int(str(item["refinement_level"]).lstrip("+"))
        return rank, level, item["size_bytes"]

    for item in sorted(report["files"], key=zone_rank, reverse=True)[:40]:
        lines.append(
            f"| {item['growth_zone']} | {item['refinement_level']} | {item['rune_state']} | "
            f"{item['size_kb']} | {item['estimated_tokens_pressure']} | {item['heading_count']} | "
            f"{item['chunk_estimate']} | `{item['path']}` | {item['recommended_action']} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- +0~+3: Stable Rune / 穩定符文",
            "- +4~+6: Heated Rune / 熾熱符文",
            "- +7~+9: Overloaded Rune / 過載符文",
            "",
            "This audit is read-only. It does not modify wiki content, PostgreSQL, or importer state.",
            "",
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Markdown source granularity and Runes source health.")
    parser.add_argument("--scan-root", default=DEFAULT_SCAN_ROOT)
    parser.add_argument("--out-dir", default=DEFAULT_OUT_DIR)
    parser.add_argument("--path", default=None, help="Analyze one Markdown file only.")
    parser.add_argument("--json", action="store_true", help="Print JSON to stdout.")
    args = parser.parse_args()

    if args.path:
        target = (ROOT / args.path).resolve()
        if not target.is_file():
            raise SystemExit(f"missing file: {args.path}")
        result = analyze_file(target)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"{result['path']} {result['growth_zone']} {result['refinement_level']} {result['rune_state']}")
        return 0

    scan_root = ROOT / args.scan_root
    files = sorted(p for p in scan_root.rglob("*.md") if p.is_file())
    analyzed = [analyze_file(p) for p in files]

    summary = {
        "files_scanned": len(analyzed),
        "green": sum(1 for item in analyzed if item["growth_zone"] == "green"),
        "yellow": sum(1 for item in analyzed if item["growth_zone"] == "yellow"),
        "red": sum(1 for item in analyzed if item["growth_zone"] == "red"),
        "max_size_kb": max((item["size_kb"] for item in analyzed), default=0),
        "max_refinement_level": max((int(item["refinement_level"].lstrip("+")) for item in analyzed), default=0),
    }

    report = {
        "schema": "m33_markdown_source_health_audit_v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scan_root": args.scan_root,
        "summary": summary,
        "files": analyzed,
    }

    out_dir = ROOT / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    latest_json = out_dir / "latest.json"
    latest_md = out_dir / "latest.md"

    latest_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown_report(report, latest_md)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"wrote {latest_json}")
        print(f"wrote {latest_md}")
        print(json.dumps(summary, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
