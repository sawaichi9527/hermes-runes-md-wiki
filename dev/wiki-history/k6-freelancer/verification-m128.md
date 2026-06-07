# M128 P0 Compact Bootstrap Documentation Recap

Status: PASS / P0 COMPACT BOOTSTRAP DOCUMENTATION RECAP ADDED
Date: 2026-06-06

## Purpose

M128 provides a concise recap of the compact bootstrap documentation baseline after M126 and the M125 runtime constraint record after M127.

This recap is intended to make future continuation easier without rereading the full M119-M127 history.

This milestone adds documentation only.

It does not change runtime behavior.

## Current Baseline Summary

Completed and frozen compact bootstrap baseline:

```text
M119 P0 Policy-to-Prompt Compact Bootstrap: PASS
M120 P0 Compact Bootstrap Prompt Smoke: PASS
M121 P0 Compact Bootstrap Prompt Smoke Freeze: PASS
M122 Compact Bootstrap Prompt Regression Checklist: PASS
M123 Compact Bootstrap Regression Checklist Smoke: PASS
M124 Compact Bootstrap Regression Checklist Smoke Freeze: PASS
M126 Compact Bootstrap Documentation Freeze: PASS
M127 M125 Runtime Constraint Record: PASS
```

Pending external-agent validation:

```text
M125 First OpenClaw-Compatible Compact Bootstrap Trial: IMPLEMENTED / PENDING
```

## Current Active Compact Bootstrap Files

Primary entry point:

```text
wiki/hermes_runes_index.md
```

Primary compact prompt:

```text
wiki/_system/p0_compact_agent_bootstrap_prompt.md
Status: ACTIVE / P0 COMPACT AGENT BOOTSTRAP PROMPT
```

Primary compact policy:

```text
wiki/_system/p0_local_agent_invocation_policy.md
```

Regression checklist:

```text
wiki/_system/p0_compact_bootstrap_regression_checklist.md
Status: ACTIVE / P0 COMPACT BOOTSTRAP REGRESSION CHECKLIST
```

Additional canonical support documents:

```text
wiki/_system/runes_shield_contract.md
wiki/_system/runes_invocation_policy.md
wiki/_system/runes_agent_guidance.md
```

## How To Start A Future Local Governed Agent Session

Use:

```text
wiki/_system/p0_compact_agent_bootstrap_prompt.md
```

The agent should then bootstrap from:

```text
wiki/hermes_runes_index.md
wiki/_system/p0_local_agent_invocation_policy.md
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
no-write/no-import behavior during bootstrap smoke
```

## How To Edit Compact Bootstrap Files Safely

Before and after editing any of these files:

```text
wiki/hermes_runes_index.md
wiki/_system/p0_local_agent_invocation_policy.md
wiki/_system/p0_compact_agent_bootstrap_prompt.md
```

use:

```text
wiki/_system/p0_compact_bootstrap_regression_checklist.md
```

The checklist protects against regressions in:

```text
index discovery
read-only-first behavior
proposal-first behavior
two-stage approval
recall-before-freeze
issue-first remediation
no autonomous writer
no external/public Runes authority
no bot/wrapper direct mutation
no secrets
no-write/no-import smoke behavior
```

## Current M125 Constraint

M125 is not complete.

Current environment:

```text
Only Hermes-agent is available.
No OpenClaw runtime is available.
No other third-party local governed agent is available.
```

Therefore:

```text
Do not mark M125 PASS using Hermes-agent-only smoke.
Do not claim real OpenClaw runtime validation.
Do not present Hermes-agent output as third-party agent validation.
```

M125 may be resumed only when:

```text
OpenClaw runtime is available
or
another non-Hermes local governed agent is available and explicitly identified
```

## Current Status Interpretation

Correct interpretation:

```text
Compact bootstrap documentation baseline: PASS / frozen
Hermes-agent compact bootstrap smoke: PASS / frozen
Regression checklist: PASS / frozen
Third-party local governed agent validation: PENDING
```

Incorrect interpretation:

```text
OpenClaw validation is complete
M125 is PASS
Hermes-agent-only smoke counts as third-party validation
```

## Suggested Future Roadmap

Recommended continuation options:

```text
M129 External Agent Trial Preparation Checklist
M130 OpenClaw Runtime Availability Check
M131 First Real Non-Hermes Local Governed Agent Trial
```

If no external agent runtime is available, continue with bounded documentation and preparation tasks only.

Do not force M125 to PASS.

## Final Lock

```text
M128 P0 Compact Bootstrap Documentation Recap
PASS / P0 compact bootstrap documentation recap added
```
