# M127 M125 Runtime Constraint Record

Status: PASS / M125 RUNTIME CONSTRAINT RECORDED
Date: 2026-06-06

## Purpose

M127 records the runtime constraint that prevents M125 from being completed in the current validation environment.

M125 defines the first OpenClaw-compatible compact bootstrap trial, but the current environment does not include OpenClaw or another third-party local governed agent.

Therefore, M125 must remain implemented but pending.

M127 exists to prevent future status drift or accidental PASS marking based only on Hermes-agent validation.

## Current Constraint

Current validation environment:

```text
Only Hermes-agent is available.
No OpenClaw runtime is available.
No other third-party local governed agent is available.
```

Current M125 state:

```text
M125 First OpenClaw-Compatible Compact Bootstrap Trial
IMPLEMENTED / PENDING OPENCLAW-COMPATIBLE COMPACT BOOTSTRAP TRIAL
```

## Explicit Non-PASS Rule

M125 must not be marked PASS under the current environment.

Do not use:

```text
Hermes-agent-only smoke
Hermes-agent pretending to be OpenClaw
Hermes-agent output reclassified as third-party agent validation
```

as evidence for M125 PASS.

## Acceptable Future Evidence

M125 may be resumed when one of the following exists:

```text
OpenClaw runtime is available in the validation environment.
Another non-Hermes local governed agent is available and explicitly identified.
```

Acceptable classifications:

```text
classification: real OpenClaw runtime validation
classification: OpenClaw-compatible shape validation with a clearly identified non-Hermes local governed agent
```

Unacceptable classification:

```text
classification: Hermes-agent-only validation presented as OpenClaw-compatible third-party validation
```

## Required Future M125 Evidence

Future M125 evidence must include:

```text
agent/runtime name
whether the runtime is OpenClaw or another non-Hermes local governed agent
exact prompt used
files read
whether any write/import/index/apply/promote operation occurred
compact bootstrap path identified
boundary summary
required P0 flow summary
forbidden operations summary
regression checklist summary
PASS freeze rule summary
explicit statement that no Hermes-agent-private behavior was required
```

## Required Future Behavior

The future non-Hermes local governed agent must show it can follow:

```text
wiki/_system/p0_compact_agent_bootstrap_prompt.md
wiki/hermes_runes_index.md
wiki/_system/p0_local_agent_invocation_policy.md
wiki/_system/p0_compact_bootstrap_regression_checklist.md
```

and preserve:

```text
read-only first
proposal draft first
two-stage explicit approval
recall verification before PASS freeze
no autonomous trusted writer behavior
no external/public Runes authority path
no bot/wrapper direct mutation
no secrets in wiki/git/proposals/logs
no-write/no-import smoke behavior
```

## Current Completed Baseline Not Affected

This constraint does not weaken or reopen the completed compact bootstrap documentation baseline.

Already frozen:

```text
M119 P0 Policy-to-Prompt Compact Bootstrap: PASS
M120 P0 Compact Bootstrap Prompt Smoke: PASS
M121 P0 Compact Bootstrap Prompt Smoke Freeze: PASS
M122 Compact Bootstrap Prompt Regression Checklist: PASS
M123 Compact Bootstrap Regression Checklist Smoke: PASS
M124 Compact Bootstrap Regression Checklist Smoke Freeze: PASS
M126 Compact Bootstrap Documentation Freeze: PASS
```

Still pending:

```text
M125 First OpenClaw-Compatible Compact Bootstrap Trial: IMPLEMENTED / PENDING
```

## Practical Roadmap Rule

Until a non-Hermes local governed agent is available:

```text
Do not block compact bootstrap documentation progress on M125.
Do not claim third-party runtime validation.
Keep M125 pending and resume later.
Use M126 as the current documentation baseline freeze.
```

## Suggested Next Step

Recommended next milestone:

```text
M128 P0 Compact Bootstrap Documentation Recap
```

Suggested purpose:

```text
Produce a concise recap of the compact bootstrap documentation baseline, the active prompt/checklist files, and the remaining external-agent validation gap.
```

Alternative next milestone:

```text
M129 External Agent Trial Preparation Checklist
```

Suggested purpose:

```text
Prepare the minimal checklist needed before testing OpenClaw or another non-Hermes local governed agent.
```

## Final Lock

```text
M127 M125 Runtime Constraint Record
PASS / M125 runtime constraint recorded
```
