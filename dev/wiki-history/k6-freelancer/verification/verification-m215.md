# Verification M215 - v0.7.2 Release Notes / Version Alignment

Status: READY FOR LOCAL RELEASE CHECK  
Scope: release notes and VERSION alignment only; tag pending

## Purpose

M215 prepares the v0.7.2 release commit after M214 approved release prep.

## Changes prepared

M215 prepared:

- `docs/releases/v0.7.2.md`
- README release references aligned to v0.7.2
- `VERSION` changed from `0.7.2-dev` to `0.7.2`

## Release scope

v0.7.2 remains limited to:

- minimal `runes-wiki-migration-guard` update safety helper
- existing-installation update flow documentation
- migration guard dogfood locks
- release documentation alignment

## Non-goals preserved

M215 does not add:

- migration guard feature expansion
- automatic repair/apply behavior
- auto-restore behavior
- Git hook behavior
- daemon behavior
- Shield integration
- user-owned `wiki/` edits

## Local release check required

Before creating tag `v0.7.2`, run:

```bash
cd ~/workspace/hermes-runes-md-wiki

./bin/runes-wiki-migration-guard update
cat VERSION
python3 -m py_compile tools/wiki_migration_guard/migration_guard.py
./bin/runes-wiki-migration-guard plan --no-fetch
./bin/runes-wiki-migration-guard update --dry-run --no-fetch
./bin/hermes-memory-smoke

git status
git log --oneline -12
```

Expected:

- `VERSION` is `0.7.2`
- guard update is SAFE
- Python compile passes
- plan / dry-run remain stable
- Core FTS smoke passes
- working tree is clean

## Tag checkpoint

After local release check passes, M216 should create the annotated tag:

```bash
git tag -a v0.7.2 -m "Release v0.7.2"
git push origin v0.7.2
```

The tag should point at the release commit that contains `VERSION = 0.7.2`.

## Current lock state

```text
M215 v0.7.2 Release Notes / Version Alignment
READY FOR LOCAL RELEASE CHECK / tag pending
```

---
