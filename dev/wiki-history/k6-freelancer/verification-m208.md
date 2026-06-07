# M208 Workspace Slug Realignment

Status: PASS / ACTIVE DEFAULTS REALIGNED / HISTORICAL REFERENCES DEFERRED TO M209
Date: 2026-06-07

## Evidence Record

```text
wiki/k6-freelancer/cb-sessions/cb-20260607-m208-workspace-slug-realignment.md
config/hermes-memory.yaml
bin/hermes-memory-check
bin/hermes_memory_common.py
README.md
docs/workspace-slug-policy.md
docs/open-beta-publication-checklist.md
```

## Scope

```text
Open Beta active workspace slug
public-facing default namespace
clean trial checkout path policy
no runtime feature development beyond default slug realignment
```

## Result

```text
PASS
```

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
config/hermes-memory.yaml default_project: freelancer
bin/hermes-memory-check default fallback: freelancer
bin/hermes_memory_common.py default fallback: freelancer
README default workspace slug section: added
docs/workspace-slug-policy.md: added
```

## Historical Reference Policy

```text
Historical verification records may keep legacy paths.
Active runtime defaults and public examples should prefer freelancer.
Remaining legacy references must be classified in M209 public download content audit.
```

## Next Step

```text
M209 Public Download Content Audit / Legacy Reference Triage
```

## Final Lock

```text
M208 Workspace Slug Realignment
PASS / active defaults realigned to freelancer / M209 audit required before tag
```
