# P0 Compact Agent Bootstrap Prompt

Status: ACTIVE / P0 COMPACT AGENT BOOTSTRAP PROMPT
Date: 2026-06-06

## Purpose

This document provides a compact reusable bootstrap prompt for future local governed agent sessions.

It is intended for Hermes-agent, OpenClaw, or another approved local governed agent operating against Hermes Runes MD Wiki through Runes Shield.

The prompt intentionally references only the compact canonical P0 bootstrap documents instead of long M112-M118 milestone history.

## Required Bootstrap Documents

Use these documents as the minimal P0 bootstrap set:

```text
wiki/hermes_runes_index.md
wiki/_system/p0_local_agent_invocation_policy.md
```

The agent may consult other canonical `_system` files listed by the index when needed:

```text
wiki/_system/runes_shield_contract.md
wiki/_system/runes_invocation_policy.md
wiki/_system/runes_agent_guidance.md
```

The agent should not depend on long milestone verification history unless the compact policy files are missing or insufficient.

## Compact Bootstrap Prompt

Copy this prompt into a new local governed agent session:

```text
You are operating against Hermes Runes MD Wiki through Runes Shield.

Repository root:
~/workspace-trial/hermes-runes-md-wiki

Use local governed agent mode.
Start read-only.
Do not create or modify files unless I explicitly approve a specific persistence action.
Do not import/index/apply/promote anything unless I explicitly approve that exact step.
Do not use external/public APIs as Runes authority paths.
Do not write secrets into wiki, git, proposals, or logs.

Bootstrap from these canonical P0 files only:
1. wiki/hermes_runes_index.md
2. wiki/_system/p0_local_agent_invocation_policy.md

Task:
1. Confirm the active repository root and local governed boundary.
2. Start from wiki/hermes_runes_index.md.
3. Identify and read wiki/_system/p0_local_agent_invocation_policy.md.
4. Summarize the required P0 durable-memory flow.
5. Summarize forbidden operations.
6. Confirm that durable knowledge must start as a proposal draft in the response first.
7. Confirm that proposal file creation and promotion require separate explicit approvals.
8. Confirm that PASS freeze requires recall verification against the promoted reviewed file.
9. Cite relevant wiki paths.

Do not rely on long M112-M118 milestone history unless the compact canonical policy files are missing or insufficient.
```

## Expected Agent Response

The agent should confirm:

```text
Local governed boundary:
User -> approved local governed agent -> Runes Shield -> Hermes Runes MD Wiki
```

The agent should cite:

```text
wiki/hermes_runes_index.md
wiki/_system/p0_local_agent_invocation_policy.md
```

The agent should summarize:

```text
Start read-only.
Recall trusted memory when useful.
Draft proposal content in the response first.
Wait for explicit approval before proposal file creation.
Create only draft/unreviewed proposal under forge-inbox.
Wait for separate approval before promotion.
Promote only approved proposal into reviewed trusted memory.
Run import/index refresh if promoted content is not recallable.
Run recall verification against promoted reviewed file.
Freeze PASS only after recall verification succeeds.
```

The agent should forbid:

```text
Direct trusted memory writes.
Proposal file creation before explicit approval.
Promotion before separate approval.
Silent persistence.
Autonomous trusted writer behavior.
External/public Runes authority path.
Bot/wrapper direct Runes mutation.
Unrelated wiki/proposal mutation.
Secrets in wiki/git/proposals/logs.
Skipping recall verification before PASS freeze.
```

## Optional Operator Shortcut

For a specific workspace, the operator may append:

```text
Active workspace:
<workspace-name>
```

Example:

```text
Active workspace:
freelancer
```

If a workspace is not explicitly provided, the agent should ask for or infer the workspace conservatively from the task context and avoid persistence until confirmed.

## Persistence Reminder

Even after this bootstrap prompt, persistence still requires two separate approvals:

```text
Approval 1: create a draft proposal file.
Approval 2: promote the reviewed proposal into trusted memory.
```

The bootstrap prompt itself is not approval to write.

## Final Lock

```text
P0 Compact Agent Bootstrap Prompt
ACTIVE / compact P0 bootstrap prompt available
```
