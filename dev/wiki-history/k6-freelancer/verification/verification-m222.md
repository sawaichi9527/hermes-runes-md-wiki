# M222 Single-Agent Baseline Sanity Check

Status: PASS / single-agent sanity locally verified  
Target: v0.7.3-dev  
Scope: mainline docs / runtime wiki seed / fresh-install baseline

## Purpose

Verify that the active `main` branch is aligned with the single-agent / agent-agnostic baseline after M221.

## Changes verified

- Remaining active OPC references were removed from `wiki/freelancer/README.md`.
- `docs/fresh-install-manual.md` was updated for the v0.7.3-dev single-agent mainline.
- `v0.7.2` and `archive/v0.7.2-opc` remain historical/archive context only.
- Repository path remains unchanged: `~/workspace/hermes-runes-md-wiki`.

## Local validation evidence

User validation confirmed:

```text
VERSION = 0.7.3-dev
main == origin/main
working tree clean
latest commit before lock: 0214dd0 Add M225 optional embedding verification
```

The active OPC overlay files were absent:

```text
docs/opc-workspace-overlay.md
wiki/_system/opc-workspace-overlay-policy.md
wiki/freelancer/opc/README.md
```

The active-doc grep for old OPC overlay paths produced no active matches before the sync-wrapper help output.

Fresh-install manual retained the required single-agent baseline markers:

```text
Status: v0.7.3-dev single-agent fresh-install baseline
PostgreSQL / pgvector via local Docker stack
single-agent / agent-agnostic mainline baseline
core profile first: PostgreSQL / migration / Markdown import / FTS recall / core smoke
git clone https://github.com/sawaichi9527/hermes-runes-md-wiki.git
./bin/hermes-memory-import
./bin/hermes-memory-smoke
./bin/runes-wiki-migration-guard update
```

## Smoke evidence

Core smoke result:

```text
Core FTS Smoke Test: PASS
Embedding profile not installed: skipping hybrid and answer-generation smoke suites
```

## Boundary

This milestone does not remove archived OPC history from:

```text
archive/v0.7.2-opc
dev/wiki-history/
docs/releases/v0.7.2.md
```

Archive references are allowed as historical evidence.

## Final lock

M222 is locked as:

```text
PASS / single-agent sanity locally verified
```
