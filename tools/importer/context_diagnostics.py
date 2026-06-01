import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


SOURCE_RE = re.compile(r"^\[Source\s+(\d+)\]$")
KEY_VALUE_RE = re.compile(r"^([A-Za-z0-9_]+):\s*(.*)$")


def parse_sources(context: str) -> list[dict]:
    sources: list[dict] = []
    current: dict | None = None

    for line in context.splitlines():
        source_match = SOURCE_RE.match(line.strip())
        if source_match:
            if current is not None:
                sources.append(current)
            current = {"source_index": int(source_match.group(1))}
            continue

        if current is None:
            continue

        match = KEY_VALUE_RE.match(line)
        if match:
            key, value = match.group(1), match.group(2)
            if key in {
                "project",
                "path",
                "heading",
                "citation",
                "merged_adjacent_chunks",
                "chunk_indexes",
                "chunk_ids",
                "doc_id",
                "chunk_id",
                "score",
                "rerank_score",
                "retrieval_mode",
            }:
                current[key] = value

    if current is not None:
        sources.append(current)

    return sources


def run_context_builder(args) -> dict:
    cmd = [
        sys.executable,
        str(BASE_DIR / "context_builder.py"),
        args.query,
        "--project",
        args.project,
        "--schema",
        args.schema,
        "--limit",
        str(args.limit),
        "--candidates",
        str(args.candidates),
        "--max-chars",
        str(args.max_chars),
        "--per-chunk-chars",
        str(args.per_chunk_chars),
        "--max-source-chunks",
        str(args.max_source_chunks),
        "--min-rerank-score",
        str(args.min_rerank_score),
        "--json",
        "--debug",
    ]

    if args.path:
        cmd.extend(["--path", args.path])
    if args.heading:
        cmd.extend(["--heading", args.heading])
    if not args.merge_adjacent_chunks:
        cmd.append("--no-merge-adjacent-chunks")

    proc = subprocess.run(
        cmd,
        cwd=str(BASE_DIR),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=os.environ.copy(),
    )

    if proc.returncode != 0:
        if proc.stderr:
            print(proc.stderr, file=sys.stderr)
        raise SystemExit(proc.returncode)

    return json.loads(proc.stdout)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Diagnose Hermes context assembly governance."
    )
    parser.add_argument("query")
    parser.add_argument("--project", required=True)
    parser.add_argument("--schema", default="public")
    parser.add_argument("--path", default=None)
    parser.add_argument("--heading", default=None)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--candidates", type=int, default=10)
    parser.add_argument("--max-chars", type=int, default=8000)
    parser.add_argument("--per-chunk-chars", type=int, default=2500)
    parser.add_argument("--max-source-chunks", type=int, default=2)
    parser.add_argument("--min-rerank-score", type=float, default=1.0)
    parser.add_argument("--no-merge-adjacent-chunks", dest="merge_adjacent_chunks", action="store_false")
    parser.set_defaults(merge_adjacent_chunks=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    payload = run_context_builder(args)
    context = payload.get("context", "")
    debug = payload.get("debug", {})
    sources = parse_sources(context)

    path_counts = Counter(source.get("path", "") for source in sources if source.get("path"))
    merged_sources = [
        source for source in sources
        if str(source.get("merged_adjacent_chunks", "")).lower() == "true"
    ]

    duplicate_source_cap_violations = {
        path: count
        for path, count in path_counts.items()
        if args.max_source_chunks > 0 and count > args.max_source_chunks
    }

    issues: list[str] = []
    if debug.get("context_chars", len(context)) > args.max_chars:
        issues.append("context_chars_exceeds_max_chars")
    if duplicate_source_cap_violations:
        issues.append("max_source_chunks_violation")
    if debug.get("selected_chunks", len(sources)) != len(sources):
        issues.append("debug_selected_chunks_differs_from_parsed_sources")

    result = {
        "status": "pass" if not issues else "warn",
        "query": args.query,
        "project": args.project,
        "schema": args.schema,
        "path": args.path,
        "heading": args.heading,
        "issues": issues,
        "summary": {
            "context_chars": debug.get("context_chars", len(context)),
            "max_chars": args.max_chars,
            "selected_sources": len(sources),
            "debug_selected_chunks": debug.get("selected_chunks"),
            "candidate_chunks": debug.get("candidate_chunks"),
            "dropped_by_char_budget": debug.get("dropped_by_char_budget"),
            "dropped_by_source_cap": debug.get("dropped_by_source_cap"),
            "skipped_empty": debug.get("skipped_empty"),
            "max_source_chunks": args.max_source_chunks,
            "unique_paths": len(path_counts),
            "merged_sources": len(merged_sources),
            "merge_adjacent_chunks": args.merge_adjacent_chunks,
            "retrieval_query_used": debug.get("retrieval_query_used"),
        },
        "path_distribution": dict(path_counts),
        "sources": sources,
        "debug": debug,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"status: {result['status']}")
    print(f"project: {args.project}")
    print(f"query: {args.query}")
    print()
    print(f"context_chars: {result['summary']['context_chars']} / {args.max_chars}")
    print(f"selected_sources: {len(sources)}")
    print(f"unique_paths: {len(path_counts)}")
    print(f"merged_sources: {len(merged_sources)}")
    print(f"dropped_by_source_cap: {debug.get('dropped_by_source_cap')}")
    print(f"dropped_by_char_budget: {debug.get('dropped_by_char_budget')}")
    print()
    print("path_distribution:")
    for path, count in path_counts.items():
        print(f"- {path}: {count}")
    print()
    print("sources:")
    for source in sources:
        chunk = source.get("chunk_indexes") or source.get("chunk_id", "")
        print(
            f"- Source {source.get('source_index')}: "
            f"{source.get('path', '')} "
            f"chunk={chunk} "
            f"heading={source.get('heading', '')!r} "
            f"rerank={source.get('rerank_score', '')}"
        )
    if issues:
        print()
        print("issues:")
        for issue in issues:
            print(f"- {issue}")


if __name__ == "__main__":
    main()
