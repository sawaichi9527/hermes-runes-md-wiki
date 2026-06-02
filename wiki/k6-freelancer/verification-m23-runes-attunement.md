# M23 Runes Attunement Workflow Verification

Status: DESIGN LOCK / P0 DRY-RUN SCOPE
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

### ingest-summary

Used for certified or official documents such as specifications, RFCs, vendor manuals, and formal design documents.

Expected characteristics:

- higher source trust
- source reference required
- scope and interpretation must still be checked
- low-risk fast attunement may be acceptable

### research-note

Used for websites, articles, public discussions, news, blog posts, titles, or externally researched topics.

Expected characteristics:

- mixed source trust
- may contain uncertainty
- should not be written as certified fact unless verified
- comparison and confidence note are preferred

### memory-candidate

Used when Hermes-agent identifies knowledge from user interaction that may deserve long-term memory solidification.

Expected characteristics:

- user-context source
- requires user confirmation
- should explain why the knowledge should be remembered

### replace-memory

Used when Hermes-agent proposes replacing, superseding, or rewriting existing wiki knowledge.

Expected characteristics:

- higher risk than add-only memory
- old reference required
- reason required
- diff preview should be introduced in later milestones

### wiki-operation

Used when Hermes-agent proposes direct Markdown wiki operations such as create, modify, remove, tag, or mark.

Expected characteristics:

- always through Runes Shield
- dry-run first
- path preview required
- trusted wiki mutation not implemented in M23

## M23 Scope

M23 includes:

- Runes Attunement terminology lock
- proposal intent model
- state transition design
- approve/reject/supersede dry-run design
- human-readable attunement preview design
- attunement trail preview design
- separation between approval and promotion

## M23 Non-goals

M23 explicitly excludes:

- automatic trusted wiki mutation
- direct database mutation
- autonomous approval
- approve execution
- reject execution
- cleanup execution
- curated promotion execution
- multi-user RBAC
- approval quorum
- reviewer assignment
- web dashboard
- background worker
- workflow engine
- enterprise policy engine

## Runes Shield Boundary

All Hermes-agent interactions with Hermes Runes MD Wiki must go through Runes Shield.

Hermes-agent must not:

- write trusted wiki files directly
- mutate proposal state directly
- mutate database records directly
- bypass Runes Shield for memory proposal operations

## Personal-use Boundary

M23 is intentionally personal-use scoped.

It should preserve extension flexibility without introducing enterprise complexity.

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

Deferred extensions:

- execute approval
- append-only attunement trail write
- metadata status update
- approved proposal listing
- stale proposal report
- promotion patch preview
- trusted wiki promotion execution
- rollback helper

## Verification Status

M23.1 Runes Attunement concept lock:

- terminology: PASS
- state model: PASS
- proposal intent model: PASS
- P0 dry-run boundary: PASS
- non-goals locked: PASS
- direct trusted wiki mutation forbidden: PASS
- autonomous trusted-memory mutation forbidden: PASS

Overall:

M23 Runes Attunement Workflow / Dry-run:
DESIGN LOCK / READY FOR DRY-RUN CLI DESIGN
