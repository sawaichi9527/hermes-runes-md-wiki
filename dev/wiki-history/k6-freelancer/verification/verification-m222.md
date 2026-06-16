# M222 Single-Agent Baseline Sanity Check

Status: READY FOR LOCAL VALIDATION  
Target: v0.7.3-dev  
Scope: mainline docs / runtime wiki seed / fresh-install baseline

## Purpose

Verify that the active `main` branch is aligned with the single-agent / agent-agnostic baseline after M221.

## Changes prepared

- Removed remaining active OPC references from `wiki/freelancer/README.md`.
- Updated `docs/fresh-install-manual.md` for the v0.7.3-dev single-agent mainline.
- Kept `v0.7.2` and `archive/v0.7.2-opc` as historical/archive context only.
- Kept repository path unchanged: `~/workspace/hermes-runes-md-wiki`.

## Expected validation

```bash
grep -RIn "docs/opc-workspace-overlay.md\|wiki/freelancer/opc\|Hermes Agent OPC profile agents\|optional OPC profile memory overlay" \
  README.md docs wiki/_system wiki/freelancer || true

cat VERSION
./bin/runes-wiki-migration-guard plan --no-fetch
./bin/hermes-memory-smoke
git status
```

Expected result:

```text
VERSION = 0.7.3-dev
No active OPC overlay references in runtime docs
Guard plan SAFE after sync
Core FTS smoke PASS
Working tree clean
```

## Boundary

This milestone does not remove archived OPC history from:

```text
archive/v0.7.2-opc
dev/wiki-history/
docs/releases/v0.7.2.md
```

Archive references are allowed as historical evidence.
