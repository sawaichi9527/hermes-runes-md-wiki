# Observation Policy

Status: P0 baseline

## Purpose

This document defines observation logging philosophy for Hermes Runes.

Observation exists for:

- retrieval diagnostics
- tuning evidence
- extraction quality review
- rerank review
- workflow debugging
- smoke verification

Observation is not canonical memory.

## Canonical Principle

```text
observe first, tune later
```

Hermes Runes should gather enough evidence to support future improvements without overcomplicating the system.

## Observation Storage

Current baseline:

```text
local JSONL logs
lightweight
human-inspectable
not database-centric
```

## Observation Safety

Observation logs should avoid storing:

- full prompts
- full answers
- raw full memory context
- secrets
- raw personal dumps

## Memory Separation

Observation logs must not automatically enter:

- Markdown source-of-truth
- RAG retrieval indexes
- canonical memory

Observation is diagnostic evidence, not trusted memory.

## Future Governance

Future tooling may summarize:

- common retrieval failures
- category confusion
- metadata issues
- stale memory patterns
- Qwen forced-thinking contamination

However:

- policy should not auto-mutate
- heuristics should not auto-rewrite themselves
- human review remains authoritative

## Retention Philosophy

Planned baseline:

- local logs
- date-based rotation
- lightweight retention cleanup
- grep/jq-friendly format

Compression and database ingestion are intentionally deferred.

## Change Log

- 2026-06-01: Initial observation policy.
