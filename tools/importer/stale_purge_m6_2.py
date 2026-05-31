#!/usr/bin/env python3
import argparse
import json
import os
import re
from pathlib import Path

import psycopg

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None


ROOT = Path(os.getenv("HERMES_MEMORY_ROOT", str(Path.home() / "workspace" / "hermes-memory"))).resolve()
IMPORTER_DIR = ROOT / "tools" / "importer"
ENV_FILE = IMPORTER_DIR / ".env"

if load_dotenv is not None and ENV_FILE.exists():
    load_dotenv(ENV_FILE)


def safe_ident(value: str) -> str:
    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", value):
        raise ValueError(f"unsafe SQL identifier: {value}")
    return value


def get_dsn() -> str:
    for key in ("DATABASE_URL", "POSTGRES_DSN", "PG_DSN", "HERMES_MEMORY_DATABASE_URL"):
        value = os.getenv(key)
        if value:
            return value

    host = os.getenv("PGHOST") or os.getenv("POSTGRES_HOST")
    port = os.getenv("PGPORT") or os.getenv("POSTGRES_PORT") or "5432"
    dbname = os.getenv("PGDATABASE") or os.getenv("POSTGRES_DB")
    user = os.getenv("PGUSER") or os.getenv("POSTGRES_USER")
    password = os.getenv("PGPASSWORD") or os.getenv("POSTGRES_PASSWORD")

    if host and dbname and user:
        parts = [f"host={host}", f"port={port}", f"dbname={dbname}", f"user={user}"]
        if password:
            parts.append(f"password={password}")
        return " ".join(parts)

    raise RuntimeError("No PostgreSQL DSN found")


def table_exists(cur, schema: str, table: str) -> bool:
    cur.execute(
        """
        select 1
        from information_schema.tables
        where table_schema = %s and table_name = %s
        limit 1
        """,
        (schema, table),
    )
    return cur.fetchone() is not None


def columns(cur, schema: str, table: str) -> set[str]:
    cur.execute(
        """
        select column_name
        from information_schema.columns
        where table_schema = %s and table_name = %s
        """,
        (schema, table),
    )
    return {row[0] for row in cur.fetchall()}


def pick_column(cols: set[str], candidates: list[str]) -> str | None:
    for name in candidates:
        if name in cols:
            return name
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="M6.2c purge stale Hermes Memory documents. Default is dry-run."
    )
    parser.add_argument("--apply", action="store_true", help="Actually delete stale DB rows.")
    args = parser.parse_args()

    schema = safe_ident(os.getenv("HERMES_MEMORY_SCHEMA", "public"))
    dsn = get_dsn()

    report = {
        "suite": "M6.2c stale purge",
        "mode": "apply" if args.apply else "dry-run",
        "root": str(ROOT),
        "schema": schema,
        "status": "UNKNOWN",
        "stale_documents": [],
        "deleted_chunks": 0,
        "deleted_documents": 0,
        "notes": [],
    }

    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            if not table_exists(cur, schema, "documents"):
                report["status"] = "FAIL"
                report["notes"].append(f"table not found: {schema}.documents")
                print(json.dumps(report, ensure_ascii=False, indent=2))
                return 1

            doc_cols = columns(cur, schema, "documents")
            id_col = pick_column(doc_cols, ["id", "document_id", "doc_id"])
            path_col = pick_column(doc_cols, ["path", "source_path", "file_path"])
            project_col = pick_column(doc_cols, ["project", "project_id", "namespace"])

            if not id_col or not path_col:
                report["status"] = "FAIL"
                report["notes"].append(f"cannot infer documents id/path columns: {sorted(doc_cols)}")
                print(json.dumps(report, ensure_ascii=False, indent=2))
                return 1

            select_cols = [id_col, path_col]
            if project_col:
                select_cols.append(project_col)

            cur.execute(
                f"""
                select {", ".join(select_cols)}
                from {schema}.documents
                where {path_col} like 'wiki/%' or {path_col} like '%.md'
                order by {path_col}
                """
            )

            stale_doc_ids = []
            for row in cur.fetchall():
                doc_id = row[0]
                path = row[1]
                project = row[2] if project_col and len(row) > 2 else None

                if not path:
                    continue

                if not (ROOT / path).exists():
                    stale_doc_ids.append(doc_id)
                    report["stale_documents"].append(
                        {
                            "document_id": doc_id,
                            "project": project,
                            "path": path,
                            "reason": "db path no longer exists on filesystem",
                        }
                    )

            if not stale_doc_ids:
                report["status"] = "PASS"
                report["notes"].append("no stale documents found")
                print(json.dumps(report, ensure_ascii=False, indent=2))
                return 0

            if not args.apply:
                report["status"] = "DRY_RUN"
                report["notes"].append("stale documents found; rerun with --apply to purge")
                print(json.dumps(report, ensure_ascii=False, indent=2))
                return 0

            chunk_tables = ["chunks", "document_chunks"]
            for table in chunk_tables:
                if not table_exists(cur, schema, table):
                    continue

                chunk_cols = columns(cur, schema, table)
                doc_ref_col = pick_column(chunk_cols, ["document_id", "doc_id"])

                if not doc_ref_col:
                    continue

                cur.execute(
                    f"delete from {schema}.{table} where {doc_ref_col} = any(%s)",
                    (stale_doc_ids,),
                )
                report["deleted_chunks"] += cur.rowcount

            cur.execute(
                f"delete from {schema}.documents where {id_col} = any(%s)",
                (stale_doc_ids,),
            )
            report["deleted_documents"] = cur.rowcount

        conn.commit()

    report["status"] = "APPLIED"
    report["notes"].append("stale documents purged")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
