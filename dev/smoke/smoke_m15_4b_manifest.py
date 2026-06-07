from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "importer"))

from forge.manifest_writer import write_manifest
from forge.operation_id import new_operation_id


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        manifest_dir = tmp_path / "manifests"

        op_id = new_operation_id()
        assert op_id.startswith("op-")

        manifest_path = write_manifest(
            manifest_dir=manifest_dir,
            operation_id=op_id,
            action="m15.4b.smoke",
            payload={
                "wiki_write": False,
                "index_update": False,
                "note_create": False,
            },
        )

        assert manifest_path.exists()

        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert data["operation_id"] == op_id
        assert data["write_mode"] == "manifest-only"
        assert data["payload"]["wiki_write"] is False

    print("PASS: M15.4b manifest helper smoke")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
