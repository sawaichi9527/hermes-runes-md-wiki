from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        manifest_dir = tmp_path / "manifests"
        lock_path = tmp_path / "forge.lock"

        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT / "tools" / "importer")

        cmd = [
            sys.executable,
            str(ROOT / "tools" / "importer" / "forge" / "create_flat.py"),
            "--project", "sample-project",
            "--title", "Sample Project",
            "--domain", "project",
            "--note-type", "overview",
            "--manifest-dir", str(manifest_dir),
            "--lock-path", str(lock_path),
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
        assert data["mode"] == "dry-run"
        assert data["plan"]["planned_path"] == "wiki/sample-project/project-sample-project-overview.md"
        assert data["plan"]["wiki_write"] is False
        assert data["plan"]["index_update"] is False
        assert data["plan"]["note_create"] is False

        manifest_path = Path(data["manifest_path"])
        assert manifest_path.exists()

        planned_note = ROOT / data["plan"]["planned_path"]
        assert not planned_note.exists(), "dry-run must not create wiki note"

    print("PASS: M15.5 forge create-flat dry-run smoke")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
