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
    for key in (
        "DATABASE_URL",
        "POSTGRES_DSN",
        "PG_DSN",
        "HERMES_MEMORY_DATABASE_URL",
    ):
        value = os.getenv(key)
        if value:
            return value

    host = os.getenv("PGHOST") or os.getenv("POSTGRES_HOST")
    port = os.getenv("PGPORT") or os.getenv("POSTGRES_PORT") or "5432"
    dbname = os.getenv("PGDATABASE") or os.getenv("POSTGRES_DB")
    user = os.getenv("PGUSER") or os.getenv("POSTGRES_USER")
    password = os.getenv("PGPASSWORD") or os.getenv("POSTGRES_PASSWORD")

    if host and dbname and user:
        parts = [
            f"host={host}",
            f"port={port}",
            f"dbname={dbname}",
            f"user={user}",
        ]
        if password:
            parts.append(f"password={password}")
        return " ".join(parts)

    raise RuntimeError(
        "No PostgreSQL DSN found. Expected DATABASE_URL / POSTGRES_DSN / PG_DSN "
        "or PGHOST+PGDATABASE+PGUSER in tools/importer/.env"
    )


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


def list_local_markdown() -> set[str]:
    wiki_dir = ROOT / "wiki"
    if not wiki_dir.exists():
        return set()

    paths = set()
    for p in wiki_dir.rglob("*.md"):
        if p.is_file():
            paths.add(str(p.relative_to(ROOT)))
    return paths


def main() -> int:
    schema = safe_ident(os.getenv("HERMES_MEMORY_SCHEMA", "public"))
    dsn = get_dsn()
    local_paths = list_local_markdown()

    report = {
        "suite": "M6.2a stale report",
        "root": str(ROOT),
        "schema": schema,
        "status": "UNKNOWN",
        "local_markdown_count": len(local_paths),
        "db_document_count": 0,
        "stale_db_documents": [],
        "local_markdown_not_in_db": [],
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
                report["notes"].append(
                    f"cannot infer documents id/path columns. columns={sorted(doc_cols)}"
                )
                print(json.dumps(report, ensure_ascii=False, indent=2))
                return 1

            select_cols = [id_col, path_col]
            if project_col:
                select_cols.append(project_col)

            sql = (
                f"select {', '.join(select_cols)} "
                f"from {schema}.documents "
                f"where {path_col} like 'wiki/%' or {path_col} like '%.md' "
                f"order by {path_col}"
            )
            cur.execute(sql)
            rows = cur.fetchall()

            db_paths = set()
            for row in rows:
                doc_id = row[0]
                path = row[1]
                project = row[2] if project_col and len(row) > 2 else None

                if not path:
                    continue

                db_paths.add(path)
                report["db_document_count"] += 1

                absolute_path = ROOT / path
                if not absolute_path.exists():
                    report["stale_db_documents"].append(
                        {
                            "document_id": doc_id,
                            "project": project,
                            "path": path,
                            "reason": "db path no longer exists on filesystem",
                        }
                    )

            report["local_markdown_not_in_db"] = sorted(local_paths - db_paths)

    stale_count = len(report["stale_db_documents"])
    missing_index_count = len(report["local_markdown_not_in_db"])

    if stale_count == 0 and missing_index_count == 0:
        report["status"] = "PASS"
    elif stale_count == 0:
        report["status"] = "WARN"
        report["notes"].append("some local Markdown files are not indexed")
    else:
        report["status"] = "STALE_FOUND"
        report["notes"].append("stale DB documents detected; purge/mark-stale step needed")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
