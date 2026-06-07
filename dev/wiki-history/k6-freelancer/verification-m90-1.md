# M90.1 Fresh Clone Bootstrap Verification Helper

Status: PASS / verification helper added / pending clean-run evidence
Date: 2026-06-05

## Purpose

M90.1 adds a repeatable verification helper for the M90 fresh clone bootstrap path.

This milestone exists because trial-run should expose and fix setup issues before beta test run.

## Implemented Files

```text
bin/hermes-memory-bootstrap-verify
docs/fresh-clone-bootstrap-verification.md
```

Related M90 files:

```text
bin/hermes-memory-bootstrap
requirements-core.txt
requirements-embedding.txt
docs/fresh-clone-bootstrap.md
wiki/k6-freelancer/verification-m90.md
```

## Verification Helper

Core verification command:

```bash
bash ./bin/hermes-memory-bootstrap-verify
```

Optional embedding verification command:

```bash
bash ./bin/hermes-memory-bootstrap-verify --with-embedding
```

## Checks

The helper validates:

```text
repo root exists
tools/importer/.venv exists
requirements files exist
bootstrap helper exists
core Python imports work
optional embedding imports work when requested
```

Core Python import checks:

```text
psycopg
pgvector
dotenv
numpy
```

Optional embedding import checks:

```text
torch
sentence_transformers
```

## Boundaries

The helper does not:

```text
start Docker
run migrations
run importer
run smoke tests
modify runtime database state
```

These steps remain explicit human-controlled verification steps.

## Expected Core Result

After running:

```bash
bash ./bin/hermes-memory-bootstrap
```

Expected verification:

```text
core-python-imports: PASS
status: PASS
embedding_imports: skipped
```

## Expected Optional Embedding Result

After running:

```bash
bash ./bin/hermes-memory-bootstrap --with-embedding
```

Expected verification:

```text
core-python-imports: PASS
embedding-python-imports: PASS
status: PASS
```

## Remaining Evidence Needed

This lock records that the verification helper has been added.

A follow-up local run should capture clean-run evidence from the trial clone:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki
bash ./bin/hermes-memory-bootstrap
bash ./bin/hermes-memory-bootstrap-verify
```

Optional full profile:

```bash
bash ./bin/hermes-memory-bootstrap --with-embedding
bash ./bin/hermes-memory-bootstrap-verify --with-embedding
```

## Final Lock

```text
M90.1 Fresh Clone Bootstrap Verification Helper
PASS / verification helper added / pending clean-run evidence
```
