# Fresh Clone Bootstrap

Status: M90 / personal-local bootstrap guide

## Purpose

This document defines the minimal fresh-clone bootstrap path for Hermes Runes MD Wiki.

It exists to close the trial-run gap recorded as:

```text
TB-20260605-001 Fresh clone lacks dependency bootstrap
```

The goal is to prepare for beta test run by fixing the known fresh-clone setup issue during trial-run instead of carrying it forward.

## Design Boundaries

The bootstrap flow is intentionally bounded:

```text
personal-local
non-enterprise
non-daemon
no orchestration
no Docker lifecycle modification
no .env secret creation
no automatic migration
no automatic import
```

The bootstrap helper only prepares Python runtime dependencies inside:

```text
tools/importer/.venv
```

It does not start or modify PostgreSQL, Docker Compose, LM Studio, Chronos, or any external model service.

## Files

```text
requirements-core.txt
requirements-embedding.txt
bin/hermes-memory-bootstrap
```

## Core Bootstrap

Use the core profile for a fresh clone when you only need:

```text
memory check
schema migration wrapper
importer
core FTS smoke
basic DB access
```

Command:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki
bash ./bin/hermes-memory-bootstrap
```

This installs:

```text
psycopg[binary]
pgvector
python-dotenv
numpy
```

It intentionally does not install `sentence-transformers` or `torch`.

## Embedding / Full Smoke Bootstrap

Use the embedding profile only when you need hybrid/vector/full-smoke behavior:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki
bash ./bin/hermes-memory-bootstrap --with-embedding
```

The helper installs CPU-only torch first:

```text
https://download.pytorch.org/whl/cpu
```

Then it installs:

```text
requirements-embedding.txt
```

This avoids pulling large CUDA wheels by default during personal-local fresh clone setup.

## What This Does Not Do

The bootstrap helper does not:

```text
create tools/importer/.env
write HERMES_MEMORY_DATABASE_URL
start Docker
create PostgreSQL databases
run migrations
run importer
run smoke tests
configure OPENAI_BASE_URL
configure OPENAI_MODEL
```

Those remain explicit human-controlled steps.

## Recommended Fresh Clone Sequence

After cloning the repo:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki
bash ./bin/hermes-memory-bootstrap
```

Then configure the runtime DB env manually:

```text
tools/importer/.env
```

Then run the existing explicit checks:

```bash
bash ./bin/hermes-backend-check
bash ./bin/hermes-memory-migrate
bash ./bin/hermes-memory-check
bash ./bin/hermes-memory-import
bash ./bin/hermes-memory-smoke
```

For full hybrid/vector smoke:

```bash
bash ./bin/hermes-memory-bootstrap --with-embedding
bash ./bin/hermes-memory-smoke
```

## Expected Smoke Behavior Without Model Env

If `OPENAI_BASE_URL` and `OPENAI_MODEL` are not configured, M10 answer-generation smoke should skip cleanly:

```text
M10 Observation Log Smoke Test
status: SKIP
reason: missing_model_env
```

This is expected until a model endpoint is explicitly configured.

## Expected Promotion Governance Behavior Without Trial Fixture

If no approved trial promotion fixture exists, M20.4 promotion governance smoke should skip cleanly:

```text
M20.4 Promotion Governance Smoke
status: SKIP
reason: promotion_governance_fixture_not_available_in_trial_workspace
```

This is expected until a governed, human-reviewed trial proposal fixture exists.

## Final Position

M90 keeps setup simple and explicit. It fixes the fresh-clone dependency gap without hiding Docker, DB, model, or secret operations inside a bootstrap script.
