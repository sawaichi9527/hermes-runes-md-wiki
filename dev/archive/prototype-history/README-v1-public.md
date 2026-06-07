# Hermes Runes MD Wiki

Markdown wiki source-of-truth for governed local RAG memory.

Hermes Runes MD Wiki is a local-first, agent-agnostic memory layer that uses curated Markdown wiki content as durable long-term knowledge, with PostgreSQL / FTS / pgvector retrieval and governed answer generation.

---

# Philosophy

Runtime memory is temporary.

Curated Markdown memory is durable.

Hermes Runes treats Markdown as intentional knowledge carved into durable runes rather than transient conversation state.

The database is an index and retrieval backend.

The Markdown wiki remains the human-readable source-of-truth.

---

# Why Markdown Source-of-Truth

Many personal RAG systems eventually become opaque memory silos:

- hidden embeddings
- hidden retrieval state
- hidden agent memory mutation
- difficult review workflows
- difficult Git integration

Hermes Runes instead uses:

```text
Markdown Wiki
    ↓
Importer
    ↓
PostgreSQL / pgvector
    ↓
Hybrid Retrieval
    ↓
Governed Answer Generation
```

This preserves:

- human readability
- Git compatibility
- long-term maintainability
- reviewability
- deterministic retrieval fixtures
- portable knowledge ownership

---

# Core Features

## Local-first

Designed primarily for local or self-hosted deployment.

No cloud dependency is required.

---

## Markdown Wiki Source-of-Truth

Curated Markdown files are the canonical knowledge layer.

The retrieval database is derived state.

---

## Hybrid Retrieval

Supports:

- PostgreSQL FTS
- vector retrieval
- rerank pipelines
- metadata filtering
- governed context building

---

## Governed Answer Generation

Supports:

- extraction quality validation
- citation integrity validation
- retry governance
- incomplete answer cleanup
- reasoning fallback extraction
- governed answer metadata

---

## Observation & Evaluation

Supports:

- lightweight JSONL observation logs
- retrieval evaluation
- smoke tests
- regression fixtures
- tuning candidate summaries

Observation is designed around:

```text
observe first, tune later
```

---

## Public-safe Retrieval Fixtures

The repository includes:

```text
wiki/sample-project/
```

This allows:

- public retrieval testing
- smoke baselines
- regression validation
- documentation examples

without exposing private engineering memory.

---

# Agent-Agnostic Design

Hermes Runes is not tightly coupled to Hermes Agent.

Although Hermes Agent is the original development target, the memory layer is intentionally designed to be reusable by other intelligent agent systems.

Potential integrations include:

- Hermes Agent
- OpenClaw
- MCP-compatible agents
- OpenAI-compatible systems
- future local agent frameworks

---

# Repository Layout

```text
wiki/                       Markdown source-of-truth
tools/importer/             Import / retrieval / governance pipeline
tools/importer/smoke/       Smoke and regression tests
bin/                        CLI wrappers
archive/                    Historical prototype artifacts
logs/                       Local runtime logs (gitignored)
backups/                    Local backups (gitignored)
```

---

# Example Knowledge Layout

Supports both:

## Flat-first layout

```text
wiki/tech-pc-hardware-ssd.md
wiki/hobbies-anime-mecha.md
```

## Folder-based project layout

```text
wiki/k6-freelancer/
├── decisions.md
├── services.md
├── verification.md
```

Engineering projects generally benefit from folder-based organization.

Small personal knowledge areas may remain flat until they grow large enough to justify folders.

---

# Quickstart

See:

```text
QUICKSTART.md
```

---

# Current Baseline Status

Current repository baseline includes:

```text
M5  Retrieval / Context Baseline             PASS
M10 Observation Governance Baseline          PASS
M11 Observation Summary Baseline             PASS
M11.6 Repository Portability Baseline        PASS
M11.6 Sample Public Fixture Baseline         PASS
M12.1 Requirements Baseline                  PASS
```

---

# Current Scope

Hermes Runes currently focuses on:

- governed local RAG
- Markdown memory governance
- retrieval quality
- evaluation
- repository portability

It is not currently intended to be:

- a full multi-user SaaS platform
- a distributed cloud memory platform
- a fully autonomous self-modifying agent framework

---

# Future Roadmap

Planned future areas include:

- MCP-compatible interfaces
- agent adapters
- retrieval/rerank improvements
- deployment packaging
- better evaluation tooling
- long-context governance
- multi-project memory orchestration

---

# Security Principles

Real secrets must never be committed into Markdown memory.

This includes:

- API keys
- PostgreSQL passwords
- Telegram tokens
- local credentials
- private user secrets

Secrets belong in:

```text
.env
local secret stores
runtime configuration
```

not in source-of-truth memory.

---

# License

License selection is currently pending.
