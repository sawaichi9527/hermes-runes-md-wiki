# Fresh Install Manual

Status: M204 draft / fresh user manual path
Target: v0.7.0-dev
Baseline release: v0.5.0
Date: 2026-06-08

## Purpose

This document records the manual fresh install path for Hermes Runes MD Wiki after the v0.5.0 release.

Validated clean-user simulation:

- removed existing workspace
- removed local venv
- removed PostgreSQL Docker stack and volume
- removed stale local hermes symlinks
- cloned repository again from GitHub

## Release target note

v0.5.0 is the released baseline.

The next development target is v0.7.0-dev.

Do not create or move a v0.7.0 tag until a future release gate passes.

## Manual install flow

### 1. Clone repository

Command summary:

- mkdir -p ~/workspace
- cd ~/workspace
- git clone https://github.com/sawaichi9527/hermes-runes-md-wiki.git
- cd hermes-runes-md-wiki
- git status
- cat VERSION

Expected result:

- repository cloned
- working tree clean
- current main is the active development line
- VERSION is v0.7.0-dev after M204 target reset

### 2. Confirm Docker runtime

Command summary:

- docker --version
- docker compose version
- systemctl is-active docker
- id
- docker run --rm hello-world

Expected result:

- Docker installed
- Docker service active
- current user can run Docker
- hello-world PASS

### 3. Create PostgreSQL / pgvector stack

Required stack path:

- ~/docker-stacks/hermes-memory-postgres/

Required .env values:

- POSTGRES_DB=hermes_memory
- POSTGRES_USER=hermes
- POSTGRES_PASSWORD=hermes-rw
- POSTGRES_PORT=5433

Required image:

- pgvector/pgvector:0.8.2-pg17

Required published port:

- 127.0.0.1:5433 -> container 5432

Required init SQL:

- CREATE EXTENSION IF NOT EXISTS vector;

Required permissions:

- chmod 755 ~/docker-stacks
- chmod 755 ~/docker-stacks/hermes-memory-postgres
- chmod 755 init
- chmod 644 init/001-init.sql
- chmod 600 .env

Expected result:

- container hermes-memory-postgres is healthy
- PostgreSQL 17.x
- pgvector extension 0.8.2

### 4. Bootstrap Python core profile

After git clone, run the core bootstrap before using importer, recall, migration, or smoke tools.

Command:

- bash ./bin/hermes-memory-bootstrap

Expected result:

- tools/importer/.venv exists
- core_requirements installed
- embedding_requirements skipped

The core profile supports:

- PostgreSQL connection
- Markdown import
- migration
- FTS recall
- core smoke checks

The default core profile does not install:

- sentence-transformers
- torch
- transformers

This is expected.

### 5. Configure tools/importer/.env

Create runtime env file:

- cp tools/importer/.env.example tools/importer/.env
- chmod 600 tools/importer/.env
- vi tools/importer/.env

Required values:

- HERMES_MEMORY_ROOT=/home/eye/workspace/hermes-runes-md-wiki
- HERMES_WORKSPACE_SLUG=freelancer
- HERMES_PROJECT=freelancer
- HERMES_MEMORY_DATABASE_URL=postgresql://hermes:hermes-rw@127.0.0.1:5433/hermes_memory

Before running tools in a reused shell, clear old overrides:

- unset HERMES_MEMORY_DATABASE_URL
- unset HERMES_RW_USER HERMES_RW_PASSWORD
- unset POSTGRES_USER POSTGRES_PASSWORD POSTGRES_DB POSTGRES_PORT POSTGRES_HOST
- unset PGHOST PGPORT PGDATABASE PGUSER PGPASSWORD
- unset DATABASE_URL

Expected DB identity:

- current_user = hermes
- current_database = hermes_memory

### 6. Backend check and migration

Command summary:

- ./bin/hermes-backend-check
- ./bin/hermes-memory-migrate

Expected result:

- backend check PASS
- migration PASS

### 7. Import Markdown memory

Command:

- ./bin/hermes-memory-import

Expected result:

- PASS: Markdown incremental import completed
- forge-inbox README skipped by forge policy

### 8. Core FTS recall smoke

Command:

- ./bin/hermes-recall "forge inbox boundary" --project freelancer --mode fts --limit 5 --json

Expected result:

- status = pass
- fusion = fts
- model = null

### 9. Core smoke

Command:

- ./bin/hermes-memory-smoke

Expected result:

- Core FTS Smoke Test PASS
- Embedding profile not installed: skipping hybrid and answer-generation smoke suites

This is a core-profile PASS.

## Optional embedding profile

Only install embedding profile when hybrid/vector recall is needed.

Command:

- bash ./bin/hermes-memory-bootstrap --with-embedding

Then run embedding writer and hybrid/vector smoke.

## Known fresh-install findings

### TB-M204-DOC001: PostgreSQL init bind mount permission requirement

Symptom:

- ls: cannot open directory /docker-entrypoint-initdb.d/: Permission denied
- container restart loop

Cause:

- host init directory mounted read-only but not readable/traversable by container user

Fix:

- chmod 755 ~/docker-stacks
- chmod 755 ~/docker-stacks/hermes-memory-postgres
- chmod 755 init
- chmod 644 init/001-init.sql
- chmod 600 .env

### TB-M204-DOC002: backend stack .env requires POSTGRES_PORT

Symptom:

- POSTGRES_PORT missing from backend .env

Fix:

- add POSTGRES_PORT=5433

### TB-M204-DOC003: bootstrap must be explicit

Fresh clone users must run:

- bash ./bin/hermes-memory-bootstrap

before importer, recall, migration, or smoke tools.

### TB-M204-FI002: hermes-memory-check still expects removed eval_all.py

Symptom:

- MISSING tools/importer/smoke/eval_all.py

Status:

- Known non-blocker for core fresh install.
- Should be fixed to check current smoke entrypoints.

### TB-M204-FI003: shell env can override tools/importer/.env

Symptom:

- password authentication failed for user hermes_rw

Cause:

- old shell HERMES_MEMORY_DATABASE_URL overrides tools/importer/.env

Fix:

- unset HERMES_MEMORY_DATABASE_URL
- unset HERMES_RW_USER HERMES_RW_PASSWORD
- unset POSTGRES_USER POSTGRES_PASSWORD POSTGRES_DB POSTGRES_PORT POSTGRES_HOST
- unset PGHOST PGPORT PGDATABASE PGUSER PGPASSWORD
- unset DATABASE_URL

### TB-M204-FI004: retrieval governance smoke is not core-profile aware

Symptom:

- blocked_missing_embedding_dependency

Current status:

- Core profile is valid without embedding dependencies.
- hermes-retrieval-governance-smoke should SKIP in core-only profile instead of FAIL.

## Current M204 result

Fresh install core profile is verified as:

- PASS / Docker / PostgreSQL / bootstrap core / migration / import / FTS recall / core smoke
