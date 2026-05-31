# Services — K6 / Freelancer Hermes Agent

## Purpose

This document records the long-lived services and infrastructure components used by the K6 / Freelancer Hermes Agent project.

Design rule:

```text
Markdown is the source-of-truth.
PostgreSQL, FTS, pgvector, and hybrid search are derived index/query layers.
```

---

# 1. Hermes Agent

Role:

```text
Primary AI agent runtime.
```

Responsibilities:

```text
Receive user requests.
Coordinate tools and memory.
Perform reasoning and task execution.
```

Status:

```text
PASS
```

---

# 2. SearXNG

Role:

```text
Local web search backend.
```

Location:

```text
Docker service.
```

Binding:

```text
127.0.0.1 only.
```

Purpose:

```text
Provide privacy-preserving web search capability.
```

Status:

```text
PASS
```

---

# 3. Tavily

Role:

```text
Web extraction backend.
```

Purpose:

```text
Retrieve and extract content from web pages.
```

Configuration:

```yaml
web:
  search_backend: searxng
  extract_backend: tavily
```

Secret storage:

```text
TAVILY_API_KEY is stored in ~/.hermes/.env.
```

Rule:

```text
Secrets must never be stored in Markdown memory.
```

Status:

```text
PASS
```

---

# 4. Telegram Integration

Role:

```text
Telegram ingress channel for Hermes Agent.
```

Mode:

```text
Long polling.
```

Purpose:

```text
Allow approved Telegram chats to submit requests to Hermes.
```

Access Control:

```text
Allowed chat list enforced.
Unknown chats are rejected.
```

Managed By:

```text
Hermes core.
```

Start / Stop:

```text
Integrated into Hermes runtime.
No standalone Telegram service.
```

Secret Storage:

```text
Telegram bot token is stored in ~/.hermes/.env.
```

Rule:

```text
Real Telegram bot token must never be stored in Markdown memory.
```

Status:

```text
PASS
```

Notes:

```text
Telegram is an ingress interface only.

Telegram is not a memory backend.

Telegram should be indexed as a Hermes access channel so memory recall queries for Telegram resolve to operational architecture information rather than only token-security guidance.
```

---

# 5. PostgreSQL Memory

Role:

```text
Primary long-term memory backend.
```

Location:

```text
~/docker-stacks/hermes-memory-postgres/
```

Database:

```text
hermes_memory
```

Schema:

```text
memory
```

Tables:

```text
memory.documents
memory.chunks
```

Capabilities:

```text
Document storage
Chunk storage
Metadata storage
Checksum tracking
```

Status:

```text
PASS
```

---

# 6. PostgreSQL FTS

Role:

```text
Keyword search layer.
```

Technology:

```text
PostgreSQL Full Text Search
GIN index
tsvector
```

Purpose:

```text
Fast exact-term retrieval.
```

Status:

```text
PASS
```

---

# 7. pgvector

Role:

```text
Semantic search layer.
```

Technology:

```text
pgvector 0.8.2
vector(768)
HNSW index
cosine similarity
```

Purpose:

```text
Semantic recall across natural-language queries.
```

Status:

```text
PASS
```

---

# 8. Markdown Memory Workspace

Role:

```text
Human-readable source-of-truth.
```

Workspace:

```text
~/workspace/hermes-memory/
```

Wiki:

```text
~/workspace/hermes-memory/wiki/k6-freelancer/
```

Imported Baselines:

```text
~/workspace/hermes-memory/imports/
```

Current Files:

```text
README.md
decisions.md
services.md
baselines.md
verification.md
next-actions.md
```

Status:

```text
PASS
```

---

# 9. Memory Adapter

Role:

```text
Bridge between Hermes and PostgreSQL memory.
```

Components:

```text
memory_adapter.py
hermes-memory-adapter
hermes-recall
```

Capabilities:

```text
FTS search
Vector search
Hybrid search
JSON output
```

Status:

```text
PASS
```

---

# Service Summary

Current Production Components:

```text
Hermes Agent
SearXNG
Tavily
Telegram Integration
PostgreSQL Memory
PostgreSQL FTS
pgvector
Markdown Memory Workspace
Memory Adapter
```

Current Memory Architecture:

```text
Markdown
    ↓
Importer
    ↓
PostgreSQL
    ↓
FTS
    ↓
pgvector
    ↓
Hybrid Search
    ↓
Memory Adapter
    ↓
Hermes Recall
```

Current Status:

```text
Phase3-Memory-MVP-baseline-20260530

PASS / frozen
```

---

# Secret Handling Rule

Status:

```text
PASS / policy
```

Rule:

```text
Real secrets must never be stored in Markdown memory, Git, shared logs, or copied into RAG-visible source files.
```

Scope:

```text
This rule applies to all real service credentials, not only API keys.
```

Protected Secret Types:

```text
PostgreSQL database read/write passwords
LM Studio / OpenAI-compatible API keys
Telegram bot tokens
Tavily API keys
Service tokens
Private keys
Any future service credentials
```

Allowed Storage:

```text
Local .env files
Local secret storage
Runtime environment variables
```

Git Exclusion:

```text
.env
tools/importer/.env
```

Operational Rule:

```text
Markdown memory may document where secrets are configured,
but must never contain the real secret values.
```

Example:

```text
Allowed:
OPENAI_API_KEY is configured in tools/importer/.env

Not allowed:
OPENAI_API_KEY=<real value>
```

RAG Rule:

```text
The memory wiki must preserve the security policy,
but real secrets must stay outside indexed memory content.
```

