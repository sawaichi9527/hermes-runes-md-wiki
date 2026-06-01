from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def write_manifest(
    manifest_dir: str | Path,
    operation_id: str,
    action: str,
    payload: dict[str, Any],
) -> Path:
    manifest_dir = Path(manifest_dir)
    manifest_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = manifest_dir / f"{operation_id}.json"
    doc = {
        "operation_id": operation_id,
        "action": action,
        "write_mode": "manifest-only",
        "created_at_local": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "payload": payload,
    }

    manifest_path.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest_path
