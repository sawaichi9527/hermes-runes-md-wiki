import argparse
import json

import psycopg

from db_config import build_conninfo


DEFAULT_SCHEMA = "public"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="PostgreSQL FTS search for Hermes memory chunks."
    )
    parser.add_argument("query")
    parser.add_argument("--project", required=True)
    parser.add_argument("--schema", default=DEFAULT_SCHEMA)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--path")
    parser.add_argument("--max-content-length", type=int, default=500)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = {
        "status": "started",
        "schema": args.schema,
        "project": args.project,
        "query": args.query,
        "limit": args.limit,
        "path": args.path,
        "max_content_length": args.max_content_length,
        "results": [],
    }

    with psycopg.connect(build_conninfo()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                WITH q AS (
                  SELECT websearch_to_tsquery('simple', %s) AS query
                )
                SELECT
                  c.id AS chunk_id,
                  d.source_path AS path,
                  c.chunk_index,
                  c.content,
                  ts_rank_cd(
                    to_tsvector('simple', c.content),
                    q.query
                  ) AS score
                FROM {args.schema}.chunks c
                JOIN {args.schema}.documents d ON d.id = c.document_id
                CROSS JOIN q
                WHERE
                  d.project = %s
                  AND (%s::text IS NULL OR d.source_path LIKE '%%' || %s::text || '%%')
                  AND q.query @@ to_tsvector('simple', c.content)
                ORDER BY score DESC, c.id ASC
                LIMIT %s;
                """,
                (args.query, args.project, args.path, args.path, args.limit),
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
            print(item["content"])


if __name__ == "__main__":
    main()
