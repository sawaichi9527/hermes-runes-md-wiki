# K6 / Freelancer Hermes Agent Memory

Host: K6 / Freelancer  
User: eye  
Phase: Phase3-M1  
Status: Active

---

## Purpose

This wiki tracks the local Hermes Agent architecture, decisions, services, baselines, verification steps, and next actions for the K6 / Freelancer host.

This directory is part of the Phase3-M1 Markdown memory source-of-truth:

```text
~/workspace/hermes-memory/wiki/k6-freelancer/
```

It is intended to be:

- Human-readable
- Hermes-readable
- Safe to back up
- Safe to index later with PostgreSQL FTS / pgvector
- Safe to use as a long-term project memory source

---

## Current Baseline

The current completed baseline is:

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

Current Hermes web architecture:

```text
Hermes Agent
  ├─ web_search
  │    └─ SearXNG Docker on 127.0.0.1:8088
  │
  └─ web_extract
       └─ Tavily API
```

---

## Current Phase

```text
Phase3-M1: Markdown wiki source-of-truth
```

Goal:

```text
Create a local, curated, Markdown-based memory workspace for K6 / Freelancer Hermes Agent.
```

This phase does not yet include PostgreSQL, pgvector, or hybrid search.

---

## Phase3 Roadmap

```text
M1: Markdown wiki source-of-truth
M1b: PostgreSQL FTS index
M2: pgvector semantic search
M3: hybrid search / rerank
```

Current status:

```text
M1: Active
M1b: Planned
M2: Planned
M3: Planned
```

---

## Key Services

### Hermes Agent

Role:

```text
Main local agent runtime on K6 / Freelancer.
```

Important paths:

```text
Hermes install:
~/.hermes/hermes-agent

Hermes command:
~/.local/bin/hermes

Hermes config:
~/.hermes/config.yaml

Hermes env:
~/.hermes/.env

Hermes gateway service:
~/.config/systemd/user/hermes-gateway.service
```

### SearXNG

Role:

```text
Local web_search backend for Hermes Agent.
```

Important paths:

```text
SearXNG stack:
~/docker-stacks/hermes-searxng/

SearXNG baseline:
~/docker-stacks/hermes-searxng/baseline-20260530/
```

Runtime URL:

```text
http://127.0.0.1:8088
```

Docker binding:

```text
127.0.0.1:8088->8080/tcp
```

### Tavily

Role:

```text
External web_extract backend for Hermes Agent.
```

Configuration:

```text
TAVILY_API_KEY is configured in ~/.hermes/.env
```

Security rule:

```text
Do not store the Tavily API key in this wiki.
```

### Future PostgreSQL Memory Backend

Planned role:

```text
M1b: PostgreSQL FTS index
M2: pgvector semantic search
M3: hybrid search / rerank
```

Planned stack path:

```text
~/docker-stacks/hermes-memory-postgres/
```

---

## Important Paths

```text
Memory workspace:
~/workspace/hermes-memory/

Project wiki:
~/workspace/hermes-memory/wiki/k6-freelancer/

Imported Phase2 baseline:
~/workspace/hermes-memory/imports/phase2-A1C1-baseline-20260530.md

Hermes install:
~/.hermes/hermes-agent

Hermes config:
~/.hermes/config.yaml

Hermes env:
~/.hermes/.env

SearXNG stack:
~/docker-stacks/hermes-searxng/

SearXNG baseline snapshot:
~/docker-stacks/hermes-searxng/baseline-20260530/

Future PostgreSQL stack:
~/docker-stacks/hermes-memory-postgres/
```

---

## Wiki Files

This project wiki should contain the following files:

```text
README.md
  Project memory overview.

decisions.md
  Architectural decisions and rationale.

services.md
  Service inventory, paths, ports, and roles.

baselines.md
  Frozen baselines and verification status.

verification.md
  Health checks and validation commands.

next-actions.md
  Deferred work and next implementation steps.
```

---

## Durable Facts

The following facts should be treated as durable project memory:

```text
K6 / Freelancer is the Hermes Agent host.

Hermes is installed natively under:
~/.hermes/hermes-agent

Hermes gateway runs as a systemd user service:
hermes-gateway.service

Phase2-A1C1 baseline-20260530 is complete and PASS.

SearXNG is the Hermes web_search backend.

SearXNG runs in Docker and is bound only to:
127.0.0.1:8088

Hermes uses:
web.search_backend: searxng

Hermes uses Tavily as:
web.extract_backend: tavily

Tavily API key is configured in ~/.hermes/.env but must never be stored in this wiki.

PostgreSQL + FTS + pgvector is the chosen long-term K6 memory/RAG backend direction.

SQLite is not the preferred long-term K6 memory backend.

The M1 Markdown wiki source-of-truth lives under:
~/workspace/hermes-memory/

The future PostgreSQL service stack should live under:
~/docker-stacks/hermes-memory-postgres/
```

---

## Do Not Store

Never store the following in this wiki:

```text
API keys
Telegram bot token
Tavily API key
Passwords
Private credentials
SSH private keys
OAuth tokens
Raw secret-bearing logs
Full tcpdump packet dumps
Temporary debug noise
```

Use redacted placeholders when needed:

```env
TAVILY_API_KEY=<configured>
SEARXNG_URL=http://127.0.0.1:8088
```

---

## Verification

After this file and the related wiki files are created, verify with:

```bash
cd ~/workspace/hermes-memory

find . -maxdepth 4 -type f | sort

rg -n "Phase2-A1C1|SearXNG|Tavily|PostgreSQL|pgvector|web.search_backend|baseline-20260530" .
```

Expected:

```text
Relevant matches should appear in README.md and the k6-freelancer wiki files.
```

---

## Current Next Step

Complete the Phase3-M1 project wiki files:

```text
decisions.md
services.md
baselines.md
verification.md
next-actions.md
```

Then create an initial Phase3-M1 backup snapshot.
