# M88 Fresh-user Trial Bootstrap Gap

## Metadata

- Project: k6-freelancer
- Milestone: M88
- Status: PARTIAL FIX / TRIAL FINDINGS RECORDED
- Date: 2026-06-05
- Scope: realistic fresh-user trial-run bootstrap gaps
- Verification type: user terminal evidence + targeted hotfixes

---

## Summary

M88 records the first realistic fresh-user trial-run bootstrap gaps discovered in the isolated trial workspace.

The trial workspace is:

```text
~/workspace-trial/hermes-runes-md-wiki
```

The developer workspace remains out of trial scope:

```text
~/workspace/hermes-runes-md-wiki
```

---

## Finding 1: Missing Python dependency bootstrap

Observed failure:

```text
ModuleNotFoundError: No module named 'psycopg'
```

Interpretation:

```text
A fresh clone does not yet provide a clear dependency bootstrap path before running smoke tests.
```

Temporary trial workaround:

```text
create tools/importer/.venv
install required runtime packages
rerun memory check / smoke
```

This confirms the issue is bootstrap ergonomics, not backend isolation.

---

## Finding 2: Fresh trial DB missing application tables

Observed failure after dependency setup:

```text
psycopg.errors.UndefinedTable: relation "public.chunks" does not exist
```

Interpretation:

```text
The M83/M86 migration baseline only installed the minimal backend extension and schema migration ledger.
A fresh trial database also needs the public memory tables used by importer / recall / smoke.
```

Implemented hotfix:

```text
migrations/postgres/002_public_memory_schema.sql
```

This migration adds the baseline public memory schema:

```text
public.documents
public.chunks
supporting indexes
```

---

## Finding 3: Workspace slug mismatch

Observed issue:

```text
Trial-run expected workspace folder: wiki/freelancer
Existing cloned workspace folder: wiki/k6-freelancer
```

Additional code finding:

```text
bin/hermes-memory-check hardcoded wiki/k6-freelancer and --project k6-freelancer
```

Implemented partial hotfix:

```text
bin/hermes-memory-check now supports HERMES_WORKSPACE_SLUG / HERMES_PROJECT
```

Remaining decision:

```text
Decide whether the realistic trial-run should create a new wiki/freelancer workspace from template/proposal, or whether the repository should rename the existing k6-freelancer project folder.
```

M88 does not automatically rename the existing development workspace because that would be a larger migration touching many references.

---

## Boundary Confirmation

M88 does not modify:

```text
~/docker-stacks/hermes-memory-postgres
~/workspace/hermes-runes-md-wiki from the trial agent context
```

M88 does not introduce:

```text
automatic workspace rename
automatic proposal apply
hidden background worker
automatic DB reset
```

---

## Implemented Files

```text
bin/hermes-memory-check
migrations/postgres/002_public_memory_schema.sql
```

---

## Recommended Trial Continuation

From the trial workspace:

```text
pull latest developer-published hotfixes into trial clone
set HERMES_WORKSPACE_SLUG=freelancer
run schema migration twice
create or prepare wiki/freelancer through governed trial flow
run importer / smoke again
```

---

## Final Lock

```text
M88 Fresh-user Trial Bootstrap Gap
PARTIAL FIX / trial findings recorded
```

The fresh-user trial is functioning as intended: it is exposing real deployment gaps before broader use.
