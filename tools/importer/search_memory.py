import os
import sys
from pathlib import Path

import psycopg
from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-base-en-v1.5"
TOP_K = 5


def load_env(path: Path) -> None:
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def vector_literal(values: list[float]) -> str:
    return "[" + ",".join(f"{v:.8f}" for v in values) + "]"


def print_rows(title: str, rows) -> None:
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)

    if not rows:
        print("(no results)")
        return

    for rank, row in enumerate(rows, start=1):
        source_path, chunk_index, heading, score, preview = row
        print(f"[{rank}] {source_path} :: chunk={chunk_index}")
        print(f"    heading: {heading or ''}")
        print(f"    score: {score}")
        print(f"    preview: {preview.replace(chr(10), ' ')[:240]}")
        print()


def main() -> None:
    if len(sys.argv) < 2:
        print('usage: python search_memory.py "query text"')
        sys.exit(1)

    query = " ".join(sys.argv[1:]).strip()
    load_env(Path(".env"))

    conninfo = (
        f"host={os.environ['PGHOST']} "
        f"port={os.environ['PGPORT']} "
        f"dbname={os.environ['PGDATABASE']} "
        f"user={os.environ['PGUSER']} "
        f"password={os.environ['PGPASSWORD']}"
    )

    print(f"query: {query}")

    print("loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)
    qvec = vector_literal(model.encode(query, normalize_embeddings=True).tolist())

    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                  d.source_path,
                  c.chunk_index,
                  c.heading,
                  ts_rank_cd(c.fts, plainto_tsquery('simple', %s)) AS score,
                  left(c.content, 360) AS preview
                FROM memory.chunks c
                JOIN memory.documents d ON d.id = c.document_id
                WHERE c.fts @@ plainto_tsquery('simple', %s)
                ORDER BY score DESC, d.source_path, c.chunk_index
                LIMIT %s;
                """,
                (query, query, TOP_K),
            )
            fts_rows = cur.fetchall()

            cur.execute(
                """
                SELECT
                  d.source_path,
                  c.chunk_index,
                  c.heading,
                  1 - (c.embedding <=> %s::vector) AS score,
                  left(c.content, 360) AS preview
                FROM memory.chunks c
                JOIN memory.documents d ON d.id = c.document_id
                WHERE c.embedding IS NOT NULL
                ORDER BY c.embedding <=> %s::vector
                LIMIT %s;
                """,
                (qvec, qvec, TOP_K),
            )
            vector_rows = cur.fetchall()

            cur.execute(
                """
                WITH fts AS (
                  SELECT
                    c.id,
                    ts_rank_cd(c.fts, plainto_tsquery('simple', %s)) AS fts_score
                  FROM memory.chunks c
                  WHERE c.fts @@ plainto_tsquery('simple', %s)
                ),
                vec AS (
                  SELECT
                    c.id,
                    1 - (c.embedding <=> %s::vector) AS vec_score
                  FROM memory.chunks c
                  WHERE c.embedding IS NOT NULL
                  ORDER BY c.embedding <=> %s::vector
                  LIMIT 20
                ),
                merged AS (
                  SELECT
                    c.id,
                    coalesce(fts.fts_score, 0) AS fts_score,
                    coalesce(vec.vec_score, 0) AS vec_score,
                    (coalesce(fts.fts_score, 0) * 0.45)
                    + (coalesce(vec.vec_score, 0) * 0.55) AS hybrid_score
                  FROM memory.chunks c
                  LEFT JOIN fts ON fts.id = c.id
                  LEFT JOIN vec ON vec.id = c.id
                  WHERE fts.id IS NOT NULL OR vec.id IS NOT NULL
                )
                SELECT
                  d.source_path,
                  c.chunk_index,
                  c.heading,
                  round(m.hybrid_score::numeric, 6) AS score,
                  left(c.content, 360) AS preview
                FROM merged m
                JOIN memory.chunks c ON c.id = m.id
                JOIN memory.documents d ON d.id = c.document_id
                ORDER BY m.hybrid_score DESC
                LIMIT %s;
                """,
                (query, query, qvec, qvec, TOP_K),
            )
            hybrid_rows = cur.fetchall()

    print_rows("FTS RESULTS", fts_rows)
    print_rows("VECTOR RESULTS", vector_rows)
    print_rows("HYBRID RESULTS", hybrid_rows)

    print("PASS: memory search completed")


if __name__ == "__main__":
    main()
