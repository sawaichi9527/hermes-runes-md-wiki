import argparse
import json
import re
from typing import Iterable

import psycopg
from sentence_transformers import SentenceTransformer

from db_config import build_conninfo


MODEL_NAME = "BAAI/bge-base-en-v1.5"
EXPECTED_DIM = 768
DEFAULT_SCHEMA = "public"


def validate_identifier(value: str, label: str) -> str:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value):
        raise SystemExit(f"Invalid {label}: {value!r}")
    return value


def vector_literal(values: Iterable[float]) -> str:
    return "[" + ",".join(f"{float(v):.8f}" for v in values) + "]"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Backfill missing pgvector embeddings for Hermes memory chunks."
    )
    parser.add_argument("--project", required=True)
    parser.add_argument("--schema", default=DEFAULT_SCHEMA)
    parser.add_argument("--path")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    schema = validate_identifier(args.schema, "schema")

    if args.limit <= 0:
        raise SystemExit("--limit must be greater than 0")
    if args.batch_size <= 0:
        raise SystemExit("--batch-size must be greater than 0")

    result = {
        "status": "started",
        "schema": schema,
        "project": args.project,
        "path": args.path,
        "model": MODEL_NAME,
        "expected_dim": EXPECTED_DIM,
        "limit": args.limit,
        "batch_size": args.batch_size,
        "dry_run": args.dry_run,
        "selected_chunks": 0,
        "updated_chunks": 0,
        "chunks": [],
    }

    with psycopg.connect(build_conninfo()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT
                  c.id,
                  d.source_path,
                  c.chunk_index,
                  c.section_heading,
                  c.content
                FROM {schema}.chunks c
                JOIN {schema}.documents d ON d.id = c.document_id
                WHERE
                  d.project = %s
                  AND (%s::text IS NULL OR d.source_path LIKE '%%' || %s::text || '%%')
                  AND c.embedding IS NULL
                ORDER BY d.source_path, c.chunk_index, c.id
                LIMIT %s;
                """,
                (args.project, args.path, args.path, args.limit),
            )
            rows = cur.fetchall()

            result["selected_chunks"] = len(rows)
            result["chunks"] = [
                {
                    "chunk_id": chunk_id,
                    "path": path,
                    "chunk_index": chunk_index,
                    "section_heading": section_heading,
                }
                for chunk_id, path, chunk_index, section_heading, _content in rows
            ]

            if args.dry_run or not rows:
                result["status"] = "pass"
                conn.rollback()
            else:
                model = SentenceTransformer(MODEL_NAME)
                updated = 0

                for offset in range(0, len(rows), args.batch_size):
                    batch = rows[offset : offset + args.batch_size]
                    texts = [content for *_prefix, content in batch]
                    embeddings = model.encode(
                        texts,
                        normalize_embeddings=True,
                    )

                    for (chunk_id, _path, _chunk_index, _heading, _content), emb in zip(batch, embeddings):
                        values = emb.tolist() if hasattr(emb, "tolist") else list(emb)
                        if len(values) != EXPECTED_DIM:
                            raise RuntimeError(
                                f"embedding dim mismatch for chunk_id={chunk_id}: "
                                f"got={len(values)} expected={EXPECTED_DIM}"
                            )

                        cur.execute(
                            f"""
                            UPDATE {schema}.chunks
                            SET embedding = %s::vector
                            WHERE id = %s;
                            """,
                            (vector_literal(values), chunk_id),
                        )
                        updated += cur.rowcount

                conn.commit()
                result["updated_chunks"] = updated
                result["status"] = "pass"

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"status: {result['status']}")
    print(f"project: {args.project}")
    print(f"schema: {schema}")
    if args.path:
        print(f"path filter: {args.path}")
    print(f"model: {MODEL_NAME}")
    print(f"selected_chunks: {result['selected_chunks']}")
    print(f"updated_chunks: {result['updated_chunks']}")
    print(f"dry_run: {args.dry_run}")
    print()
    for item in result["chunks"]:
        print(
            f"- chunk_id={item['chunk_id']} "
            f"{item['path']}#chunk-{item['chunk_index']} "
            f"heading={item['section_heading']!r}"
        )


if __name__ == "__main__":
    main()
