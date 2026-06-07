# Fresh Clone Bootstrap Verification

Status: M90.1 / clean-clone verification helper

## Purpose

M90.1 adds a repeatable verification helper for the M90 bootstrap path.

It is intended to verify that a fresh clone can prepare the minimal Python runtime before the project enters beta test run.

## Files

```text
bin/hermes-memory-bootstrap-verify
```

Related files:

```text
bin/hermes-memory-bootstrap
requirements-core.txt
requirements-embedding.txt
docs/fresh-clone-bootstrap.md
```

## Core Verification Flow

After running the bootstrap helper:

```bash
bash ./bin/hermes-memory-bootstrap
```

Run:

```bash
bash ./bin/hermes-memory-bootstrap-verify
```

Expected result:

```text
core-python-imports: PASS
status: PASS
embedding_imports: skipped
```

## Optional Embedding Verification Flow

After running:

```bash
bash ./bin/hermes-memory-bootstrap --with-embedding
```

Run:

```bash
bash ./bin/hermes-memory-bootstrap-verify --with-embedding
```

Expected result:

```text
core-python-imports: PASS
embedding-python-imports: PASS
status: PASS
```

## What The Verification Helper Checks

The helper checks:

```text
repo root exists
tools/importer/.venv exists
requirements files exist
bootstrap helper exists
core Python imports work
optional embedding imports work when requested
```

Core Python imports:

```text
psycopg
pgvector
dotenv
numpy
```

Optional embedding imports:

```text
torch
sentence_transformers
```

## What The Verification Helper Does Not Do

The helper does not:

```text
start Docker
run migrations
run importer
run smoke tests
modify runtime database state
```

Those remain separate explicit verification steps.

## Recommended M90.1 Local Verification

In a clean or reset trial clone:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki
bash ./bin/hermes-memory-bootstrap
bash ./bin/hermes-memory-bootstrap-verify
```

Then continue the normal trial checks:

```bash
bash ./bin/hermes-backend-check
bash ./bin/hermes-memory-migrate
bash ./bin/hermes-memory-check
bash ./bin/hermes-memory-import
bash ./bin/hermes-memory-smoke
```

For full hybrid/vector verification:

```bash
bash ./bin/hermes-memory-bootstrap --with-embedding
bash ./bin/hermes-memory-bootstrap-verify --with-embedding
bash ./bin/hermes-memory-smoke
```

## Final Position

M90.1 keeps bootstrap verification explicit and repeatable. It does not hide DB, Docker, import, smoke, or model steps inside the bootstrap helper.
