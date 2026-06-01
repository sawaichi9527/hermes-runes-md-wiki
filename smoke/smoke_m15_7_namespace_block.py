from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET_NOTE = ROOT / "wiki" / "k6-freelancer" / "project-m15-7-block-test-overview.md"


def main() -> int:
    if TARGET_NOTE.exists():
        raise RuntimeError("unexpected pre-existing target note")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT / "tools" / "importer")

        cmd = [
            sys.executable,
            str(ROOT / "tools" / "importer" / "forge" / "create_flat.py"),
            "--project", "k6-freelancer",
            "--title", "M15 7 Block Test",
            "--domain", "project",
            "--note-type", "overview",
            "--manifest-dir", str(tmp_path / "manifests"),
            "--lock-path", str(tmp_path / "forge.lock"),
            "--execute",
            "--allow-real-write",
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
        checks = data["plan"]["guard"]["checks"]

        assert data["status"] == "PASS"
        assert data["mode"] == "dry-run"
        assert checks["allowed_project"] is True
        assert checks["real_write_project_allowed"] is False
        assert checks["real_write_blocked_by_namespace"] is True
        assert checks["execute_requested"] is True
        assert checks["allow_real_write_requested"] is True
        assert checks["real_write_enabled"] is False
        assert data["plan"]["guard"]["ok_for_real_write"] is False
        assert data["plan"]["wiki_write"] is False
        assert data["plan"]["note_create"] is False
        assert data["plan"]["index_update"] is False
        assert not TARGET_NOTE.exists(), "k6-freelancer must remain blocked"

    print("PASS: M15.7 namespace block smoke")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
