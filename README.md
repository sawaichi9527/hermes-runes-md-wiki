# Hermes Runes MD Wiki

Markdown wiki source-of-truth for governed local RAG memory.

> **Open Beta:** Hermes Runes MD Wiki is prepared for public Open Beta evaluation. It is suitable for personal/local evaluation and feedback collection, but it is not a stable public release, not an enterprise support commitment, and not a production guarantee.

Hermes Runes MD Wiki is a local-first, agent-agnostic memory substrate that uses curated Markdown wiki content as durable long-term knowledge, with PostgreSQL / FTS / pgvector retrieval, governed context assembly, and controlled wiki operations.

Hermes Runes was originally developed for Hermes Agent, but it is intentionally designed as an agent-agnostic subsystem that can be called by Hermes Agent, OpenClaw, MCP-compatible agents, OpenAI-compatible systems, or future local agent frameworks.

---

## Open Beta Boundary

```text
Open Beta means:
- public repository evaluation
- personal/local testing
- feedback and issue discovery are welcome
- docs and implementation may still change

Open Beta does not mean:
- stable release
- production support guarantee
- enterprise support commitment
- autonomous trusted memory writing
- automatic proposal apply
- storing secrets in Markdown wiki memory
```

See also:

```text
docs/open-beta-publication-checklist.md
SECURITY.md
```

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
Retrieval / Context Builder
```
