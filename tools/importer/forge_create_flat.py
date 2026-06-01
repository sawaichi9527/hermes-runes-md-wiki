#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from operation_manifest import build_manifest, write_manifest
from write_guard import (
    assert_p0_write_allowed,
    file_lock,
    new_operation_id,
)


def slugify(title: str) -> str:
    text = title.strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "untitled"


def build_content(
    *,
    title: str,
    project: str,
    operation_id: str,
    body: str,
    proposal_type: str,
    proposed_by: str,
    provenance: str,
    confidence: str,
    trust_class: str,
) -> str:
    body = body.strip() or "TODO: fill content."

    return f"""---
title: {title}
project: {project}
status: draft
source: forge.create-flat
operation_id: {operation_id}
proposal_type: {proposal_type}
proposed_by: {proposed_by}
provenance: {provenance}
confidence: {confidence}
trust_class: {trust_class}
---

# {title}

{body}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="P0 forge create-flat MVP")

    parser.add_argument("--project", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", default="")
    parser.add_argument("--proposal-type", default="manual_note")
    parser.add_argument("--proposed-by", default="human")
    parser.add_argument("--provenance", default="manual_cli")
    parser.add_argument("--confidence", default="1.0")
    parser.add_argument("--trust-class", default="human-reviewed")
    parser.add_argument("--root", default=str(Path.cwd()))

    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")

    args = parser.parse_args()

    if args.dry_run and args.write:
        raise SystemExit("cannot use --dry-run and --write together")

    root = Path(args.root).resolve()

    op_id = new_operation_id("forge")

    slug = slugify(args.title)

    target = (
        root
        / "wiki"
        / args.project
        / "forge-inbox"
        / f"{slug}-{op_id}.md"
    )

    assert_p0_write_allowed(root, target, args.project)

    content = build_content(
        title=args.title,
        project=args.project,
        operation_id=op_id,
        body=args.body,
        proposal_type=args.proposal_type,
        proposed_by=args.proposed_by,
        provenance=args.provenance,
        confidence=args.confidence,
        trust_class=args.trust_class,
    )

    if args.dry_run:
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
                "proposal_type": args.proposal_type,
                "proposed_by": args.proposed_by,
                "provenance": args.provenance,
                "confidence": args.confidence,
                "trust_class": args.trust_class,
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

        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if not args.write:
        raise SystemExit("must specify either --dry-run or --write")

    lock_path = root / "var" / "locks" / "forge.lock"

    with file_lock(lock_path):
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

        manifest = build_manifest(
            operation_id=op_id,
            operation="forge.create-flat",
            project=args.project,
            write=True,
            target_path=str(target.relative_to(root)),
            status="PASS",
            extra={
                "title": args.title,
                "slug": slug,
                "content_chars": len(content),
                "proposal_type": args.proposal_type,
                "proposed_by": args.proposed_by,
                "provenance": args.provenance,
                "confidence": args.confidence,
                "trust_class": args.trust_class,
            },
        )

        manifest_path = write_manifest(root, manifest)

    result = {
        "status": "PASS",
        "operation": "forge.create-flat",
        "write": True,
        "dry_run": False,
        "operation_id": op_id,
        "written_path": str(target.relative_to(root)),
        "manifest_path": str(manifest_path.relative_to(root)),
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"PASS wrote {result['written_path']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
