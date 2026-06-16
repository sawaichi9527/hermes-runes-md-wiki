# M224 hermes-memory-sync Path Fix

Status: READY FOR LOCAL VALIDATION  
Target: v0.7.3-dev

## Purpose

Fix stale repository-root assumptions in the sync wrapper while keeping the personal/local setup simple.

## Changes prepared

- `bin/hermes-memory-sync` now resolves the repo root from a modern runes-wiki root override, a legacy root override, or the parent of `bin/`.
- `tools/importer/root_resolver.py` now prefers the modern runes-wiki root override, then legacy compatibility, then inferred repo root, then current workspace fallback.

## Expected validation

```bash
python3 -m py_compile tools/importer/root_resolver.py
bash -n bin/hermes-memory-sync
./bin/hermes-memory-sync --help
HERMES_RUNES_MD_WIKI_ROOT="$PWD" ./bin/hermes-memory-sync --help
```

Optional runtime check when local database settings are ready:

```bash
./bin/hermes-memory-sync --smoke
```
