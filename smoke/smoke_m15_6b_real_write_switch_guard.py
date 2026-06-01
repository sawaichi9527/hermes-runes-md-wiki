from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_case(manifest_dir: Path, lock_path: Path, extra_args: list[str]) -> dict:
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
        *extra_args,
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


def assert_no_wiki_note(data: dict) -> None:
    planned_note = ROOT / data["plan"]["planned_path"]
    assert not planned_note.exists(), "guard smoke must not create wiki note"


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        execute_only = run_case(
            manifest_dir=tmp_path / "manifests-execute-only",
            lock_path=tmp_path / "execute-only.lock",
            extra_args=["--execute"],
        )
        checks = execute_only["plan"]["guard"]["checks"]
        assert execute_only["status"] == "PASS"
        assert execute_only["mode"] == "dry-run"
        assert checks["execute_requested"] is True
        assert checks["allow_real_write_requested"] is False
        assert checks["real_write_enabled"] is False
        assert execute_only["plan"]["guard"]["ok_for_real_write"] is False
        assert execute_only["plan"]["wiki_write"] is False
        assert execute_only["plan"]["index_update"] is False
        assert execute_only["plan"]["note_create"] is False
        assert_no_wiki_note(execute_only)

        double_confirm = run_case(
            manifest_dir=tmp_path / "manifests-double-confirm",
            lock_path=tmp_path / "double-confirm.lock",
            extra_args=["--execute", "--allow-real-write"],
        )
        checks = double_confirm["plan"]["guard"]["checks"]
        assert double_confirm["status"] == "PASS"
        assert double_confirm["mode"] == "dry-run"
        assert checks["execute_requested"] is True
        assert checks["allow_real_write_requested"] is True
        assert checks["real_write_enabled"] is True
        assert double_confirm["plan"]["guard"]["ok_for_real_write"] is True
        assert double_confirm["plan"]["wiki_write"] is False
        assert double_confirm["plan"]["index_update"] is False
        assert double_confirm["plan"]["note_create"] is False
        assert_no_wiki_note(double_confirm)

    print("PASS: M15.6b real-write switch guard smoke")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
