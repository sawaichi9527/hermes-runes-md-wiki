# Hermes Runes MD Wiki

Markdown wiki source-of-truth for governed local RAG memory.

---

# 1. Project Identity

Hermes Runes MD Wiki is a local-first, governed Markdown knowledge layer designed for long-term personal and project memory.

The system uses Markdown wiki files as the source-of-truth, while PostgreSQL, FTS, and pgvector provide indexing and retrieval capabilities.

Hermes Agent is the first target consumer, but the architecture is intentionally agent-agnostic.

Future compatible consumers may include:

- Hermes Agent
- OpenClaw
- MCP-compatible runtimes
- local automation frameworks
- future intelligent agent systems

---

# 2. Core Philosophy

Not all runtime memory should become durable memory.

Hermes Runes focuses on curated long-term memory:

- architecture decisions
- baselines
- verification records
- deployment procedures
- operations knowledge
- structured technical notes
- curated personal knowledge

The system intentionally separates:

- temporary runtime state
- conversational memory
- observation logs
- exploratory reasoning
- durable curated knowledge

The goal is to preserve high-value knowledge in a human-reviewable Markdown form.

---

# 3. What Hermes Runes Is

Hermes Runes MD Wiki is:

- local-first
- Markdown-centric
- governance-aware
- regression-testable
- inspectable by humans
- portable across systems
- agent-agnostic
- suitable for technical and personal knowledge

The project supports:

- Markdown ingestion
- PostgreSQL full-text indexing
- pgvector semantic search
- hybrid retrieval
- context building
- governed answer generation
- citation integrity checking
- bounded retry behavior
- response sanitization
- observation logging
- smoke validation

---

# 4. What Hermes Runes Is NOT

Hermes Runes is NOT:

- a raw chat transcript archive
- an autonomous self-modifying memory system
- a cloud-first SaaS platform
- a replacement for runtime conversational memory
- a hidden opaque vector database
- a fully automatic knowledge ingestion pipeline

The project intentionally prefers:

- explicit curation
- governance
- inspectability
- reproducibility
- stable source-of-truth documents

---

# 5. Memory Layer Model

The Hermes ecosystem separates memory into multiple conceptual layers.

## Layer 1: Runtime Memory

Examples:

- current task state
- recent conversations
- temporary agent context
- execution state
- short-lived preferences

Characteristics:

- dynamic
- mutable
- temporary
- runtime-oriented

---

## Layer 2: Curated Markdown Memory

Hermes Runes primarily focuses on this layer.

Examples:

- architecture decisions
- baselines
- verification
- deployment procedures
- operations documentation
- curated references

Characteristics:

- durable
- human-reviewable
- governance-aware
- source-of-truth
- regression-testable

---

## Layer 3: Personal Knowledge Garden

Examples:

- Obsidian-like notes
- hobby knowledge
- reading notes
- semi-structured references
- exploratory ideas

Characteristics:

- partially curated
- lightweight
- flexible
- may later become curated memory

---

## Layer 4: External / Specialized RAG

Examples:

- external document systems
- wiki-like memory systems
- semantic memory services
- high-volume exploratory knowledge

Characteristics:

- optional
- replaceable
- externally managed

---

# 6. Architecture Overview

Current baseline architecture:

```text
Markdown Wiki
    ↓
Importer
    ↓
PostgreSQL / FTS / pgvector
    ↓
Hybrid Retrieval
    ↓
Context Builder
    ↓
Answer Generator
    ↓
Governance / Retry / Sanitization
    ↓
Observation Logging
```

The Markdown wiki remains the durable source-of-truth.

The database layer exists to accelerate retrieval, not replace human-readable knowledge.

---

# 7. Repository Layout Philosophy

Hermes Runes adopts a:

```text
flat-first, folder-when-needed
```

layout policy.

Small personal knowledge namespaces may use flat filenames:

```text
tech-pc-hardware-ssd.md
hobbies-anime-watchlist.md
```

Long-lived engineering projects default to folder-based layouts:

```text
wiki/k6-freelancer/
```

Engineering project namespaces are treated as curated project-memory baselines.

---

# 8. Governance Model

Hermes Runes uses governance-aware memory principles.

High-governance namespaces may require:

- verification
- reproducibility
- smoke tests
- curated review
- stable baselines

Lower-governance namespaces may prioritize:

- lightweight organization
- personal convenience
- flexible references

The project intentionally avoids:

- uncontrolled auto-memory
- silent memory mutation
- opaque hidden state

---

# 9. Observation & Evaluation

Hermes Runes includes observation and evaluation tooling.

Observation logging is intended for:

- sanitizer tuning
- retry evaluation
- extraction quality monitoring
- governance analysis
- regression detection

The project intentionally keeps observation lightweight:

- local JSONL logs
- no raw full prompts by default
- no automatic self-modification
- grep/jq-friendly structure

---

# 10. Portability & Local-First Design

The repository supports configurable root paths.

Default personal development layout:

```text
~/workspace/hermes-memory
```

Override:

```bash
export HERMES_MEMORY_ROOT="/custom/path"
```

The project is intended to:

- avoid root requirements
- remain portable across machines
- support personal deployments
- support future GitHub users

---

# 11. Current Baseline Status

Current baseline capabilities:

```text
Markdown ingestion                PASS
PostgreSQL indexing               PASS
FTS retrieval                     PASS
pgvector retrieval                PASS
Hybrid retrieval                  PASS
Context builder                   PASS
Governed answer generation        PASS
Citation integrity checking       PASS
Bounded retry                     PASS
Observation logging               PASS
Observation summary               PASS
Smoke validation                  PASS
Portable root policy              PASS
```

Current status:

```text
Governed Local RAG Baseline: PASS
```

---

# 12. Planned Next Steps

Planned future work may include:

- Hermes Agent integration adapter
- MCP-compatible interfaces
- HTTP API layer
- retrieval/rerank improvements
- metadata-aware filtering
- portable deployment tooling
- Obsidian interoperability
- archive/downrank policy
- multi-agent integration

---

# 13. Guiding Principle

Runtime memory is temporary.

Curated Markdown memory is knowledge intentionally carved into durable runes.
