# P0 Local Agent Invocation Policy

Status: ACTIVE / P0 LOCAL AGENT INVOCATION POLICY
Date: 2026-06-06

## Purpose

This document consolidates the repeated P0 practical trial-run behavior verified by M112 through M115.

It gives local governed agents a short, stable policy reference for invoking Hermes Runes MD Wiki through Runes Shield.

This policy applies to Hermes-agent and any future approved local governed agent, including OpenClaw or other third-party local agents, when operating against Hermes Runes MD Wiki.

## Core Boundary

The only allowed P0 access shape is:

```text
User -> approved local governed agent -> Runes Shield -> Hermes Runes MD Wiki
```

Bot or wrapper channels may only act as user ingress into the approved local governed agent:

```text
User -> approved bot/wrapper channel -> approved local governed agent -> Runes Shield -> Hermes Runes MD Wiki
```

Bots, wrappers, external clients, and public APIs are not direct Runes clients during P0.

## Required P0 Flow

For durable knowledge persistence, the agent must follow this order:

```text
1. Start read-only.
2. Recall existing trusted memory when useful.
3. Draft proposal content in the response first.
4. Wait for explicit operator approval before creating a proposal file.
5. Create only a draft/unreviewed proposal under the approved forge-inbox path.
6. Wait for a separate explicit operator approval before promotion.
7. Promote only the approved proposal into reviewed trusted memory.
8. Run import/index refresh if the promoted file is not recallable yet.
9. Run recall verification against the promoted reviewed file.
10. Freeze PASS only after recall verification succeeds.
```

## Agent Must Not

The agent must not:

```text
Write trusted memory directly.
Create proposal files before explicit operator approval.
Promote content before a separate explicit operator approval.
Treat draft proposal content as trusted memory.
Modify unrelated proposals or wiki files.
Silently persist user-provided material.
Skip recall verification before PASS freeze.
Use external/public API access as a Runes authority path.
Let bots or wrappers directly mutate Runes state.
Write secrets into wiki, git, proposals, or logs.
```

## Explicit Approval Rules

Two separate approvals are required:

```text
Approval 1: create a draft proposal file.
Approval 2: promote the reviewed proposal into trusted memory.
```

A single approval to draft is not approval to promote.

A discussion response is not persistence approval.

## Proposal File Rule

Before promotion, proposal files should remain in the workspace forge-inbox:

```text
wiki/<workspace>/forge-inbox/<proposal-slug>.md
```

The draft proposal should use:

```text
status: draft
trust_class: unreviewed
```

## Promoted Memory Rule

After explicit review/promotion approval, the promoted reviewed file should live under the workspace root or approved workspace path:

```text
wiki/<workspace>/<reviewed-memory-slug>.md
```

The promoted memory should use:

```text
status: approved
trust_class: reviewed
```

## Recall Verification Rule

A practical P0 trial-run is not PASS until recall verification succeeds against the promoted reviewed file.

Expected verification shape:

```bash
python3 tools/runes/recall_verify_m28_3.py \
  --project <workspace> \
  "<query>" \
  --expected-path wiki/<workspace>/<reviewed-memory-slug>.md \
  --required-marker "<required marker>"
```

Expected result:

```text
Status: PASS
Result count positive: True
Expected path found: True
Required marker found: True
Post-refresh recall verified: True
```

If recall initially fails because the file is not indexed yet, run a bounded import/index refresh, then rerun recall verification.

## Issue-first Remediation Rule

If a practical trial-run discovers a blocker:

```text
1. Do not mark the trial-run PASS.
2. Capture the issue in a verification or remediation milestone.
3. Remediate in a bounded follow-up step.
4. Rerun the relevant verification.
5. Freeze PASS only after the verification succeeds.
```

This rule was repeated and validated during M112/M112.1/M112.2 and M114/M115.

## Secrets Rule

Real secrets are prohibited from Markdown memory and git.

Do not persist:

```text
API keys
Database passwords
Telegram bot tokens
LM Studio / OpenAI-compatible API keys
Tavily keys
Private credentials
Private tokens
Raw secret-bearing logs
```

If content may contain secrets, the agent must ask the user for sanitized content before proposing persistence.

## PASS Freeze Rule

A P0 practical trial-run may be frozen as PASS only when:

```text
Proposal-first flow was followed.
Explicit operator approvals were separated.
Promoted reviewed memory exists.
Recall verification against the promoted file returns PASS.
No unrelated files were modified.
No secrets were written.
The result is documented in verification memory.
```

## Provenance

This policy consolidates the repeated practical evidence from:

```text
M112 First Practical P0 Trial-run Session: PASS
M113 First Practical P0 Trial-run Result Freeze: PASS
M114 Second Practical P0 Trial-run Session: PASS
M115 Second Practical P0 Trial-run Result Freeze: PASS
```

## Final Lock

```text
P0 Local Agent Invocation Policy
ACTIVE / repeatable P0 local-agent invocation behavior consolidated
```
