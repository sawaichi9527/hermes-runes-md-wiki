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

### Verification

M90.1 confirmed core and optional embedding bootstrap verification in the trial clone:

```text
core-python-imports: PASS
embedding-python-imports: PASS
embedding_imports: PASS
```

M90.2 confirmed optional embedding bootstrap in a clean temporary venv:

```text
status: PASS
check: embedding-cpu-clean-verify
import_failures: []
blocked_packages: []
package_count: 45
```

Observed clean package:

```text
torch-2.12.0+cpu
```

M90.3 marks the fresh clone bootstrap baseline ready for beta preparation.

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

Status: FIXED
Severity: S1 major
Milestone: M88 / M89
First observed: 2026-06-05
Fixed by: workspace-aware check/import/smoke path

### Symptom

Expected trial workspace:

```text
wiki/freelancer
```

Observed development workspace:

```text
wiki/k6-freelancer
```

### Context

During realistic trial-run, the actual user-facing workspace should be `freelancer`, while `k6-freelancer` represents the engineering/development history.

### Root Cause

Development-era paths and project names were embedded in repo layout and scripts.

### Fix

The trial path now supports:

```text
HERMES_WORKSPACE_SLUG=freelancer
HERMES_PROJECT=freelancer
```

The implementation keeps `wiki/k6-freelancer` as engineering/development memory and uses `wiki/freelancer` as the realistic fresh-user trial workspace.

---

## TB-20260605-004 Memory check stops without clear required-script failure detail

Status: FIXED
Severity: S2 normal
Milestone: M89
First observed: 2026-06-05
Fixed by: c1243c0 Show missing required script in memory check

### Symptom

The trial-run command reached:

```text
[6/8] required scripts
```

and returned to the shell without printing which required file check failed.

### Root Cause

`bin/hermes-memory-check` used direct `test -f` checks under `set -e`, so a missing file exited the script without a diagnostic line naming the missing file.

### Fix

Required-script validation now prints actionable file-level results.

---

## TB-20260605-005 Memory check required obsolete smoke scripts

Status: FIXED
Severity: S2 normal
Milestone: M89
First observed: 2026-06-05
Fixed by: 194fa42 Fix memory check obsolete smoke requirements

### Symptom

Fresh trial memory check failed because it expected obsolete smoke or backup helper scripts that are no longer part of the current repo baseline.

### Fix

Removed obsolete required-script checks from the memory check baseline.

---

## TB-20260605-006 Memory check command discovery was not repo-local enough

Status: FIXED
Severity: S2 normal
Milestone: M89
First observed: 2026-06-05
Fixed by: 520884a Fix memory check command discovery

### Symptom

Fresh clone verification depended too much on external PATH state instead of resolving repo-local commands.

### Fix

Memory check now resolves repo-local command paths more reliably for the trial clone.

---

## TB-20260605-007 delete_source used hardcoded legacy DB config

Status: FIXED
Severity: S1 major
Milestone: M89
First observed: 2026-06-05
Fixed by: 545606b Use shared DB config in delete source

### Symptom

`delete_source.py` did not use the trial clone runtime DB configuration and could resolve toward legacy development paths.

### Fix

`delete_source.py` now uses the shared DB configuration path so trial clone operations can target `hermes_memory_trial` correctly.

---

## TB-20260605-008 Importer initially imported the full development wiki into trial DB

Status: FIXED
Severity: S1 major
Milestone: M89
First observed: 2026-06-05
Fixed by: bde86a3 Add workspace filter to importer

### Symptom

Initial trial import wrote development and sample project content into the trial database, including:

```text
k6-freelancer
sample-project
```

### Root Cause

The importer did not yet respect the trial workspace scope.

### Fix

Importer now filters by active workspace scope when `HERMES_WORKSPACE_SLUG` / `HERMES_PROJECT` is set.

---

## TB-20260605-009 Core FTS smoke hardcoded sample-project

Status: FIXED
Severity: S1 major
Milestone: M89
First observed: 2026-06-05
Fixed by: 09fbd36 Make core FTS smoke workspace aware

### Symptom

Core FTS smoke queried `sample-project` even when the trial workspace was `freelancer`.

### Fix

Core FTS smoke now derives project, path, query, and expected prefix from the active workspace environment.

---

## TB-20260605-010 Scoped import missed root wiki and owner-runes

Status: FIXED
Severity: S1 major
Milestone: M89
First observed: 2026-06-05
Fixed by:

```text
0d6a316 Include root wiki and owner-runes in scoped import
1371882 Add owner-runes seed memory layer
```

### Symptom

After workspace filtering, trial import included `_system` and `freelancer`, but excluded:

```text
wiki/*.md
wiki/owner-runes/**
```

### Fix

Scoped import now includes:

```text
wiki/_system/**
wiki/owner-runes/**
wiki/<workspace>/**
wiki/*.md
```

