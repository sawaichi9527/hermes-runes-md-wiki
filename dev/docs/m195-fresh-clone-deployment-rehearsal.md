# M195 Fresh Clone Deployment Rehearsal

Status: PASS / clean-env rerun verified
Date: 2026-06-08
Scope: v0.3.0 fresh clone deployment rehearsal

## Purpose

M195 verifies that a normal user can start from a fresh clone without relying on:

- old local workspaces
- old `.venv` state
- old root developer folders
- heavyweight default dependencies
- hidden developer-only paths

## Fresh Clone Target

Verification clone path:

```text
/tmp/hermes-runes-v030-fresh
```

Fresh clone commit:

```text
e277688 Add M194 support evidence check result
```

## Root Layout Verification

Observed root layout:

```text
archive/
bin/
config/
dev/
docs/
.git/
migrations/
reports/
tools/
wiki/
```

Old developer-only root directories were absent:

```text
PASS: root db absent
PASS: root fixtures absent
PASS: root smoke absent
PASS: root templates absent
```

Required runtime/support directories were present:

```text
PASS: migrations/postgres
PASS: reports/m33-markdown-source-health
PASS: dev
```

## Bootstrap Verification

Command:

```bash
bash ./bin/hermes-memory-bootstrap
```

Result:

```json
{
  "status": "PASS",
  "tool": "hermes-memory-bootstrap",
  "root": "/tmp/hermes-runes-v030-fresh",
  "venv": "/tmp/hermes-runes-v030-fresh/tools/importer/.venv",
  "core_requirements": "installed",
  "embedding_requirements": "skipped"
}
```

Default dependency footprint:

```text
pip list | wc -l
9
```

No output was produced for the heavyweight dependency grep:

```bash
pip freeze | grep -Ei 'torch|nvidia|cuda|cudnn|triton|sentence|transformers' || true
```

This confirms the default fresh clone path does not install torch, CUDA, sentence-transformers, transformers, or Triton.

## Support Evidence Verification

The following user-facing support commands remained reachable in a fresh clone:

```bash
bash ./bin/hermes-observe --help
python tools/runes/ragnarok_observation_bundle.py --help
python tools/importer/observation_summary.py --help
```

Observed successful `hermes-observe` output:

```text
usage: hermes_observe.py [-h] [--observe-dir OBSERVE_DIR]
                         {tail,stats,report} ...

Hermes observation JSONL viewer
```

Observed successful Ragnarok bundle output:

```text
usage: ragnarok_observation_bundle.py [-h] [--out-root OUT_ROOT]
                                      [--bundle-id BUNDLE_ID] [--json]

Generate local-only Ragnarok observation bundle MVP.
```

Observed successful observation summary output:

```text
usage: observation_summary.py [-h] [--days DAYS] [--json]

Summarize Hermes Memory observation JSONL logs.
```

Minimal support module compile check passed:

```bash
python -m py_compile \
  tools/importer/hermes_observe.py \
  tools/importer/observation_logger.py \
  tools/importer/observation_summary.py \
  tools/runes/ragnarok_observation_bundle.py \
  tools/runes/ragnarok_incantation_boundary.py \
  tools/runes/markdown_source_health_audit.py
```

## Migration Wrapper Verification

Initial rehearsal showed a confusing migration path from the existing workspace:

```text
/home/eye/workspace/hermes-runes-md-wiki/migrations/postgres/001_backend_baseline.sql
```

This was treated as an environment contamination concern and rerun with a clean environment.

Clean rerun commands:

```bash
unset HERMES_MEMORY_ROOT
unset HERMES_POSTGRES_MIGRATIONS_DIR
bash ./bin/hermes-memory-migrate

HERMES_MEMORY_ROOT=/tmp/hermes-runes-v030-fresh \
bash ./bin/hermes-memory-migrate
```

Clean rerun result:

```text
{"status":"PASS","backend":"postgres","db_source":"backend_stack_env","applied":0,"skipped":2,"message":"Hermes schema migration completed."}
```

The clean rerun did not show the old workspace SQL path again.

## Git State

Fresh clone working tree after verification:

```text
main == origin/main
working tree clean
```

## Result

```text
M195: PASS / fresh clone rehearsal verified with clean env
```

## Notes

- The migration wrapper can legitimately return applied or skipped migrations depending on current backend state.
- `backend_stack_env` is acceptable in the Freelancer environment.
- The rehearsal does not require embedding profile installation.
- The rehearsal does not require a real user support bundle upload.

## Next Step

Proceed to:

```text
M196 v0.3.0 Release Docs / Tag Lock
```

Before tagging `v0.3.0`, confirm:

- release docs point users to the v0.3.0 baseline
- old `v0.1.0-beta.1` is documented as superseded
- temporary M192 branches are cleaned if no longer needed
- final verification references M191-M195 PASS
