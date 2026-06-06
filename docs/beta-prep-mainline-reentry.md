# Beta-prep Mainline Re-entry

Status: ACTIVE / BETA-PREP MAINLINE RE-ENTRY
Date: 2026-06-06

## Purpose

This document returns the project to the beta-prep / Hermes-agent governed trial-run mainline after M134 locked the external runtime line into wait-state.

This is a planning and status document only.

It does not change runtime behavior.

It does not run smoke tests.

It does not apply or promote memory.

## Current Baseline

Current state:

```text
P0 governed memory baseline: available
Fresh-clone bootstrap baseline: ready through M90.3
External-agent preparation: ready / wait-state
M125 OpenClaw-compatible runtime validation: IMPLEMENTED / PENDING
Mainline: beta-prep / Hermes-agent governed trial-run
```

The external runtime line should not receive more preparation-only milestones until a real external runtime exists.

## Mainline Goal

The beta-prep mainline goal is to validate Hermes-agent governed use of the memory system in a realistic personal-local trial-run.

Focus areas:

```text
trial workspace correctness
model endpoint configuration
Hermes-agent governed read-only recall behavior
trial promotion fixture through human-reviewed flow
post-promotion recall verification
clear PASS / SKIP / BLOCKED evidence
```

## Explicit Non-goals

Do not add:

```text
enterprise orchestration
websocket bridge
centralized policy service
enterprise telemetry system
automatic proposal apply
autonomous promotion
direct wiki mutation by runtime wrappers
more external-agent preparation-only documents
```

## Current Open Items

The beta-prep line has two known controllable gaps:

```text
model endpoint configuration
trial promotion fixture
```

Supporting items:

```text
fresh-user / trial workspace verification
Hermes-agent governed trial-run path
expected SKIP handling for model-dependent smoke when model endpoint is absent
expected SKIP handling for promotion governance when no approved trial fixture exists
```

## Recommended Next Milestone Order

Recommended next milestones:

```text
M136 Beta-prep Model Endpoint Configuration Check
M137 Trial Promotion Fixture Definition
M138 Hermes-agent Governed Trial-run Dry-run
M139 Trial Promotion Fixture Apply / Recall Verification
```

These should remain personal-local and bounded.

## M136 Scope Hint

M136 should check model endpoint configuration without forcing a model dependency into every smoke path.

Expected behavior:

```text
if model endpoint is configured: run model-dependent smoke
if model endpoint is not configured: record SKIP / expected
no sensitive values copied into wiki/git/logs
no runtime mutation
```

## M137 Scope Hint

M137 should define the minimal approved trial promotion fixture.

The fixture must be:

```text
small
non-sensitive
human-reviewed
workspace-scoped
safe for trial recall verification
created through governed proposal flow
```

Do not create a broad ingestion fixture.

## M138 Scope Hint

M138 should validate Hermes-agent governed trial-run behavior in dry-run mode.

Expected behavior:

```text
read-only first
proposal draft first
explicit approval boundary preserved
no direct trusted memory write
no import/index/apply/promote unless explicitly part of the controlled test
```

## M139 Scope Hint

M139 should validate the first controlled trial promotion fixture only after M137 and M138 are ready.

Expected behavior:

```text
human-reviewed fixture
controlled apply/promote path
import/index refresh only when required
recall verification before PASS freeze
clear issue record if verification fails
```

## Evidence Rules

Each future beta-prep milestone should record:

```text
scope
preconditions
commands or manual steps
observed result
PASS / SKIP / BLOCKED classification
whether any write/import/index/apply/promote occurred
human approval state when relevant
```

## Personal-use Boundary

The mainline remains:

```text
personal-local
Markdown-native
human-reviewed
simple
bounded
no enterprise policy engine
no extra burden on Hermes-agent
```

## Current Final State

```text
External runtime line: WAIT-STATE
External-agent preparation: READY
M125: IMPLEMENTED / PENDING
Mainline: beta-prep / Hermes-agent governed trial-run
Next focus: model endpoint configuration and trial promotion fixture
```

## Final Lock

```text
Beta-prep Mainline Re-entry
ACTIVE / mainline restored / external runtime remains wait-state
```
