# Optional Embedding Profile Boundary

Status: v0.7.3-dev guidance  
Scope: personal/local hybrid-vector and full-smoke dependency boundary

## Purpose

Hermes Runes MD Wiki keeps the default fresh-clone path lightweight.

The required baseline is:

```text
PostgreSQL + Markdown import + FTS recall + core smoke
```

Embedding, hybrid/vector recall, and answer-generation smoke suites are optional profile checks. They are useful when installed, but their absence must not fail the core personal/local baseline.

## Required core baseline

Core baseline requires:

```text
requirements-core.txt
```

Core validation command:

```bash
./bin/hermes-memory-smoke
```

Expected result without embedding dependencies:

```text
Core FTS Smoke Test: PASS
Embedding profile not installed: skipping hybrid and answer-generation smoke suites
```

This is a valid core pass.

## Optional embedding profile

Optional embedding/full-smoke setup uses:

```bash
bash ./bin/hermes-memory-bootstrap --with-embedding
```

The bootstrap path installs CPU-only torch first, then:

```text
requirements-embedding.txt
```

This keeps the normal personal/local install from pulling large GPU/CUDA dependency sets by default.

## Boundary

Do not make `sentence_transformers` a required core dependency.

Do not make hybrid/vector recall a release blocker unless the release explicitly targets the optional embedding profile.

Do not add enterprise-grade dependency management or multi-environment orchestration for this profile.

## Recommended validation split

Core smoke:

```bash
./bin/hermes-memory-smoke
```

Optional full-smoke after embedding profile install:

```bash
bash ./bin/hermes-memory-bootstrap --with-embedding
./bin/hermes-memory-smoke
```

## Decision

For v0.7.3-dev, the project treats embedding/full-smoke support as optional.

The baseline remains simple:

```text
Core FTS PASS is required.
Hybrid/vector/full answer generation is optional when dependencies are installed.
```
