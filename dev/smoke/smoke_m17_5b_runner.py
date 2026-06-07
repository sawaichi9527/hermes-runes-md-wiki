from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "importer" / "retrieval_regression_smoke.py"),
        "--json",
    ]

    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    data = json.loads(proc.stdout)

    assert data["read_only"] is True
    assert data["db_write"] is False
    assert data["chunk_create"] is False
    assert data["index_update"] is False
    assert data["importer_trigger"] is False
    assert data["git_write"] is False

    assert data["total"] >= 5
    assert isinstance(data["results"], list)

    for item in data["results"]:
        assert "id" in item
        assert "status" in item
        assert "query" in item
        assert "project" in item
        assert "blacklist_hits" in item

    print("PASS: M17.5b retrieval regression runner smoke")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
