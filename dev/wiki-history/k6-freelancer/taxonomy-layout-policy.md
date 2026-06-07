# Hermes Runes MD Wiki - Taxonomy & Layout Policy

Status: Draft Baseline
Phase: M11.6 Repository Readiness
Purpose: Define long-term Markdown knowledge organization policy for Hermes Runes MD Wiki.

---

# 1. Core Philosophy

Hermes Runes MD Wiki is a curated Markdown knowledge layer for governed local RAG memory.

Not all runtime memory becomes durable memory.

Only reviewed, curated, and intentionally preserved knowledge should become Markdown source-of-truth content.

The Markdown wiki is intended to store:

* architecture decisions
* baselines
* verification records
* operations knowledge
* long-term technical notes
* curated personal knowledge
* structured reference material

The wiki is NOT intended to store:

* raw prompts
* full chat transcripts
* raw observation logs
* temporary runtime state
* unreviewed agent reasoning
* secrets / API keys / passwords

---

# 2. Memory Layer Model

Hermes ecosystem memory is divided into multiple conceptual layers.

## Layer 1: Runtime Memory

Examples:

* current task state
* recent chat context
* tool execution state
* user preferences
* temporary agent memory

Characteristics:

* dynamic
* short-lived
* runtime-oriented
* may be automatically modified

---

## Layer 2: Curated Markdown Memory

Hermes Runes MD Wiki primarily focuses on this layer.

Examples:

* architecture decisions
* baselines
* technical verification
* deployment procedures
* project operations
* curated long-term notes

Characteristics:

* human-reviewable
* durable
* source-of-truth
* governance-aware
* regression-testable

---

## Layer 3: Personal Notes / Knowledge Garden

Examples:

* Obsidian-like notes
* reading notes
* hobby notes
* draft ideas
* semi-structured references

Characteristics:

* partially curated
* less formal
* may later become curated wiki content

---

## Layer 4: External / Specialized RAG

Examples:

* LLM wiki-like systems
* memPalace-like memory
* external document libraries
* semantic memory systems
* high-volume exploratory knowledge

Characteristics:

* optional
* replaceable
* may have weaker governance guarantees

---

# 3. Domain / Namespace / Note Type Model

Hermes Runes normalizes Markdown content into three conceptual dimensions.

## Domain

High-level category.

Examples:

* work
* tech
* hobbies
* life
* archive

---

## Namespace

Specific project or topic area.

Examples:

* k6-freelancer
* anime
* pc-hardware
* linux
* travel-japan

---

## Note Type

Purpose of the note.

Examples:

* baselines
* decisions
* verification
* operations
* references
* watchlist
* glossary
* comparisons

---

# 4. Flat-First Layout Policy

Hermes Runes adopts a lightweight "flat-first" layout policy.

Small namespaces SHOULD prefer flat Markdown filenames.

Example:

```text
wiki/hobbies-anime-watchlist.md
wiki/tech-pc-hardware-ssd.md
wiki/life-travel-japan.md
```

Recommended filename format:

```text
<domain>-<namespace>-<note_type>.md
```

Advantages:

* lightweight
* grep-friendly
* simple navigation
* low management overhead
* easy personal usage

---

# 5. Folder-When-Needed Policy

Namespaces MAY migrate into dedicated folders when complexity increases.

Typical triggers:

* more than ~8-12 Markdown files
* attachments/assets needed
* multiple related subtopics
* dedicated README/templates required
* long-term project maintenance

Example:

```text
wiki/hobbies/anime/
├── README.md
├── watchlist.md
├── studios.md
└── timelines.md
```

---

# 6. Engineering Project Exception

Engineering and long-lived technical projects SHOULD default to folder-based layout.

Reason:

* highest governance requirements
* future technical-document extraction
* stable path references
* verification-oriented structure
* long-term maintainability

Current example:

```text
wiki/k6-freelancer/
├── README.md
├── baselines.md
├── decisions.md
├── next-actions.md
├── operations.md
├── services.md
└── verification.md
```

This namespace is treated as a curated project-memory source-of-truth baseline.

---

# 7. Metadata Normalization

Regardless of physical file layout, importer logic SHOULD normalize content into common metadata fields.

Conceptual model:

```json
{
  "domain": "tech",
  "namespace": "pc-hardware",
  "note_type": "ssd",
  "path": "wiki/tech-pc-hardware-ssd.md"
}
```

or:

```json
{
  "domain": "tech",
  "namespace": "pc-hardware",
  "note_type": "ssd",
  "path": "wiki/tech/pc-hardware/ssd.md"
}
```

Folder structure is a human organization tool.

Metadata normalization is the system organization model.

---

# 8. Governance Levels

Different namespaces may use different governance strengths.

## High Governance

Examples:

* engineering projects
* deployment procedures
* baselines
* security policy

Expected:

* verification
* reproducibility
* smoke tests
* curated review

---

## Medium Governance

Examples:

* hardware knowledge
* Linux notes
* AI server comparisons

Expected:

* structured notes
* references
* periodic review

---

## Low Governance

Examples:

* anime notes
* hobby collections
* casual references

Expected:

* lightweight organization
* optional review
* personal convenience

---

# 9. Archive Policy

Deprecated or inactive namespaces SHOULD prefer archive migration instead of deletion.

Example:

```text
wiki/archive/
```

Reason:

* preserve historical context
* avoid accidental retrieval regression
* allow future restoration
* support long-term memory continuity

---

# 10. Agent-Agnostic Design

Hermes Runes MD Wiki is NOT tightly coupled to Hermes Agent runtime.

Hermes Agent is the first target consumer, but the memory layer is intended to be reusable by:

* OpenClaw
* future local agents
* MCP-compatible runtimes
* custom automation frameworks

The Markdown wiki layer should remain:

* portable
* inspectable
* independently queryable
* agent-agnostic

---

# 11. Guiding Principle

Runtime memory is temporary.

Curated Markdown memory is knowledge intentionally carved into durable runes.
