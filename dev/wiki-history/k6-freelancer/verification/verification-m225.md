# M225 Optional Embedding Profile Boundary

Status: PASS / optional embedding boundary locally verified  
Target: v0.7.3-dev

## Purpose

Clarify that embedding, hybrid/vector recall, and answer-generation smoke suites are optional profile checks, not required core baseline checks.

## Changes verified

- Added `docs/optional-embedding-profile.md`.
- Preserved lightweight default install behavior.
- Kept `requirements-core.txt` as the default dependency baseline.
- Kept `requirements-embedding.txt` as the optional embedding/full-smoke profile.

## Local validation evidence

User validation confirmed that `docs/optional-embedding-profile.md` states:

```text
Core FTS PASS is required.
Hybrid/vector/full answer generation is optional when dependencies are installed.
```

Core smoke result:

```text
Core FTS Smoke Test: PASS
Embedding profile not installed: skipping hybrid and answer-generation smoke suites
```

This remains a valid core pass.

## Boundary

M225 does not make `sentence_transformers` a required core dependency.

M225 does not make hybrid/vector recall a release blocker for the default personal/local baseline.

M225 does not add enterprise-grade dependency management or multi-environment orchestration.

## Final lock

M225 is locked as:

```text
PASS / optional embedding boundary locally verified
```
