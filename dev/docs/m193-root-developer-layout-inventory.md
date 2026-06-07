# M193 Root Developer Layout Inventory

Status: PASS / root developer layout consolidated
Date: 2026-06-08
Scope: v0.3.0 root layout cleanup

## Purpose

M193 prepares and verifies root repository layout consolidation for `v0.3.0`.

Goal:

```text
Keep normal fresh-clone root simple while preserving user-facing observation and support evidence workflows.
```

This inventory is based on local verification output from the Freelancer checkout after M192 and the follow-up M193 move commit.

## Current Root Directories After Move

Current root directories after M193:

```text
archive/
bin/
config/
dev/
docs/
migrations/
reports/
tools/
wiki/
```

Developer-only root directories removed from root:

```text
db/
fixtures/
smoke/
templates/
```

Runtime-facing root now remains focused on:

```text
bin/
config/
docs/
tools/
wiki/
dev/
migrations/
reports/
```

`migrations/` remains because it is currently the runtime migration default path.

`reports/` remains because `reports/m33-markdown-source-health/` is currently used by Ragnarok / markdown health support tooling.

## Developer-only Directories Moved

The following developer/milestone/test directories were moved under `dev/`:

```text
db/        -> dev/db/
fixtures/  -> dev/fixtures/
smoke/     -> dev/smoke/
templates/ -> dev/templates/
```

Observed moved examples:

```text
dev/db/migrations/001_m3_memory_schema.sql
dev/db/migrations/002_m3_metadata_columns.sql
dev/db/migrations/003_m3_assets_table.sql
dev/fixtures/m60/... through dev/fixtures/m82/...
dev/smoke/m31_4_archive_lock_smoke.sh through dev/smoke/m33_7_ragnarok_incantation_boundary_smoke.sh
dev/smoke/smoke_m15_4b_lock_manifest.py through dev/smoke/smoke_m17_5b_runner.py
dev/templates/external-agent-trial-evidence.md
dev/templates/hermes-agent-governed-trial-run-dry-run-record.md
dev/templates/trial-observation-record.md
dev/templates/trial-promotion-fixture-definition.md
```

## Reports Directory Classification

`reports/` is mixed and must not be blindly deleted or hidden.

Moved developer-only report evidence:

```text
reports/m29-runes-seal-local-inventory/ -> dev/reports/m29-runes-seal-local-inventory/
```

Kept runtime/support output path:

```text
reports/m33-markdown-source-health/latest.json
reports/m33-markdown-source-health/latest.md
```

References found and preserved:

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
Do not move reports/ wholesale in M193.
```

Reason:

- old milestone inventory reports are developer evidence and moved under `dev/reports/`
- `reports/m33-markdown-source-health/` is currently user-support evidence output/read path
- Ragnarok / health audit output must remain available to normal users

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

Observed user/support surface after M193:

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

Smoke/test files related to observation may be developer-only, but runtime commands and support evidence generation remain reachable.

## Reference Update Result

Updated references include:

```text
bin/hermes-m138-2-dry-run-record-init
  dev/templates/hermes-agent-governed-trial-run-dry-run-record.md
  dev/templates/trial-promotion-fixture-definition.md

tools/runes/ragnarok_observation_bundle.py
  dev/smoke/m31_7_final_verification_lock.sh
  dev/smoke/m32_7_p0_trial_run_lock.sh
  dev/smoke/m33_*.sh
  reports/m33-markdown-source-health/latest.json
  reports/m33-markdown-source-health/latest.md

tools/archive/milestone-shell/README.md
  dev/smoke/m31_4_archive_lock_smoke.sh

wiki/_system/ragnarok_observation_evidence_inventory.md
  dev/reports/m29-runes-seal-local-inventory/
  reports/m33-markdown-source-health/latest.json
  reports/m33-markdown-source-health/latest.md
```

Remaining `dev/docs/` references to old `templates/...` paths are historical developer documentation references and do not affect runtime fresh-clone behavior. They may be normalized in a later documentation sweep.

## Verification Summary

Local sync verification after commit `210abd9 Move developer-only root assets under dev` showed:

```text
PASS: root db removed
PASS: root fixtures removed
PASS: root smoke removed
PASS: root templates removed
PASS: migrations/postgres remains
PASS: reports/m33-markdown-source-health remains
```

Moved developer directories exist under:

```text
dev/db/
dev/fixtures/
dev/reports/m29-runes-seal-local-inventory/
dev/smoke/
dev/templates/
```

Support evidence surface remains visible under `bin/` and `tools/`.

## M193 Safety Decision

Do not move `migrations/postgres/` in M193.

Do not move `reports/m33-markdown-source-health/` in M193.

Do not move user-facing observation / Ragnarok / diagnostic / support evidence tools into `dev/`.

## Status

```text
M191: PASS / boundary clarified
M192: PASS / default install lightweight
M193: PASS / root developer layout consolidated
v0.3.0: not tagged
```
