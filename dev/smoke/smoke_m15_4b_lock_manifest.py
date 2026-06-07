from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "importer"))

from forge.file_lock import FileLock, FileLockError
from forge.manifest_writer import write_manifest
from forge.operation_id import new_operation_id


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        lock_path = tmp_path / "locks" / "forge.lock"
        manifest_dir = tmp_path / "manifests"

        op_id = new_operation_id()
        assert op_id.startswith("op-")

        lock = FileLock(lock_path)
        lock.acquire(owner=op_id)
        assert lock_path.exists()

        blocked = False
        try:
            FileLock(lock_path).acquire(owner="second-owner")
        except FileLockError:
            blocked = True

        assert blocked, "second lock acquisition should be blocked"

        manifest_path = write_manifest(
            manifest_dir=manifest_dir,
            operation_id=op_id,
            action="m15.4b.lock_manifest.smoke",
            payload={
                "wiki_write": False,
                "index_update": False,
                "note_create": False,
                "lock_acquired": True,
            },
        )

        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert data["operation_id"] == op_id
        assert data["write_mode"] == "manifest-only"
        assert data["payload"]["wiki_write"] is False
        assert data["payload"]["lock_acquired"] is True

        lock.release()
        assert not lock_path.exists()

    print("PASS: M15.4b lock + manifest helper smoke")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
