#!/usr/bin/env python3
# M25.2 curated promotion patch dry-run helper.

from __future__ import annotations

import argparse
import difflib
import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "m25.2.p0.v1"
DEFAULT_PROJECT = "k6-freelancer"


def parse_heading(line: str) -> tuple[int, str] | None:
    stripped = line.strip()
    if not stripped.startswith("#"):
        return None
    level = len(stripped) - len(stripped.lstrip("#"))
    return level, stripped[level:].strip()


def find_heading(lines: list[str], heading: str) -> tuple[int, int] | None:
    wanted = heading.strip().lower()
    for idx, line in enumerate(lines):
        parsed = parse_heading(line)
        if parsed and parsed[1].lower() == wanted:
            return idx, parsed[0]
    return None


def section_end(lines: list[str], start: int, level: int) -> int:
    for idx in range(start + 1, len(lines)):
        parsed = parse_heading(lines[idx])
        if parsed and parsed[0] <= level:
            return idx
    return len(lines)


def as_lines(text: str) -> list[str]:
    out = [line.rstrip() + "\n" for line in text.splitlines()]
    if out and out[-1].strip():
        out.append("\n")
    return out


def candidate_lines(original: list[str], heading: str, insert_text: str) -> tuple[list[str], dict[str, Any]]:
    found = find_heading(original, heading)
    add = as_lines(insert_text)
    if found:
        start, level = found
        end = section_end(original, start, level)
        spacer = [] if end > 0 and original[end - 1].strip() == "" else ["\n"]
        return original[:end] + spacer + add + original[end:], {
            "target_heading_found": True,
            "operation": "append_to_existing_heading",
            "heading_start_line": start + 1,
            "insertion_line": end + 1,
        }

    new_section = ["\n", f"## {heading}\n", "\n"] + add
    return original + new_section, {
        "target_heading_found": False,
        "operation": "append_new_heading_at_end",
        "heading_start_line": None,
        "insertion_line": len(original) + 1,
    }


def build_promotion_patch_preview(
    root: Path,
    project: str,
    proposal_id: str,
    target_path: str,
    heading: str,
    insert_text: str,
    reason: str | None = None,
) -> dict[str, Any]:
    rel = Path(target_path)
    abs_path = (root / rel).resolve()
    abs_path.relative_to(root.resolve())

    original = abs_path.read_text(encoding="utf-8").splitlines(keepends=True) if abs_path.exists() else []
    candidate, meta = candidate_lines(original, heading, insert_text)
    diff = "\n".join(difflib.unified_diff(original, candidate, fromfile=f"a/{target_path}", tofile=f"b/{target_path}", lineterm=""))

    return {
        "schema_version": SCHEMA_VERSION,
        "suite": "M25.2 Curated promotion patch dry-run",
        "status": "PASS",
        "mode": "dry_run_only",
        "project": project,
        "proposal_id": proposal_id,
        "target": {"path": target_path, "exists": abs_path.exists(), "heading": heading, **meta},
        "reason": reason,
        "unified_diff": diff,
        "promotion": {
            "curated_promotion": True,
            "forge_suggestion": True,
            "promotion_execution_implemented": False,
            "trusted_wiki_mutation_allowed": False,
        },
        "preview": {
            "would_write_target_file": False,
            "would_update_proposal_state": False,
            "would_promote_to_wiki": False,
            "would_mutate_database": False,
            "would_run_importer": False,
            "human_review_required_for_future_apply": True,
        },
        "mutations": {
            "target_file_written": False,
            "proposal_state_mutated": False,
            "trusted_memory_created": False,
            "curated_wiki_mutated": False,
            "database_mutated": False,
            "importer_mutated": False,
            "files_written": False,
        },
    }


def render_patch_markdown_preview(result: dict[str, Any]) -> str:
    target = result["target"]
    preview = result["preview"]
    mutations = result["mutations"]
    return "\n".join([
        "## Curated Promotion Patch Preview",
        "",
        f"Status: {result['status']}",
        f"Mode: {result['mode']}",
        f"Project: {result['project']}",
        f"Proposal ID: {result['proposal_id']}",
        f"Target path: {target['path']}",
        f"Target heading: {target['heading']}",
        "",
        "### Meaning",
        "",
        "- This is a forge suggestion, not forge execution.",
        "- Patch preview is not trusted wiki mutation.",
        "- Human review is required before any future apply.",
        "",
        "### Unified diff",
        "",
        "```diff",
        result.get("unified_diff") or "",
        "```",
        "",
        "### Boundary",
        "",
        f"- Would write target file now: {preview['would_write_target_file']}",
        f"- Would promote to wiki now: {preview['would_promote_to_wiki']}",
        f"- Target file written now: {mutations['target_file_written']}",
        f"- Trusted wiki mutation now: {mutations['curated_wiki_mutated']}",
        f"- Database mutation now: {mutations['database_mutated']}",
        f"- Importer mutation now: {mutations['importer_mutated']}",
        "",
        "This is a Markdown preview only. M25.2 does not apply the patch.",
        "",
    ])


def print_patch_preview(result: dict[str, Any]) -> None:
    print("Curated Promotion Patch Preview")
    print("===============================")
    print(render_patch_markdown_preview(result))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Curated promotion patch dry-run helper.")
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--proposal-id", required=True)
    parser.add_argument("--target-path", required=True)
    parser.add_argument("--heading", required=True)
    parser.add_argument("--insert-text", required=True)
    parser.add_argument("--reason")
    parser.add_argument("--dry-run", action="store_true", required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--markdown", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(__file__).resolve().parents[2]
    result = build_promotion_patch_preview(root, args.project, args.proposal_id, args.target_path, args.heading, args.insert_text, args.reason)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    elif args.markdown:
        print(render_patch_markdown_preview(result))
    else:
        print_patch_preview(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
