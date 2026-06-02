# M26 Human-approved Promotion Apply Verification

Status: PASS / M26 STABLE SAFETY-BOUNDARY BASELINE / NO APPLY IMPLEMENTATION
Milestone: M26 Human-approved Promotion Apply / Dry-run-to-Apply Boundary
Chinese: M26 人類核准升格套用 / 乾跑到套用邊界

## Purpose

M26 defines the safety boundary for a future human-approved promotion apply flow.

M26 starts from the M25 stable forge-preview baseline and asks:

```text
If a human approves a curated promotion patch preview, what must be true before the patch may ever be applied to trusted Markdown wiki memory?
```

M26 does not implement trusted wiki apply.

It locks the safety model, preconditions, dry-run preflight, confirmation-token preview, rollback-plan preview, invariants, and non-goals for a future apply path.

## Core Principle

Human-approved apply must be explicit, bounded, reversible, and auditable.

A future apply operation must never be inferred from:

- proposal creation
- attunement approval
- attunement trail preview
- promotion patch preview
- preflight PASS
- rollback-plan preview
- smoke test success
- agent recommendation alone

## Relationship to Previous Milestones

M22 established proposal governance.

M23 established Runes Attunement dry-run.

M24 established Attunement Trail dry-run.

M25 established Curated Promotion Patch Preview dry-run.

M26 establishes the safety boundary for future human-approved apply.

The chain remains:

```text
proposal
→ attunement
→ attunement trail
→ curated promotion patch preview
→ human-approved apply safety boundary
```

M26 still ends before actual trusted wiki mutation.

## Required Future Preconditions

Before any future promotion patch apply can exist, all of the following must be required:

1. A concrete proposal ID.
2. A human-approved attunement state.
3. A generated promotion patch preview.
4. A stable target path inside `wiki/`.
5. A single intended target heading or insertion point.
6. A pre-apply file hash.
7. A post-apply expected hash or generated candidate hash.
8. A visible unified diff.
9. A human confirmation token or equivalent explicit approval signal.
10. An append-only operation record / attunement trail event.
11. A rollback or restore path.
12. A post-apply smoke / verification step.

## M26.1 Design Scope

M26.1 defines:

- dry-run-to-apply terminology
- apply preconditions
- single-target apply boundary
- expected file hash checks
- operation record requirement
- rollback requirement
- post-apply verification requirement
- no-autonomous-apply invariant

## M26.2 Apply Preflight Dry-run CLI Scope

M26.2 implements a preflight dry-run CLI that validates and previews:

- target path containment
- wiki-only path policy
- current target SHA256 evidence
- optional expected pre-apply hash check
- human confirmation token preview
- candidate patch diff evidence
- rollback plan preview
- operation record preview

M26.2 does not apply patches and does not write operation records or rollback snapshots.

## M26.3 Confirmation Token / Blocking Smoke Scope

M26.3 verifies:

- required confirmation token generation
- matching confirmation token remains preview-only
- hash mismatch blocks preflight
- non-wiki path blocks preflight
- outside-root path blocks preflight
- CLI JSON PASS route
- CLI JSON BLOCKED route
- target Markdown hash remains unchanged
- no trusted wiki mutation
- no database mutation
- no operation record write
- no rollback snapshot write

## M26.4 Rollback Plan Preview Scope

M26.4 previews:

- rollback strategy
- pre-apply hash evidence
- candidate evidence hash
- ordered rollback steps
- operation record plan

M26.4 does not write snapshots, does not apply rollback, and does not mutate trusted memory.

## M26.5 Roadmap / Verification Lock Scope

M26.5 locks M26 as a stable safety-boundary baseline.

Verification record:

- `wiki/k6-freelancer/verification-m26-5-roadmap-verification-lock.md`

M26.5 confirms:

- M26.1 safety design lock: PASS
- M26.2 preflight dry-run CLI: PASS
- M26.3 confirmation token / blocking smoke: PASS
- M26.4 rollback plan preview: PASS
- M26.5 roadmap / verification lock: PASS

M26.5 is not an apply MVP.

It is the lock point before any future controlled-write milestone.

## Non-goals

M26 explicitly does not implement:

- actual patch apply
- trusted wiki write
- database mutation
- importer mutation
- proposal state mutation
- attunement state mutation
- promotion state mutation
- automatic approval
- background apply worker
- multi-file merge engine
- enterprise approval workflow

## Locked Safety Invariants

A future apply implementation must preserve:

- proposal is not trusted memory
- attunement is not promotion
- patch preview is not wiki mutation
- preflight PASS is not apply approval
- rollback-plan preview is not rollback execution
- human-approved apply is not autonomous apply
- apply must be single-target first
- apply must verify target path containment
- apply must verify pre-apply hash
- apply must record operation evidence
- apply must support rollback or restoration
- apply must trigger or require post-apply verification

## Forbidden Behavior

The following remain forbidden:

- agent silently applying patches
- apply without explicit human confirmation
- apply from stale preview without hash check
- writing outside `wiki/`
- modifying `.env` or secret-bearing files
- modifying database directly
- running importer as an implicit side effect
- promoting unreviewed proposal content
- treating preview smoke PASS as approval
- treating rollback preview as rollback execution
- treating attunement approval as trusted memory mutation

## Future Direction

Future work may continue with:

- M27 Human-approved Apply MVP / Controlled Write Boundary

M27 must preserve the M26.5 contract and may only introduce a controlled write path if the following remain mandatory:

- explicit human approval
- confirmation token or equivalent approval signal
- single-target containment
- pre-apply hash validation
- visible diff or candidate evidence
- operation record evidence
- rollback or restore evidence
- post-apply verification
- no autonomous apply

## Verification Status

M26.1 Human-approved Promotion Apply Safety Design Lock:

- terminology: PASS
- preconditions: PASS
- no-apply boundary: PASS
- no-autonomous-apply invariant: PASS
- single-target first policy: PASS
- rollback requirement: PASS
- post-apply verification requirement: PASS

M26.2 Apply Preflight Dry-run CLI:

- path containment: PASS
- wiki-only path policy: PASS
- hash evidence: PASS
- confirmation token preview: PASS
- rollback plan preview: PASS
- operation record preview: PASS
- no mutation: PASS

M26.3 Apply Confirmation Token / Blocking Smoke:

- confirmation token generation: PASS
- hash mismatch block: PASS
- unsafe path block: PASS
- target hash unchanged: PASS
- no operation record write: PASS
- no rollback snapshot write: PASS
- no trusted wiki mutation: PASS

M26.4 Rollback Plan Preview:

- rollback strategy preview: PASS
- rollback evidence hashes: PASS
- ordered rollback steps: PASS
- operation record preview: PASS
- no rollback apply: PASS
- no trusted wiki mutation: PASS

M26.5 Roadmap / Verification Lock:

- completed M26 milestones enumerated: PASS
- stable safety baseline declared: PASS
- no-apply boundary preserved: PASS
- no-autonomous-apply invariant preserved: PASS
- future M27 boundary clarified: PASS

Overall:

M26 Human-approved Promotion Apply / Dry-run-to-Apply Boundary:
PASS / stable safety-boundary baseline / no apply implementation
