# Memory Policy

Status: P0 baseline

## Purpose

This document defines the relationship between Hermes Agent memory, Hermes Runes MD Wiki, third-party RAG, notes, and external sources.

## Memory Layers

### Current conversation

The current user instruction and current conversation have immediate task priority.

### Hermes Agent native memory

Hermes Agent native memory may store:

- runtime preferences
- recent working state
- operation skill cache
- short summaries
- routing habits

Native memory is not the canonical long-term source-of-truth for governed project knowledge.

### Hermes Runes MD Wiki

Hermes Runes MD Wiki is the canonical governed personal/project long-term memory substrate.

It stores curated Markdown source-of-truth and provides indexed RAG recall evidence.

### Third-party RAG / notes

Third-party RAG and notes such as Obsidian are auxiliary sources.

They may be used as:

- comparison sources
- explicit search targets
- raw note sources
- import candidates

They do not silently replace Hermes Runes canonical memory.

### Web / external sources

Web and external sources are used for:

- current facts
- version-sensitive information
- public verification
- latest news or releases

## Canonical Memory

For normal Markdown memory files, confirmed long-term knowledge should be placed under:

```markdown
## Canonical Memory
```

`Metadata` helps classify.

`Summary` helps determine relevance.

`Evidence / Source Notes` records support context.

`Open Questions` should not be treated as confirmed truth.

## Memory Status

Baseline status values:

```text
draft
active
superseded
archived
```

Baseline memory quality values:

```text
verified
user-approved
agent-drafted
inferred
needs-review
```

Hermes Agent should treat draft, inferred, superseded, and archived memory with caution.

## Conflict Rule

If active memory conflicts with other active memory or external sources, Hermes Runes should expose the conflict as evidence.

Hermes Agent must perform final comparison and may ask the user for resolution.

## Change Log

- 2026-06-01: Initial memory policy.
