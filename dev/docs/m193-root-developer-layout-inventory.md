# M193 Root Developer Layout Inventory

Status: inventory locked / move plan ready
Date: 2026-06-08
Scope: v0.3.0 root layout cleanup

## Purpose

M193 prepares root repository layout consolidation for `v0.3.0`.

Goal:

```text
Keep normal fresh-clone root simple while preserving user-facing observation and support evidence workflows.
```

This inventory is based on local verification output from the Freelancer checkout after M192.

## Current Root Directories

Observed root directories:

```text
archive/
bin/
config/
db/
dev/
docs/
fixtures/
.git/
migrations/
reports/
smoke/
templates/
tools/
.venv/
wiki/
```

Runtime-facing root should eventually focus on:

```text
bin/
config/
docs/
tools/
wiki/
dev/
```

`migrations/` requires special handling because it is currently the runtime migration default path.

## Candidate Developer-only Directories

The following root directories are developer/milestone/test oriented and should be moved under `dev/` after reference updates:

```text
db/
fixtures/
smoke/
templates/
```

Observed examples:

```text
db/migrations/001_m3_memory_schema.sql
db/migrations/002_m3_metadata_columns.sql
db/migrations/003_m3_assets_table.sql
fixtures/m60/... through fixtures/m82/...
dev/smoke/m31_4_archive_lock_smoke.sh through dev/smoke/m33_7_ragnarok_incantation_boundary_smoke.sh
smoke/smoke_m15_4b_lock_manifest.py through smoke/smoke_m17_5b_runner.py
dev/templates/external-agent-trial-evidence.md
dev/templates/hermes-agent-governed-trial-run-dry-run-record.md
dev/templates/trial-observation-record.md
dev/templates/trial-promotion-fixture-definition.md
```

Target paths:

```text
dev/db/
dev/fixtures/
dev/smoke/
dev/templates/
```

## Reports Directory Classification

`reports/` is mixed and must not be blindly deleted or hidden.

Observed checked-in reports:

```text
dev/reports/m29-runes-seal-local-inventory/*
reports/m33-markdown-source-health/latest.json
reports/m33-markdown-source-health/latest.md
```

References found:

```text
wiki/_system/ragnarok_observation_evidence_inventory.md
  dev/reports/m29-runes-seal-local-inventory/
  reports/m33-markdown-source-health/latest.json
  reports/m33-markdown-source-health/latest.md

tools/runes/ragnarok_observation_bundle.py
  reports/m33-markdown-source-health/latest.json
  reports/m33-markdown-source-health/latest.md

tools/runes/markdown_source_health_audit.py
  DEFAULT_OUT_DIR = "reports/m33-markdown-source-health"
```

Decision:

```text
Do not move reports/ wholesale in one step.
```

Recommended M193 handling:

- Move old milestone inventory reports to `dev/reports/` if they are only developer evidence.
- Keep user-support output path user-facing or configure a new local artifact path such as `runtime/reports/` or gitignored `reports/`.
- Keep Ragnarok / health audit output available to normal users.
- Ensure generated support evidence is gitignored unless intentionally committed as public-safe documentation evidence.

## Migrations Directory Classification

`migrations/postgres/` remains runtime-needed for now.

References found:

```text
bin/hermes-memory-migrate
  MIGRATIONS_DIR="${HERMES_POSTGRES_MIGRATIONS_DIR:-$ROOT/migrations/postgres}"
  error message: migrations/postgres directory not found

QUICKSTART.md
  migrations/postgres/

docs/reference-postgres-backend.md
  Hermes-specific migrations/
  bash ./bin/hermes-memory-migrate

AGENTS.md
  Hermes application schema migration
  bash ./bin/hermes-memory-migrate
```

Decision:

```text
Keep migrations/postgres/ at root for M193 unless moving it together with bin/hermes-memory-migrate and all docs.
```

Possible future cleanup:

```text
tools/importer/migrations/postgres/
```

but that is not required for v0.3.0 root cleanup.

## Must Preserve for Normal Users

The support evidence and observation surface is user-facing and must not be moved into a developer-only path.

Observed user/support surface:

```text
bin/hermes-observe
bin/hermes-trial-observation-check
tools/importer/context_diagnostics.py
tools/importer/hermes_observe.py
tools/importer/observation_logger.py
tools/importer/observation_summary.py
tools/importer/retrieval_diagnostics.py
tools/runes/ragnarok_incantation_boundary.py
tools/runes/ragnarok_observation_bundle.py
tools/runes_shield/format_observation.py
tools/runes_shield/integrate_observation.py
tools/runes_shield/observe_health.py
tools/runes_shield/proposal_governance_observation_export.py
```

Smoke/test files related to observation may be developer-only, but the runtime commands and support evidence generation must remain reachable.

## Reference Update Requirements

Before or during the move, update references in:

```text
bin/hermes-m138-2-dry-run-record-init
  dev/templates/hermes-agent-governed-trial-run-dry-run-record.md
  dev/templates/trial-promotion-fixture-definition.md

tools/runes/ragnarok_observation_bundle.py
  dev/smoke/m31_7_final_verification_lock.sh
  dev/smoke/m32_7_p0_trial_run_lock.sh
  smoke/m33_*.sh
  reports/m33-markdown-source-health/latest.json
  reports/m33-markdown-source-health/latest.md

tools/runes/markdown_source_health_audit.py
  reports/m33-markdown-source-health

wiki/_system/ragnarok_observation_evidence_inventory.md
  dev/reports/m29-runes-seal-local-inventory/
  reports/m33-markdown-source-health/latest.json
  reports/m33-markdown-source-health/latest.md
```

## Proposed M193 Move Plan

Phase A: safe developer-only moves

```text
db/        -> dev/db/
fixtures/  -> dev/fixtures/
smoke/     -> dev/smoke/
templates/ -> dev/templates/
```

Update direct references after this phase.

Phase B: reports split

```text
dev/reports/m29-runes-seal-local-inventory/ -> dev/dev/reports/m29-runes-seal-local-inventory/
```

Keep or redesign:

```text
reports/m33-markdown-source-health/
```

because it is currently produced/read by user-facing Ragnarok/health-audit tooling.

Phase C: verify support evidence remains user-facing

```bash
find bin tools -maxdepth 4 -type f | sort | grep -Ei 'observe|observation|support|bundle|ragnarok|diagnostic|log' || true
```

Phase D: smoke / compile

```bash
python -m py_compile tools/importer/*.py tools/runes/*.py tools/runes_shield/*.py
bash ./bin/hermes-memory-bootstrap-verify
bash ./bin/hermes-memory-smoke
```

## M193 Safety Decision

Do not perform a blind root move.

Because GitHub connector access does not provide a convenient recursive move operation here, the actual M193 file relocation should be done either:

1. locally with a controlled `git mv` script and then pushed, or
2. through a generated patch file if the move/update set becomes too large for chat code blocks.

The layout decision itself is now locked for implementation.

## Status

```text
M191: PASS / boundary clarified
M192: PASS / default install lightweight
M193: INVENTORY LOCKED / move plan ready
v0.3.0: not tagged
```
