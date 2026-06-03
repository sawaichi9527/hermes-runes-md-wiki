# Hermes Runes MD Wiki

Markdown wiki source-of-truth for governed local RAG memory.

Hermes Runes MD Wiki is a local-first, agent-agnostic memory substrate that uses curated Markdown wiki content as durable long-term knowledge, with PostgreSQL / FTS / pgvector retrieval, governed context assembly, and controlled wiki operations.

Hermes Runes was originally developed for Hermes Agent, but it is intentionally designed as an agent-agnostic subsystem that can be called by Hermes Agent, OpenClaw, MCP-compatible agents, OpenAI-compatible systems, or future local agent frameworks.

---

## Philosophy

Runtime memory is temporary.

Curated Markdown memory is durable.

Hermes Runes treats Markdown as intentional knowledge carved into durable runes rather than transient conversation state.

The database is an index and retrieval backend.

The Markdown wiki remains the human-readable source-of-truth.

Hermes Runes does not decide truth for the agent.

Hermes Runes provides governed memory evidence, source metadata, and operational safety. The calling agent remains responsible for comparing Hermes Runes evidence with current user instructions, native memory, third-party RAG / notes, web search results, and other available sources.

---

## Agent Onboarding / Runes Summoning Trial

External AI agents should begin onboarding from:

```text
README.md
    ↓
AGENTS.md
    ↓
wiki/_system/README.md
```

For first-connect / post-install readiness checks, see:

```text
wiki/_system/m58-runes-summoning-trial.md
```

M58 Runes Summoning Trial is an agent-agnostic governed onboarding diagnostic for external agents entering Hermes Runes MD Wiki through Runes Shield.

M58 is intentionally lightweight:

- read-only
- bounded
- non-recursive
- personal-local
- diagnostic-oriented

The optional onboarding subtitles and world-setting references are UX-only flavor text and are not runtime requirements.

---

## Core Design

```text
Hermes Agent or other caller
    ↓
Hermes Runes controlled interface
    ├── decipher   deterministic wiki policy / guide / index reads
    ├── forge      governed Markdown wiki mutations
    ├── evoke      RAG recall over indexed memory
    ├── inscribe   import / embedding / index lifecycle
    ├── probe      diagnostics and consistency checks
    └── chronicle  structural change history, normally written by forge
    ↓
wiki/ Markdown source-of-truth
    ↓
PostgreSQL / FTS / pgvector derived index
```

The calling agent should not freely edit `wiki/` files for structural changes.

Structural wiki changes should go through the governed writer path so that indexes, objective README files, change history, import, embeddings, and diagnostics remain consistent.

---

## Command Vocabulary

Hermes Runes uses rune-themed command names, but every term has a plain engineering meaning.

| Rune term | Plain meaning | Scope |
|---|---|---|
| `decipher` | deterministic read | Read canonical policy, wiki guide, category indexes, and objective README files. |
| `forge` | governed write | Create, update, rename, archive, or otherwise mutate Markdown wiki structure. |
| `evoke` | recall / retrieve | Query indexed personal RAG memory using retrieval pipelines. |
| `inscribe` | index / embed | Import Markdown source-of-truth into searchable PostgreSQL / FTS / vector indexes. |
| `probe` | diagnose / check | Check retrieval, context, links, locks, metadata, policy, and index consistency. |
| `chronicle` | change history | Record structural Markdown wiki changes, normally as an internal effect of `forge`. |

Rune terms are interface names, not hidden magic. Documentation and CLI help must include plain-language explanations.

---

## Why Markdown Source-of-Truth

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
Importer / Inscribe
    ↓
PostgreSQL / pgvector
    ↓
Hybrid Retrieval / Evoke
    ↓
