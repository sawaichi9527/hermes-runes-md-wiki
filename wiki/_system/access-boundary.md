# Access Boundary Policy

Status: P0 baseline

## Purpose

This document defines access boundaries for Hermes Runes MD Wiki.

Hermes Runes is a personal single-owner system, but Hermes Agent may have 2–4 concurrent personas or access paths reading from the same memory substrate.

## Read Boundary

Concurrent reads are allowed.

Allowed concurrent read operations include:

- `decipher` policy/index/objective reads
- `evoke` RAG recall
- context diagnostics
- retrieval diagnostics
- read-only `probe` checks

Read operations should not mutate Markdown source files.

## Write Boundary

Only one governed writer may operate at a time.

Writer means any operation that changes:

- Markdown source-of-truth files
- objective namespace structure
- category indexes
- objective README file maps
- change-history
- archive/delete state
- import/embed/index lifecycle as part of a write operation

## Single-writer Rule

Structural writes must go through governed `forge` operations.

`forge` should eventually enforce:

- local write lock
- path validation
- staged writes
- atomic file replace where practical
- index relationship updates
- change-history append
- import/index refresh
- consistency probe

## Failure and Recovery

P0 policy must account for:

- process crash
- partial write
- import failure after Markdown write
- embedding failure after import
- local power or hardware failure

Future writer tooling should use:

- operation manifest
- temporary files
- backup when replacing existing files
- clear partial-success reporting
- recovery probe

## Partial Success Reporting

If Markdown write succeeds but `inscribe` fails, the operation must not be reported as fully successful.

Example status:

```text
Forge: PASS
Inscribe: FAIL
Probe: SKIPPED
Recovery: rerun inscribe/probe
```

## Agent Boundary

Hermes Agent should not directly perform structural Markdown writes by manually editing wiki files.

Hermes Agent should request governed `forge` operations.

## Change Log

- 2026-06-01: Initial access boundary policy.
