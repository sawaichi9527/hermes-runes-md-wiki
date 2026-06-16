# M225 Optional Embedding Profile Boundary

Status: READY FOR LOCAL VALIDATION  
Target: v0.7.3-dev

## Purpose

Clarify that embedding, hybrid/vector recall, and answer-generation smoke suites are optional profile checks, not required core baseline checks.

## Changes prepared

- Added `docs/optional-embedding-profile.md`.
- Preserved lightweight default install behavior.
- Kept `requirements-core.txt` as the default dependency baseline.
- Kept `requirements-embedding.txt` as the optional embedding/full-smoke profile.

## Expected validation

```bash
cat requirements-core.txt
cat requirements-embedding.txt
cat docs/optional-embedding-profile.md
./bin/hermes-memory-smoke
```

Expected core behavior without embedding dependencies:

```text
Core FTS Smoke Test: PASS
Embedding profile not installed: skipping hybrid and answer-generation smoke suites
```

This remains a valid core pass.
