# M30.1 Repository Inventory / Technical Debt Map

Status: M30.1 INVENTORY / PRE-REFACTOR REVIEW
Milestone: M30.1 Repository Inventory / Technical Debt Map
Chinese: M30.1 儲存庫盤點 / 技術債地圖

## Purpose

M30 begins the pre-release hardening phase after the M29 Runes Seal baseline was successfully established.

M30.1 does not perform cleanup or refactor yet.

Instead, this milestone captures:

- current repository state
- local workspace technical debt
- modified/untracked artifact categories
- rollback anchors
- cleanup risks
- preservation boundaries
- refactor constraints before trial run

This document acts as the canonical preparation layer before M30 structural cleanup work.

## Current Baseline

Current remote sealed baseline:

```text
origin/archive/p0-runes-seal
```

Current sealed commit:

```text
3c6f860 docs: add M29 Runes Seal baseline
```

Current state summary:

```text
M29.1 Add Knowledge Scenario: PASS
M29.2 Reject / No-promotion Scenario: PASS
M29.3 Correction / Update Scenario: PASS
M29.5 Runes Seal Baseline: PASS
M29.6 Local Workspace Debt Inventory: PASS
```

## Local Backup State

Pre-M30 local backup:

```text
~/workspace/hermes-runes-md-wiki.local-backup-20260602-runes-seal-pre-m30/
```

Purpose:

```text
Preserve dirty workspace and runtime artifacts before M30 cleanup/refactor work.
```

Old pre-GitHub backup state:

```text
~/workspace/_delete_candidate_hermes-memory.local-backup-20260601-003128
```

Status:

```text
Kept temporarily.
Planned deletion only after P0 trial run begins and M30 cleanup stabilizes.
```

## Local Workspace Inventory Summary

Captured inventory statistics:

```text
modified files: 21
untracked files: 41
operations records: 20
root milestone shell files: 13
forge-inbox files: 5
inventory lines: 141
```

Inventory source directory:

```text
reports/m29-runes-seal-local-inventory/
```

## Modified File Categories

### Runtime / Entrypoint Drift

```text
bin/hermes-memory-smoke
bin/hermes-recall
bin/runes
```

Risk:

```text
Potential runtime behavior drift and inconsistent entrypoint conventions.
```

M30 review targets:

- canonical CLI naming
- entrypoint consolidation
- wrapper duplication
- shell/python boundary consistency

---

### Importer / Retrieval Runtime Modifications

```text
tools/importer/hybrid_search.py
tools/importer/observation_logger.py
```

Risk:

```text
Accumulated workaround logic, parser drift, retrieval compatibility patches, and observation-layer expansion.
```

M30 review targets:

- parser robustness
- retrieval mode compatibility
- warning handling policy
- observation schema consistency
- subprocess reliability

---

### Governance / Proposal / Smoke Helpers

```text
tools/runes/*.py
```

Examples:

```text
proposal_reader_m22_2.py
proposal_writer_m22_1.py
proposal_hygiene_m22_3.py
cleanup_plan_m22_4.py
trial_run_m21_4.py
smoke_runes_shield.py
```

Risk:

```text
Milestone-numbered helper sprawl and overlapping governance helper responsibilities.
```

M30 review targets:

- canonical naming policy
- module ownership boundaries
- stable public helper API
- smoke/helper separation
- long-term governance subsystem structure

---

### Trusted Wiki Drift

```text
wiki/k6-freelancer/next-actions.md
wiki/k6-freelancer/p0-trial-scenarios.md
wiki/k6-freelancer/verification.md
```

Risk:

```text
Scenario append duplication and mixed runtime/manual edits.
```

M30 review targets:

- idempotency policy
- scenario evidence normalization
- append-vs-rewrite governance
- verification document structure

## Untracked Artifact Categories

### Root Milestone Shell Scripts

Examples:

```text
m24_*.sh
m25_*.sh
m26_*.sh
```

Current interpretation:

```text
Temporary milestone execution helpers and debugging wrappers.
```

M30 review targets:

- archive vs retain decision
- conversion into canonical tools
- deletion policy
- naming policy

---

### Operations Evidence

Directory:

```text
operations/
```

Current interpretation:

```text
Valuable runtime governance evidence.
```

M30 review targets:

- retention policy
- archive policy
- git inclusion policy
- operational evidence schema

---

### Forge / Proposal Artifacts

Directories:

```text
tools/forge/
wiki/k6-freelancer/forge-inbox/
```

Current interpretation:

```text
Important governance and proposal-generation history.
```

M30 review targets:

- inbox lifecycle
- proposal archival policy
- forge tool structure
- trusted vs untrusted artifact separation

---

### Reports

Directory:

```text
reports/
```

Current interpretation:

```text
Pre-release technical debt evidence and inventory snapshots.
```

M30 review targets:

- report retention policy
- report archival policy
- reproducible inventory generation

## Preservation Rules Before Cleanup

M30 must preserve:

- M29 behavioral guarantees
- Runes Seal rollback anchor
- controlled apply safety boundaries
- explicit refresh boundary
- strict recall verification behavior
- negative recall semantics
- rollback evidence generation
- operation evidence generation

M30 must not:

- silently delete evidence
- refactor without rollback anchor
- remove governance provenance
- introduce autonomous trusted mutation
- weaken strict recall verification

## M30 No-delete-before-review Rule

Before deleting or consolidating any file category, M30 should first classify the file into one of the following:

```text
canonical runtime
canonical governance tool
temporary milestone helper
historical evidence
runtime artifact
archive candidate
delete candidate
```

Deletion should only occur after classification review.

## Known Technical Debt Themes

Known pre-release debt themes:

```text
milestone-numbered naming
v1/v2 style drift
helper duplication
wrapper layering
append duplication
manual/runtime mixed edits
partial schema evolution
inconsistent CLI conventions
runtime warning leakage
non-canonical tool layout
```

## M30 Refactor Constraints

M30 may improve implementation structure, but must preserve:

```text
behavioral compatibility
trusted-memory governance semantics
rollback capability
retrieval provenance visibility
strict retrieval-result-only verification
explicit refresh boundary
```

## Planned M30 Sequence

Planned sequence:

```text
M30.1 Repository Inventory / Technical Debt Map
M30.2 Canonical Naming Policy
M30.3 File Header / Version Metadata Standard
M30.4 Entrypoint Consolidation Plan
M30.5 Code Risk Review
M30.6 Legacy Archive / Deprecation Plan
M30.7 Pre-release Smoke Suite
```

## Verification Status

M30.1 Repository Inventory / Technical Debt Map:

- remote Runes Seal anchor verified: PASS
- pre-M30 local backup verified: PASS
- dirty workspace inventory captured: PASS
- modified file categories classified: PASS
- untracked artifact categories classified: PASS
- preservation rules documented: PASS
- no-delete-before-review rule established: PASS
- M30 refactor constraints documented: PASS

Overall:

M30.1 Repository Inventory / Technical Debt Map:
PASS / inventory baseline established
