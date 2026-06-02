#!/usr/bin/env python3
"""M22.2 read-only proposal list/show helper.

This module inspects governed proposal files without mutating proposal state,
trusted wiki content, importer artifacts, or database/index records.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "m22.2.p0.v1"
DEFAULT_PROJECT = "k6-freelancer"
STATE_DIRS = {
    "draft": ["forge-inbox", "proposals/draft"],
    "approved": ["proposals/approved"],
    "rejected": ["proposals/rejected"],
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def safe_project(project: str) -> str:
    project = project.strip()
    if not re.fullmatch(r"[a-zA-Z0-9._-]+", project):
        raise ValueError(f"unsafe project name: {project!r}")
    return project


def parse_frontmatter_and_body(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, text
    raw_meta = parts[1]
    body = parts[2]
    meta: dict[str, str] = {}
    for line in raw_meta.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, body.strip()


def proposal_roots(root: Path, project: str, output_root: str | None = None) -> list[tuple[str, Path]]:
    project = safe_project(project)
    if output_root:
        base = Path(output_root).expanduser().resolve() / project
    else:
        base = root / "wiki" / project

    result: list[tuple[str, Path]] = []
    for state, rels in STATE_DIRS.items():
        for rel in rels:
            result.append((state, base / rel))
    return result


def read_summary(path: Path, state: str, root: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter_and_body(text)
    rel_path = str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
    return {
        "proposal_id": meta.get("proposal_id") or path.stem,
        "title": meta.get("title") or path.stem,
        "state": state,
        "metadata_status": meta.get("status"),
        "trusted_memory": meta.get("trusted_memory"),
        "project": meta.get("project"),
        "created_at": meta.get("created_at"),
        "source_context": meta.get("source_context"),
        "path": str(path),
        "relative_path": rel_path,
        "body_chars": len(body),
    }


def list_proposals(root: Path, project: str, state_filter: str = "all", output_root: str | None = None) -> dict[str, Any]:
    if state_filter not in {"all", "draft", "approved", "rejected"}:
        raise ValueError("state must be one of: all, draft, approved, rejected")

    items: list[dict[str, Any]] = []
    for state, directory in proposal_roots(root, project, output_root):
        if state_filter != "all" and state != state_filter:
            continue
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.md")):
            items.append(read_summary(path, state, root))

    return {
        "schema_version": SCHEMA_VERSION,
        "suite": "M22.2 Read-only proposal list",
        "command": "proposal list",
        "status": "PASS",
        "mode": "read_only",
        "project": project,
        "state_filter": state_filter,
        "count": len(items),
        "items": items,
        "mutations": {
            "proposal_state_mutated": False,
            "trusted_memory_created": False,
            "curated_wiki_mutated": False,
            "database_mutated": False,
            "importer_mutated": False,
        },
    }


def resolve_proposal(root: Path, project: str, proposal_id: str, output_root: str | None = None) -> tuple[str, Path] | None:
    wanted = proposal_id[:-3] if proposal_id.endswith(".md") else proposal_id
    for state, directory in proposal_roots(root, project, output_root):
        candidates = []
        if directory.exists():
            candidates.extend(directory.glob(f"{wanted}.md"))
            candidates.extend(path for path in directory.glob("*.md") if path.stem == wanted)
        for path in candidates:
            if path.exists():
                return state, path
    return None


def show_proposal(root: Path, project: str, proposal_id: str, output_root: str | None = None, include_body: bool = True) -> dict[str, Any]:
    resolved = resolve_proposal(root, project, proposal_id, output_root)
    if not resolved:
        return {
            "schema_version": SCHEMA_VERSION,
            "suite": "M22.2 Read-only proposal show",
            "command": "proposal show",
            "status": "NOT_FOUND",
            "mode": "read_only",
            "project": project,
            "proposal_id": proposal_id,
            "mutations": {
                "proposal_state_mutated": False,
                "trusted_memory_created": False,
                "curated_wiki_mutated": False,
                "database_mutated": False,
                "importer_mutated": False,
            },
        }

    state, path = resolved
    text = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter_and_body(text)
    summary = read_summary(path, state, root)
    return {
        "schema_version": SCHEMA_VERSION,
        "suite": "M22.2 Read-only proposal show",
        "command": "proposal show",
        "status": "PASS",
        "mode": "read_only",
        "project": project,
        "proposal": summary,
        "metadata": meta,
        "body": body if include_body else None,
        "body_included": include_body,
        "mutations": {
            "proposal_state_mutated": False,
            "trusted_memory_created": False,
            "curated_wiki_mutated": False,
            "database_mutated": False,
            "importer_mutated": False,
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read-only governed proposal list/show helper.")
    sub = parser.add_subparsers(dest="command", required=True)

    list_cmd = sub.add_parser("list", help="List proposals without mutating them.")
    list_cmd.add_argument("--project", default=DEFAULT_PROJECT)
    list_cmd.add_argument("--state", default="all", choices=["all", "draft", "approved", "rejected"])
    list_cmd.add_argument("--output-root", help="Optional alternate proposal root for sandbox/smoke reads.")
    list_cmd.add_argument("--json", action="store_true")

    show_cmd = sub.add_parser("show", help="Show one proposal without mutating it.")
    show_cmd.add_argument("--project", default=DEFAULT_PROJECT)
    show_cmd.add_argument("--id", required=True, help="Proposal id or filename.")
    show_cmd.add_argument("--output-root", help="Optional alternate proposal root for sandbox/smoke reads.")
    show_cmd.add_argument("--no-body", action="store_true", help="Omit body from JSON output.")
    show_cmd.add_argument("--json", action="store_true")

    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = repo_root()
    try:
        if args.command == "list":
            result = list_proposals(root, args.project, args.state, args.output_root)
        elif args.command == "show":
            result = show_proposal(root, args.project, args.id, args.output_root, include_body=not args.no_body)
        else:  # pragma: no cover
            raise ValueError(f"unsupported command: {args.command}")
    except Exception as exc:
        result = {
            "schema_version": SCHEMA_VERSION,
            "suite": "M22.2 Read-only proposal reader",
            "status": "FAIL",
            "mode": "read_only",
            "error": str(exc),
        }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"{result.get('suite')}: {result.get('status')}")
        if "count" in result:
            print(f"count={result['count']}")
        print("Use --json for details.")

    return 0 if result.get("status") in {"PASS", "NOT_FOUND"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
