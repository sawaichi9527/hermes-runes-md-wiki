#!/usr/bin/env python3
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any


def build_manifest(
    *,
    operation_id: str,
    operation: str,
    project: str,
    write: bool,
    target_path: str,
    status: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "schema": "hermes.operation_manifest.v1",
        "operation_id": operation_id,
        "operation": operation,
        "project": project,
        "write": write,
        "target_path": target_path,
        "status": status,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "extra": extra or {},
    }


def write_manifest(root: Path, manifest: dict[str, Any]) -> Path:
    op_id = manifest["operation_id"]
    out_dir = root / "var" / "operations"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / f"{op_id}.json"
    tmp_path = out_dir / f".{op_id}.json.tmp"

    tmp_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    tmp_path.replace(out_path)
    return out_path
