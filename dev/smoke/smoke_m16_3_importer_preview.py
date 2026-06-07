from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    env = os.environ.copy()

    cmd = [
        sys.executable,
        str(ROOT / "tools" / "importer" / "importer_preview.py"),
        "--path", "wiki/sample-project/project-first-real-write-overview.md",
        "--path", "tmp/forge-manifests/example.json",
        "--json",
    ]

    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )

    data = json.loads(proc.stdout)

    assert data["status"] == "PASS"
    assert data["mode"] == "preview-only"
    assert data["db_write"] is False
    assert data["chunk_create"] is False
    assert data["index_update"] is False
    assert data["count"] == 2

    include_item = data["results"][0]
    assert include_item["include"] is True
    assert include_item["project"] == "sample-project"
    assert "eligible_markdown_wiki_file" in include_item["reasons"]

    exclude_item = data["results"][1]
    assert exclude_item["include"] is False
    assert "outside_wiki" in exclude_item["reasons"]

    print("PASS: M16.3 importer preview smoke")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
