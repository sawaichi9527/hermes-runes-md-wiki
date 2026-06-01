#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from operation_manifest import build_manifest, write_manifest
from write_guard import assert_p0_write_allowed, file_lock, new_operation_id


STATUS_PATTERN = re.compile(
    r"^(status:\s*)(.+?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def approve_content(content: str) -> tuple[str, str, str]:
    match = STATUS_PATTERN.search(content)

    if not match:
        raise SystemExit("missing status field")

    old_status = match.group(2).strip()
    new_content = STATUS_PATTERN.sub(r"\1approved", content, count=1)

    return new_content, old_status, "approved"


def main() -> int:
    parser = argparse.ArgumentParser(description="Approve P0 forge-inbox note")
    parser.add_argument("--path", required=True)
    parser.add_argument("--root", default=str(Path.cwd()))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    target = (root / args.path).resolve()
    project = target.relative_to(root).parts[1]

    assert_p0_write_allowed(root, target, project)

    if not target.exists():
        raise SystemExit(f"target not found: {target}")

    op_id = new_operation_id("forge-approve")
    lock_path = root / "var" / "locks" / "forge.lock"

    with file_lock(lock_path):
        old_content = target.read_text(encoding="utf-8")
        new_content, old_status, new_status = approve_content(old_content)
        target.write_text(new_content, encoding="utf-8")

        manifest = build_manifest(
            operation_id=op_id,
            operation="forge.approve",
            project=project,
            write=True,
            target_path=str(target.relative_to(root)),
            status="PASS",
            extra={
                "old_status": old_status,
                "new_status": new_status,
            },
        )

        manifest_path = write_manifest(root, manifest)

    result = {
        "status": "PASS",
        "operation": "forge.approve",
        "write": True,
        "operation_id": op_id,
        "path": str(target.relative_to(root)),
        "old_status": old_status,
        "new_status": new_status,
        "manifest_path": str(manifest_path.relative_to(root)),
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"PASS approved {result['path']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
