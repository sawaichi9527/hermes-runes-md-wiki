# CB-20260607-M208 Workspace Slug Realignment

Status: PASS / ACTIVE DEFAULTS REALIGNED / HISTORICAL REFERENCES DEFERRED TO M209
Date: 2026-06-07
Milestone: M208
Stage: Open Beta Publication

## Purpose

Realign the active Open Beta workspace slug before public tester notification.

## Decision

```text
canonical_active_slug: freelancer
canonical_wiki_namespace: wiki/freelancer/
main_checkout: ~/workspace/hermes-runes-md-wiki
clean_trial_checkout: ~/workspace/trial/hermes-runes-md-wiki
legacy_engineering_namespace: wiki/k6-freelancer/
deprecated_trial_checkout: ~/workspace-trial/hermes-runes-md-wiki
```

## Updated Active Defaults

```text
config/hermes-memory.yaml: default_project set to freelancer
bin/hermes-memory-check: default workspace fallback set to freelancer
bin/hermes_memory_common.py: default project fallback set to freelancer
README.md: default workspace slug documented
docs/workspace-slug-policy.md: added
docs/open-beta-publication-checklist.md: updated
```

## Migration Policy

```text
Do not bulk-edit historical verification evidence just to rename old paths.
Keep wiki/k6-freelancer/ as legacy engineering history.
Use freelancer for active runtime defaults and public examples.
Classify remaining legacy references during M209 public download content audit.
```

## Tag Gate

```text
v0.1.0-beta.1 tag remains deferred until M209 public download audit passes.
```

## Reviewer Classification

```text
PASS
```

## Final Lock

```text
M208 Workspace Slug Realignment
PASS / active defaults realigned to freelancer / M209 audit required before tag
```
