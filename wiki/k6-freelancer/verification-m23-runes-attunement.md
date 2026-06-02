# M23 Runes Attunement Workflow Verification

Status: PASS / STABLE P0 GOVERNED ATTUNEMENT BASELINE
Milestone: M23 Runes Attunement Workflow / Dry-run
Chinese: M23 符文調律流程 / 乾跑

## Purpose

M23 defines the personal human-governed approval workflow for Hermes-agent memory proposals.

Runes Attunement replaces enterprise-style audit/review terminology with a project-native concept:

- Hermes-agent may propose memory solidification.
- Runes Shield enforces the invocation boundary.
- Runes Attunement aligns proposals with user intent, source trust, existing wiki memory, and promotion boundaries.
- Trusted wiki mutation remains forbidden in M23.

## Terminology

- Attunement: noun; the proposal alignment workflow.
- Attune: verb; to perform proposal alignment.
- Attuned: adjective / past participle; a proposal accepted as a promotion candidate.

## Core Principle

Approved does not mean promoted.

In M23:

- approved means attuned as a promotion candidate.
- promotion means later trusted wiki mutation.
- promotion execution is not implemented in M23.

## State Model

M23 uses a minimal personal-use state model:

- pending
- approved
- rejected
- superseded

State meaning:

- pending: awaiting attunement.
- approved: attuned as promotion candidate.
- rejected: attunement rejected.
- superseded: replaced by newer attunement candidate.

## Proposal Intent Model

M23 defines proposal intent categories for future Runes Shield proposal handling.

- ingest-summary: certified specs, RFCs, manuals, official documents.
- research-note: websites, articles, public discussions, research topics.
- memory-candidate: user-context knowledge proposed for long-term memory.
- replace-memory: replacement or supersession of existing wiki knowledge.
- wiki-operation: proposed Markdown wiki create/modify/remove/tag/mark operation.

## M23 Completed Scope

- M23.1 Runes Attunement Concept Lock: PASS
- M23.2 Attunement dry-run CLI: PASS
- M23.3 Human-readable Attunement Preview: PASS
- M23.4 Attunement smoke test: PASS
- M23.5 Roadmap / verification lock: PASS

## M23.4 Smoke Baseline

Smoke test:

```text
tools/runes/smoke_m23_4_attunement.py
```

Verified behaviors:

- attune dry-run payload: PASS
- reject dry-run payload: PASS
- supersede dry-run payload: PASS
- readable preview availability: PASS
- no proposal state mutation: PASS
- no trusted memory creation: PASS
- no curated wiki mutation: PASS
- no database mutation: PASS
- no importer mutation: PASS
- no file writes: PASS

Latest verified local smoke result:

```text
suite: M23.4 Runes Attunement smoke test
status: PASS
failed: 0
total: 27
```

## Locked Governance Boundaries

M23 explicitly locks the following boundaries:

- approve execution: not implemented
- reject execution: not implemented
- supersede execution: not implemented
- cleanup execution: not implemented
- curated promotion execution: not implemented
- trusted wiki mutation: forbidden
- direct database mutation: forbidden
- importer mutation: forbidden
- autonomous attunement execution: forbidden
- autonomous trusted-memory mutation: forbidden

## Runes Shield Boundary

All Hermes-agent interactions with Hermes Runes MD Wiki must go through Runes Shield.

Hermes-agent must not:

- write trusted wiki files directly
- mutate proposal state directly
- mutate database records directly
- bypass Runes Shield for memory proposal operations
- treat attuned proposals as already-promoted trusted memory

## Personal-use Boundary

M23 is intentionally personal-use scoped.

It preserves extension flexibility without introducing enterprise complexity.

Allowed extension points:

- risk_level
- source_type
- source_trust
- target_path
- target_heading
- old_reference
- superseded_by
- decision_reason
- promotion_status
- attunement trail write

Deferred extensions:

- execute approval
- append-only attunement trail write
- metadata status update
- approved proposal listing
- stale proposal report
- promotion patch preview
- trusted wiki promotion execution
- rollback helper

## Non-goals

M23 explicitly excludes:

- automatic trusted wiki mutation
- direct database mutation
- autonomous approval
- autonomous rejection
- autonomous supersession
- multi-user RBAC
- approval quorum
- reviewer assignment
- web dashboard
- background worker
- workflow engine
- enterprise policy engine

## Overall Verification Status

M23 Runes Attunement Workflow / Dry-run:

```text
PASS / stable P0 governed attunement baseline
```
