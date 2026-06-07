# M89 Fresh-user Trial Smoke Hardening

Status: PASS / trial smoke hardened / verified
Date: 2026-06-05

## Purpose

M89 records the fresh-user trial-run smoke hardening pass performed after the isolated trial clone and trial database became operational.

The goal was not to broaden the system into enterprise orchestration. The goal was to make the existing personal-local smoke chain correctly respect the realistic trial workspace boundary:

```text
Developer checkout: ~/workspace/hermes-runes-md-wiki
Trial checkout:     ~/workspace-trial/hermes-runes-md-wiki
Trial DB:           hermes_memory_trial
Trial workspace:    wiki/freelancer
Owner layer:        wiki/owner-runes
Root indexes:       wiki/*.md
```

## Scope

This verification lock covers the trial-run smoke issues discovered after M88:

```text
TB-20260605-010 through TB-20260605-014
```

It also confirms that the smoke chain can now distinguish:

```text
legacy engineering workspace: wiki/k6-freelancer
fresh-user trial workspace:   wiki/freelancer
owner preference layer:       wiki/owner-runes
root-level wiki indexes:      wiki/*.md
```

## Implemented Fixes

### TB-20260605-010 Scoped import missed root wiki and owner-runes

Status: FIXED / pulled verified / scoped import verified

Fix commits:

```text
0d6a316 Include root wiki and owner-runes in scoped import
1371882 Add owner-runes seed memory layer
```

Verified import scope:

```text
project=default       # wiki/*.md root-level index files
project=_system       # wiki/_system/**
project=freelancer    # wiki/freelancer/**
project=owner-runes   # wiki/owner-runes/**
```

Excluded from trial DB as expected:

```text
project=k6-freelancer
project=sample-project
```

Verified result:

```text
summary: schema=public import_scope=freelancer imported_or_changed=58 updated=0 skipped=0 chunks_written=520
PASS: Markdown incremental import completed
```

### TB-20260605-011 M5.2 used legacy k6-freelancer cases

Status: FIXED / pulled verified / workspace smoke verified

Fix commit:

```text
d490e6f Make M5.2 smoke workspace aware
```

Verified workspace profile:

```text
profile: workspace-freelancer
status: PASS
```

Verified cases:

```text
freelancer_baseline_context_recall
owner_runes_context_recall
root_index_context_recall
```

### TB-20260605-012 M10 required model env during fresh trial smoke

Status: FIXED / pulled verified / skip verified

Fix commit:

```text
2ed6945 Make M10 observation smoke trial aware
```

Expected behavior without configured OpenAI-compatible model runtime:

```text
profile: workspace-freelancer
status: SKIP
reason: missing_model_env
missing: OPENAI_BASE_URL, OPENAI_MODEL
```

This is intentional. Fresh-user trial smoke should not fail before a model endpoint is configured.

### TB-20260605-013 M11.6 used legacy sample-project cases

Status: FIXED / pulled verified / workspace smoke verified

Fix commit:

```text
2bfeb51 Make M11.6 sample smoke workspace aware
```

Verified workspace profile:

```text
profile: workspace-freelancer
status: PASS
```

Verified cases:

```text
freelancer_workspace_seed
owner_runes_seed
```

### TB-20260605-014 M20.4 promotion smoke required legacy promotion fixture

Status: FIXED / pulled verified / trial smoke verified

Fix commit:

```text
40a25df Skip M20.4 promotion smoke without trial fixture
```

Expected behavior in fresh trial workspace before an approved promotion fixture exists:

```text
profile: workspace-freelancer
status: SKIP
reason: promotion_governance_fixture_not_available_in_trial_workspace
failed: 0
```

This preserves the semantics of M20.4. Promotion governance must be tested with an approved forge/proposal fixture, not replaced by a generic recall check.

## Final Smoke Status

Latest trial smoke chain:

```text
Core FTS                         PASS
M5.2 workspace evaluation         PASS
M10 observation log               SKIP / expected: missing model env
M11 observation summary           PASS
M11.6 workspace/sample smoke      PASS
M20.4 promotion governance        SKIP / expected: no trial fixture
```

## Boundary Confirmation

The trial-run smoke hardening did not introduce:

```text
no orchestration daemon
no websocket bridge
no enterprise telemetry system
no automatic proposal apply
no direct wiki mutation by agent
no runtime authority escalation
no PostgreSQL Docker lifecycle ownership by the repo
```

The implementation remains:

```text
personal-local
bounded
Markdown-native
human-reviewed
trial-run oriented
```

## Remaining Open Trial Gap

Dependency/bootstrap setup remains open:

```text
TB-20260605-001 Fresh clone lacks dependency bootstrap
```

A later milestone should provide a simple, bounded bootstrap path without enterprise installers or hidden background setup.

## Final Lock

```text
M89 Fresh-user Trial Smoke Hardening
PASS / trial smoke hardened / verified
```
