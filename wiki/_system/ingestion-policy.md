# Ingestion Policy

Status: P0 baseline

## Purpose

This document defines how external information may become Hermes Runes canonical memory.

## Canonical Principle

Not all retrieved information should become canonical memory.

Hermes Runes is intended for:

- curated memory
- governed memory
- durable project knowledge
- reviewed operational knowledge

not raw accumulation.

## Typical Ingestion Sources

Possible sources:

- user-authored Markdown
- Hermes Agent summaries
- uploaded documents
- web research summaries
- third-party RAG / Obsidian references
- operational verification notes

## Suggested Ingestion Flow

```text
source acquisition
↓
summary / normalization
↓
placement decision
↓
user approval when required
↓
forge Markdown source-of-truth
↓
inscribe import/index
↓
probe consistency
```

## Placement Decision

Hermes Agent should decide:

- existing objective namespace
- new objective namespace
- flat-first file
- no Hermes Runes write

based on:

- long-term value
- expected future reuse
- relationship complexity
- project/domain lifecycle

## External Sources

Third-party notes and web sources are not automatically canonical.

Hermes Agent should not automatically solidify:

- web search results
- scraped notes
- generated summaries
- external speculative content

without user approval.

## Draft vs Active

Imported information may begin as:

```text
Status: draft
```

Promotion to:

```text
Status: active
```

should normally involve user approval.

## Observation

Observation logs must not automatically become canonical memory.

Observation is for:

- diagnostics
- tuning
- retrieval evaluation
- workflow review

not memory ingestion.

## Change Log

- 2026-06-01: Initial ingestion policy.
