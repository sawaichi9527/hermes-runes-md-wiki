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
        description="Vector search for Hermes memory chunks."
    )
    parser.add_argument("query")
    parser.add_argument("--project", required=True)
    parser.add_argument("--schema", default=DEFAULT_SCHEMA)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--path")
    parser.add_argument("--max-content-length", type=int, default=500)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    model = SentenceTransformer(MODEL_NAME)

    emb = model.encode(
        args.query,
        normalize_embeddings=True,
    ).tolist()

    if len(emb) != EXPECTED_DIM:
        raise RuntimeError(
            f"embedding dim mismatch: got={len(emb)} expected={EXPECTED_DIM}"
        )

    query_vec = vector_literal(emb)

    result = {
        "status": "started",
        "schema": args.schema,
        "project": args.project,
        "query": args.query,
        "model": MODEL_NAME,
        "limit": args.limit,
        "path": args.path,
        "max_content_length": args.max_content_length,
        "results": [],
    }

    with psycopg.connect(build_conninfo()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT
                  c.id AS chunk_id,
                  d.source_path AS path,
                  c.chunk_index,
                  c.content,
                  1 - (c.embedding <=> %s::vector) AS score
                FROM {args.schema}.chunks c
                JOIN {args.schema}.documents d ON d.id = c.document_id
                WHERE
                  d.project = %s
                  AND (%s::text IS NULL OR d.source_path LIKE '%%' || %s::text || '%%')
                  AND c.embedding IS NOT NULL
                ORDER BY c.embedding <=> %s::vector
                LIMIT %s;
                """,
                (query_vec, args.project, args.path, args.path, query_vec, args.limit),
            )

            rows = cur.fetchall()

    for chunk_id, path, chunk_index, content, score in rows:
        result["results"].append(
            {
                "chunk_id": chunk_id,
                "path": path,
                "chunk_index": chunk_index,
                "score": float(score),
                "content": content[: args.max_content_length],
                "content_truncated": len(content) > args.max_content_length,
            }
        )

    result["status"] = "pass"

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"query: {args.query}")
        print(f"results: {len(result['results'])}")
        for item in result["results"]:
            print()
            print(f"[{item['score']:.4f}] {item['path']}#chunk-{item['chunk_index']}")
            print(item["content"][:500])


if __name__ == "__main__":
    main()
