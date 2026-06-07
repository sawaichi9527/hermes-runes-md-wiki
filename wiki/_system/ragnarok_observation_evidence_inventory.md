# Ragnarok Observation Evidence Inventory

Status: M33.5 evidence inventory lock

## Purpose

Ragnarok Observation Evidence Inventory defines what kinds of evidence may be collected by a future Ragnarok Observation Bundle / 諸神的黃昏觀測封包.

This document prevents the bundle workflow from being reduced to only Markdown Source Health.

Runes Markdown Source Health is one branch of the World Tree.
Ragnarok Observation Bundle is intended to shake the whole World Tree and collect selected non-secret observation echoes across the project.

## Scope

A future Ragnarok Observation Bundle may collect selected non-secret evidence from these categories.

## Evidence Category 1: Repository State

Purpose:

- understand current source state
- support regression analysis
- identify local modifications before analysis

Allowed examples:

- `git status --short`
- `git log --oneline -20`
- tracked file inventory
- ignored local evidence existence summary
- branch / HEAD summary

Must exclude:

- credentials
- remote tokens
- private `.env` content
- unbounded raw file dumps

## Evidence Category 2: Smoke and Verification Results

Purpose:

- understand whether baseline and governance locks still pass
- identify regression points

Allowed examples:

- M31 final verification lock result
- M32 P0 trial run lock result
- M33 smoke result summaries
- `hermes-memory-smoke` summary
- PASS / FAIL / duration / return code metadata

Must exclude:

- raw full prompts
- raw full answers
- raw memory context
- unrestricted terminal scrollback

## Evidence Category 3: Operations Metadata

Purpose:

- summarize governed apply / refresh / recall / reject activity
- support observe-analyze-fix-observe loops

Allowed examples:

- operation type
- operation timestamp
- status
- return code
- risk class
- write flag
- duration
- target path summary
- operation count by type

Must exclude:

- raw secrets
- full sensitive payloads
- unrestricted raw operations logs
- database dumps

## Evidence Category 4: Observation Summaries

Purpose:

- summarize model / sanitizer / retrieval / answer-generation behavior
- provide tuning evidence without leaking raw conversation content

Allowed examples:

- observation record counts
- valid / invalid count
- parse error count
- selected model profile counts
- quality issue counts
- sanitizer issue counts
- retry counts
- citation integrity summary

Must exclude:

- raw full prompt
- raw full answer
- raw full memory context
- API keys
- Telegram bot tokens
- credentials

## Evidence Category 5: Reports

Purpose:

- preserve curated analysis snapshots
- provide durable observation baselines

Allowed examples:

- `dev/reports/m29-runes-seal-local-inventory/`
- `reports/m33-markdown-source-health/latest.json`
- `reports/m33-markdown-source-health/latest.md`
- future curated reports

Must exclude:

- ad hoc secret-bearing report files
- large raw logs
- database dumps
- vector embeddings

## Evidence Category 6: Markdown Source Health

Purpose:

- detect whether Markdown source-of-truth files are becoming giant prompt burdens
- provide Runes Shield Forge Readiness input

Allowed examples:

- file size summary
- estimated token pressure
- heading count
- chunk estimate
- largest heading span
- growth zone
- refinement level
- rune state
- recommended write behavior

Must exclude:

- replacing Markdown source-of-truth with PostgreSQL
- treating PostgreSQL as project identity
- automatic split without proposal / review / controlled apply

## Evidence Category 7: Tool and Runtime Inventory

Purpose:

- understand active local tool surface
- support debugging and regression analysis

Allowed examples:

- active `tools/runes/` script inventory
- smoke script inventory
- Python version
- selected tool version output
- executable bit summary
- local path summary

Must exclude:

- environment variable dumps
- `.env`
- shell history
- credentials
- tokens

## Evidence Category 8: Bundle Metadata

Purpose:

- make each bundle auditable and reproducible

Allowed examples:

- bundle id
- generated timestamp
- generator script version
- selected profile
- included evidence categories
- excluded categories
- warnings
- secret scan summary
- local output path

Must exclude:

- secrets
- raw sensitive payloads

## Output Location Policy

Default local output should be:

`bundles/ragnarok-observation/<timestamp>/`

Optional packaged export may be:

`~/Downloads/hermes-runes-ragnarok-observation-<timestamp>.tar.gz`

Bundle output should remain local-only unless the developer explicitly shares it.

The repository should ignore generated bundle outputs.

## Relationship to Ragnarok Policy

This inventory complements:

`wiki/_system/ragnarok_observation_bundle_policy.md`

The policy defines the incantation boundary and governance behavior.
This inventory defines what evidence may be collected after the workflow is validly invoked.

## Relationship to Runes Markdown Source Health

Runes Markdown Source Health is an evidence category within the Ragnarok Observation Bundle.

It is not the full bundle scope.

## Safety Rules

A Ragnarok Observation Bundle must be selective, summarized, and non-secret by default.

It must not include:

- `.env`
- API keys
- PostgreSQL passwords
- Telegram bot tokens
- raw full prompts
- raw full answers
- raw full memory context
- database dumps
- vector embeddings
- unrestricted raw logs
- shell history
- secret-bearing terminal output

## Summary

Ragnarok Observation Bundle is the developer diagnostic ritual for collecting selected echoes from the whole World Tree.

Markdown Source Health is only one branch.

The final bundle should support observe-analyze-fix-observe cycles without turning observation itself into a secret-leaking or heavy operational burden.
