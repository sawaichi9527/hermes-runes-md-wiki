# M25 Curated Promotion Patch Preview Verification

Status: PASS / STABLE DRY-RUN BASELINE
Milestone: M25 Curated Promotion Patch Preview / Dry-run
Chinese: M25 精選升格補丁預覽 / 乾跑

## Final Status

M25 Curated Promotion Patch Preview / Dry-run is now locked as:

```text
PASS / stable governed forge-preview baseline
```

M25 establishes the first governed forge-preview layer for Hermes Runes MD Wiki.

It allows Hermes-agent / Runes Shield to recommend how an attuned proposal could become a trusted Markdown wiki patch, while preserving the no-autonomous-write boundary.

## Core Principle

Forge suggestion, not forge execution.

M25 locks the following distinctions:

- proposal is not trusted memory
- attunement is not promotion
- patch preview is not wiki mutation
- forge preview is not forge execution
- promotion preview is not promotion execution
- human review remains required before any future apply

## Completed Scope

### M25.1 Curated Promotion Patch Design Lock

Status: PASS

M25.1 defined:

- curated promotion terminology
- candidate Markdown diff semantics
- single-target patch preview philosophy
- promotion evidence vs trusted memory distinction
- preview-only / no-mutation boundary

### M25.2 Promotion Patch Dry-run CLI

Status: PASS

M25.2 implemented:

```text
runes promotion preview \
  --proposal-id '<proposal_id>' \
  --target-path '<path>' \
  --heading '<heading>' \
  --insert-text '<markdown>' \
  --dry-run
```

Supported output:

- terminal-readable preview
- Markdown diff preview
- JSON preview

### M25.3 Promotion Patch Smoke Test

Status: PASS

Regression target:

```text
tools/runes/smoke_m25_3_promotion_patch.py
```

Confirmed smoke status:

```text
suite: M25.3 Curated Promotion Patch smoke test
status: PASS
failed: 0
total: 34
```

## Verified Capabilities

M25 verifies:

- helper payload generation
- CLI route through `bin/runes promotion preview`
- terminal-readable preview
- Markdown preview
- JSON preview
- unified diff generation
- candidate Markdown evidence rendering
- target Markdown hash unchanged
- no trusted wiki mutation
- no database mutation
- no importer mutation
- no promotion execution

## Locked Boundaries

M25 explicitly keeps the following unimplemented / forbidden:

- actual patch apply: not implemented
- trusted wiki write: forbidden
- proposal state mutation: forbidden
- attunement state mutation: forbidden
- database mutation: forbidden
- importer mutation: forbidden
- promotion execution: not implemented
- autonomous promotion execution: forbidden
- autonomous trusted-memory mutation: forbidden

## Current Tool Boundary

Current P0 command:

```text
runes promotion preview --proposal-id ... --target-path ... --heading ... --insert-text ... --dry-run
```

This command may render candidate patch evidence.

It must not:

- modify Markdown files
- write trusted wiki memory
- modify proposal metadata
- write to the database
- run importer/indexing
- mark a proposal as promoted
- apply a patch

## Personal-use Boundary

M25 remains personal-use scoped.

It must not become:

- an enterprise PR automation engine
- a multi-file merge engine
- a background promotion worker
- an autonomous wiki writer
- a direct database mutator
- a policy-heavy approval platform

## Next Milestone Boundary

The next milestone may explore:

```text
M26 Human-approved Promotion Apply / Dry-run-to-Apply Boundary
```

But M26 must start by designing the safety boundary before any actual apply behavior.

M25 itself ends at forge-preview dry-run only.
