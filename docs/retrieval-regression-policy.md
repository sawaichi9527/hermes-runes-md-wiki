# Retrieval Regression Policy

Status: M17.1 planning baseline

This policy defines the minimum regression checks required after importer-related operations.

## Goal

Prevent retrieval quality degradation after:

- new Markdown note creation
- importer execution
- future index updates
- future writer/importer integration

The regression policy exists to ensure that:

- useful memory remains retrievable
- temporary/generated files do not pollute retrieval
- retrieval ordering remains stable
- governance protections remain effective

## Current baseline

M17.1 is planning-only.

No automatic retrieval regression runner exists yet.

All regression checks remain manual.

## Required regression categories

After importer-related changes, verify:

- known-good retrieval still works
- newly imported note is retrievable
- blocked runtime files remain excluded
- manifest/tmp/log paths remain excluded
- retrieval ordering is not obviously degraded
- high-value governance notes still rank correctly

## Minimum required recall smoke

At least one query should verify:

- Markdown source-of-truth
- secret policy retrieval
- forge writer governance retrieval
- newly added note retrieval
- manifest/tmp exclusion

## Example smoke queries

### Markdown source-of-truth

```bash
./bin/hermes-recall "Markdown source-of-truth" \
  --mode hybrid \
  --limit 5 \
  --json
```

Expected:

- governance/source-of-truth notes remain retrievable
- ranking remains reasonable

### Secret policy regression

```bash
./bin/hermes-recall "secrets API keys passwords" \
  --mode hybrid \
  --limit 5 \
  --json
```

Expected:

- secret-governance notes remain retrievable
- runtime/tmp files do not appear

### Generated note retrieval

```bash
./bin/hermes-recall "First Real Write" \
  --project sample-project \
  --mode hybrid \
  --limit 5 \
  --json
```

Expected:

- generated sample note is retrievable
- retrieval does not return manifests/tmp files

### Manifest exclusion regression

```bash
./bin/hermes-recall "forge-manifests" \
  --mode hybrid \
  --limit 5 \
  --json
```

Expected:

- generated manifests are not retrieved as memory
- tmp/runtime artifacts remain excluded

## Required review items

During regression review, verify:

- retrieval ranking remains stable
- no accidental spam dominates results
- no duplicated generated note flood exists
- no runtime/debug artifacts appear
- no secrets appear in retrieval output

## Safety invariants

- regression smoke must be safe to run repeatedly
- regression smoke must not modify memory
- regression smoke must not trigger importer automatically
- regression smoke must remain human-reviewed

## Future direction

A future regression helper may be added later, for example:

```bash
python tools/importer/retrieval_regression_smoke.py --json
```

But M17.1 remains planning-only.
