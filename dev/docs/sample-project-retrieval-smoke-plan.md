# Sample Project Retrieval Smoke Plan

Status: M17.2 planning baseline

This document defines the manual retrieval smoke checks for `sample-project`.

M17.2 does not add an automatic runner.

## Goal

Verify that sample-project retrieval remains useful and uncontaminated after importer-related operations.

## Required smoke queries

### 1. Markdown source-of-truth

```bash
./bin/hermes-recall "Markdown source-of-truth" \
  --project sample-project \
  --mode hybrid \
  --limit 5 \
  --json
```

Expected:

- source-of-truth or governance-related sample notes are retrieved
- results do not include tmp/runtime/manifest paths

### 2. Secret policy

```bash
./bin/hermes-recall "secrets API keys passwords" \
  --project sample-project \
  --mode hybrid \
  --limit 5 \
  --json
```

Expected:

- secret policy decision or verification notes are retrieved
- no real secrets appear in results
- results do not include tmp/runtime/manifest paths

### 3. First Real Write sample note

```bash
./bin/hermes-recall "First Real Write" \
  --project sample-project \
  --mode hybrid \
  --limit 5 \
  --json
```

Expected:

- `wiki/sample-project/project-first-real-write-overview.md` is retrievable after importer execution
- retrieval does not return generated manifests or tmp files

### 4. Manifest exclusion

```bash
./bin/hermes-recall "forge-manifests" \
  --project sample-project \
  --mode hybrid \
  --limit 5 \
  --json
```

Expected:

- generated manifest files are not returned as memory sources
- tmp paths are not returned
- runtime artifacts are not returned

## Manual review checklist

For each query, review:

- top result path
- source path quality
- whether result belongs to sample-project
- whether tmp/manifest/log paths appear
- whether irrelevant generated content dominates
- whether any secret-like value appears

## Pass criteria

Manual smoke can be considered PASS when:

- expected sample-project notes are retrievable
- manifest/tmp/log paths are absent
- no secret-like content appears
- ranking is reasonable for the query
- no importer or writer command runs automatically

## Failure indicators

Treat the smoke as FAIL if:

- generated manifests are retrieved as memory
- tmp/runtime/log files appear as sources
- secret-like content appears
- expected sample notes cannot be retrieved after importer execution
- unrelated generated note spam dominates the top results

## Future runner direction

A future `retrieval_regression_smoke.py` may automate these checks, but M17.2 remains manual and planning-only.
