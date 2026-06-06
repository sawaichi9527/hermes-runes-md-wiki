# M119 P0 Policy-to-Prompt Compact Bootstrap

Status: PASS / P0 POLICY-TO-PROMPT COMPACT BOOTSTRAP ADDED
Date: 2026-06-06

## Purpose

M119 creates a compact reusable bootstrap prompt for future local governed agent sessions.

M118 froze the result that Hermes-agent can bootstrap from compact canonical `_system` policy documents instead of long M112-M115 verification history.

M119 converts that baseline into an explicit prompt artifact that can be reused with Hermes-agent, OpenClaw, or another approved local governed agent.

This milestone adds documentation only.

It does not change runtime behavior.

## Files Added / Updated

Added:

```text
wiki/_system/p0_compact_agent_bootstrap_prompt.md
```

Updated:

```text
wiki/hermes_runes_index.md
```

## Compact Bootstrap Prompt File

The new prompt file is:

```text
wiki/_system/p0_compact_agent_bootstrap_prompt.md
```

It provides a reusable prompt that instructs a local governed agent to bootstrap from:

```text
wiki/hermes_runes_index.md
wiki/_system/p0_local_agent_invocation_policy.md
```

The prompt explicitly forbids:

```text
file creation or modification without explicit approval
import/index/apply/promote without exact explicit approval
external/public APIs as Runes authority paths
secrets in wiki, git, proposals, or logs
reliance on long M112-M118 milestone history unless compact policy files are missing or insufficient
```

## Index Update

`wiki/hermes_runes_index.md` now includes:

```text
wiki/_system/p0_compact_agent_bootstrap_prompt.md
```

under canonical P0 / trial run files.

The index bootstrap summary now also asks compliant P0 agents to answer:

```text
What compact bootstrap prompt should be used for a new local governed agent session?
```

## Reusable Prompt Summary

The compact prompt tells the agent to:

```text
Confirm repository root and local governed boundary.
Start from wiki/hermes_runes_index.md.
Identify and read wiki/_system/p0_local_agent_invocation_policy.md.
Summarize required P0 durable-memory flow.
Summarize forbidden operations.
Confirm durable knowledge must start as proposal draft in the response first.
Confirm proposal file creation and promotion require separate explicit approvals.
Confirm PASS freeze requires recall verification against promoted reviewed file.
Cite relevant wiki paths.
```

## Governance Preservation

M119 preserves M112-M118 governance behavior:

```text
read-only first
proposal draft first
explicit approval before proposal file creation
separate approval before promotion
import/index refresh if needed
recall verification before PASS freeze
no autonomous writer
no external/public Runes API
no secrets
```

## Verification Commands

Recommended developer repo verification:

```bash
cd ~/workspace/hermes-runes-md-wiki

grep -n "Status:\|Final Lock\|Compact Bootstrap Prompt\|Required Bootstrap Documents\|Compact Bootstrap Prompt\|Expected Agent Response" \
  wiki/_system/p0_compact_agent_bootstrap_prompt.md

grep -n "p0_compact_agent_bootstrap_prompt\|compact bootstrap prompt" \
  wiki/hermes_runes_index.md
```

Recommended trial repo verification:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short

grep -n "Status:\|Final Lock\|Compact Bootstrap Prompt\|Required Bootstrap Documents\|Compact Bootstrap Prompt\|Expected Agent Response" \
  wiki/_system/p0_compact_agent_bootstrap_prompt.md

grep -n "p0_compact_agent_bootstrap_prompt\|compact bootstrap prompt" \
  wiki/hermes_runes_index.md
```

## Suggested Smoke Prompt

After syncing, a future smoke can ask Hermes-agent:

```text
Start a P0 local governed session using wiki/_system/p0_compact_agent_bootstrap_prompt.md.
Do not create or modify files.
Do not import/index/apply/promote anything.
Confirm the compact bootstrap path, required P0 flow, forbidden operations, and PASS freeze rule.
```

## PASS Criteria

M119 is PASS when:

```text
The compact bootstrap prompt file exists.
The index lists the compact bootstrap prompt as canonical P0 / trial run guidance.
The prompt references only the compact bootstrap documents by default.
The prompt preserves read-only/proposal-first/two-approval/recall-verified flow.
The prompt forbids autonomous writing, external/public Runes authority, direct bot/wrapper mutation, and secrets.
```

## Suggested Next Step

Recommended next milestone:

```text
M120 P0 Compact Bootstrap Prompt Smoke
```

Suggested purpose:

```text
Run Hermes-agent with the new compact bootstrap prompt and verify it can initialize the correct P0 local governed behavior from that prompt alone.
```

Alternative next milestone:

```text
M119.1 Compact Bootstrap Prompt Freeze
```

Suggested purpose:

```text
Freeze the prompt artifact after developer/trial repo sync verification.
```

## Final Lock

```text
M119 P0 Policy-to-Prompt Compact Bootstrap
PASS / P0 policy-to-prompt compact bootstrap added
```
