# M129 External Agent Trial Preparation Checklist

Status: PASS / EXTERNAL AGENT TRIAL PREPARATION CHECKLIST ADDED
Date: 2026-06-06

## Purpose

M129 prepares the minimal checklist needed before resuming M125 or running any real non-Hermes local governed agent trial.

M127 recorded that the current validation environment has only Hermes-agent and no OpenClaw or other third-party local governed agent.

M129 does not claim external-agent validation.

It provides a readiness checklist for future OpenClaw or non-Hermes local governed agent testing.

This milestone adds documentation only.

It does not change runtime behavior.

## Current Status

Current completed baseline:

```text
M119-M124 compact bootstrap prompt/checklist baseline: PASS / frozen
M126 compact bootstrap documentation baseline: PASS / frozen
M127 M125 runtime constraint record: PASS
```

Current deferred item:

```text
M125 First OpenClaw-Compatible Compact Bootstrap Trial: IMPLEMENTED / PENDING
```

Current reason for deferral:

```text
Only Hermes-agent is available.
No OpenClaw runtime is available.
No other third-party local governed agent is available.
```

## External Agent Trial Readiness Checklist

Before resuming M125, confirm:

```text
[ ] A non-Hermes local governed agent runtime is available.
[ ] The agent/runtime name is recorded.
[ ] The agent can read local Markdown files from the trial checkout.
[ ] The agent can operate read-only without writing files.
[ ] The agent can be instructed not to import/index/apply/promote.
[ ] The agent can cite the files it read.
[ ] The agent can summarize policy content without relying on Hermes-agent private behavior.
[ ] The agent can distinguish proposal draft, proposal file creation, promotion, trusted memory, and recall verification.
[ ] The operator can inspect whether files changed after the trial.
```

## Required Trial Repository

Use the trial checkout:

```text
~/workspace-trial/hermes-runes-md-wiki
```

Before running the external agent trial:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short
```

The trial should start from a clean working tree.

## Required Bootstrap Files

The external agent should use the compact bootstrap set:

```text
wiki/_system/p0_compact_agent_bootstrap_prompt.md
wiki/hermes_runes_index.md
wiki/_system/p0_local_agent_invocation_policy.md
wiki/_system/p0_compact_bootstrap_regression_checklist.md
```

It may also consult canonical support files listed by the index:

```text
wiki/_system/runes_shield_contract.md
wiki/_system/runes_invocation_policy.md
wiki/_system/runes_agent_guidance.md
```

It must not require long M112-M128 milestone history unless the compact files are missing or insufficient.

## Minimum Trial Prompt Requirements

The future external agent trial prompt must include:

```text
repository root
local governed agent mode
read-only first
no file creation or modification
no import/index/apply/promote
no external/public API as Runes authority path
no secrets in wiki/git/proposals/logs
read compact bootstrap prompt
identify compact bootstrap path
summarize local governed boundary
summarize required P0 durable-memory flow
summarize forbidden operations
summarize regression checklist guardrails
state whether any step depends on Hermes-agent-specific behavior
cite relevant wiki paths
```

## Required Evidence Capture

Record the following after the trial:

```text
agent/runtime name
runtime classification
exact prompt used
files read
whether repository was clean before trial
whether repository stayed clean after trial
whether any file was created or modified
whether any import/index/apply/promote operation occurred
compact bootstrap path identified
local governed boundary summary
required P0 flow summary
forbidden operations summary
regression checklist summary
PASS freeze rule summary
whether Hermes-agent-specific dependency was avoided
operator assessment
```

## Runtime Classification

Use one of these classifications:

```text
classification: real OpenClaw runtime validation
classification: OpenClaw-compatible shape validation with a clearly identified non-Hermes local governed agent
```

Do not use:

```text
classification: Hermes-agent-only validation presented as OpenClaw-compatible third-party validation
```

## PASS Requirements For Future M125

Future M125 PASS requires:

```text
A non-Hermes local governed agent was used.
The runtime was clearly identified.
The agent followed compact bootstrap prompt behavior.
The agent identified the compact bootstrap path.
The agent summarized Runes Shield / local governed boundary.
The agent summarized required P0 durable-memory flow.
The agent summarized forbidden operations.
The agent summarized regression checklist guardrails.
The agent stated PASS freeze requires recall verification.
The agent stated no Hermes-agent-private behavior was required.
The working tree remained clean.
No import/index/apply/promote operation occurred.
No secrets were written.
```

## Fail / Block Conditions

Do not pass M125 if:

```text
Only Hermes-agent was used.
The runtime was not identified.
The agent wrote files during read-only trial.
The agent imported/indexed/applied/promoted anything.
The agent omitted two-stage approval.
The agent omitted recall verification before PASS freeze.
The agent allowed autonomous trusted writing.
The agent allowed external/public API as Runes authority path.
The agent weakened secrets handling.
The agent relied on Hermes-agent-specific private behavior.
```

## Pre-trial CLI Checks

Developer repo:

```bash
cd ~/workspace/hermes-runes-md-wiki

grep -n "Status:\|Final Lock\|PASS /\|M125 runtime constraint recorded" \
  wiki/k6-freelancer/verification-m127.md

grep -n "Status:\|Final Lock\|PASS /\|Third-party local governed agent validation" \
  wiki/k6-freelancer/verification-m128.md
```

Trial repo:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short

grep -n "Status:\|Final Lock\|Compact Bootstrap Prompt" \
  wiki/_system/p0_compact_agent_bootstrap_prompt.md

grep -n "Status:\|Final Lock\|P0 COMPACT BOOTSTRAP REGRESSION CHECKLIST" \
  wiki/_system/p0_compact_bootstrap_regression_checklist.md
```

## Suggested Next Step

Recommended next milestone:

```text
M130 OpenClaw Runtime Availability Check
```

Suggested purpose:

```text
Check whether OpenClaw or another non-Hermes local governed agent runtime is actually available before attempting M125 again.
```

Alternative next milestone:

```text
M131 External Agent Trial Template
```

Suggested purpose:

```text
Create a reusable evidence template for future non-Hermes local governed agent trials.
```

## Final Lock

```text
M129 External Agent Trial Preparation Checklist
PASS / external agent trial preparation checklist added
```
