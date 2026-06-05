# M86 Trial-run Environment Isolation Baseline

## Metadata

- Project: k6-freelancer
- Milestone: M86
- Status: PASS / DESIGN READY / IMPLEMENTED
- Date: 2026-06-05
- Scope: realistic fresh-user trial-run isolation
- Verification type: documentation + migration target resolution update

---

## Summary

M86 defines the baseline for running a realistic fresh-user trial-run without deleting or contaminating the active developer environment.

The selected baseline is:

```text
shared PostgreSQL Docker service
separate developer and trial-run repository clones
separate developer and trial-run runtime databases
separate local runtime configs
```

This preserves simplicity while preventing trial-run importer, migration, recall, and smoke outputs from contaminating the developer baseline.

---

## Implemented Files

```text
docs/trial-run-environment-isolation.md
bin/hermes-memory-migrate
```

---

## Environment Boundary

Developer environment:

```text
~/workspace/hermes-runes-md-wiki
```

Trial-run user environment:

```text
~/workspace-trial/hermes-runes-md-wiki
```

Developer DB:

```text
hermes_memory
```

Trial-run DB:

```text
hermes_memory_trial
```

---

## Migration Target Resolution

`bin/hermes-memory-migrate` now resolves the database target in this order:

```text
1. runtime database URL from current shell
2. runtime database URL from importer-local config
3. fallback to external PostgreSQL stack default database
```

This prevents a trial-run clone from accidentally migrating the developer default database when the trial clone points to a separate trial database.

---

## Design Rationale

A fully separate PostgreSQL Docker stack would provide stronger isolation, but it would also increase:

```text
setup friction
port management complexity
backup complexity
agent burden
```

For P0 / early trial-run, separate runtime databases under one local PostgreSQL service are mature enough and simpler.

---

## Safety Boundary

M86 does not introduce:

```text
new Docker stack automation
automatic DB repair
automatic DB reset
automatic backend failover
background workers
enterprise orchestration
```

M86 preserves:

```text
personal-local scope
simple setup
human-visible trial preparation
developer / trial-run separation
```

---

## Expected Trial-run Flow

```text
prepare trial database
clone repo under ~/workspace-trial/
configure trial runtime DB target
run backend guard
run schema migration twice
run smoke / recall checks
keep trial artifacts local unless explicitly promoted
```

---

## Final Lock

```text
M86 Trial-run Environment Isolation Baseline
PASS / design ready / implemented
```

The project is ready for realistic fresh-user trial-run simulation without deleting the developer checkout.
