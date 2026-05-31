#!/usr/bin/env python3
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


def get_columns(cur, schema: str, table: str):
    cur.execute(
        """
        select
          column_name,
          data_type,
          is_nullable,
          column_default
        from information_schema.columns
        where table_schema = %s and table_name = %s
        order by ordinal_position
        """,
        (schema, table),
    )
    return [
        {
            "name": row[0],
            "type": row[1],
            "nullable": row[2],
            "default": row[3],
        }
        for row in cur.fetchall()
    ]


def column_names(cols):
    return {c["name"] for c in cols}


def pick(cols, candidates):
    names = column_names(cols)
    for c in candidates:
        if c in names:
            return c
    return None


def main() -> int:
    schema = safe_ident(os.getenv("HERMES_MEMORY_SCHEMA", "public"))
    dsn = get_dsn()

    report = {
        "suite": "M6.4a metadata schema inspection",
        "root": str(ROOT),
        "schema": schema,
        "status": "UNKNOWN",
        "tables": {},
        "inferred": {},
        "documents": [],
        "notes": [],
    }

    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            for table in ("documents", "chunks", "document_chunks"):
                if not table_exists(cur, schema, table):
                    report["tables"][table] = {"exists": False, "columns": []}
                    continue

                cols = get_columns(cur, schema, table)
                report["tables"][table] = {"exists": True, "columns": cols}

            if not report["tables"].get("documents", {}).get("exists"):
                report["status"] = "FAIL"
                report["notes"].append(f"{schema}.documents not found")
                print(json.dumps(report, ensure_ascii=False, indent=2))
                return 1

            doc_cols = report["tables"]["documents"]["columns"]
            doc_id_col = pick(doc_cols, ["id", "document_id", "doc_id"])
            project_col = pick(doc_cols, ["project", "project_id", "namespace"])
            path_col = pick(doc_cols, ["path", "source_path", "file_path"])

            chunk_table = None
            for t in ("chunks", "document_chunks"):
                if report["tables"].get(t, {}).get("exists"):
                    chunk_table = t
                    break

            chunk_doc_ref_col = None
            if chunk_table:
                chunk_cols = report["tables"][chunk_table]["columns"]
                chunk_doc_ref_col = pick(chunk_cols, ["document_id", "doc_id"])

            report["inferred"] = {
                "document_id_column": doc_id_col,
                "project_column": project_col,
                "path_column": path_col,
                "chunk_table": chunk_table,
                "chunk_document_ref_column": chunk_doc_ref_col,
            }

            if not doc_id_col or not path_col:
                report["status"] = "FAIL"
                report["notes"].append("cannot infer document id/path columns")
                print(json.dumps(report, ensure_ascii=False, indent=2))
                return 1

            if chunk_table and chunk_doc_ref_col:
                project_select = project_col if project_col else "null"
                cur.execute(
                    f"""
                    select
                      d.{doc_id_col} as document_id,
                      {f'd.{project_col}' if project_col else 'null'} as project,
                      d.{path_col} as path,
                      count(c.*) as chunks
                    from {schema}.documents d
                    left join {schema}.{chunk_table} c
                      on c.{chunk_doc_ref_col} = d.{doc_id_col}
                    group by d.{doc_id_col}, {f'd.{project_col}' if project_col else 'null'}, d.{path_col}
                    order by d.{path_col}
                    """
                )
            else:
                cur.execute(
                    f"""
                    select
                      d.{doc_id_col} as document_id,
                      {f'd.{project_col}' if project_col else 'null'} as project,
                      d.{path_col} as path,
                      0 as chunks
                    from {schema}.documents d
                    order by d.{path_col}
                    """
                )

            for row in cur.fetchall():
                report["documents"].append(
                    {
                        "document_id": row[0],
                        "project": row[1],
                        "path": row[2],
                        "chunks": row[3],
                    }
                )

    missing = []
    for key, value in report["inferred"].items():
        if value is None and key in ("document_id_column", "project_column", "path_column", "chunk_table", "chunk_document_ref_column"):
            missing.append(key)

    if missing:
        report["status"] = "WARN"
        report["notes"].append(f"some metadata fields could not be inferred: {missing}")
    else:
        report["status"] = "PASS"

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
