# Operations Baseline

Status: P0 baseline

## Purpose

This file records operational baseline notes for Hermes Runes governance and workflow behavior.

Unlike `change-history.md`, this file may include:

- operational observations
- workflow notes
- governance baseline checkpoints
- migration notes
- operational TODO context

## Current Operational Baseline

### Retrieval Core

```text
M13   Retrieval Governance + Semantic Hybrid   PASS / frozen
M14.1 Context Assembly Diagnostics             PASS / frozen / observation-enabled
```

Retrieval and context assembly baselines should remain stable while P0 governance policy is introduced.

### Governance Direction

Current governance direction:

```text
single-owner
local-first
human-approved write
Markdown source-of-truth
database as index
flat-first
folder-when-needed
```

### Agent Boundary

Hermes Runes provides:

- governed memory evidence
- source metadata
- operational safety
- deterministic wiki operations

Hermes Agent performs:

- source comparison
- final answer judgment
- memory placement decisions
- approval interaction

### Writer Philosophy

Planned writer direction:

```text
multiple readers
single governed writer
```

Structural writes should eventually support:

- write lock
- staged writes
- atomic replace where practical
- recovery-friendly workflow
- change-history append
- index consistency

## Current Priority

Current priority:

```text
P0 governance protection rails before trial run
```

Not current priority:

- enterprise scaling
- distributed cloud memory
- autonomous self-modifying systems
- excessive metadata complexity

## Change Log

- 2026-06-01: Initial operations baseline.
