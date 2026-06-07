#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import psycopg

from db_config import build_conninfo
from root_resolver import resolve_root

PROJECT = "freelancer"
TARGET_PATH = "wiki/freelancer/trial-promotion-fixtures.md"
MARKER = "M137 beta-prep trial promotion fixture marker"


def run_importer(root: Path) -> dict[str, object]:
    env = os.environ.copy()
    env["HERMES_MEMORY_ROOT"] = str(root)
    env["HERMES_IMPORT_WORKSPACE_SLUG"] = PROJECT
    env["HERMES_WORKSPACE_SLUG"] = PROJECT
    env["HERMES_PROJECT"] = PROJECT

    proc = subprocess.run(
        [sys.executable, "importer.py"],
        cwd=str(root / "tools" / "importer"),
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return {
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-4000:],
        "stderr_tail": proc.stderr[-2000:],
    }


def query_marker() -> dict[str, object]:
    rows = []
    with psycopg.connect(build_conninfo()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                  d.id AS document_id,
                  d.project,
                  d.source_path,
                  c.id AS chunk_id,
                  c.chunk_index,
                  c.section_heading
                FROM public.documents d
                JOIN public.chunks c ON c.document_id = d.id
                WHERE d.project = %s
                  AND d.source_path = %s
                  AND c.content ILIKE %s
                  AND d.is_deleted = false
                ORDER BY c.chunk_index, c.id
                LIMIT 10;
                """,
                (PROJECT, TARGET_PATH, f"%{MARKER}%"),
            )
            for row in cur.fetchall():
                rows.append(
                    {
                        "document_id": row[0],
                        "project": row[1],
                        "path": row[2],
                        "chunk_id": row[3],
                        "chunk_index": row[4],
                        "section_heading": row[5],
                    }
                )
    return {"row_count": len(rows), "rows": rows}


def main() -> int:
    root = resolve_root()
    target = root / TARGET_PATH
    result: dict[str, object] = {
        "suite": "M139.2 Local Import and Recall Verification",
        "project": PROJECT,
        "target_path": TARGET_PATH,
        "marker": MARKER,
        "root": str(root),
        "target_exists": target.exists(),
        "status": "UNKNOWN",
        "failures": [],
    }

    if not target.exists():
        result["status"] = "FAIL"
        result["failures"] = ["target_missing"]
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    text = target.read_text(encoding="utf-8")
    if MARKER not in text:
        result["status"] = "FAIL"
        result["failures"] = ["marker_missing_in_markdown"]
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    import_result = run_importer(root)
    result["import_result"] = import_result
    if import_result["returncode"] != 0:
        result["status"] = "FAIL"
        result["failures"] = ["importer_failed"]
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    marker_result = query_marker()
    result["marker_result"] = marker_result

    failures = []
    if marker_result["row_count"] < 1:
        failures.append("marker_not_found_in_index")

    result["failures"] = failures
    result["status"] = "PASS" if not failures else "FAIL"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
