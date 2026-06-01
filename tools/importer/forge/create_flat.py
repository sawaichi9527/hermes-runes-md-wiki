from __future__ import annotations

import argparse
import json
import re

from forge.file_lock import FileLock
from forge.manifest_writer import write_manifest
from forge.operation_id import new_operation_id


def slugify(text: str) -> str:
    slug = text.strip().lower()
    slug = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "untitled"


def build_note_plan(project: str, title: str, domain: str, note_type: str) -> dict:
    slug = slugify(title)
    filename = f"{domain}-{slug}-{note_type}.md"
    path = f"wiki/{project}/{filename}"

    body = f"""---
title: {title}
project: {project}
domain: {domain}
note_type: {note_type}
status: draft
---

# {title}

## Objective

TBD.

## Notes

TBD.
"""

    return {
        "planned_path": path,
        "metadata": {
            "title": title,
            "project": project,
            "domain": domain,
            "note_type": note_type,
            "status": "draft",
        },
        "body_preview": body,
        "wiki_write": False,
        "index_update": False,
        "note_create": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Forge flat note planner. Dry-run only.")
    parser.add_argument("--project", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--note-type", required=True)
    parser.add_argument("--manifest-dir", default="tmp/forge-manifests")
    parser.add_argument("--lock-path", default="tmp/forge.lock")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    op_id = new_operation_id()
    lock = FileLock(args.lock_path)

    lock.acquire(owner=op_id)
    try:
        plan = build_note_plan(args.project, args.title, args.domain, args.note_type)
        manifest_path = write_manifest(
            manifest_dir=args.manifest_dir,
            operation_id=op_id,
            action="forge.create-flat.dry-run",
            payload=plan,
        )

        result = {
            "status": "PASS",
            "mode": "dry-run",
            "operation_id": op_id,
            "manifest_path": str(manifest_path),
            "plan": plan,
        }

        print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else result)
    finally:
        lock.release()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
