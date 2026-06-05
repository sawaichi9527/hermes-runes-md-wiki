# Trial-run Bug Registry

## Purpose

This registry tracks concrete bugs and deployment gaps discovered during the realistic fresh-user trial-run stage.

The registry is intentionally lightweight:

```text
personal-local
Markdown-native
human-reviewed
no issue tracker dependency required
no enterprise workflow
```

---

## Bug ID Format

```text
TB-YYYYMMDD-NNN
```

Example:

```text
TB-20260605-001
```

Rules:

- `TB` means Trial Bug.
- Date is the first observed date.
- Number is monotonic within the same date.
- A bug remains in the registry after it is fixed.
- Fix status should be updated, not deleted.

---

## Status Values

```text
OPEN
FIXED
PARTIAL FIX
WON'T FIX
SUPERSEDED
NEEDS DECISION
```

---

## Severity Values

```text
S0 blocker
S1 major
S2 normal
S3 minor
```

---

## TB-20260605-001 Fresh clone lacks dependency bootstrap

Status: OPEN
Severity: S1 major
Milestone: M88
First observed: 2026-06-05

### Symptom

```text
ModuleNotFoundError: No module named 'psycopg'
```

### Context

Observed during realistic fresh-user trial-run after creating a clean trial clone under:

```text
~/workspace-trial/hermes-runes-md-wiki
```

### Root Cause

The repository does not yet provide a clear, bounded fresh-user bootstrap command/file for installing the runtime dependencies needed by memory check and smoke commands.

### Temporary Workaround

Create `tools/importer/.venv` and manually install runtime packages.

### Required Fix

Add a simple personal-local bootstrap path, likely one of:

```text
requirements-core.txt
requirements-embedding.txt
bin/hermes-memory-bootstrap
```

Avoid enterprise installers or hidden background setup.

---

## TB-20260605-002 Fresh trial DB lacks public memory schema

Status: FIXED
Severity: S0 blocker
Milestone: M88
First observed: 2026-06-05
Fixed by: migrations/postgres/002_public_memory_schema.sql

### Symptom

```text
psycopg.errors.UndefinedTable: relation "public.chunks" does not exist
```

### Context

Observed after dependency setup when running smoke against the isolated trial database:

```text
hermes_memory_trial
```

### Root Cause

The initial migration baseline only prepared the minimal backend extension and migration ledger. A fresh trial DB also needs application tables used by importer, recall, and smoke.

### Fix

Added idempotent public memory schema migration:

```text
migrations/postgres/002_public_memory_schema.sql
```

It creates:

```text
public.documents
public.chunks
supporting indexes
```

### Verification

Second migration run returned:

```text
applied=0 skipped=2
```

---

## TB-20260605-003 Trial workspace slug mismatch

Status: PARTIAL FIX
Severity: S1 major
Milestone: M88
First observed: 2026-06-05
Partial fix: bin/hermes-memory-check supports HERMES_WORKSPACE_SLUG / HERMES_PROJECT

### Symptom

Expected trial workspace:

```text
wiki/freelancer
```

Observed cloned development workspace:

```text
wiki/k6-freelancer
```

### Context

During realistic trial-run, the actual user-facing workspace should be `freelancer`, while `k6-freelancer` represents the engineering/development history.

### Root Cause

Development-era paths and project names are still embedded in repo layout and scripts.

### Partial Fix

`bin/hermes-memory-check` now resolves workspace via:

```text
HERMES_WORKSPACE_SLUG
HERMES_PROJECT
fallback: k6-freelancer
```

### Remaining Decision

Do not rename `wiki/k6-freelancer` automatically.

Recommended direction:

```text
Keep wiki/k6-freelancer as engineering/development memory.
Create wiki/freelancer as the realistic fresh-user trial workspace.
```

---

## TB-20260605-004 Memory check stops without clear required-script failure detail

Status: OPEN
Severity: S2 normal
Milestone: M89
First observed: 2026-06-05

### Symptom

The trial-run command reached:

```text
[6/8] required scripts
```

and returned to the shell without printing which required file check failed.

### Context

Observed after setting:

```text
HERMES_WORKSPACE_SLUG=freelancer
HERMES_PROJECT=freelancer
```

The workspace check succeeded:

```text
PASS wiki=/home/eye/workspace-trial/hermes-runes-md-wiki/wiki/freelancer
```

### Root Cause

`bin/hermes-memory-check` uses direct `test -f` checks under `set -e`, so a missing file exits the script without a diagnostic line naming the missing file.

### Required Fix

Make required-script validation verbose and actionable:

```text
PASS file=<path>
FAIL missing file=<path>
```

This should remain a simple shell-level diagnostic improvement.

---

## Current Summary

```text
TB-20260605-001 OPEN        dependency bootstrap missing
TB-20260605-002 FIXED       fresh DB public schema missing
TB-20260605-003 PARTIAL FIX workspace slug mismatch
TB-20260605-004 OPEN        memory check missing-file diagnostic gap
```
