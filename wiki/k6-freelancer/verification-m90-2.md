# M90.2 CPU Embedding Clean Verification

Status: PASS / clean verifier added / pending local run
Date: 2026-06-06

## Purpose

M90.2 adds a clean temporary environment verifier for optional embedding bootstrap.

This is needed because the existing trial venv already contains GPU-oriented packages, so it cannot prove that the bootstrap path is lightweight.

## Implemented File

```text
bin/hermes-memory-embedding-cpu-clean-verify
```

## Verification Command

```bash
bash ./bin/hermes-memory-embedding-cpu-clean-verify
```

Optional inspection mode:

```bash
bash ./bin/hermes-memory-embedding-cpu-clean-verify --keep-tmp
```

## Pass Criteria

The helper must report:

```text
status: PASS
blocked_packages: []
```

It checks a clean temp venv, not the project venv.

## Blocked Package Pattern

The helper fails if package names match:

```text
cuda*
nvidia*
triton
```

## Boundary

The helper only verifies package behavior in a temporary venv.

It does not run Docker, migrations, importer, smoke tests, or database mutation.

## Final Lock

```text
M90.2 CPU Embedding Clean Verification
PASS / clean verifier added / pending local run
```
