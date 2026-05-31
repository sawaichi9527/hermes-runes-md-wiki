import argparse
import json

import psycopg
from sentence_transformers import SentenceTransformer

from db_config import build_conninfo


MODEL_NAME = "BAAI/bge-base-en-v1.5"
EXPECTED_DIM = 768
DEFAULT_SCHEMA = "public"


def vector_literal(values: list[float]) -> str:
    return "[" + ",".join(f"{v:.8f}" for v in values) + "]"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate embeddings for Hermes memory chunks."
    )
    parser.add_argument("--project", required=True)
    parser.add_argument("--schema", default=DEFAULT_SCHEMA)
    parser.add_argument("--missing-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    conninfo = build_conninfo()
    schema = args.schema

    result = {
        "status": "started",
        "schema": schema,
        "project": args.project,
        "model": MODEL_NAME,
        "expected_dim": EXPECTED_DIM,
        "missing_only": args.missing_only,
        "chunks_selected": 0,
        "chunks_embedded": 0,
        "coverage": {},
    }

    if not args.json:
        print(f"Loading embedding model: {MODEL_NAME}")

    model = SentenceTransformer(MODEL_NAME)

    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            where = ["d.project = %s"]
            params = [args.project]

            if args.missing_only:
                where.append("c.embedding IS NULL")

            where_sql = " AND ".join(where)

            cur.execute(
                f"""
                SELECT
                  c.id,
                  c.content AS text
                FROM {schema}.chunks c
                JOIN {schema}.documents d ON d.id = c.document_id
                WHERE {where_sql}
                ORDER BY c.id;
                """,
                params,
            )

            rows = cur.fetchall()
            result["chunks_selected"] = len(rows)

            if not args.json:
                print(f"chunks selected: {len(rows)}")

            for chunk_id, text in rows:
                emb = model.encode(
                    text,
                    normalize_embeddings=True,
                ).tolist()

                if len(emb) != EXPECTED_DIM:
                    raise RuntimeError(
                        f"embedding dim mismatch: got={len(emb)} expected={EXPECTED_DIM}"
                    )

                cur.execute(
                    f"""
                    UPDATE {schema}.chunks
                    SET
                      embedding = %s::vector,
                      updated_at = now()
                    WHERE id = %s;
                    """,
                    (vector_literal(emb), chunk_id),
                )

                result["chunks_embedded"] += 1

                if not args.json:
                    print(f"embedded chunk id={chunk_id}")

            cur.execute(
                f"""
                SELECT
                  count(*) AS total_chunks,
                  count(*) FILTER (WHERE c.embedding IS NOT NULL) AS embedded_chunks,
                  count(*) FILTER (WHERE c.embedding IS NULL) AS missing_chunks
                FROM {schema}.chunks c
                JOIN {schema}.documents d ON d.id = c.document_id
                WHERE d.project = %s;
                """,
                (args.project,),
            )

            total, embedded, missing = cur.fetchone()

            coverage_ratio = 0.0
            if total:
                coverage_ratio = round(float(embedded) / float(total), 6)

            result["coverage"] = {
                "total_chunks": total,
                "embedded_chunks": embedded,
                "missing_chunks": missing,
                "coverage_ratio": coverage_ratio,
            }

    result["status"] = "pass" if result["coverage"]["missing_chunks"] == 0 else "partial"

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("coverage:", result["coverage"])
        print(f"PASS: embeddings generated, status={result['status']}")


if __name__ == "__main__":
    main()
