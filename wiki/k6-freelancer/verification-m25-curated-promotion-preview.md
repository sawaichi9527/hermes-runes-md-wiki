# M25 Curated Promotion Patch Preview Verification

Status: DESIGN LOCK / DRY-RUN CLI BASELINE
Milestone: M25 Curated Promotion Patch Preview / Dry-run
Chinese: M25 精選升格補丁預覽 / 乾跑

## Purpose

M25 defines a preview-only curated promotion patch layer.

It lets Hermes-agent recommend how an attuned proposal could be promoted into trusted Markdown wiki content, without granting autonomous write authority.

## Core Principle

Forge suggestion, not forge execution.

- proposal is not trusted memory
- patch preview is not wiki mutation
- forge preview is not promotion execution
- human review is required before any future apply

## M25.1 Design Scope

M25.1 defines:

- curated promotion terminology
- candidate Markdown diff semantics
- single-target patch preview philosophy
- promotion evidence vs trusted memory distinction
- preview-only / no-mutation boundary

## M25.2 CLI Baseline

M25.2 introduces:

```text
runes promotion preview --proposal-id '<proposal_id>' --target-path '<path>' --heading '<heading>' --insert-text '<markdown>' --dry-run --json
```

Supported previews:

- terminal-readable preview
- Markdown diff preview
- JSON preview

## Locked Boundaries

- promotion execution: not implemented
- trusted wiki mutation: forbidden
- proposal state mutation: forbidden
- database mutation: forbidden
- importer mutation: forbidden
- autonomous promotion execution: forbidden
- autonomous trusted-memory mutation: forbidden

## Verification Status

M25.1 Curated Promotion Patch Design Lock: PASS

M25.2 Promotion Patch Dry-run CLI: PASS

Overall:

M25 Curated Promotion Patch Preview / Dry-run:
DESIGN LOCK / DRY-RUN CLI BASELINE
