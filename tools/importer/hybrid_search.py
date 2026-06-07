import argparse
from retrieval_profiles import select_retrieval_profile
import json

import psycopg

from db_config import build_conninfo


MODEL_NAME = "BAAI/bge-base-en-v1.5"
EXPECTED_DIM = 768
DEFAULT_SCHEMA = "public"


def vector_literal(values: list[float]) -> str:
    return "[" + ",".join(f"{v:.8f}" for v in values) + "]"


def encode_query_embedding(query: str) -> str:
    try:
        from sentence_transformers import SentenceTransformer
    except ModuleNotFoundError as exc:
        payload = {
            "status": "blocked_missing_embedding_dependency",
            "message": (
                "sentence-transformers is required for --mode hybrid/vector. "
                "Use --mode fts for lightweight core recall, or install embedding requirements."
            ),
            "missing_module": "sentence_transformers",
        }
        raise SystemExit(json.dumps(payload, ensure_ascii=False, indent=2)) from exc

    model = SentenceTransformer(MODEL_NAME)
    emb = model.encode(query, normalize_embeddings=True).tolist()

    if len(emb) != EXPECTED_DIM:
        raise RuntimeError(
            f"embedding dim mismatch: got={len(emb)} expected={EXPECTED_DIM}"
        )

    return vector_literal(emb)


def slugify_heading(value: str | None) -> str:
    if not value:
        return "no-section"

    out = []
    last_dash = False

    for ch in value.lower():
        if ch.isalnum():
            out.append(ch)
            last_dash = False
        elif not last_dash:
            out.append("-")
            last_dash = True

    slug = "".join(out).strip("-")
    return slug or "no-section"



TRUST_POLICY_NAME = "m20.5-personal-governance-v1"


def compute_trust_bias(forge: dict) -> int:
    if not forge:
        return 0

    status = str(forge.get("status", "")).lower()
    trust_class = str(forge.get("trust_class", "")).lower()
    proposed_by = str(forge.get("proposed_by", "")).lower()
    provenance = str(forge.get("provenance", "")).lower()
    proposal_type = str(forge.get("proposal_type", "")).lower()

    if status in {"draft", "rejected"}:
        return -99

    bias = 0

    # M20.5 personal governance policy:
    # - draft/rejected are handled as hard negative above.
    # - approved+reviewed forge proposals are retrieval-visible but neutral.
    # - normal wiki content remains the baseline source of truth by location.
    # - keep provenance fields observable without turning them into enterprise-grade scoring.
    if trust_class in {"unverified"}:
        bias -= 2

    if trust_class in {"reviewed", "human-reviewed"} and status == "approved":
        bias += 0

    if proposal_type == "agent_memory":
        bias += 0

    if proposed_by == "human" and provenance == "manual_cli":
        bias += 0

    return bias


