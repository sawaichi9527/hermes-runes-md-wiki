# M224 hermes-memory-sync Path Fix

Status: PASS / sync path locally verified  
Target: v0.7.3-dev

## Purpose

Fix stale repository-root assumptions in the sync wrapper while keeping the personal/local setup simple.

## Changes verified

- `bin/hermes-memory-sync` resolves the repo root from a modern runes-wiki root override, a legacy root override, or the parent of `bin/`.
- `tools/importer/root_resolver.py` prefers the modern runes-wiki root override, then legacy compatibility, then inferred repo root, then current workspace fallback.

## Local validation evidence

User validation confirmed:

```bash
python3 -m py_compile tools/importer/root_resolver.py
bash -n bin/hermes-memory-sync
./bin/hermes-memory-sync --help
HERMES_RUNES_MD_WIKI_ROOT="$PWD" ./bin/hermes-memory-sync --help
```

Both help checks printed the expected wrapper usage and environment section:

```text
HERMES_RUNES_MD_WIKI_ROOT Repo root override for hermes-runes-md-wiki
HERMES_MEMORY_ROOT        Legacy repo root override, still accepted
```

## Boundary

M224 does not add a daemon, service manager, or enterprise configuration layer.

It only repairs local root discovery for the existing personal/local wrapper.

## Final lock

M224 is locked as:

```text
PASS / sync path locally verified
```