### Verification

Trial import produced:

```text
project=default
project=_system
project=freelancer
project=owner-runes
```

and excluded:

```text
project=k6-freelancer
project=sample-project
```

---

## TB-20260605-011 M5.2 evaluation smoke used legacy k6-freelancer cases

Status: FIXED
Severity: S1 major
Milestone: M89
First observed: 2026-06-05
Fixed by: d490e6f Make M5.2 smoke workspace aware

### Symptom

M5.2 still queried `project=k6-freelancer` for Telegram and legacy Phase3 cases.

### Fix

M5.2 now keeps legacy checks for `k6-freelancer` and uses workspace-aware checks under `HERMES_PROJECT=freelancer`.

### Verification

```text
profile: workspace-freelancer
status: PASS
```

---

## TB-20260605-012 M10 observation smoke required model env during fresh trial smoke

Status: FIXED
Severity: S2 normal
Milestone: M89
First observed: 2026-06-05
Fixed by: 2ed6945 Make M10 observation smoke trial aware

### Symptom

M10 failed before a model endpoint was configured:

```text
OPENAI_BASE_URL and OPENAI_MODEL must be set
```

### Fix

M10 now returns `SKIP` with exit code 0 when the OpenAI-compatible model environment is not configured.

### Verification

```text
profile: workspace-freelancer
status: SKIP
reason: missing_model_env
```

---

## TB-20260605-013 M11.6 sample project smoke was not workspace-aware

Status: FIXED
Severity: S1 major
Milestone: M89
First observed: 2026-06-05
Fixed by: 2bfeb51 Make M11.6 sample smoke workspace aware

### Symptom

M11.6 queried `sample-project`, which is intentionally excluded from the fresh trial DB.

### Fix

M11.6 now keeps legacy sample-project cases for legacy runs and uses workspace-aware seed checks for `freelancer` and `owner-runes`.

### Verification

```text
profile: workspace-freelancer
status: PASS
```

---

## TB-20260605-014 M20.4 promotion governance smoke lacked trial fixture handling

Status: FIXED
Severity: S2 normal
Milestone: M89
First observed: 2026-06-05
Fixed by: 40a25df Skip M20.4 promotion smoke without trial fixture

### Symptom

M20.4 queried legacy `k6-freelancer` promotion governance fixtures even in the fresh trial workspace.

### Root Cause

M20.4 validates promotion governance semantics and requires an approved forge/proposal fixture. Fresh `freelancer` trial workspace does not yet have such a fixture.

### Fix

For non-legacy workspaces, M20.4 now returns `SKIP` with exit code 0 until a trial promotion fixture exists.

### Verification

```text
profile: workspace-freelancer
status: SKIP
reason: promotion_governance_fixture_not_available_in_trial_workspace
failed: 0
```

---

## TB-20260605-015 Embedding bootstrap CPU-only guarantee not proven on contaminated venv

Status: FIXED
Severity: S1 major
Milestone: M90.2 / M90.3
First observed: 2026-06-06
Fixed by: bin/hermes-memory-embedding-cpu-clean-verify

### Symptom

M90.1 verified imports successfully, but the existing trial `.venv` already contained GPU-oriented packages from earlier manual installation.

That environment could prove imports worked, but could not prove that the bootstrap path avoided GPU package bloat.

### Fix

M90.2 added a clean temporary venv verifier:

```text
bin/hermes-memory-embedding-cpu-clean-verify
```

### Verification

The clean verifier returned:

```text
status: PASS
check: embedding-cpu-clean-verify
import_failures: []
blocked_packages: []
package_count: 45
```

Observed clean package:

```text
torch-2.12.0+cpu
```

The clean temp venv did not install package names matching:

```text
cuda*
nvidia*
triton
```

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

---

## TB-20260607-002 trial-bugs registry truncation caused by incomplete overwrite

Status: OPEN
Severity: S1 major
Milestone: M156 follow-up
First observed: 2026-06-07

### Symptom

After adding TB-20260607-001, `git pull` showed that `wiki/k6-freelancer/trial-bugs.md` had a large unintended deletion:

```text
wiki/k6-freelancer/trial-bugs.md | 478 +++++-------------------------------------------------------------------
3 files changed, 64 insertions(+), 451 deletions(-)
```

### Context

The direct GitHub update used an incomplete fetched view of `trial-bugs.md`, causing older registry entries to be overwritten.

### Impact

```text
Bug registry history was partially truncated in the repository.
Existing TB-20260605 records must be restored from git history.
This affects documentation integrity, not runtime behavior.
```

### Fix Plan

Restore `wiki/k6-freelancer/trial-bugs.md` from the last known-good commit before truncation, then append TB-20260607-001 and TB-20260607-002.

### Fix Verification

Expected after fix:

```text
TB-20260605-001 through TB-20260605-015 remain present.
TB-20260607-001 is present.
TB-20260607-002 is present.
git diff should show only appended new 20260607 entries after restore.
```

