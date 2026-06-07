# M90 Fresh Clone Bootstrap Minimal Path

Status: PASS / bootstrap path added / pending local verification
Date: 2026-06-05

## Purpose

M90 addresses the remaining open trial-run gap:

```text
TB-20260605-001 Fresh clone lacks dependency bootstrap
```

The goal is to prevent this known trial-run issue from being carried into beta test run.

## Implemented Files

```text
requirements-core.txt
requirements-embedding.txt
bin/hermes-memory-bootstrap
docs/fresh-clone-bootstrap.md
```

## Bootstrap Design

The bootstrap path is intentionally minimal and explicit:

```text
personal-local
bounded
non-enterprise
non-daemon
no orchestration
```

It prepares only the local Python runtime environment:

```text
tools/importer/.venv
```

It does not modify:

```text
Docker
PostgreSQL service lifecycle
runtime databases
local secret files
model endpoint settings
migration state
import state
```

## Core Profile

Command:

```bash
bash ./bin/hermes-memory-bootstrap
```

Installs:

```text
requirements-core.txt
```

Purpose:

```text
memory check
migration wrapper
importer
core FTS smoke
basic PostgreSQL access
```

## Optional Embedding Profile

Command:

```bash
bash ./bin/hermes-memory-bootstrap --with-embedding
```

Behavior:

```text
install CPU-only torch first
then install requirements-embedding.txt
```

Purpose:

```text
hybrid/vector/full smoke support
```

This avoids pulling large CUDA wheels by default during fresh clone setup.

## Verification Target

A later local verification should run the bootstrap in a clean or reset trial clone and confirm:

```bash
bash ./bin/hermes-memory-bootstrap
bash ./bin/hermes-memory-check
bash ./bin/hermes-memory-smoke
```

Expected core smoke behavior without embedding profile:

```text
Core FTS: PASS
Embedding profile not installed: skipping hybrid and answer-generation smoke suites
```

Expected full smoke behavior with embedding profile but no model env:

```text
Core FTS: PASS
M5.2: PASS
M10: SKIP / missing_model_env
M11: PASS
M11.6: PASS
M20.4: SKIP / no trial fixture
```

## Boundaries Preserved

M90 does not introduce:

```text
no orchestration daemon
no websocket bridge
no enterprise telemetry system
no automatic proposal apply
no direct wiki mutation by agent
no runtime authority escalation
no Docker lifecycle ownership by the repo
```

## Final Lock

```text
M90 Fresh Clone Bootstrap Minimal Path
PASS / bootstrap path added / pending local verification
```
