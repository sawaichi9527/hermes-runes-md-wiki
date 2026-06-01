#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from operation_manifest import build_manifest
from write_guard import assert_p0_write_allowed, new_operation_id


def slugify(title: str) -> str:
    text = title.strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "untitled"


def build_content(*, title: str, project: str, operation_id: str, body: str) -> str:
    body = body.strip() or "TODO: fill content."
    return f"""---
title: {title}
project: {project}
status: draft
source: forge.create-flat
operation_id: {operation_id}
---

# {title}

{body}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="P0 forge create-flat MVP")
    parser.add_argument("--project", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", default="")
    parser.add_argument("--root", default=str(Path.cwd()))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    op_id = new_operation_id("forge")
    slug = slugify(args.title)
    target = root / "wiki" / args.project / "forge-inbox" / f"{slug}-{op_id}.md"

    assert_p0_write_allowed(root, target, args.project)

    content = build_content(
        title=args.title,
        project=args.project,
        operation_id=op_id,
        body=args.body,
    )

    manifest = build_manifest(
        operation_id=op_id,
        operation="forge.create-flat",
        project=args.project,
        write=False,
        target_path=str(target.relative_to(root)),
        status="DRY_RUN",
        extra={
            "title": args.title,
            "slug": slug,
            "content_chars": len(content),
        },
    )

    result = {
        "status": "PASS",
        "operation": "forge.create-flat",
        "write": False,
        "dry_run": True,
        "operation_id": op_id,
        "planned_path": str(target.relative_to(root)),
        "planned_content_preview": content,
        "manifest_preview": manifest,
    }

    if not args.dry_run:
        result["status"] = "FAIL"
        result["error"] = "M18.2 supports --dry-run only"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"PASS dry-run planned_path={result['planned_path']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
