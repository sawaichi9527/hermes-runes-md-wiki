# M28 Importer / Retrieval Refresh Boundary

Status: PASS / GOVERNED RETRIEVAL REFRESH BASELINE / P0 TRIAL-RUN READY
Milestone: M28 Importer / Retrieval Refresh Boundary
Chinese: M28 匯入器 / 檢索刷新邊界

## Purpose

M28 establishes the governance boundary between:

```text
trusted Markdown wiki mutation
and
retrieval/index/vector refresh
```

M27 established controlled trusted wiki mutation.

M28 establishes how newly applied trusted Markdown memory becomes visible to:

- importer
- PostgreSQL FTS
- pgvector
- hybrid retrieval
- recall
- context builder
- answer generator

without allowing hidden or implicit index mutation.

## Core Principle

M28 preserves:

```text
trusted wiki apply != implicit importer mutation
```

Controlled trusted wiki apply must never silently:

- run importer
- rebuild retrieval indexes
- mutate PostgreSQL
- mutate pgvector
- refresh retrieval cache
- refresh vector embeddings
- alter retrieval ordering

Importer and retrieval refresh are explicit governed operations.

## Relationship to M27

M27 established:

```text
controlled trusted wiki mutation baseline
```

M27 intentionally preserved:

```text
database_mutated: false
importer_mutated: false
proposal_state_mutated: false
```

M28 introduces a separately governed refresh path and proves retrieval visibility after explicit refresh.

## M28.1 Design Lock

M28.1 locked the retrieval refresh design before implementation.

A refresh operation must:

1. be explicitly invoked
2. identify a concrete target path or project
3. expose importer execution status
4. expose changed chunk counts
5. expose retrieval refresh evidence
6. expose post-refresh recall evidence
7. preserve rollback and operation evidence
8. avoid hidden side effects
9. avoid autonomous background refresh
10. remain inspectable from CLI output

## M28.2 Controlled Importer Refresh Helper

M28.2 implemented:

```text
tools/runes/import_refresh_m28_2.py
```

The helper explicitly runs:

```text
tools/importer/importer.py
```

M28.2 verified:

- controlled refresh status: PASS
- importer executed: PASS
- database refresh attempted: PASS
- importer summary parsed: PASS
- operation record written: PASS
- post-refresh recall verification required: PASS
- trusted wiki mutated: false
- proposal state mutated: false
- attunement state mutated: false
- promotion state mutated: false

Observed smoke summary:

```text
schema=public
imported_or_changed=17
updated=1
skipped=40
chunks_written=215
```

## M28.3 Post-refresh Recall Verification

M28.3 implemented:

```text
tools/runes/recall_verify_m28_3.py
```

M28.3 verifies that post-refresh retrieval can find canonical trusted memory evidence.

Verified target:

```text
wiki/k6-freelancer/verification-m27-human-approved-apply-mvp.md
```

Verified marker:

```text
CONTROLLED TRUSTED WIKI MUTATION BASELINE
```

M28.3 verified:

- status: PASS
- json_parse_ok: true
- recall_returncode_ok: true
- expected_path_found: true
- required_marker_found: true
- post_refresh_recall_verified: true
- retrieval_provenance_checked: true

M28.3 preserves:

- trusted_wiki_mutated: false
- database_mutated: false
- importer_mutated: false
- proposal_state_mutated: false

## M28.4 Retrieval Consistency Smoke

M28.4 implemented:

```text
tools/runes/retrieval_consistency_m28_4.py
```

M28.4 verifies multiple canonical governance baselines in the retrieval layer.

Verified cases:

1. `m27_controlled_apply_baseline`
2. `m27_smoke_lock`
3. `m28_refresh_boundary`

M28.4 local smoke result:

```text
status: PASS
case_count: 3
failed_count: 0
```

Each case verified:

- expected_path_found: true
- required_marker_found: true
- json_parse_ok: true
- recall_returncode_ok: true
- post_refresh_recall_verified: true
- retrieval_provenance_checked: true

M28.4 preserves:

- apply_not_executed_here: true
- refresh_not_executed_here: true
- retrieval_consistency_only: true
- trusted_wiki_mutated: false
- database_mutated: false
- importer_mutated: false
- proposal_state_mutated: false

## Locked Safety Invariants

M28 preserves:

- trusted wiki apply is not importer refresh
- importer refresh is not proposal approval
- retrieval refresh is not autonomous mutation
- importer execution must remain explicit
- retrieval evidence must remain inspectable
- post-refresh recall verification must remain explicit
- governance provenance must remain visible
- retrieval consistency smoke must not mutate wiki or database

## Governed Pipeline Now Established

M28.5 freezes the governed P0 pipeline:

```text
proposal
→ attunement
→ promotion preview
→ preflight
→ controlled apply
→ explicit importer refresh
→ post-refresh recall verification
→ retrieval consistency smoke
```

This establishes:

```text
P0 Governed Trial Run Ready
```

## Remaining Scope After M28

Trial-run work should now focus on real operational usage, not new core boundary construction.

Recommended next stage:

```text
M29 P0 Trial Run Scenario Pack
```

M29 should validate:

- real user-provided knowledge proposal
- human attunement decision
- controlled promotion preview
- controlled apply
- explicit refresh
- post-refresh recall
- provenance review
- reject/no-promotion case
- correction/update case

## Verification Status

M28.1 Importer / Retrieval Refresh Design Lock:

- apply vs refresh boundary locked: PASS
- explicit importer execution policy locked: PASS
- no hidden refresh invariant locked: PASS
- retrieval provenance preservation locked: PASS
- post-refresh recall verification requirement locked: PASS
- no autonomous refresh invariant preserved: PASS

M28.2 Controlled Importer Refresh Helper:

- helper implemented: PASS
- importer executed explicitly: PASS
- importer summary parsed: PASS
- operation record written: PASS
- post-refresh recall verification required: PASS
- no trusted wiki mutation: PASS
- no proposal-state mutation: PASS

M28.3 Post-refresh Recall Verification:

- helper implemented: PASS
- recall JSON parsed: PASS
- expected path found: PASS
- required marker found: PASS
- retrieval provenance checked: PASS
- no mutation boundary preserved: PASS

M28.4 Retrieval Consistency Smoke:

- helper implemented: PASS
- canonical case count: 3
- failed count: 0
- M27 controlled apply baseline retrieved: PASS
- M27 smoke lock baseline retrieved: PASS
- M28 refresh boundary retrieved: PASS
- consistency-only boundary preserved: PASS

M28.5 Roadmap / Verification Freeze:

- M28 baseline frozen: PASS
- P0 governed pipeline declared: PASS
- P0 trial-run readiness declared: PASS
- M29 next-stage direction declared: PASS

Overall:

M28 Importer / Retrieval Refresh Boundary:
PASS / governed retrieval refresh baseline / P0 trial-run ready
