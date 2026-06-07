# M91 Beta-prep Clean Trial Run

Status: PASS / beta-prep clean trial run verified
Date: 2026-06-06

## Purpose

M91 starts the beta-prep clean trial run after M90.3 closed the fresh clone bootstrap baseline.

The goal is to run the current trial clone through the verified bootstrap baseline and then continue through the normal explicit verification chain.

## Scope

M91 is a manual, explicit, beta-prep verification run.

It remains:

```text
personal-local
bounded
non-enterprise
non-daemon
human-controlled
```

## Preconditions

```text
developer repo is clean and synced
trial clone is clean and synced
trial clone uses HERMES_WORKSPACE_SLUG=freelancer
trial clone uses HERMES_PROJECT=freelancer
external PostgreSQL service remains unchanged
trial database remains isolated
```

## Executed Commands

Synchronized developer and trial clone to:

```text
accae0f Add M91 beta prep clean trial run lock
```

Executed in trial clone:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

bash ./bin/hermes-memory-bootstrap
bash ./bin/hermes-memory-bootstrap-verify

bash ./bin/hermes-memory-bootstrap --with-embedding
bash ./bin/hermes-memory-bootstrap-verify --with-embedding
bash ./bin/hermes-memory-embedding-cpu-clean-verify

bash ./bin/hermes-backend-check
bash ./bin/hermes-memory-migrate
bash ./bin/hermes-memory-check
bash ./bin/hermes-memory-import
bash ./bin/hermes-memory-smoke
```

## Verified Results

Bootstrap core:

```text
hermes-memory-bootstrap: PASS
core-python-imports: PASS
embedding_imports: skipped
```

Bootstrap embedding:

```text
hermes-memory-bootstrap --with-embedding: PASS
core-python-imports: PASS
embedding-python-imports: PASS
embedding_imports: PASS
```

Clean temp venv CPU embedding verification:

```text
status: PASS
check: embedding-cpu-clean-verify
import_failures: []
blocked_packages: []
package_count: 45
```

Backend and migration:

```text
backend-check: PASS
migration wrapper: PASS
applied=0
skipped=2
```

Memory check:

```text
status=PASS
wiki=/home/eye/workspace-trial/hermes-runes-md-wiki/wiki/freelancer
database/schema probe: PASS
```

Import:

```text
summary: schema=public import_scope=freelancer imported_or_changed=0 updated=0 skipped=58 chunks_written=0
PASS: Markdown incremental import completed
```

Smoke:

```text
Core FTS: PASS
M5.2 workspace evaluation: PASS
M10 observation log: SKIP / expected missing model env
M11 observation summary: PASS
M11.6 workspace/sample smoke: PASS
M20.4 promotion governance: SKIP / expected no trial fixture
```

## Expected SKIP States

The following SKIP states are expected during M91:

```text
M10: missing_model_env
M20.4: promotion_governance_fixture_not_available_in_trial_workspace
```

These do not block M91 because model endpoint configuration and approved trial promotion fixture creation are outside this beta-prep clean trial verification step.

## Boundaries

M91 does not introduce:

```text
no orchestration daemon
no websocket bridge
no enterprise telemetry system
no automatic proposal apply
no direct wiki mutation by agent
no runtime authority escalation
```

## Final Lock

```text
M91 Beta-prep Clean Trial Run
PASS / beta-prep clean trial run verified
```