def build_citation(path: str, section_heading: str | None, chunk_index: int, chunk_id: int) -> dict:
    section = section_heading or ""
    section_slug = slugify_heading(section_heading)
    ref = f"{path}#{section_slug}:chunk-{chunk_index}"

    return {
        "path": path,
        "section": section,
        "chunk_index": chunk_index,
        "chunk_id": chunk_id,
        "ref": ref,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Hybrid FTS + pgvector search for Hermes memory chunks."
    )
    parser.add_argument("query")
    parser.add_argument("--project", required=True)
    parser.add_argument("--schema", default=DEFAULT_SCHEMA)
    parser.add_argument(
        "--mode",
        choices=["hybrid", "fts", "vector"],
        default="hybrid",
        help="Compatibility option. Current retrieval uses the default hybrid/RRF pipeline.",
    )
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--path")
    parser.add_argument("--heading")

    parser.add_argument(
        "--query-type",
        default="default",
    )
    parser.add_argument("--candidate-limit", type=int, default=20)
    parser.add_argument("--max-content-length", type=int, default=500)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    retrieval_profile_name, retrieval_profile = (
        select_retrieval_profile(
            args.query_type
        )
    )

    query_vec = None
    if args.mode in {"hybrid", "vector"}:
        query_vec = encode_query_embedding(args.query)

    result = {
        "status": "started",
        "retrieval_profile": retrieval_profile_name,
        "schema": args.schema,
        "project": args.project,
        "query": args.query,
        "model": MODEL_NAME if args.mode in {"hybrid", "vector"} else None,
        "limit": args.limit,
        "path": args.path,
        "heading": args.heading,
        "candidate_limit": args.candidate_limit,
        "max_content_length": args.max_content_length,
        "fusion": "rrf" if args.mode == "hybrid" else args.mode,
        "results": [],
    }

    if args.mode == "fts":
        with psycopg.connect(build_conninfo()) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    WITH q AS (
                      SELECT
                        websearch_to_tsquery('simple', %s) AS tsq,
                        %s::text AS raw_query
                    ),
                    fts_hits AS (
                      SELECT
                        c.id AS chunk_id,
                        row_number() OVER (
                          ORDER BY
                            (
                              ts_rank_cd(to_tsvector('simple', c.content), q.tsq)
                              +
                              (
                                SELECT count(*)::float
                                FROM regexp_split_to_table(q.raw_query, '\\s+') AS token
                                WHERE length(token) >= 3
                                  AND (
                                    c.content ILIKE '%%' || token || '%%'
                                    OR c.section_heading ILIKE '%%' || token || '%%'
                                  )
                              ) * 0.01
                            ) DESC,
                            c.id ASC
                        ) AS fts_rank,
                        (
                          ts_rank_cd(to_tsvector('simple', c.content), q.tsq)
                          +
                          (
                            SELECT count(*)::float
                            FROM regexp_split_to_table(q.raw_query, '\\s+') AS token
                            WHERE length(token) >= 3
                              AND (
                                c.content ILIKE '%%' || token || '%%'
                                OR c.section_heading ILIKE '%%' || token || '%%'
                              )
                          ) * 0.01
                        ) AS fts_score
                      FROM {args.schema}.chunks c
                      JOIN {args.schema}.documents d ON d.id = c.document_id
                      CROSS JOIN q
                      WHERE
                        d.project = %s
                        AND (%s::text IS NULL OR d.source_path LIKE '%%' || %s::text || '%%')
                        AND (%s::text IS NULL OR c.section_heading ILIKE '%%' || %s::text || '%%')
                        AND (
                          q.tsq @@ to_tsvector('simple', c.content)
                          OR EXISTS (
                            SELECT 1
                            FROM regexp_split_to_table(%s::text, '\\s+') AS token
                            WHERE length(token) >= 3
                              AND (
                                c.content ILIKE '%%' || token || '%%'
                                OR c.section_heading ILIKE '%%' || token || '%%'
                              )
                          )
                        )
                      ORDER BY fts_score DESC, c.id ASC
                      LIMIT %s
                    )
                    SELECT
                      c.id AS chunk_id,
                      d.source_path AS path,
                      c.chunk_index,
                      c.section_heading,
                      c.metadata AS chunk_metadata,
                      fts_hits.fts_score AS hybrid_score,
                      NULL::integer AS vector_rank,
                      NULL::float AS vector_score,
                      fts_hits.fts_rank,
                      fts_hits.fts_score,
                      c.content
                    FROM fts_hits
                    JOIN {args.schema}.chunks c ON c.id = fts_hits.chunk_id
                    JOIN {args.schema}.documents d ON d.id = c.document_id
                    ORDER BY fts_hits.fts_score DESC, c.id ASC
                    LIMIT %s;
                    """,
                    (
                        args.query,
                        args.query,
                        args.project,
                        args.path,
                        args.path,
                        args.heading,
                        args.heading,
                        args.query,
                        args.candidate_limit,
                        args.limit,
                    ),
                )

                rows = cur.fetchall()
    else:
        with psycopg.connect(build_conninfo()) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    WITH
                    q AS (
                      SELECT
                        websearch_to_tsquery('simple', %s) AS tsq,
                        %s::vector AS vec,
                        %s::text AS raw_query
                    ),
                    vector_hits AS (
                      SELECT
                        c.id AS chunk_id,
                        row_number() OVER (
                          ORDER BY c.embedding <=> q.vec
                        ) AS vector_rank,
                        1 - (c.embedding <=> q.vec) AS vector_score
                      FROM {args.schema}.chunks c
                      JOIN {args.schema}.documents d ON d.id = c.document_id
                      CROSS JOIN q
                      WHERE
                        d.project = %s
                        AND (%s::text IS NULL OR d.source_path LIKE '%%' || %s::text || '%%')
                        AND (%s::text IS NULL OR c.section_heading ILIKE '%%' || %s::text || '%%')
                        AND c.embedding IS NOT NULL
                      ORDER BY c.embedding <=> q.vec
                      LIMIT %s
                    ),
                    fts_hits AS (
                      SELECT
                        c.id AS chunk_id,
                        row_number() OVER (
                          ORDER BY
                            (
                              ts_rank_cd(to_tsvector('simple', c.content), q.tsq)
                              +
                              (
                                SELECT count(*)::float
                                FROM regexp_split_to_table(q.raw_query, '\\s+') AS token
                                WHERE length(token) >= 3
                                  AND (
                                    c.content ILIKE '%%' || token || '%%'
                                    OR c.section_heading ILIKE '%%' || token || '%%'
                                  )
                              ) * 0.01
                            ) DESC,
                            c.id ASC
                        ) AS fts_rank,
                        (
                          ts_rank_cd(to_tsvector('simple', c.content), q.tsq)
                          +
                          (
                            SELECT count(*)::float
                            FROM regexp_split_to_table(q.raw_query, '\\s+') AS token
                            WHERE length(token) >= 3
                              AND (
                                c.content ILIKE '%%' || token || '%%'
                                OR c.section_heading ILIKE '%%' || token || '%%'
                              )
                          ) * 0.01
                        ) AS fts_score
                      FROM {args.schema}.chunks c
                      JOIN {args.schema}.documents d ON d.id = c.document_id
                      CROSS JOIN q
                      WHERE
                        d.project = %s
                        AND (%s::text IS NULL OR d.source_path LIKE '%%' || %s::text || '%%')
                        AND (%s::text IS NULL OR c.section_heading ILIKE '%%' || %s::text || '%%')
                        AND (
                          q.tsq @@ to_tsvector('simple', c.content)
                          OR EXISTS (
                            SELECT 1
                            FROM regexp_split_to_table(%s::text, '\\s+') AS token
                            WHERE length(token) >= 3
                              AND (
                                c.content ILIKE '%%' || token || '%%'
                                OR c.section_heading ILIKE '%%' || token || '%%'
                              )
                          )
                        )
                      ORDER BY fts_score DESC, c.id ASC
                      LIMIT %s
                    ),
                    fused AS (
                      SELECT
                        coalesce(v.chunk_id, f.chunk_id) AS chunk_id,
                        v.vector_rank,
                        v.vector_score,
                        f.fts_rank,
                        f.fts_score,
                        coalesce(1.0 / (60 + v.vector_rank), 0) +
                        coalesce(1.0 / (60 + f.fts_rank), 0) AS hybrid_score
                      FROM vector_hits v
                      FULL OUTER JOIN fts_hits f ON f.chunk_id = v.chunk_id
                    )
                    SELECT
                      c.id AS chunk_id,
                      d.source_path AS path,
                      c.chunk_index,
                      c.section_heading,
                      c.metadata AS chunk_metadata,
                      fused.hybrid_score,
                      fused.vector_rank,
                      fused.vector_score,
                      fused.fts_rank,
                      fused.fts_score,
                      c.content
                    FROM fused
                    JOIN {args.schema}.chunks c ON c.id = fused.chunk_id
                    JOIN {args.schema}.documents d ON d.id = c.document_id
                    ORDER BY
                      fused.hybrid_score DESC,
                      fused.vector_rank NULLS LAST,
                      fused.fts_rank NULLS LAST,
                      c.id ASC
                    LIMIT %s;
                    """,
                    (
                        args.query,
                        query_vec,
                        args.query,
                        args.project,
                        args.path,
                        args.path,
                        args.heading,
                        args.heading,
                        args.candidate_limit,
                        args.project,
                        args.path,
                        args.path,
                        args.heading,
                        args.heading,
                        args.query,
                        args.candidate_limit,
                        args.limit,
                    ),
                )

                rows = cur.fetchall()

    for (
        chunk_id,
        path,
        chunk_index,
        section_heading,
        chunk_metadata,
        hybrid_score,
        vector_rank,
        vector_score,
        fts_rank,
        fts_score,
        content,
    ) in rows:
        citation = build_citation(path, section_heading, chunk_index, chunk_id)
        forge_metadata = (chunk_metadata or {}).get("forge", {})
        trust_bias = compute_trust_bias(forge_metadata)

        result["results"].append(
            {
                "chunk_id": chunk_id,
                "path": path,
                "chunk_index": chunk_index,
                "section_heading": section_heading,
                "citation": citation,
                "forge": forge_metadata,
                "trust_bias": trust_bias,
                "trust_policy": TRUST_POLICY_NAME,
                "hybrid_score": float(hybrid_score),
                "profile_bias": 0,
                "vector_rank": vector_rank,
                "vector_score": float(vector_score) if vector_score is not None else None,
                "fts_rank": fts_rank,
                "fts_score": float(fts_score) if fts_score is not None else None,
                "content": content[: args.max_content_length],
                "content_truncated": len(content) > args.max_content_length,
            }
        )

    heading_bias_tokens = retrieval_profile.get(
        "heading_bias",
        [],
    )

    for item in result["results"]:
        heading = (
            item.get("section_heading") or ""
        ).lower()

        bias = 0

        for token in heading_bias_tokens:
            if token.lower() in heading:
                bias += 2

        item["profile_bias"] = bias

    result["results"].sort(
        key=lambda x: (
            x.get("profile_bias", 0),
            x.get("trust_bias", 0),
            x.get("hybrid_score", 0),
        ),
        reverse=True,
    )

    result["status"] = "pass"

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"query: {args.query}")
        print(f"results: {len(result['results'])}")
        for item in result["results"]:
            print()
            print(
                f"[hybrid={item['hybrid_score']:.6f} "
                f"v_rank={item['vector_rank']} fts_rank={item['fts_rank']}] "
                f"{item['citation']['ref']} heading={item['section_heading']!r}"
            )
            print(item["content"])


if __name__ == "__main__":
    main()
