# M91 Beta-prep Clean Trial Run

Status: PLAN READY / pending local execution
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

## Recommended Commands

Synchronize trial clone:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki
git fetch origin
git pull
git status
git log --oneline -10
```

Run verified bootstrap baseline:

```bash
bash ./bin/hermes-memory-bootstrap
bash ./bin/hermes-memory-bootstrap-verify
```

Optional embedding baseline:

```bash
bash ./bin/hermes-memory-bootstrap --with-embedding
bash ./bin/hermes-memory-bootstrap-verify --with-embedding
bash ./bin/hermes-memory-embedding-cpu-clean-verify
```

Run backend and memory verification chain:

```bash
bash ./bin/hermes-backend-check
bash ./bin/hermes-memory-migrate
bash ./bin/hermes-memory-check
bash ./bin/hermes-memory-import
bash ./bin/hermes-memory-smoke
```

## Expected Result

```text
bootstrap: PASS
bootstrap verify: PASS
optional embedding clean verify: PASS
backend check: PASS
migration wrapper: PASS
memory check: PASS
scoped import: PASS
smoke suite: PASS or expected SKIP for model-dependent/trial-fixture-dependent checks
```

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
PLAN READY / pending local execution
```
