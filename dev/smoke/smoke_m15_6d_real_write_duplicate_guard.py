from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_NOTE = ROOT / "wiki" / "sample-project" / "project-m15-6d-smoke-real-write-overview.md"


def run_create_flat(manifest_dir: Path, lock_path: Path) -> dict:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "tools" / "importer")

    cmd = [
        sys.executable,
        str(ROOT / "tools" / "importer" / "forge" / "create_flat.py"),
        "--project", "sample-project",
        "--title", "M15 6d Smoke Real Write",
        "--domain", "project",
        "--note-type", "overview",
        "--manifest-dir", str(manifest_dir),
        "--lock-path", str(lock_path),
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
    return json.loads(proc.stdout)


def main() -> int:
    if TEST_NOTE.exists():
        TEST_NOTE.unlink()

    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)

            first = run_create_flat(
                manifest_dir=tmp_path / "manifests-first",
                lock_path=tmp_path / "first.lock",
            )
            assert first["status"] == "PASS"
            assert first["mode"] == "real-write"
            assert first["plan"]["wiki_write"] is True
            assert first["plan"]["note_create"] is True
            assert first["plan"]["index_update"] is False
            assert TEST_NOTE.exists()

            second = run_create_flat(
                manifest_dir=tmp_path / "manifests-second",
                lock_path=tmp_path / "second.lock",
            )
            guard = second["plan"]["guard"]
            checks = guard["checks"]

            assert second["status"] == "PASS"
            assert second["mode"] == "dry-run"
            assert checks["planned_path_absent"] is False
            assert guard["ok_for_real_write"] is False
            assert second["plan"]["wiki_write"] is False
            assert second["plan"]["note_create"] is False
            assert second["plan"]["index_update"] is False
    finally:
        if TEST_NOTE.exists():
            TEST_NOTE.unlink()

    print("PASS: M15.6d real-write duplicate guard smoke")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
