# Developer Policy

Status: P0 baseline

## Purpose

This document describes developer-only expectations and exceptions.

Hermes Runes is primarily intended to be operated through Hermes Agent.

However, repository developers may still need direct tooling for:

- smoke tests
- importer validation
- observation review
- retrieval diagnostics
- tuning experiments
- migration work
- standalone verification

## Runtime Environment

Normal runtime configuration currently uses:

```text
tools/importer/.env
```

This is intended for:

- local developer testing
- importer runtime config
- observation experiments
- smoke verification
- direct retrieval tooling

It is not intended to be committed into Git.

## Canonical Principle

Developer convenience must not bypass:

- Markdown source-of-truth
- governed operation policy
- safety boundaries
- repository portability

## Direct Tooling

Direct developer tooling is allowed for:

- debugging
- evaluation
- migration
- benchmarking
- retrieval inspection
- metadata inspection

But production Hermes Agent workflows should prefer governed interfaces.

## Local-first Philosophy

Hermes Runes is intentionally optimized for:

- local-first workflows
- personal usage
- inspectability
- maintainability
- low operational complexity

Developer tooling should preserve this philosophy.

## Change Log

- 2026-06-01: Initial developer policy.
