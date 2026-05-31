#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

ROOT = Path.home() / "workspace/hermes-memory"
ENV_FILE = ROOT / "tools/importer/.env"


def load_db_url():
    load_dotenv(ENV_FILE)
    db_url = (
        os.getenv("DATABASE_URL")
        or os.getenv("POSTGRES_DSN")
        or os.getenv("HERMES_MEMORY_DATABASE_URL")
    )
    if not db_url:
        raise RuntimeError("Missing DATABASE_URL / POSTGRES_DSN / HERMES_MEMORY_DATABASE_URL")
    return db_url


def get_columns(cur, table):
    cur.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = %s
        ORDER BY ordinal_position
        """,
        (table,),
    )
    return [r[0] for r in cur.fetchall()]


def pick_column(columns, candidates):
    for c in candidates:
        if c in columns:
            return c
    return None


def normalize_paths(project, path):
    candidates = {path}
    if not path.startswith("wiki/"):
        candidates.add(f"wiki/{project}/{path}")
    if path.startswith(f"wiki/{project}/"):
        candidates.add(path.removeprefix(f"wiki/{project}/"))
    return sorted(candidates)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    db_url = load_db_url()
    path_candidates = normalize_paths(args.project, args.path)

    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            doc_cols = get_columns(cur, "documents")
            chunk_cols = get_columns(cur, "chunks")

            path_col = pick_column(
                doc_cols,
                ["path", "source_path", "file_path", "rel_path", "relative_path"],
            )
            project_col = pick_column(
                doc_cols,
                ["project", "project_name"],
            )
            doc_id_col = pick_column(
                chunk_cols,
                ["document_id", "doc_id"],
            )

            if not path_col:
                raise RuntimeError(f"Cannot find document path column. documents columns={doc_cols}")
            if not project_col:
                raise RuntimeError(f"Cannot find project column. documents columns={doc_cols}")
            if not doc_id_col:
                raise RuntimeError(f"Cannot find chunk document FK column. chunks columns={chunk_cols}")

            cur.execute(
                f"""
                SELECT id, {project_col}, {path_col}
                FROM documents
                WHERE {project_col} = %s
                  AND {path_col} = ANY(%s)
                ORDER BY id
                """,
                (args.project, path_candidates),
            )
            docs = cur.fetchall()
            doc_ids = [r[0] for r in docs]

            if not doc_ids:
                result = {
                    "status": "not_found",
                    "project": args.project,
                    "path": args.path,
                    "path_candidates": path_candidates,
                    "detected_columns": {
                        "documents_path": path_col,
                        "documents_project": project_col,
                        "chunks_document_fk": doc_id_col,
                    },
                    "deleted_documents": 0,
                    "deleted_chunks": 0,
                }
                print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else result)
                return 0

            cur.execute(
                f"DELETE FROM chunks WHERE {doc_id_col} = ANY(%s)",
                (doc_ids,),
            )
            deleted_chunks = cur.rowcount

            cur.execute(
                "DELETE FROM documents WHERE id = ANY(%s)",
                (doc_ids,),
            )
            deleted_documents = cur.rowcount

        conn.commit()

    result = {
        "status": "deleted",
        "project": args.project,
        "path": args.path,
        "path_candidates": path_candidates,
        "document_ids": doc_ids,
        "deleted_documents": deleted_documents,
        "deleted_chunks": deleted_chunks,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
