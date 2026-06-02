# M28 Importer / Retrieval Refresh Boundary

Status: DESIGN STARTED / GOVERNED REFRESH BOUNDARY
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

M28 introduces a separately governed refresh path.

## M28.1 Design Lock

M28.1 locks the retrieval refresh design before implementation.

A future refresh operation must:

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

## M28.2 Controlled Refresh Scope

A future M28 controlled refresh helper may:

- run importer explicitly
- refresh PostgreSQL FTS entries
- refresh pgvector entries
- refresh hybrid retrieval visibility
- generate refresh operation evidence
- run recall verification smoke

A future M28 controlled refresh helper must not:

- mutate trusted Markdown wiki content
- auto-approve proposals
- auto-apply promotion patches
- bypass Runes Shield governance
- mutate proposal state silently
- mutate attunement state silently
- mutate promotion state silently
- perform hidden background refresh

## M28.3 Retrieval Verification Scope

M28 retrieval verification must confirm:

- newly applied trusted memory becomes retrievable
- retrieval provenance remains visible
- retrieval citations remain valid
- trusted memory visibility matches importer state
- rejected/unapproved content remains excluded
- quarantine isolation remains preserved

## Locked Safety Invariants

M28 preserves:

- trusted wiki apply is not importer refresh
- importer refresh is not proposal approval
- retrieval refresh is not autonomous mutation
- importer execution must remain explicit
- retrieval evidence must remain inspectable
- post-refresh recall verification must remain explicit
- governance provenance must remain visible

## Future Direction

Planned follow-up milestones:

- M28.2 Controlled Importer Refresh CLI
- M28.3 Post-refresh Recall Verification
- M28.4 Retrieval Consistency Smoke
- M28.5 Roadmap / Verification Freeze

## Verification Status

M28.1 Importer / Retrieval Refresh Design Lock:

- apply vs refresh boundary locked: PASS
- explicit importer execution policy locked: PASS
- no hidden refresh invariant locked: PASS
- retrieval provenance preservation locked: PASS
- post-refresh recall verification requirement locked: PASS
- no autonomous refresh invariant preserved: PASS

Overall:

M28.1 Importer / Retrieval Refresh Design Lock:
PASS / governed refresh boundary design locked
