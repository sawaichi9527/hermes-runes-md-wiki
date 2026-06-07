# Sample Project Decisions

## D-001: Use Markdown as Source-of-Truth

Status: DECIDED

Decision:
- Use Markdown files as the durable human-readable source-of-truth.
- Use the database as an index and retrieval backend, not as the primary knowledge authoring surface.

Rationale:
- Markdown is portable.
- Markdown is easy to review.
- Markdown works well with version control.
- Human-readable source material reduces hidden state.

---

## D-002: Keep Secrets Out of Markdown

Status: DECIDED

Decision:
- Do not store real API keys, database passwords, tokens, or credentials in Markdown memory.

Rationale:
- Markdown files may be committed to Git.
- RAG systems may retrieve Markdown content.
- Secrets must remain in local `.env` files or secret stores.
