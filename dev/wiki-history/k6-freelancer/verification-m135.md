# M135 Beta-prep Mainline Re-entry

Status: PASS / MAINLINE RE-ENTRY ADDED
Date: 2026-06-06

## Purpose

M135 returns the project to the beta-prep / Hermes-agent governed trial-run mainline after M134 locked the external runtime line into wait-state.

This milestone is documentation-only.

It does not change runtime behavior.

It does not run smoke tests.

It does not apply or promote memory.

## Added Artifact

M135 adds:

```text
docs/beta-prep-mainline-reentry.md
```

## Current Baseline

Current baseline:

```text
P0 governed memory baseline: available
Fresh-clone bootstrap baseline: ready through M90.3
External-agent preparation: ready / wait-state
M125 OpenClaw-compatible runtime validation: IMPLEMENTED / PENDING
Mainline: beta-prep / Hermes-agent governed trial-run
```

## Mainline Decision

Current decision:

```text
Return to beta-prep / Hermes-agent governed trial-run.
Do not continue external-agent preparation-only milestones.
Keep M125 pending until a real external runtime exists.
Keep the system personal-local and simple.
```

## Current Open Items

The next controllable beta-prep gaps are:

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

## Recommended Next Milestones

Recommended next milestone order:

```text
M136 Beta-prep Model Endpoint Configuration Check
M137 Trial Promotion Fixture Definition
M138 Hermes-agent Governed Trial-run Dry-run
M139 Trial Promotion Fixture Apply / Recall Verification
```

## Personal-use Boundary

M135 preserves the personal-local boundary.

It does not add:

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

It keeps the project:

```text
personal-local
Markdown-native
human-reviewed
simple
bounded
no enterprise policy engine
no extra burden on Hermes-agent
```

## Verification Scope

Static documentation verification scope:

```text
mainline re-entry artifact exists
external runtime line remains wait-state
M125 pending state is preserved
model endpoint configuration is identified as next controllable gap
trial promotion fixture is identified as next controllable gap
recommended M136-M139 order is documented
personal-local boundary is preserved
enterprise complexity is avoided
```

No runtime smoke is required because this milestone changes documentation only.

## Final Lock

```text
M135 Beta-prep Mainline Re-entry
PASS / mainline re-entry added / external runtime remains wait-state
```
