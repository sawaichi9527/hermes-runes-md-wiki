from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_NOTE = ROOT / "wiki" / "sample-project" / "project-m16-4-changed-files-preview-overview.md"


def main() -> int:
    if TEST_NOTE.exists():
        TEST_NOTE.unlink()

    try:
        TEST_NOTE.write_text(
            "---\n"
            "title: M16.4 Changed Files Preview\n"
            "project: sample-project\n"
            "domain: project\n"
            "note_type: overview\n"
            "status: draft\n"
            "---\n\n"
            "# M16.4 Changed Files Preview\n\n"
            "Temporary smoke note for changed-files preview.\n",
            encoding="utf-8",
        )

        env = os.environ.copy()
        cmd = [
            sys.executable,
            str(ROOT / "tools" / "importer" / "importer_preview.py"),
            "--changed-files",
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

        target_path = "wiki/sample-project/project-m16-4-changed-files-preview-overview.md"
        matches = [item for item in data["results"] if item["path"] == target_path]
        assert matches, "changed-files preview should include temporary smoke note"

        item = matches[0]
        assert item["include"] is True
        assert item["project"] == "sample-project"
        assert "eligible_markdown_wiki_file" in item["reasons"]
        assert item["db_write"] is False
        assert item["chunk_create"] is False
        assert item["index_update"] is False
    finally:
        if TEST_NOTE.exists():
            TEST_NOTE.unlink()

    print("PASS: M16.4 changed-files preview smoke")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
