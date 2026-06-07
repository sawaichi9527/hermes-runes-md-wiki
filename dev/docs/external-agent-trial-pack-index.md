# External Agent Trial Pack Index

Status: ACTIVE / EXTERNAL AGENT TRIAL PACK INDEX
Date: 2026-06-06

## Purpose

This document is the compact entry index for future OpenClaw / non-Hermes local governed agent trials.

It gathers the minimal documents needed to understand, run, and record a future external-agent trial without rereading the full milestone history.

It is an index only.

It does not grant runtime authority.

It does not change implementation behavior.

It does not resume M125.

## Current State

Current external-agent state:

```text
Only Hermes-agent is available.
No OpenClaw runtime is available.
No other third-party local governed agent is available.
```

Therefore:

```text
M125 remains IMPLEMENTED / PENDING.
Do not claim real OpenClaw validation.
Do not present Hermes-agent-only output as third-party validation.
```

## Trial Pack Reading Order

Use this order for future external-agent trial preparation:

```text
1. docs/compact-bootstrap-stable-baseline-recap.md
2. wiki/k6-freelancer/verification-m125.md
3. wiki/k6-freelancer/verification-m129.md
4. wiki/k6-freelancer/verification-m130.md
5. templates/external-agent-trial-evidence.md
```

Optional supporting references:

```text
wiki/_system/p0_compact_agent_bootstrap_prompt.md
wiki/hermes_runes_index.md
wiki/_system/p0_local_agent_invocation_policy.md
wiki/_system/p0_compact_bootstrap_regression_checklist.md
wiki/_system/runes_shield_contract.md
wiki/_system/runes_invocation_policy.md
wiki/_system/runes_agent_guidance.md
```

## Document Roles

### Stable baseline recap

```text
docs/compact-bootstrap-stable-baseline-recap.md
```

Use this first to understand the current M119-M132 baseline and why M125 remains pending.

### M125 trial prompt / baseline

```text
wiki/k6-freelancer/verification-m125.md
```

Use this for the external-agent trial prompt and expected answer shape.

### M129 preparation checklist

```text
wiki/k6-freelancer/verification-m129.md
```

Use this before attempting a future non-Hermes runtime trial.

### M130 runtime availability rule

```text
wiki/k6-freelancer/verification-m130.md
```

Use this to avoid falsely resuming M125 when only Hermes-agent is available.

### M131 evidence template

```text
templates/external-agent-trial-evidence.md
```

Use this to record the future trial evidence.

## Minimal Future Trial Flow

When a real OpenClaw or clearly identified non-Hermes local governed agent runtime exists:

```text
1. Pull the trial checkout.
2. Confirm git status is clean.
3. Record runtime identity and classification.
4. Run the M125 prompt with the external runtime in read-only mode.
5. Record files read and raw output.
6. Check forbidden operations.
7. Confirm git status remains clean.
8. Complete the M131 evidence template.
9. Only then assess PASS / FAIL / BLOCKED.
```

## Required Trial Checkout

Use the trial checkout:

```text
~/workspace-trial/hermes-runes-md-wiki
```

Do not use developer checkout as the actual external-agent trial workspace unless explicitly recorded as a separate developer-only precheck.

## Required Pre-check

Before the external agent starts:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short
git log --oneline -5
```

Expected working tree state:

```text
no output from git status --short
```

## Required Post-check

After the external agent trial:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git status --short
```

Expected result:

```text
no output
```

## Runtime Classification

Valid future classifications:

```text
real OpenClaw runtime validation
OpenClaw-compatible shape validation with a clearly identified non-Hermes local governed agent
```

Invalid classification:

```text
Hermes-agent-only validation presented as OpenClaw-compatible third-party validation
```

## Forbidden Operations

The future external-agent trial is read-only.

Forbidden operations:

```text
file write
wiki mutation
proposal mutation
import/index
database mutation
apply/promote
runtime authority escalation
```

If any forbidden operation occurs, the trial cannot be marked PASS.

## PASS Gate Reminder

Do not mark M125 PASS unless the future evidence includes:

```text
identified non-Hermes runtime
honest runtime classification
exact prompt used
files read / cited
raw output
pre-trial clean git status
post-trial clean git status
forbidden operation check
operator assessment
no Hermes-agent-specific private dependency
```

## Personal-use Boundary

This trial pack remains personal-local and intentionally simple.

It does not introduce:

```text
orchestration daemon
websocket bridge
centralized policy service
enterprise telemetry system
automatic proposal apply
autonomous promotion
direct wiki mutation by runtime wrappers
```

## Current Final State

Until a real external runtime exists:

```text
External Agent Trial Pack Index: ACTIVE
External-agent evidence template: READY
M125: IMPLEMENTED / PENDING
OpenClaw / non-Hermes runtime validation: PENDING
```

## Final Lock

```text
External Agent Trial Pack Index
ACTIVE / external-agent trial entrypoint ready / M125 remains pending
```
