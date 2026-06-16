# M226 v0.7.3 Release Candidate Prep

Status: READY FOR LOCAL RC CHECK  
Date: 2026-06-17

## Purpose

Prepare v0.7.3 release candidate documentation after M222-M225 are resolved.

M226 does not create a release tag.

## Entry criteria

```text
M222 PASS / single-agent sanity locally verified
M223 PASS / active guidance approved and documented
M224 PASS / sync path locally verified
M225 PASS / optional embedding boundary locally verified
```

## Prepared release notes

```text
docs/releases/v0.7.3.md
```

## RC scope

v0.7.3 release candidate scope:

```text
single-agent mainline stabilization
agent / subagent / Kanban active guidance
hermes-memory-sync root resolution fix
optional embedding profile boundary
Core FTS smoke as required baseline
```

## Not in RC scope

```text
release tag creation
enterprise workflow layer
new runtime daemon
new task queue
new database
profile-agent runtime restoration
mandatory embedding dependency
```

## Required local check

Run:

```bash
cat VERSION
python3 -m py_compile tools/importer/root_resolver.py
bash -n bin/hermes-memory-sync
./bin/runes-wiki-migration-guard plan --no-fetch
./bin/hermes-memory-smoke
git status
git log --oneline -12
```

Expected:

```text
VERSION = 0.7.3-dev
py_compile PASS
shell syntax PASS
guard plan SAFE when no incoming changes exist
Core FTS smoke PASS
embedding profile may be skipped when not installed
working tree clean
```

## Current decision

M226 is ready for local RC check.

Final release/tag lock is deferred until local validation confirms the RC baseline.
