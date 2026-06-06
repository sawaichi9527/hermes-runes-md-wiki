# External Runtime Wait-state Lock

Status: ACTIVE / EXTERNAL RUNTIME WAIT-STATE LOCK
Date: 2026-06-06

## Purpose

This document locks the OpenClaw / non-Hermes external-agent validation line into wait-state.

M129 through M133 already prepared the future external-agent trial materials:

```text
M129 external-agent preparation checklist
M130 runtime availability check
M131 external-agent evidence template
M132 compact bootstrap stable baseline recap
M133 external-agent trial pack index
```

The preparation line is now sufficient for personal-use P0 needs.

Do not continue adding external-agent preparation documents until a real external runtime exists.

## Current Runtime State

Current runtime availability remains:

```text
Only Hermes-agent is available.
No OpenClaw runtime is available.
No other third-party local governed agent is available.
```

Therefore:

```text
M125 remains IMPLEMENTED / PENDING.
OpenClaw / non-Hermes runtime validation remains PENDING.
External-agent preparation is READY / WAIT-STATE.
```

## Wait-state Decision

Current decision:

```text
Do not resume M125 yet.
Do not add more external-agent preparation-only milestones.
Do not claim OpenClaw validation.
Do not present Hermes-agent-only output as third-party validation.
Return to beta-prep / Hermes-agent governed trial-run mainline.
```

## What Is Already Ready

The following artifacts are enough to resume later when a real external runtime exists:

```text
docs/compact-bootstrap-stable-baseline-recap.md
docs/external-agent-trial-pack-index.md
templates/external-agent-trial-evidence.md
wiki/k6-freelancer/verification-m125.md
wiki/k6-freelancer/verification-m129.md
wiki/k6-freelancer/verification-m130.md
wiki/k6-freelancer/verification-m131.md
wiki/k6-freelancer/verification-m132.md
wiki/k6-freelancer/verification-m133.md
```

## Resume Condition

Resume the external-agent validation line only when one of these is true:

```text
OpenClaw runtime is installed and usable in the validation environment.
A different non-Hermes local governed agent runtime is installed and explicitly identified.
```

The runtime must be able to:

```text
read local Markdown from ~/workspace-trial/hermes-runes-md-wiki
operate read-only
cite files it read
avoid file creation/modification
avoid import/index/apply/promote operations
avoid database mutation
avoid Hermes-agent-specific private behavior
leave the working tree clean
```

## Resume Procedure

When the resume condition is met:

```text
1. Start from docs/external-agent-trial-pack-index.md.
2. Use the M125 prompt from wiki/k6-freelancer/verification-m125.md.
3. Record evidence with templates/external-agent-trial-evidence.md.
4. Keep the trial checkout clean before and after the trial.
5. Classify the runtime honestly.
6. Decide PASS / FAIL / BLOCKED only after complete evidence exists.
```

## Mainline Direction While Waiting

While external-agent validation is in wait-state, continue with the mainline:

```text
beta-prep
Hermes-agent governed trial-run
fresh-user/trial workspace verification
model endpoint configuration when needed
trial promotion fixture only through governed human-reviewed flow
```

Do not expand the external-agent line into:

```text
more preparation-only milestone documents
orchestration daemon
websocket bridge
centralized policy service
enterprise telemetry system
automatic proposal apply
autonomous promotion
direct wiki mutation by runtime wrappers
```

## Personal-use Boundary

The wait-state lock preserves the intended project scope:

```text
personal-local
Markdown-native
simple
human-reviewed
bounded
no enterprise policy engine
no extra burden on Hermes-agent
```

## Current Final State

```text
External runtime line: WAIT-STATE
External-agent preparation: READY
M125: IMPLEMENTED / PENDING
OpenClaw / non-Hermes runtime validation: PENDING
Mainline: return to beta-prep / Hermes-agent governed trial-run
```

## Final Lock

```text
External Runtime Wait-state Lock
ACTIVE / external-agent preparation complete / M125 remains pending
```
