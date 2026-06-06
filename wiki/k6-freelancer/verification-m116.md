# M116 Local Agent Invocation Policy Consolidation

Status: PASS / LOCAL AGENT INVOCATION POLICY CONSOLIDATED
Date: 2026-06-06

## Purpose

M116 consolidates the repeated P0 practical local-agent invocation behavior into a concise `_system` policy reference.

M112 through M115 proved that the P0 governed memory flow is repeatable:

```text
read-only first
proposal draft first
explicit approval before proposal file creation
separate approval before promotion
import/index refresh when needed
recall verification before PASS freeze
no autonomous writer
no external/public Runes API
no secrets
```

M116 promotes that behavior into canonical system guidance so future Hermes-agent, OpenClaw, or other approved local governed agents do not need to infer behavior from long verification history.

## Files Added / Updated

Added:

```text
wiki/_system/p0_local_agent_invocation_policy.md
```

Updated:

```text
wiki/hermes_runes_index.md
```

## New Canonical Policy

The new policy document is:

```text
wiki/_system/p0_local_agent_invocation_policy.md
```

It defines:

```text
Core local governed agent boundary
Required P0 persistence flow
Forbidden operations
Explicit approval rules
Proposal file rule
Promoted memory rule
Recall verification rule
Issue-first remediation rule
Secrets rule
PASS freeze rule
M112-M115 provenance
```

## Index Update

`wiki/hermes_runes_index.md` now includes:

```text
wiki/_system/p0_local_agent_invocation_policy.md
```

under canonical P0 / trial run files.

The index bootstrap summary now also asks compliant P0 agents to answer:

```text
What is the repeated practical P0 local-agent invocation flow?
When is a practical P0 trial-run allowed to be frozen as PASS?
```

## Policy Summary

The consolidated policy freezes this access shape:

```text
User -> approved local governed agent -> Runes Shield -> Hermes Runes MD Wiki
```

and this indirect bot/wrapper shape:

```text
User -> approved bot/wrapper channel -> approved local governed agent -> Runes Shield -> Hermes Runes MD Wiki
```

Bots, wrappers, external clients, and public APIs are not direct Runes clients during P0.

## Required P0 Flow

The required durable-memory flow is:

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

## Provenance

M116 is based on repeated evidence from:

```text
M112 First Practical P0 Trial-run Session: PASS
M113 First Practical P0 Trial-run Result Freeze: PASS
M114 Second Practical P0 Trial-run Session: PASS
M115 Second Practical P0 Trial-run Result Freeze: PASS
```

## Governance Result

Governance consolidation result:

```text
Repeated P0 local-agent invocation behavior captured: PASS
System policy created: PASS
Canonical index updated: PASS
Agent-agnostic local boundary preserved: PASS
No autonomous writer behavior introduced: PASS
No external/public Runes API introduced: PASS
No secrets written: PASS
```

## Verification Commands

Recommended verification:

```bash
cd ~/workspace/hermes-runes-md-wiki

grep -n "Status:\|Final Lock\|P0 Local Agent Invocation Policy\|Required P0 Flow\|PASS freeze" \
  wiki/_system/p0_local_agent_invocation_policy.md

grep -n "p0_local_agent_invocation_policy\|repeated practical P0" \
  wiki/hermes_runes_index.md
```

Trial repo verification:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short

grep -n "Status:\|Final Lock\|P0 Local Agent Invocation Policy\|Required P0 Flow\|PASS freeze" \
  wiki/_system/p0_local_agent_invocation_policy.md

grep -n "p0_local_agent_invocation_policy\|repeated practical P0" \
  wiki/hermes_runes_index.md
```

## Suggested Next Step

Recommended next milestone:

```text
M117 P0 Local Agent Policy Recall Smoke
```

Suggested purpose:

```text
Verify that the new _system P0 local agent invocation policy can be recalled or directly bootstrapped by the local governed agent and that it correctly summarizes the M112-M115 flow.
```

Alternative next milestone:

```text
M114.2 / M115.1 Repeatability Regression Smoke
```

Suggested purpose:

```text
Create a small regression checklist or smoke command set that verifies M112 and M114 markers remain recallable.
```

## Final Lock

```text
M116 Local Agent Invocation Policy Consolidation
PASS / local agent invocation policy consolidated
```
