# M27 Human-approved Apply MVP Verification

Status: PASS / CONTROLLED TRUSTED WIKI MUTATION BASELINE
Milestone: M27 Human-approved Apply MVP / Controlled Write Boundary
Chinese: M27 人類核准套用 MVP / 受控寫入邊界

## Purpose

M27 introduces the first controlled trusted Markdown wiki mutation path from a human-approved promotion patch preview into governed long-term memory.

M27 preserves the M26.5 safety contract while allowing a bounded, explicit, single-target trusted wiki write.

M27 is not autonomous memory writing.

M27 is a:

- human-approved
- single-target
- hash-guarded
- confirmation-token-gated
- rollback-aware
- operation-recorded
- post-verification-aware

controlled write boundary.

## Relationship to M26.5

M26.5 locked the safety boundary:

```text
M26 Human-approved Promotion Apply / Dry-run-to-Apply Boundary:
PASS / stable safety-boundary baseline / no apply implementation
```

M27 crosses from preview into trusted Markdown mutation only while preserving the M26.5 governance contract.

## M27.1 Design Lock

M27.1 locked the controlled apply design before introducing the apply CLI.

Locked requirements:

1. concrete proposal ID
2. target path under `wiki/`
3. single target heading/insertion point
4. explicit insert text
5. current pre-apply file hash
6. expected pre-apply hash
7. matching confirmation token
8. visible patch candidate/diff
9. rollback snapshot
10. operation record
11. post-apply hash evidence

## M27.2 Controlled Apply CLI MVP

M27.2 implemented the first controlled trusted wiki mutation helper:

```text
tools/runes/promotion_apply_m27_2.py
```

M27.2 controlled apply requires:

```text
--apply
--expected-pre-hash
--human-confirmation
```

M27.2 is allowed to write:

- one target Markdown wiki file
- one rollback snapshot
- one operation record

M27.2 is not allowed to:

- write outside `wiki/`
- write multiple wiki files
- mutate proposal state
- mutate attunement state
- mutate promotion state
- mutate PostgreSQL / FTS / pgvector
- run importer implicitly
- rebuild indexes implicitly
- infer approval from smoke PASS
- run autonomous apply

## M27.3 Controlled Apply Smoke Lock

Verification record:

```text
wiki/k6-freelancer/verification-m27-3-controlled-apply-smoke-lock.md
```

M27.3 verified:

- controlled trusted wiki mutation
- rollback snapshot generation
- operation record generation
- expected pre-hash validation
- confirmation-token validation
- candidate post-hash verification
- single-target containment
- wrong-hash BLOCKED behavior
- no database mutation
- no importer mutation
- no proposal-state mutation

M27.3 established the first real trusted Markdown mutation regression baseline.

## Locked Safety Invariants

M27 preserves:

- proposal is not trusted memory until controlled apply succeeds
- preview is not apply
- preflight PASS is not apply approval
- rollback-plan preview is not rollback execution
- confirmation token is mandatory
- pre-apply hash validation is mandatory
- single-target apply only
- rollback snapshot evidence is mandatory
- operation record evidence is mandatory
- post-apply verification is mandatory
- importer/index refresh remains a separate future boundary
- trusted wiki apply is not autonomous apply

## Locked Non-Mutation Boundary

M27 verified and preserves:

```text
database_mutated: false
importer_mutated: false
proposal_state_mutated: false
```

This boundary remains mandatory until M28.

## Relationship to M28

M27 establishes controlled trusted wiki mutation.

M28 will establish the importer / retrieval refresh boundary.

M28 must preserve:

```text
trusted wiki apply != implicit importer mutation
```

Importer refresh, vector refresh, retrieval refresh, and recall verification remain explicitly separate governance boundaries.

## Verification Status

M27.1 Human-approved Apply Design Lock:

- M26.5 contract preserved: PASS
- controlled write boundary defined: PASS
- single-target policy locked: PASS
- expected pre-hash requirement locked: PASS
- confirmation-token requirement locked: PASS
- rollback snapshot requirement locked: PASS
- operation record requirement locked: PASS
- no implicit importer/index mutation: PASS
- no autonomous apply invariant preserved: PASS

M27.2 Controlled Apply CLI MVP:

- controlled apply helper implemented: PASS
- trusted wiki mutation implemented: PASS
- rollback snapshot generation implemented: PASS
- operation record generation implemented: PASS
- confirmation-token enforcement implemented: PASS
- expected pre-hash enforcement implemented: PASS
- no database mutation preserved: PASS
- no importer mutation preserved: PASS
- no proposal-state mutation preserved: PASS

M27.3 Controlled Apply Smoke Lock:

- controlled write path verified: PASS
- rollback evidence verified: PASS
- operation evidence verified: PASS
- wrong-hash blocking verified: PASS
- trusted wiki mutation verified: PASS
- no database mutation verified: PASS
- no importer mutation verified: PASS
- no proposal-state mutation verified: PASS
- governance boundary preserved: PASS

Overall:

M27 Human-approved Apply MVP / Controlled Write Boundary:
PASS / controlled trusted wiki mutation baseline
