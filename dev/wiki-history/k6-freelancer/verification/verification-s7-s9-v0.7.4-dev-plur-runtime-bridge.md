# Verification: S7-S9 v0.7.4-dev PLUR Runtime Bridge

Status: IMPLEMENTED / pending local pull smoke  
Date: 2026-06-27  
Version line: 0.7.4-dev

## Scope

This verification note records the S7-S9 implementation for the optional PLUR runtime memory bridge.

The implementation remains read-only and no-op-first. It does not read existing deployed PLUR memory, write PLUR memory, migrate PLUR records, delete PLUR records, or change Hermes Agent native configuration.

## Implementation artifacts

```text
tools/importer/plur_runtime_bridge.py
tools/importer/smoke/eval_smoke_plur_bridge.py
bin/hermes-memory-smoke
docs/plur-runtime-memory-bridge.md
CHANGELOG.md
dev/wiki-history/k6-freelancer/next-actions.md
```

## S7 — PLUR read-only discovery / status check

Implemented command:

```bash
python3 tools/importer/plur_runtime_bridge.py status --json
```

Expected behavior:

```text
- reports provider_requested and provider_selected
- reports read_only=true
- reports memory_read=false
- reports memory_write=false
- reports writes_performed=false
- detects PLUR availability signals without importing modules or running commands
- does not print environment variable values
```

Status: IMPLEMENTED

## S8 — Runtime memory provider abstraction / Noop provider

Implemented provider boundary:

```text
RuntimeMemoryProvider.status() -> ProviderStatus
```

Providers:

```text
noop = always available safe fallback
plur = read-only availability detector
```

`--provider auto` intentionally selects `noop` during S7-S9. This avoids accidental interaction with already-deployed PLUR memory.

Status: IMPLEMENTED

## S9 — PLUR memory schema mapping

Implemented command:

```bash
python3 tools/importer/plur_runtime_bridge.py schema --json
```

Expected roles:

```text
engram
episode
checkpoint
candidate
```

Expected safety behavior:

```text
episode.default_prompt_injection = disabled
candidate.auto_promote_to_runes_wiki = false
schema read_only = true
schema writes_performed = false
```

Status: IMPLEMENTED

## Core smoke integration

`./bin/hermes-memory-smoke` now runs:

```text
smoke/eval_smoke_core_fts.py
smoke/eval_smoke_plur_bridge.py
```

The PLUR bridge smoke is part of the lightweight core profile and does not require PLUR or embedding dependencies.

Status: IMPLEMENTED

## Local verification commands

Run after pulling from GitHub:

```bash
cd ~/workspace/hermes-runes-md-wiki
git pull
git status
python3 tools/importer/plur_runtime_bridge.py status --json
python3 tools/importer/plur_runtime_bridge.py schema --json
./bin/hermes-memory-smoke
```

Expected result:

```text
git status clean
status command PASS with provider_selected=noop in auto mode
schema command PASS with engram/episode/checkpoint/candidate
Core FTS smoke PASS
PLUR Runtime Bridge Smoke Test PASS
embedding smoke SKIP remains acceptable when embedding profile is not installed
```

## Result

```text
PASS: S7 read-only status helper implemented.
PASS: S8 Noop provider abstraction implemented.
PASS: S9 schema mapping implemented.
PASS: Core smoke now includes PLUR bridge smoke.
PENDING: User local pull and smoke verification.
```
