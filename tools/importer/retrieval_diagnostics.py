import argparse
import json
import re
from collections import Counter

import psycopg

from db_config import build_conninfo


DEFAULT_SCHEMA = "public"


def validate_identifier(value: str, label: str) -> str:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value):
        raise SystemExit(f"Invalid {label}: {value!r}")
    return value


def pct(part: int, total: int) -> float:
    if total == 0:
        return 0.0
    return round((part / total) * 100.0, 2)


def summarize_paths(rows: list[tuple[str, int, int]]) -> list[dict]:
    return [
        {
            "path": path,
            "chunks": chunks,
            "embedded_chunks": embedded_chunks,
            "embedding_coverage_pct": pct(embedded_chunks, chunks),
        }
        for path, chunks, embedded_chunks in rows
    ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Diagnose Hermes Runes retrieval readiness and embedding coverage."
    )
    parser.add_argument("--project", required=True)
    parser.add_argument("--schema", default=DEFAULT_SCHEMA)
    parser.add_argument("--path")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    schema = validate_identifier(args.schema, "schema")

    result = {
        "status": "started",
        "schema": schema,
        "project": args.project,
        "path": args.path,
        "diagnostics": {},
        "recommendations": [],
    }

    with psycopg.connect(build_conninfo()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT
                  count(*)::int AS documents
                FROM {schema}.documents d
                WHERE
                  d.project = %s
                  AND (%s::text IS NULL OR d.source_path LIKE '%%' || %s::text || '%%');
                """,
                (args.project, args.path, args.path),
            )
            documents = cur.fetchone()[0]

            cur.execute(
                f"""
                SELECT
                  count(*)::int AS chunks,
                  count(c.embedding)::int AS embedded_chunks,
                  count(*) FILTER (WHERE c.embedding IS NULL)::int AS missing_embeddings
                FROM {schema}.chunks c
                JOIN {schema}.documents d ON d.id = c.document_id
                WHERE
                  d.project = %s
                  AND (%s::text IS NULL OR d.source_path LIKE '%%' || %s::text || '%%');
                """,
                (args.project, args.path, args.path),
            )
            chunks, embedded_chunks, missing_embeddings = cur.fetchone()

            cur.execute(
                f"""
                SELECT
                  d.source_path,
                  count(*)::int AS chunks,
                  count(c.embedding)::int AS embedded_chunks
                FROM {schema}.chunks c
                JOIN {schema}.documents d ON d.id = c.document_id
                WHERE
                  d.project = %s
                  AND (%s::text IS NULL OR d.source_path LIKE '%%' || %s::text || '%%')
                GROUP BY d.source_path
                ORDER BY d.source_path
                LIMIT %s;
                """,
                (args.project, args.path, args.path, args.limit),
            )
            path_rows = cur.fetchall()

            cur.execute(
                f"""
                SELECT
                  d.source_path,
                  c.chunk_index,
                  c.section_heading,
                  c.embedding IS NOT NULL AS has_embedding
                FROM {schema}.chunks c
                JOIN {schema}.documents d ON d.id = c.document_id
                WHERE
                  d.project = %s
                  AND (%s::text IS NULL OR d.source_path LIKE '%%' || %s::text || '%%')
                ORDER BY d.source_path, c.chunk_index
                LIMIT %s;
                """,
                (args.project, args.path, args.path, args.limit),
            )
            sample_rows = cur.fetchall()

    path_summary = summarize_paths(path_rows)
    per_path_counts = Counter(row[0] for row in sample_rows)

    result["diagnostics"] = {
        "documents": documents,
        "chunks": chunks,
        "embedded_chunks": embedded_chunks,
        "missing_embeddings": missing_embeddings,
        "embedding_coverage_pct": pct(embedded_chunks, chunks),
        "paths": path_summary,
        "sample_chunks": [
            {
                "path": path,
                "chunk_index": chunk_index,
                "section_heading": section_heading,
                "has_embedding": has_embedding,
            }
            for path, chunk_index, section_heading, has_embedding in sample_rows
        ],
        "sample_path_distribution": dict(per_path_counts),
    }

    if chunks == 0:
        result["recommendations"].append(
            "No chunks found. Run the importer for this project/path first."
        )
    elif embedded_chunks == 0:
        result["recommendations"].append(
            "No embeddings found. Hybrid recall will be FTS-only until embeddings are generated."
        )
    elif missing_embeddings > 0:
        result["recommendations"].append(
            "Embedding coverage is partial. Re-run embedding/import pipeline for stable hybrid retrieval."
        )
    else:
        result["recommendations"].append(
            "Embedding coverage is complete. If hybrid recall still shows vector_rank=null, inspect vector branch filtering or pgvector query behavior."
        )

    result["status"] = "pass"

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"status: {result['status']}")
    print(f"project: {args.project}")
    print(f"schema: {schema}")
    if args.path:
        print(f"path filter: {args.path}")
    print()
    print(f"documents: {documents}")
    print(f"chunks: {chunks}")
    print(f"embedded_chunks: {embedded_chunks}")
    print(f"missing_embeddings: {missing_embeddings}")
    print(f"embedding_coverage_pct: {result['diagnostics']['embedding_coverage_pct']}")
    print()
    print("paths:")
    for item in path_summary:
        print(
            f"- {item['path']}: "
            f"chunks={item['chunks']} "
            f"embedded={item['embedded_chunks']} "
            f"coverage={item['embedding_coverage_pct']}%"
        )
    print()
    print("recommendations:")
    for item in result["recommendations"]:
        print(f"- {item}")


if __name__ == "__main__":
    main()
