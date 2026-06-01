# K6 Protected Retrieval Regression Plan

Status: M17.3 planning baseline

This document defines protected retrieval regression checks for the `k6-freelancer` namespace.

M17.3 does not enable `k6-freelancer` real-write.

## Goal

Define what must remain retrievable and protected before any future `k6-freelancer` writer/importer enablement.

The plan protects:

- project baseline knowledge
- operations history
- verification history
- service documentation
- governance decisions
- next-action continuity

## Current namespace status

`k6-freelancer` remains protected:

- forge real-write is blocked
- importer execution remains manual
- index update remains manually gated
- retrieval regression remains manual

## Required protected queries

### 1. M15 writer governance

```bash
./bin/hermes-recall "M15 forge writer governance baseline" \
  --project k6-freelancer \
  --mode hybrid \
  --limit 5 \
  --json
```

Expected:

- governance or verification notes are retrievable
- tmp/manifest/log artifacts do not appear

### 2. M16 importer preview governance

```bash
./bin/hermes-recall "M16 importer preview read-only baseline" \
  --project k6-freelancer \
  --mode hybrid \
  --limit 5 \
  --json
```

Expected:

- importer preview/manual import governance remains retrievable
- generated manifests are absent

### 3. Operations continuity

```bash
./bin/hermes-recall "operations memory audit PASS" \
  --project k6-freelancer \
  --mode hybrid \
  --limit 5 \
  --json
```

Expected:

- operations-related records remain retrievable
- ordering is not dominated by generated note spam

### 4. Services continuity

```bash
./bin/hermes-recall "Telegram integration service" \
  --project k6-freelancer \
  --mode hybrid \
  --limit 5 \
  --json
```

Expected:

- service documentation remains retrievable
- core service notes rank reasonably

### 5. Verification continuity

```bash
./bin/hermes-recall "verification smoke PASS" \
  --project k6-freelancer \
  --mode hybrid \
  --limit 5 \
  --json
```

Expected:

- verification records remain retrievable
- retrieval does not return temporary runtime files

## Protected failure indicators

Treat regression as FAIL if:

- `tmp/` files appear as memory sources
- `logs/` or observation files appear as memory sources
- forge manifests appear as memory sources
- generated draft notes dominate protected queries
- k6-freelancer governance notes become hard to retrieve
- secret-like values appear in retrieval output

## Enablement gate

Before future `k6-freelancer` real-write enablement, run this plan manually and record PASS status.

Do not enable k6 writer/importer integration if protected retrieval is already unstable.

## Future runner direction

A future helper may add a protected namespace regression suite, but M17.3 remains planning-only.
