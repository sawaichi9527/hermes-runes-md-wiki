# Hermes Memory Workspace

Host: K6 / Freelancer  
Owner: eye  
Purpose: Local Markdown source-of-truth for Hermes Agent memory and project state.

---

## Role

This directory is the human-readable and Hermes-readable memory workspace.

It is **not** a Docker service.  
It is **not** the PostgreSQL index.  
It is **not** the Hermes internal runtime memory directory.

This workspace is intended to be:

- Human-readable
- Hermes-readable
- Backup-friendly
- Git-friendly
- Safe to inspect and edit manually
- Safe to index later with PostgreSQL FTS / pgvector

---

## Layout

```text
~/workspace/hermes-memory/
  ├─ README.md
  ├─ wiki/
  │   └─ k6-freelancer/
  ├─ imports/
  ├─ exports/
  └─ backups/
```

Directory roles:

```text
README.md
  Root overview for the Hermes memory workspace.

wiki/
  Curated Markdown wiki source-of-truth.

wiki/k6-freelancer/
  Project memory for the K6 / Freelancer Hermes Agent host.

imports/
  Imported source documents, previous baselines, migration notes, or raw reference Markdown.

exports/
  Exported summaries, generated handoff files, or future machine-readable outputs.

backups/
  Manual or scripted snapshots of this memory workspace.
```


---

## Design Principles

### 1. Markdown is the source-of-truth

The Markdown files in this workspace are the canonical, human-readable project memory.

PostgreSQL, FTS, pgvector, or any future RAG backend should be treated as an index or retrieval layer, not the primary truth source.

```text
Markdown wiki
  ↓ ingest / sync
PostgreSQL FTS / pgvector
  ↓ query
Hermes recall / RAG
```

### 2. Keep Hermes runtime state separate

This workspace should not replace or directly modify Hermes internal runtime state.

Hermes internal files remain under:

```text
~/.hermes/
```

This workspace lives under:

```text
~/workspace/hermes-memory/
```

The separation keeps project memory independent from Hermes upgrades, runtime changes, and internal memory implementation details.

### 3. Keep Docker service state separate

Docker services remain under:

```text
~/docker-stacks/
```

For example, the future PostgreSQL memory backend should live under:

```text
~/docker-stacks/hermes-memory-postgres/
```

This workspace is not a Docker stack and should not contain PostgreSQL data directories.

### 4. Do not store secrets

Never store the following in this workspace:

```text
API keys
Telegram bot tokens
Tavily API key
Passwords
Private credentials
SSH private keys
OAuth tokens
Raw secret-bearing logs
```

Secrets should remain in their proper runtime configuration files, such as:

```text
~/.hermes/.env
```

If secret-related settings need to be documented, redact the values:

```env
TAVILY_API_KEY=<configured>
SEARXNG_URL=http://127.0.0.1:8088
```

### 5. Prefer durable facts over temporary logs

This workspace should store durable project memory, such as:

```text
Architecture decisions
Service paths
Baseline status
Verification commands
Known deferred tasks
Recovery notes
```

Avoid storing temporary noise, such as:

```text
One-off debug logs
Raw tcpdump dumps
Transient stack traces
Temporary shell output
Old failed attempts unless they explain a permanent decision
```


---

## Current Phase

```text
Phase3-M1: Markdown wiki source-of-truth baseline
```

Current goal:

```text
Create a local, curated, human-readable memory workspace for Hermes Agent on K6 / Freelancer.
```

This phase does not yet include PostgreSQL, pgvector, or hybrid search.

---

## Phase Roadmap

### Phase3-M1 — Markdown Wiki Source-of-Truth

Status: Active

Goals:

```text
1. Establish ~/workspace/hermes-memory/
2. Create k6-freelancer project wiki
3. Import Phase2-A1C1 baseline
4. Record durable decisions and service paths
5. Validate with ripgrep
6. Create initial backup snapshot
```

### Phase3-M1b — PostgreSQL FTS Index

Status: Planned

Goal:

```text
Create a PostgreSQL Docker service that indexes the Markdown wiki with full-text search.
```

Planned stack path:

```text
~/docker-stacks/hermes-memory-postgres/
```

Planned capabilities:

```text
documents table
chunks table
metadata
tsvector FTS index
keyword recall
```

### Phase3-M2 — pgvector Semantic Search

Status: Planned

Goal:

```text
Add embedding-based semantic retrieval using pgvector.
```

Planned capabilities:

```text
embedding column
vector similarity search
semantic recall
local or provider-based embedding pipeline
```

### Phase3-M3 — Hybrid Search / Rerank

Status: Planned

Goal:

```text
Combine keyword search, semantic search, metadata filters, and ranking logic.
```

Planned capabilities:

```text
FTS keyword score
vector similarity score
project / phase / recency metadata
sensitivity filtering
hybrid ranking
rerank policy
```


---

## Current K6 / Freelancer Context

The current completed baseline before Phase3 is:

```text
Phase2-A1C1 baseline-20260530
```

Summary:

```text
A1 local SearXNG search: PASS
C1 Tavily extract backend: PASS
Hermes search + extract pipeline: PASS
Health check script: PASS
Baseline snapshot: PASS
```

Important paths:

```text
Hermes install:
~/.hermes/hermes-agent

Hermes config:
~/.hermes/config.yaml

Hermes env:
~/.hermes/.env

SearXNG stack:
~/docker-stacks/hermes-searxng/

SearXNG baseline:
~/docker-stacks/hermes-searxng/baseline-20260530/

Memory workspace:
~/workspace/hermes-memory/

Future PostgreSQL memory stack:
~/docker-stacks/hermes-memory-postgres/
```

Current Hermes web backend configuration:

```yaml
web:
  backend: ''
  search_backend: searxng
  extract_backend: tavily
```

Current web search / extract roles:

```text
web_search:
  SearXNG Docker at http://127.0.0.1:8088

web_extract:
  Tavily API
```

---

## Verification

After creating or updating this workspace, verify with:

```bash
cd ~/workspace/hermes-memory

find . -maxdepth 4 -type f | sort

rg -n "Phase2-A1C1|SearXNG|Tavily|PostgreSQL|pgvector|web.search_backend|baseline-20260530" .
```

Expected result:

```text
The search should return matches from README.md and the project wiki files.
```

---

## Backup Recommendation

Create a Phase3-M1 initial snapshot after the first wiki files are completed:

```bash
cd ~/workspace/hermes-memory

mkdir -p backups/phase3-M1-initial-20260530

cp README.md backups/phase3-M1-initial-20260530/
cp -a wiki backups/phase3-M1-initial-20260530/
cp -a imports backups/phase3-M1-initial-20260530/

find backups/phase3-M1-initial-20260530 -maxdepth 4 -type f | sort
```

---

## Operational Rule

Treat this directory as the long-term project memory source-of-truth.

```text
If it is important for future Hermes behavior, architecture recovery, or project continuity,
write it here in Markdown first.

If it is only an index, cache, generated embedding, or temporary runtime state,
do not treat it as the source-of-truth.
```
