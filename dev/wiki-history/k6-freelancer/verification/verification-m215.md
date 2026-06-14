# Verification M215 - v0.7.2 Release Notes / Version Alignment

Status: PASS / local release check verified / tag handoff complete  
Scope: release notes and VERSION alignment only; annotated tag handled by M216

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

## Local release check evidence

The local release check was completed after guarded update to the v0.7.2 release baseline.

Observed results:

- `./bin/runes-wiki-migration-guard update`: SAFE
- Incoming changed files: README / VERSION / dev verification / release notes only
- Guard applied `git pull --ff-only`
- `cat VERSION`: `0.7.2`
- `python3 -m py_compile tools/wiki_migration_guard/migration_guard.py`: PASS
- `./bin/runes-wiki-migration-guard plan --no-fetch`: PASS / no incoming changes
- `./bin/runes-wiki-migration-guard update --dry-run --no-fetch`: PASS / dry run only
- `./bin/hermes-memory-smoke`: PASS for Core FTS smoke
- embedding profile not installed; hybrid and answer-generation smoke skipped as expected
- `git status`: working tree clean

## Tag handoff

M215 handed off to M216 for annotated tag lock.

M216 confirmed:

```text
v0.7.2 -> 6f68494
```

The tag points at the release baseline that contains `VERSION = 0.7.2`.

## Final lock

```text
M215 v0.7.2 Release Notes / Version Alignment
PASS / local release check verified / tag handoff complete
```

---
