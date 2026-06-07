# Sample Project Services

## PostgreSQL

Role:
- Retrieval backend.
- Stores imported documents and chunks.
- Supports keyword and vector search.

Notes:
- PostgreSQL data is runtime state.
- Database volumes should not be committed to Git.

---

## Local LLM Endpoint

Role:
- OpenAI-compatible local or LAN model endpoint.
- Used by answer generation.

Notes:
- Endpoint configuration belongs in local `.env`.
- API keys or local secrets must not be committed.

---

## Observation Logs

Role:
- Lightweight local JSONL runtime observations.
- Used for failure analysis and tuning candidates.

Policy:
- Observation logs are local-only.
- They should not be ingested back into RAG memory.
- They should not contain raw full prompts or full retrieved context by default.
