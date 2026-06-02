# M27 Human-approved Apply MVP Verification

Status: DESIGN LOCK / CONTROLLED WRITE MVP STARTED
Milestone: M27 Human-approved Apply MVP / Controlled Write Boundary
Chinese: M27 人類核准套用 MVP / 受控寫入邊界

## Purpose

M27 introduces the smallest possible controlled write path from a human-approved promotion patch preview into trusted Markdown wiki memory.

M27 must preserve the M26.5 safety contract.

M27 is not autonomous memory writing. It is a human-approved, single-target, hash-guarded, confirmation-token-gated apply path.

## Relationship to M26.5

M26.5 locked the safety boundary:

```text
M26 Human-approved Promotion Apply / Dry-run-to-Apply Boundary:
PASS / stable safety-boundary baseline / no apply implementation
```

M27 may cross from preview into trusted Markdown mutation only if the M26.5 contract is preserved.

## M27.1 Design Lock

M27.1 locks the controlled apply design before introducing the apply CLI.

The controlled apply operation must require:

1. A concrete proposal ID.
2. A target path under `wiki/`.
3. A single target heading or insertion point.
4. Insert text supplied explicitly by the operator / agent-facing command.
5. The current pre-apply file hash.
6. An expected pre-apply hash supplied by the human/operator.
7. A matching confirmation token.
8. A visible patch candidate / diff from the M25/M26 preview chain.
9. A rollback snapshot before writing.
10. An operation record after writing.
11. Post-apply hash evidence.

## M27.2 Controlled Apply CLI MVP Scope

M27.2 may implement a direct script-level CLI:

```text
python tools/runes/promotion_apply_m27_2.py \
  --proposal-id '<proposal_id>' \
  --target-path 'wiki/k6-freelancer/<file>.md' \
  --heading '<heading>' \
  --insert-text '<markdown>' \
  --expected-pre-hash '<sha256>' \
  --human-confirmation '<token>' \
  --apply \
  --json
```

M27.2 is allowed to write:

- the single target Markdown wiki file
- one rollback snapshot under `backups/runes-apply/`
- one JSON operation record under `operations/runes-apply/`

M27.2 is not allowed to:

- write outside `wiki/` for the target
- write multiple wiki files
- mutate proposal state
- mutate attunement state
- mutate promotion state
- mutate PostgreSQL / FTS / pgvector
- run importer implicitly
- rebuild indexes implicitly
- apply without expected pre-hash
- apply without matching confirmation token
- run in background
- infer approval from smoke PASS

## Locked Safety Invariants

M27 preserves:

- proposal is not trusted memory until controlled apply succeeds
- preview is not apply
- preflight PASS is not apply approval
- rollback-plan preview is not rollback execution
- confirmation token is mandatory
- pre-apply hash validation is mandatory
- single-target apply only
- operation record evidence is mandatory
- rollback snapshot evidence is mandatory
- post-apply verification is mandatory
- importer/index refresh remains a separate future boundary

## M27.1 Verification Status

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

Overall:

M27.1 Human-approved Apply Design Lock:
PASS / controlled write MVP design locked