Context Assembly / Answer Support
```

This preserves:

- human readability
- Git compatibility
- long-term maintainability
- reviewability
- deterministic retrieval fixtures
- portable knowledge ownership

---

## Core Features

### Local-first

Designed primarily for local or self-hosted deployment.

No cloud dependency is required.

### Markdown Wiki Source-of-Truth

Curated Markdown files are the canonical knowledge layer.

The retrieval database is derived state.

### Hybrid Retrieval

Supports:

- PostgreSQL FTS
- vector retrieval
- rerank pipelines
- governed context building
- retrieval diagnostics
- context diagnostics

Metadata filtering and source-status-aware retrieval are planned as follow-up work after the P0 wiki governance baseline.

### Governed Answer Support

Supports:

- extraction quality validation
- citation integrity validation
- retry governance
- incomplete answer cleanup
- reasoning fallback extraction
- governed answer metadata

Hermes Runes should expose evidence and source metadata. The calling agent should perform final source comparison and answer judgment.

### Observation & Evaluation

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

Observation logs must not be ingested into RAG memory.

### Public-safe Retrieval Fixtures

The repository currently includes:

```text
wiki/sample-project/
```

This supports public retrieval testing, smoke baselines, regression validation, and documentation examples without exposing private engineering memory.

Long-term direction: sample fixtures should remain clearly marked as fixtures and may later move under a fixture/test namespace so normal deployments do not confuse sample data with real user knowledge.

---

## Repository Layout

```text
wiki/                         Markdown source-of-truth
wiki/_system/                 Planned self-describing policy and operation guides
wiki/*-index.md               Planned category indexes for flat-first knowledge files
wiki/<objective-slug>/         Objective namespaces for long-running projects/domains
tools/importer/               Import / retrieval / governance pipeline
tools/importer/.env.example   Importer runtime env template
tools/importer/.env           Local runtime env, gitignored
bin/                          CLI wrappers
archive/                      Historical prototype artifacts
logs/                         Local runtime logs, gitignored
backups/                      Local backups, gitignored
```

---

## Wiki Knowledge Layout

Hermes Runes uses a flat-first, folder-when-needed Markdown layout.

### Flat-first files

General personal RAG notes should start as flat files under `wiki/`:

```text
wiki/<category>-<topic>-<note_type>.md
```

Baseline categories:

```text
specs
engineering
products
operations
references
personal
```

Example:

```text
wiki/specs-voip-softbank-sip-spec.md
wiki/engineering-rag-context-assembly-design.md
wiki/products-platform-chronos-grace-c1-profile.md
```

### Objective namespaces

Long-running projects, platforms, product investigations, or engineering objectives may be promoted into an objective namespace:

```text
wiki/<objective-slug>/
```

Example:

```text
wiki/k6-freelancer/
├── README.md
├── baselines.md
├── decisions.md
├── services.md
├── verification.md
├── next-actions.md
└── operations.md
```

Objective namespaces may contain additional purpose-specific Markdown files when default lifecycle files are not enough. When a new file is added inside an objective namespace, the objective `README.md` must be updated with the relationship, and the new file must link back through its metadata section.

### Markdown-native metadata

P0 baseline uses Markdown-native metadata sections, not YAML frontmatter.

A normal memory file should use:

```markdown
# <Title>

## Metadata

- Category: <specs|engineering|products|operations|references|personal>
- Topic: <topic-slug>
- Note type: <spec|requirements|design|decision|baseline|profile|runbook|troubleshooting|reference|preference|note>
- Status: <draft|active|superseded|archived>
- Memory quality: <verified|user-approved|agent-drafted|inferred|needs-review>
- Related objective: <none|objective-slug>
- Parent index: wiki/<category>-index.md
- Source type: <user-curated|hermes-agent-curated|external-summary|manual-note>
- Last reviewed: <YYYY-MM-DD>

## Summary

## Canonical Memory

## Evidence / Source Notes

## Open Questions

## Change Log
```

The primary solidified memory belongs in `## Canonical Memory`.

Metadata classifies the file. Summary helps relevance. Evidence records source context. Open Questions must not be treated as confirmed truth.

---

## Hermes Agent Integration Boundary

Hermes Agent may learn how to use Hermes Runes as a native-memory skill, but native memory is not the authority for Hermes Runes policy.

Before operating Hermes Runes, the agent should `decipher` the current policy / guide state or at least verify freshness through policy hashes and the latest chronicle entry.

Hermes Agent should use Hermes Runes as follows:

```text
Policy / operation guide read       → decipher
Personal RAG retrieval              → evoke
Markdown source-of-truth mutation   → forge
Import / embed / index lifecycle    → inscribe
Diagnostics / consistency checks    → probe
Structural change record            → chronicle
```

Hermes Runes is one governed personal RAG source among multiple possible sources. Hermes Agent must still compare:

```text
current user instruction
Hermes Agent native memory
Hermes Runes evidence
third-party RAG / notes / Obsidian
web search or external public sources
```

Third-party RAG and note systems are auxiliary sources, import candidates, comparison sources, or explicitly requested search targets. They should not silently override Hermes Runes canonical personal memory, and Hermes Runes should not silently override them either. The agent performs the comparison.

---

## Runtime Environment

The normal quickstart uses an importer-local environment file:

```text
tools/importer/.env.example  # public template, tracked by git
tools/importer/.env          # local runtime config, never committed
```

Create it with:

```bash
cp tools/importer/.env.example tools/importer/.env
vi tools/importer/.env
```

A root `.env` is not required for the normal deployment flow. Keeping the active runtime config under `tools/importer/` avoids ambiguity between multiple environment files.

Database connection resolution is centralized in:

```text
tools/importer/db_config.py
```

Core importer, FTS, hybrid, vector, embedding, legacy search, metadata inspection, stale report, and stale purge tools use the shared database config helper.

Developer-only direct tooling may use local `.env` settings for observation, tuning, smoke tests, and single-feature verification. Real secrets must never be committed.

---

## Quickstart

See:

```text
QUICKSTART.md
```

---

## Current Baseline Status

Current repository baseline includes:

```text
M5      Retrieval / Context Baseline              PASS
M10     Observation Governance Baseline           PASS
M11     Observation Summary Baseline              PASS
M11.6   Repository Portability Baseline           PASS
M11.6   Sample Public Fixture Baseline            PASS
M12.1   Requirements Baseline                     PASS
M12.2   Importer-local Environment Layout         PASS
M12.3   Runtime Safety Audit                      PASS
M12.3a  DB Config Portability Cleanup             PASS
M13     Retrieval Governance + Semantic Hybrid    PASS / frozen
M14.1   Context Assembly Diagnostics              PASS / frozen
```

M12.3 local-only LM Studio token exposure is accepted/deferred because it is LAN-only, not committed to GitHub, and can be rotated before long-term production use.

---

## Current Scope

Hermes Runes currently focuses on:

- governed local personal RAG
- Markdown memory governance
- retrieval quality
- context assembly diagnostics
- evaluation
- repository portability
- Hermes Agent integration boundary design

It is not currently intended to be:

- a full multi-user SaaS platform
- a distributed cloud memory platform
- a fully autonomous self-modifying agent framework
- a replacement for Hermes Agent decision-making

---

## Roadmap

See:

```text
ROADMAP.md
```

Current roadmap direction:

```text
P0 before trial run:
- self-describing wiki policy baseline
- Hermes Agent operation guide
- source priority and third-party RAG relationship
- governed wiki operation policy
- change-history / chronicle policy
- index consistency rules
- forge / decipher / evoke / inscribe / probe vocabulary
- P0 writer and consistency-probe boundaries

P1 after trial feedback:
- policy bundle hash / freshness implementation
- conflict handling
- archive/delete/purge separation
- metadata extraction into database fields
- source-status-aware retrieval filtering/downranking
- objective promotion tooling

P2 mature improvements:
- split / merge automation
- redirects / tombstones
- stronger metadata schema or YAML frontmatter if justified
- advanced source reconciliation support for Hermes Agent
- sensitivity classifier and purge workflow
```

---

## Security Principles

Real secrets must never be committed into Markdown memory or repository-tracked files.

This includes:

- API keys
- PostgreSQL passwords
- Telegram tokens
- local credentials