---

## Current Summary

```text
TB-20260605-001 FIXED        dependency bootstrap path and clean verification
TB-20260605-002 FIXED        fresh DB public schema missing
TB-20260605-003 FIXED        workspace slug mismatch
TB-20260605-004 FIXED        memory check missing-file diagnostic gap
TB-20260605-005 FIXED        obsolete memory-check smoke requirements
TB-20260605-006 FIXED        repo-local command discovery
TB-20260605-007 FIXED        delete_source shared DB config
TB-20260605-008 FIXED        importer workspace filter
TB-20260605-009 FIXED        core FTS workspace-aware smoke
TB-20260605-010 FIXED        scoped import root wiki + owner-runes
TB-20260605-011 FIXED        M5.2 workspace-aware smoke
TB-20260605-012 FIXED        M10 trial-aware model-env skip
TB-20260605-013 FIXED        M11.6 workspace-aware smoke
TB-20260605-014 FIXED        M20.4 trial fixture skip
TB-20260605-015 FIXED        embedding CPU-only clean verifier
TB-20260607-001 OPEN         M156 trial-root quote typo
TB-20260607-002 OPEN         trial-bugs registry truncation caused by incomplete overwrite
```
---

## TB-20260607-003 M157 prompt path initially resolved outside repo before fallback

Status: OPEN
Severity: S3 minor
Milestone: M157
First observed: 2026-06-07

### Symptom

During M157 Hermes-agent read-only technical input validation, the agent first attempted to read the M157 prompt from:

```text
/home/eye/docs/cb-m157-technical-input-readonly-prompt.md
```

That path was not the repository path.

The agent then recovered and read the correct prompt from the controlled trial checkout:

```text
/home/eye/workspace-trial/hermes-runes-md-wiki/docs/cb-m157-technical-input-readonly-prompt.md
```

### Context

Observed during:

```text
M157 First Real User Technical Input CB Session
```

The session result remained PASS because Hermes-agent recovered safely, used the correct prompt, and preserved read-only behavior.

### Impact

```text
Non-blocking path-resolution issue.
No proposal was created.
No promotion occurred.
No trusted memory mutation occurred.
M157 read-only analysis result remains valid.
```

### Tracking Decision

Keep this bug open until prompt path guidance is clarified.

Potential future fixes:

```text
Use absolute trial-root prompt paths in CB instructions.
Require Hermes-agent to resolve docs paths relative to active repository root.
Add a boundary self-check field for prompt_path_used.
```

### Next Check

During M158, verify whether Hermes-agent resolves prompt paths under:

```text
/home/eye/workspace-trial/hermes-runes-md-wiki
```

before falling back to developer checkout or home-relative paths.
---

## TB-20260607-004 placeholder append path caused local append failure

Status: OPEN
Severity: S3 minor
Milestone: M157 follow-up
First observed: 2026-06-07

### Symptom

During M157 follow-up, the append command used a placeholder path:

```text
/path/to/tb-20260607-003-append.md
```

This failed locally because the file did not exist at that path.

### Context

Observed while appending the M157 prompt-path bug record to:

```text
wiki/k6-freelancer/trial-bugs.md
```

The actual downloaded/placed append file was present as an untracked file under:

```text
wiki/k6-freelancer/tb-20260607-003-append.md
```

### Impact

```text
Non-blocking process/instruction issue.
M157 result lock remained valid.
No repository content was committed from the failed append attempt.
```

### Fix Plan

Use the actual local file path when appending:

```text
wiki/k6-freelancer/tb-20260607-003-append.md
```

Future instructions should avoid placeholder paths when a concrete local path is known.
---

## TB-20260607-005 M158 optional reference file lookup failed but did not block session

Status: OPEN
Severity: S3 minor
Milestone: M158
First observed: 2026-06-07

### Symptom

During M158 proposal-first CB validation, Hermes-agent successfully read the M158 prompt from the trial checkout, then attempted to read an optional reference file:

```text
/home/eye/workspace-trial/hermes-runes-md-wiki/references/readonly-analysis-pattern.md
```

The file was not found.

### Context

Observed during:

```text
M158 Proposal-first CB Session
```

The session result remained PASS because Hermes-agent had already read the correct M158 prompt and completed the draft-only proposal session safely.

### Impact

```text
Non-blocking optional reference lookup issue.
No proposal was written to the trusted wiki.
No promotion occurred.
No import or index refresh occurred.
M158 proposal-first result remains valid.
```

### Tracking Decision

Keep this bug open until the missing reference path is clarified.

Potential future fixes:

```text
Create the optional reference file if it is intended.
Remove the lookup expectation if the file is obsolete.
Update prompt or skill guidance to avoid optional missing reads.
```

### Next Check

During M159, observe whether Hermes-agent attempts to read missing optional reference files again.
