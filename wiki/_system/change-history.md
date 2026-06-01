# Hermes Runes Change History

Status: P0 baseline

## Purpose

This file records structural Markdown wiki changes.

It exists to support:

- freshness awareness
- relationship tracking
- structural recovery
- policy evolution awareness
- future consistency probes

## Scope

This file should record:

- create file
- create objective namespace
- create objective file
- rename file
- move file
- archive file
- delete file
- promote file
- split/merge operation
- index repair
- policy update

This file should not record:

- ordinary RAG recall
- context build
- answer generation
- full prompts
- raw memory dumps
- secrets

## Baseline Event Format

```text
[YYYY-MM-DD HH:MM TZ]
TYPE: <event-type>
PATH: <path>
DETAILS: <summary>
```

## Initial Events

[2026-06-01 00:00 UTC]
TYPE: POLICY_UPDATE
PATH: wiki/_system/
DETAILS: Initial P0 governance policy baseline created.
