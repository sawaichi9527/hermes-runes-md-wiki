# Forge Safety Design

Status: M15.4 design baseline  
Scope: planned governed Markdown writer safety model

## Purpose

This document defines the safety model for future `hermes-runes forge` operations.

`forge` is the governed write layer for `wiki/` Markdown source-of-truth.

It must protect:

- Markdown source files
- category indexes
- objective README file maps
- change-history
- import / embedding consistency
- local recovery after partial failure

This document is design guidance, not a full writer implementation.

---

## Core Principle

```text
Multiple readers are allowed.
Only one governed writer may mutate wiki/ at a time.
```

Hermes Agent should not directly perform structural wiki edits.

Hermes Agent should request `forge` operations.

---

## P0 Forge Operations

P0 operations:

```text
create-flat
create-objective
create-objective-file
update-content
rename
archive
```

Reserved operations:

```text
move
promote
restore
purge
resolve-conflict
split
merge
```

Reserved operations should be represented in policy and change-history event types, but do not need full P0 implementation.

---

## Write Critical Section

A future `forge` operation should treat the following as one critical section:

```text
acquire lock
create operation manifest
validate paths
stage files
write temp files
atomic replace target files
update indexes / objective README
append change-history
run inscribe
run probe subset
write final manifest status
release lock
```

The critical section is local and cooperative.

It is not intended to be a distributed transaction system.

---

## Locking Strategy

P0 direction:

```text
local cooperative file lock
```

Suggested lock file:

```text
.runes/locks/wiki-write.lock
```

Rules:

- all governed write tools must respect the same lock
- read-only operations do not require the write lock
- write lock must record owner/process metadata where practical
- stale lock recovery should be conservative

Future implementation may use Python `fcntl.flock` on Linux.

---

## Operation Manifest

Every forge operation should create a manifest.

Suggested location:

```text
.runes/operations/<operation-id>.json
```

Suggested fields:

```json
{
  "operation_id": "20260601-000001-create-flat",
  "operation": "create-flat",
  "status": "started",
  "started_at": "2026-06-01T00:00:00+08:00",
  "finished_at": null,
  "actor": "hermes-agent",
  "approved_by": "user",
  "paths": {
    "targets": [],
    "indexes": [],
    "backups": [],
    "temps": []
  },
  "steps": {
    "lock": "pass",
    "validate": "pending",
    "stage": "pending",
    "replace": "pending",
    "indexes": "pending",
    "chronicle": "pending",
    "inscribe": "pending",
    "probe": "pending"
  },
  "error": null,
  "recovery_hint": null
}
```

The manifest is for recovery and diagnosis.

It is not canonical memory.

It should not be ingested into RAG.

---

## Staging and Atomic Replace

A future writer should avoid direct overwrite.

Preferred flow for file writes:

```text
write temp file
fsync temp file where practical
backup old target if target exists
atomic replace temp → target
fsync parent directory where practical
```

Suggested temp naming:

```text
.<target-name>.tmp.<operation-id>
```

Atomic replace should occur only within the same filesystem.

---

## Backup Policy

Before replacing an existing file, create a local backup path recorded in the manifest.

Suggested location:

```text
.runes/backups/<operation-id>/<relative-path>
```

Backups are local recovery artifacts.

They should not be treated as canonical memory.

They should normally be gitignored.

---

## Path Safety

`forge` must reject:

- absolute paths
- `../` traversal
- symlink escape
- writes outside repository `wiki/`
- normal knowledge writes under `wiki/_system/` unless operation explicitly targets policy maintenance

Paths should use lowercase slug-style names where practical.

Human-readable titles belong inside Markdown headings, not necessarily in file paths.

---

## Index Consistency

Structural operations must update affected relationship files.

Examples:

| Operation | Affected relationship files |
|---|---|
| create flat file | `wiki/<category>-index.md` |
| create objective | `wiki/long-term-objectives-index.md` |
| create objective file | `wiki/<objective-slug>/README.md` |
| rename | all affected indexes and README references |
| archive | affected indexes, README references, change-history |

Index updates belong inside the same forge operation.

---

## Change History

Structural operations must append to:

```text
wiki/_system/change-history.md
```

The change-history entry should include:

```text
event type
operation id
actor
approval
paths changed
indexes updated
inscribe status
probe status
recovery hint if partial
```

Normal RAG recall and answer generation must not write change-history.

---

## Partial Success States

`forge` must distinguish file write success from index lifecycle success.

Example states:

```text
FORGE_PASS_INSCRIBE_PASS_PROBE_PASS
FORGE_PASS_INSCRIBE_FAIL_PROBE_SKIPPED
FORGE_PASS_INDEX_WARN_INSCRIBE_PASS_PROBE_WARN
FORGE_FAIL_NO_WRITE
FORGE_FAIL_PARTIAL_WRITE_RECOVERY_REQUIRED
```

A Markdown write can succeed while import/embed/probe fails.

This must be reported honestly.

---

## Recovery Principles

If recovery is needed:

1. Do not guess silently.
2. Read the operation manifest.
3. Inspect target files.
4. Inspect temp files.
5. Inspect backups.
6. Check index relationship files.
7. Re-run `inscribe` if Markdown is already correct.
8. Re-run `probe` after recovery.
9. Ask user before destructive recovery.

## Crash Scenarios

### Crash before replace

Likely state:

- temp file exists
- target unchanged
- manifest status incomplete

Recovery:

- discard temp or ask user to inspect
- mark manifest failed/recovered

### Crash after replace before index update

Likely state:

- target changed
- index not updated

Recovery:

- update index or restore backup after user confirmation
- run inscribe/probe

### Crash after index update before inscribe

Likely state:

- Markdown state probably valid
- derived index stale

Recovery:

- run `inscribe refresh`
- run `probe policy/indexes`

### Crash during inscribe

Likely state:

- Markdown valid
- derived index uncertain

Recovery:

- rerun importer/embed-missing
- run retrieval smoke if needed

---

## Probe After Write

After write, run a minimal probe subset:

```text
probe policy
probe indexes
probe objectives
probe links
```

P0 may implement only available probes, but the manifest should record what was run or skipped.

---

## User Approval Boundary

Forge should require approval for:

- creating objective namespace
- creating new flat-first memory
- creating new objective file
- changing draft to active
- renaming
- archiving/deleting
- importing external notes as canonical memory
- conflict resolution

Non-destructive automatic steps may proceed after approval:

- index update
- change-history append
- inscribe
- probe

---

## Non-goals

P0 Forge is not:

- a distributed lock manager
- a database transaction manager
- an enterprise CMS workflow
- a multi-user approval system
- an autonomous memory rewriting agent

Keep it local, simple, inspectable, and recovery-friendly.

---

## Implementation Milestones

### M15.4a

Document safety design.

### M15.4b

Implement lock/manifest helper only.

### M15.4c

Implement read-only recovery/probe helper.

### M15.5

Implement first minimal `forge create-flat --dry-run`.

### M15.6

Implement first real write path after dry-run smoke passes.

---

## Change Log

- 2026-06-01: Initial Forge safety design baseline.
