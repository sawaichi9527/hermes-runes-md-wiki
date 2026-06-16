# M227 v0.7.3 Final Release Lock

Status: READY FOR FINAL TAG CHECK  
Date: 2026-06-17

## Purpose

Finalize the v0.7.3 release documentation after M226 local RC validation.

M227 records the final release file state and prepares the repository for the `v0.7.3` annotated tag.

## Entry state

```text
M222 PASS / single-agent sanity locally verified
M223 PASS / active guidance approved and documented
M224 PASS / sync path locally verified
M225 PASS / optional embedding boundary locally verified
M226 PASS / RC locally verified / ready for final release tag
```

## Finalized files

```text
VERSION

docs/releases/v0.7.3.md
```

## Expected final validation

```bash
cat VERSION
python3 -m py_compile tools/importer/root_resolver.py
bash -n bin/hermes-memory-sync
./bin/runes-wiki-migration-guard plan --no-fetch
./bin/hermes-memory-smoke
git status
git log --oneline -10
```

Expected result:

```text
VERSION = 0.7.3
migration guard plan SAFE
Core FTS smoke PASS
working tree clean
```

## Tag command

The tag is expected to be created manually from a clean local checkout after this verification passes:

```bash
git tag -a v0.7.3 -m "Release v0.7.3"
git push origin v0.7.3
```

## Boundary

M227 does not add runtime features.

M227 does not reintroduce OPC profile agents.

M227 does not add daemons, queues, databases, or enterprise workflow components.

## Current lock state

```text
READY FOR FINAL TAG CHECK
```
