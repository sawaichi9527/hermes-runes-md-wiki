import re
import json
import hashlib
from pathlib import Path

from root_resolver import resolve_root
from datetime import datetime, timezone

import psycopg

from db_config import build_conninfo


ROOT = resolve_root()
WIKI_ROOT = ROOT / "wiki"


import re


FORGE_STATUS_PATTERN = re.compile(
    r"^status:\s*(.+?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def should_ingest_forge_doc(path_str: str, content: str) -> tuple[bool, str]:
    """
    P0 forge governance rule.

    forge-inbox:
      approved => ingest
      draft => skip
      missing status => skip
    """

    if "/forge-inbox/" not in path_str:
        return True, "non-forge-path"

    match = FORGE_STATUS_PATTERN.search(content)

    if not match:
        return False, "forge-missing-status"

    status = match.group(1).strip().lower()

    if status == "approved":
        return True, "forge-approved"

    return False, f"forge-status-{status}"


PARSER_NAME = "markdown_conservative_recursive"
PARSER_VERSION = "0.3.0-m3.1"

CHUNK_TARGET_CHARS = 1600
CHUNK_OVERLAP_CHARS = 240
CHUNK_MIN_CHARS = 300
CHUNK_MAX_CHARS = 2200


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def guess_project(path: Path) -> str:
    rel = path.relative_to(WIKI_ROOT)
    return rel.parts[0] if len(rel.parts) > 1 else "default"


def title_from_markdown(text: str, fallback: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def normalize_markdown(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def estimate_tokens(text: str) -> int:
    """Lightweight mixed-language token estimate for metadata only.

    This is not a tokenizer. It intentionally stays cheap for K6.
    CJK chars are counted closer to 1 token each; latin chars use ~4 chars/token.
    """
    if not text:
        return 0

    cjk = len(re.findall(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]", text))
    latin = len(re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]", text))
    other = max(len(text) - cjk - latin, 0)

    return max(1, int(cjk * 1.0 + latin / 4.0 + other / 4.0))


def split_by_separator(parts: list[str], separator: str) -> tuple[list[str], bool]:
    new_parts: list[str] = []
    changed = False

    for part in parts:
        if len(part) <= CHUNK_MAX_CHARS:
            new_parts.append(part)
            continue

        if separator not in part:
            new_parts.append(part)
            continue

        split_parts = [p.strip() for p in part.split(separator) if p.strip()]

        # Preserve a visible hint of punctuation separators when possible.
        if separator.strip():
            split_parts = [p + separator.strip() for p in split_parts]

        new_parts.extend(split_parts)
        changed = True

    return new_parts, changed


def hard_window_split(text: str) -> list[str]:
    chunks: list[str] = []
    start = 0

    while start < len(text):
        end = min(start + CHUNK_TARGET_CHARS, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = max(end - CHUNK_OVERLAP_CHARS, start + 1)

    return chunks


def merge_small_chunks(chunks: list[str]) -> list[str]:
    merged: list[str] = []

    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue

        if (
            merged
            and len(chunk) < CHUNK_MIN_CHARS
            and len(merged[-1]) + len(chunk) + 2 <= CHUNK_MAX_CHARS
        ):
            merged[-1] = merged[-1] + "\n\n" + chunk
        else:
            merged.append(chunk)

    return merged


def split_long_block(block: str) -> list[str]:
    """Conservative multilingual Markdown fallback splitter.

    Policy:
    - Keep semantic blocks intact when possible.
    - Split only when block exceeds CHUNK_MAX_CHARS.
    - Prefer paragraph / newline / multilingual punctuation boundaries.
    - Use overlapping hard window only as the final fallback.
    """
    block = block.strip()
    if not block:
        return []

    if len(block) <= CHUNK_MAX_CHARS:
        return [block]

    separators = [
        "\n\n",
        "\n",
        "。", "！", "？",
        "；", ";",
        "，", ",",
        "、",
        ". ", "! ", "? ",
        ": ", "：",
        " ",
    ]

    parts = [block]

    for sep in separators:
        parts, changed = split_by_separator(parts, sep)

        if changed and all(len(p) <= CHUNK_MAX_CHARS for p in parts):
            break

    chunks: list[str] = []
    current = ""

    for part in parts:
        part = part.strip()
        if not part:
            continue

        candidate = f"{current}\n\n{part}".strip() if current else part

        if len(candidate) <= CHUNK_TARGET_CHARS:
            current = candidate
            continue

        if current:
            chunks.append(current)

        if len(part) <= CHUNK_MAX_CHARS:
            current = part
        else:
            current = ""
            chunks.extend(hard_window_split(part))

    if current:
        chunks.append(current)

    return merge_small_chunks(chunks)


def chunk_markdown(text: str) -> list[tuple[str | None, str]]:
    """
    Heading-aware Markdown chunker.

    Rules:
    - Split at Markdown headings first.
    - Keep each heading section as its own chunk when possible.
    - Do not merge unrelated service sections together.
    - If a section is too large, split inside that section only.
    """
    text = text.strip()
    if not text:
        return []

    heading_re = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

    sections: list[tuple[str | None, str]] = []
    current_lines: list[str] = []
    current_heading: str | None = None

    for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        m = heading_re.match(line.strip())

        if m and current_lines:
            block = "\n".join(current_lines).strip()
            if block:
                sections.append((current_heading, block))

            current_lines = [line]
            current_heading = m.group(2).strip()
            continue

        if m and not current_lines:
            current_heading = m.group(2).strip()

        current_lines.append(line)

    if current_lines:
        block = "\n".join(current_lines).strip()
        if block:
            sections.append((current_heading, block))

    chunks: list[tuple[str | None, str]] = []

    for heading, block in sections:
        if len(block) <= CHUNK_MAX_CHARS:
            chunks.append((heading, block))
            continue

        start = 0
        while start < len(block):
            end = min(start + CHUNK_TARGET_CHARS, len(block))
            part = block[start:end].strip()

            if part:
                chunks.append((heading, part))

            if end >= len(block):
                break

            start = max(end - CHUNK_OVERLAP_CHARS, start + 1)

    return chunks


def schema_mode(conn) -> str:
    """Return 'public' for M3.1 schema or 'memory' for legacy M2 schema."""
    with conn.cursor() as cur:
        cur.execute("select to_regclass('public.documents') is not null;")
        has_public = cur.fetchone()[0]

        cur.execute("select to_regclass('memory.documents') is not null;")
        has_memory = cur.fetchone()[0]

    if has_public:
        return "public"
    if has_memory:
        return "memory"

    raise RuntimeError("No documents table found in public or memory schema")


def import_public(cur, project: str, rel_path: str, title: str, checksum: str, normalized: str, md: Path) -> tuple[int, int, str]:
    cur.execute(
        """
        SELECT id, sha256
        FROM public.documents
        WHERE project = %s
          AND source_path = %s
          AND is_deleted = false;
        """,
        (project, rel_path),
    )

    row = cur.fetchone()

    if row is not None:
        doc_id, old_checksum = row

        if old_checksum == checksum:
            return doc_id, 0, "skipped"
    else:
        doc_id = None

    chunks = chunk_markdown(normalized)
    now = datetime.now(timezone.utc).isoformat()

    metadata = json.dumps(
        {
            "importer": "hermes-memory-import",
            "source": "wiki",
            "path": rel_path,
            "source_sha256": checksum,
            "parser": PARSER_NAME,
            "parser_version": PARSER_VERSION,
            "parser_config": {
                "strategy": PARSER_NAME,
                "target_chars": CHUNK_TARGET_CHARS,
                "overlap_chars": CHUNK_OVERLAP_CHARS,
                "min_chars": CHUNK_MIN_CHARS,
                "max_chars": CHUNK_MAX_CHARS,
            },
            "visibility": "private",
            "project_scope": project,
            "source_preserved": True,
            "ingested_at": now,
        },
        ensure_ascii=False,
    )

    if doc_id is None:
        cur.execute(
            """
            INSERT INTO public.documents (
              project,
              source_path,
              title,
              sha256,
              bytes,
              mtime,
              content,
              content_type,
              parser,
              parser_version,
              metadata,
              is_deleted,
              deleted_at
            )
            VALUES (
              %s, %s, %s, %s, %s, to_timestamp(%s), %s,
              'markdown', %s, %s, %s::jsonb, false, null
            )
            RETURNING id;
            """,
            (
                project,
                rel_path,
                title,
                checksum,
                md.stat().st_size,
                md.stat().st_mtime,
                normalized,
                PARSER_NAME,
                PARSER_VERSION,
                metadata,
            ),
        )
        doc_id = cur.fetchone()[0]
        action = "inserted"
    else:
        cur.execute(
            """
            UPDATE public.documents
            SET
              title = %s,
              sha256 = %s,
              bytes = %s,
              mtime = to_timestamp(%s),
              content = %s,
              content_type = 'markdown',
              parser = %s,
              parser_version = %s,
              metadata = %s::jsonb,
              is_deleted = false,
              deleted_at = null,
              updated_at = now()
            WHERE id = %s;
            """,
            (
                title,
                checksum,
                md.stat().st_size,
                md.stat().st_mtime,
                normalized,
                PARSER_NAME,
                PARSER_VERSION,
                metadata,
                doc_id,
            ),
        )
        action = "updated"

    cur.execute(
        """
        DELETE FROM public.chunks
        WHERE document_id = %s;
        """,
        (doc_id,),
    )

    for idx, (heading, chunk) in enumerate(chunks):
        chunk_metadata = json.dumps(
            {
                "parser": PARSER_NAME,
                "parser_version": PARSER_VERSION,
                "source_sha256": checksum,
                "heading": heading,
                "chunk_chars": len(chunk),
                "chunk_policy": {
                    "strategy": PARSER_NAME,
                    "target_chars": CHUNK_TARGET_CHARS,
                    "overlap_chars": CHUNK_OVERLAP_CHARS,
                    "min_chars": CHUNK_MIN_CHARS,
                    "max_chars": CHUNK_MAX_CHARS,
                },
            },
            ensure_ascii=False,
        )

        cur.execute(
            """
            INSERT INTO public.chunks (
              document_id,
              project,
              source_path,
              chunk_index,
              content,
              token_estimate,
              content_type,
              section_heading,
              metadata
            )
            VALUES (
              %s, %s, %s, %s, %s, %s,
              'text', %s, %s::jsonb
            );
            """,
            (
                doc_id,
                project,
                rel_path,
                idx,
                chunk,
                estimate_tokens(chunk),
                heading,
                chunk_metadata,
            ),
        )

    return doc_id, len(chunks), action


def import_memory_legacy(cur, project: str, rel_path: str, title: str, checksum: str, normalized: str) -> tuple[int, int, str]:
    """Legacy M2 schema compatibility path.

    Kept only for older memory schema. M3.1 should use public schema.
    """
    cur.execute(
        """
        SELECT id, checksum
        FROM memory.documents
        WHERE source_path = %s;
        """,
        (rel_path,),
    )

    row = cur.fetchone()

    if row is not None:
        doc_id, old_checksum = row

        if old_checksum == checksum:
            return doc_id, 0, "skipped"
    else:
        doc_id = None

    metadata = json.dumps(
        {
            "importer": "hermes-memory-import",
            "source": "wiki",
            "path": rel_path,
            "source_sha256": checksum,
            "parser": PARSER_NAME,
            "parser_version": PARSER_VERSION,
        },
        ensure_ascii=False,
    )

    cur.execute(
        """
        INSERT INTO memory.documents (
          project,
          source_path,
          title,
          checksum,
          metadata
        )
        VALUES (
          %s,
          %s,
          %s,
          %s,
          %s::jsonb
        )
        ON CONFLICT (source_path) DO UPDATE
        SET
          project = EXCLUDED.project,
          title = EXCLUDED.title,
          checksum = EXCLUDED.checksum,
          metadata = EXCLUDED.metadata,
          updated_at = now()
        RETURNING id;
        """,
        (project, rel_path, title, checksum, metadata),
    )

    doc_id = cur.fetchone()[0]
    chunks = chunk_markdown(normalized)

    cur.execute(
        """
        DELETE FROM memory.chunks
        WHERE document_id = %s;
        """,
        (doc_id,),
    )

    for idx, (heading, chunk) in enumerate(chunks):
        cur.execute(
            """
            INSERT INTO memory.chunks (
              document_id,
              chunk_index,
              heading,
              content,
              token_hint
            )
            VALUES (
              %s,
              %s,
              %s,
              %s,
              %s
            );
            """,
            (
                doc_id,
                idx,
                heading,
                chunk,
                estimate_tokens(chunk),
            ),
        )

    return doc_id, len(chunks), "upserted"


def main() -> None:
    conninfo = build_conninfo()
    md_files = sorted(WIKI_ROOT.rglob("*.md"))

    imported = 0
    updated = 0
    skipped = 0
    chunks_total = 0

    with psycopg.connect(conninfo) as conn:
        mode = schema_mode(conn)

        with conn.cursor() as cur:
            for md in md_files:
                text = md.read_text(encoding="utf-8")

                rel_path = str(md.relative_to(ROOT))

                allowed, reason = should_ingest_forge_doc(
                    rel_path,
                    text,
                )

                if not allowed:
                    print(
                        f"skipped-forge-policy: "
                        f"project={project} "
                        f"path={rel_path} "
                        f"reason={reason}"
                    )
                    continue

                normalized = normalize_markdown(text)
                project = guess_project(md)
                title = title_from_markdown(normalized, md.stem)
                checksum = sha256_text(normalized)

                if mode == "public":
                    doc_id, chunk_count, action = import_public(
                        cur,
                        project,
                        rel_path,
                        title,
                        checksum,
                        normalized,
                        md,
                    )
                else:
                    doc_id, chunk_count, action = import_memory_legacy(
                        cur,
                        project,
                        rel_path,
                        title,
                        checksum,
                        normalized,
                    )

                if action == "skipped":
                    skipped += 1
                elif action == "updated":
                    updated += 1
                    imported += 1
                else:
                    imported += 1

                chunks_total += chunk_count

                print(
                    f"{action}: id={doc_id} "
                    f"chunks={chunk_count} "
                    f"project={project} "
                    f"path={rel_path}"
                )

    print(
        "summary: "
        f"schema={mode} "
        f"imported_or_changed={imported} "
        f"updated={updated} "
        f"skipped={skipped} "
        f"chunks_written={chunks_total}"
    )
    print("PASS: Markdown incremental import completed")


if __name__ == "__main__":
    main()
