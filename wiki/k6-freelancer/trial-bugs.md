# Trial-run Bug Registry

## Purpose

This registry tracks concrete bugs and deployment gaps discovered during the realistic fresh-user trial-run and Closed Beta validation stages.

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
- CB validation findings should also receive a TB id when they may require future tracking.

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

Status: FIXED
Severity: S1 major
Milestone: M88 / M89 / M90 / M90.1 / M90.2 / M90.3
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

The repository previously did not provide a clear, bounded fresh-user bootstrap command/file for installing the runtime dependencies needed by memory check and smoke commands.

Manual installation also pulled a large default dependency set, including CUDA-related packages, which is not ideal for a personal-local CPU-oriented fresh-user bootstrap.

### Temporary Workaround

Create `tools/importer/.venv` and manually install runtime packages.

### Fix

M90 added a bounded bootstrap path:

```text
requirements-core.txt
requirements-embedding.txt
bin/hermes-memory-bootstrap
docs/fresh-clone-bootstrap.md
wiki/k6-freelancer/verification-m90.md
```

Core bootstrap:

```bash
bash ./bin/hermes-memory-bootstrap
```

Optional embedding/full-smoke bootstrap:

```bash
bash ./bin/hermes-memory-bootstrap --with-embedding
```

The embedding path installs CPU-only torch first to avoid pulling large CUDA wheels by default.

---

## TB-20260607-001 M156 trial-root quote typo in Hermes-agent output

Status: OPEN
Severity: S3 minor
Milestone: M156
First observed: 2026-06-07

### Symptom

During M156 Hermes-agent CB trial-root discipline verification, the agent correctly identified the expected trial root in its final answer and boundary self-check, but one quoted line contained a likely typo:

```text
hermes-rnes-md-wiki
```

Expected path:

```text
hermes-runes-md-wiki
```

### Context

Observed during:

```text
M156 Trial-root Discipline CB Check
```

The session result remained PASS because Hermes-agent explicitly identified:

```text
~/workspace-trial/hermes-runes-md-wiki
```

and distinguished it from:

```text
~/workspace/hermes-runes-md-wiki
```

### Impact

```text
Non-blocking documentation / quote accuracy issue.
No trusted memory mutation occurred.
No proposal was created.
No promotion occurred.
Trial-root discipline result remains valid.
```

### Tracking Decision

Keep this bug open until the source of the typo is confirmed:

```text
agent transcription issue
source document typo
prompt quoting issue
```

### Next Check

During M157 or a later CB session, search the repo for the misspelled string and decide whether to fix source documentation or mark this as an agent-output-only typo.
