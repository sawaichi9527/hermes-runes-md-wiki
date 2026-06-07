# Retrieval Regression Runner Scope

Status: M17.5a scope baseline

This document defines the initial scope for a future read-only retrieval regression runner.

The runner is not implemented in M17.5a.

## Goal

Convert the manual M17 retrieval smoke plan into a repeatable helper while keeping it read-only.

Future command target:

```bash
python tools/importer/retrieval_regression_smoke.py --json
```

## Non-goals

The runner must not:

- modify the database
- update indexes
- trigger importer execution
- trigger writer execution
- create or edit Markdown notes
- commit or push git changes
- ingest manifests or runtime artifacts

## Required initial query set

The first runner MVP should execute a small fixed query set.

### sample-project queries

- `Markdown source-of-truth`
- `secrets API keys passwords`
- `First Real Write`
- `forge-manifests`

### k6-freelancer protected queries

- `M15 forge writer governance baseline`
- `M16 importer preview read-only baseline`
- `operations memory audit PASS`
- `Telegram integration service`
- `verification smoke PASS`

## Required blacklist checks

The runner should inspect returned source paths and fail if any path contains:

- `/tmp/`
- `tmp/`
- `/logs/`
- `logs/`
- `observations/`
- `forge-manifests`
- `.jsonl`

## Required output fields

The runner should emit JSON with:

- suite name
- status
- failed count
- total count
- per-query result status
- query text
- project namespace
- source paths observed
- blacklist hits
- command return code

## PASS criteria

A query should PASS when:

- the recall command exits successfully
- JSON output is parseable
- no blacklisted source path appears
- at least one result is returned for positive retrieval queries

## FAIL criteria

A query should FAIL when:

- recall command fails
- JSON output cannot be parsed
- blacklisted source path appears
- expected positive retrieval returns zero results
- secret-like or runtime artifact source appears

## Initial implementation constraints

The first implementation should:

- use existing `./bin/hermes-recall`
- support `--json`
- remain deterministic enough for smoke usage
- avoid ranking-sensitive hard assertions where possible
- fail on blacklist/source contamination
- avoid modifying any repository file

## Future expansion

Later versions may add:

- configurable query YAML/JSON
- stricter expected source assertions
- ranking stability checks
- before/after comparison
- CI integration

M17.5a remains planning-only.
