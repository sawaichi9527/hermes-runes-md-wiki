from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from forge.file_lock import FileLock
from forge.manifest_writer import write_manifest
from forge.operation_id import new_operation_id


ALLOWED_PROJECTS = {"sample-project", "k6-freelancer"}


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


def pre_write_guard(
    root: Path,
    plan: dict,
    project: str,
    execute: bool,
    allow_real_write: bool,
) -> dict:
    planned_path = root / plan["planned_path"]
    parent_dir = planned_path.parent
    real_write_enabled = execute and allow_real_write

    checks = {
        "allowed_project": project in ALLOWED_PROJECTS,
        "parent_dir_exists": parent_dir.exists(),
        "planned_path_absent": not planned_path.exists(),
        "execute_requested": execute,
        "allow_real_write_requested": allow_real_write,
        "real_write_enabled": real_write_enabled,
    }

    return {
        "checks": checks,
        "ok_for_real_write": all([
            checks["allowed_project"],
            checks["parent_dir_exists"],
            checks["planned_path_absent"],
            checks["execute_requested"],
            checks["allow_real_write_requested"],
            checks["real_write_enabled"],
        ]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Forge flat note planner. Dry-run by default.")
    parser.add_argument("--project", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--note-type", required=True)
    parser.add_argument("--manifest-dir", default="tmp/forge-manifests")
    parser.add_argument("--lock-path", default="tmp/forge.lock")
    parser.add_argument("--execute", action="store_true", help="Request real-write mode.")
    parser.add_argument("--allow-real-write", action="store_true", help="Second confirmation switch for future writes.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path.cwd()
    op_id = new_operation_id()
    lock = FileLock(args.lock_path)

    lock.acquire(owner=op_id)
    try:
        plan = build_note_plan(args.project, args.title, args.domain, args.note_type)
        guard = pre_write_guard(
            root=root,
            plan=plan,
            project=args.project,
            execute=args.execute,
            allow_real_write=args.allow_real_write,
        )
        plan["guard"] = guard

        manifest_path = write_manifest(
            manifest_dir=args.manifest_dir,
            operation_id=op_id,
            action="forge.create-flat.real-write-switch-guard",
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
