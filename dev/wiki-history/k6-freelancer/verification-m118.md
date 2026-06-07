# M118 P0 Local Agent Policy Smoke Freeze

Status: PASS / P0 LOCAL AGENT POLICY SMOKE BASELINE FROZEN
Date: 2026-06-06

## Purpose

M118 freezes the M117 P0 local agent policy smoke result.

M116 consolidated the repeated M112-M115 practical P0 behavior into a compact `_system` policy:

```text
wiki/_system/p0_local_agent_invocation_policy.md
```

M117 verified that Hermes-agent can bootstrap from:

```text
wiki/hermes_runes_index.md
wiki/_system/p0_local_agent_invocation_policy.md
```

without relying on long M112-M115 verification history.

M118 freezes that smoke result as the current baseline.

This milestone is a result freeze/status lock only.

It does not change runtime behavior.

## Frozen Baseline Head

Frozen baseline head:

```text
d576a21 Record M117 P0 local agent policy smoke pass
```

M116-M117 commit chain included:

```text
400d45c Add P0 local agent invocation policy
28d36d3 Add P0 local agent invocation policy to index
c467415 Add M116 local agent invocation policy consolidation
cce4d4c Add M117 P0 local agent policy recall smoke
d576a21 Record M117 P0 local agent policy smoke pass
```

## Frozen Bootstrap Path

The frozen compact bootstrap path is:

```text
wiki/hermes_runes_index.md
wiki/_system/p0_local_agent_invocation_policy.md
```

The local governed agent should start from the index, discover the policy, and summarize the P0 flow from the policy.

## Frozen Smoke Path

Observed and frozen smoke path:

```text
Path A: direct canonical index + file read
```

The Hermes-agent smoke:

```text
read wiki/hermes_runes_index.md
identified wiki/_system/p0_local_agent_invocation_policy.md
read wiki/_system/p0_local_agent_invocation_policy.md
summarized the policy directly
```

It did not rely on full M112-M115 verification history.

## Frozen Required P0 Flow

The smoke verified that Hermes-agent can summarize the required P0 durable-memory flow:

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

## Frozen PASS Freeze Rule

The smoke verified that Hermes-agent can summarize the PASS freeze rule:

```text
Proposal-first flow is followed.
Operator approvals are separated.
Promoted reviewed memory exists.
Recall verification against the promoted file returns PASS.
No unrelated files are modified.
No secrets are written.
The result is documented in verification memory.
```

The smoke also verified that if recall initially fails because the file is not indexed, bounded import/index refresh should be run before rerunning recall verification.

## Frozen Forbidden Operations

The smoke verified that Hermes-agent can list forbidden operations:

```text
No direct trusted memory write.
No proposal file before explicit approval.
No promotion before separate approval.
No treating draft proposal as trusted memory.
No unrelated wiki/proposal mutation.
No silent persistence.
No skipping recall verification before PASS freeze.
No external/public API as Runes authority path.
No bot/wrapper direct Runes mutation.
No secrets in wiki/git/proposals/logs.
```

## Frozen No-write Behavior

Observed no-write smoke behavior:

```text
No files created: PASS
No files modified: PASS
No import/index/apply/promote operation performed: PASS
No proposal created: PASS
No trusted memory mutated: PASS
```

## Frozen M117 Result

Frozen M117 result:

```text
Developer CLI grep: PASS
Trial repo sync: PASS
Trial CLI grep: PASS
Local agent policy identification: PASS
Local agent required-flow summary: PASS
Local agent forbidden-operation summary: PASS
No-write smoke behavior: PASS
Overall: PASS
```

## Baseline Meaning

The frozen M118 baseline means:

```text
A local governed agent can now bootstrap practical P0 Runes behavior from compact canonical _system policy documents instead of reading long M112-M115 milestone history.
```

The required minimum bootstrap set is:

```text
wiki/hermes_runes_index.md
wiki/_system/runes_shield_contract.md
wiki/_system/runes_invocation_policy.md
wiki/_system/runes_agent_guidance.md
wiki/_system/p0_local_agent_invocation_policy.md
```

## Still Not Allowed

M118 does not allow:

```text
Autonomous trusted writer mode.
Silent persistence.
Automatic proposal promotion.
Direct wiki mutation by bot/wrapper/external client.
Public/external Runes API access.
Secrets in wiki/git/logs.
Skipping recall verification before PASS freeze.
```

## Future Sessions Should Preserve

Future local governed agent sessions should preserve:

```text
Start from wiki/hermes_runes_index.md.
Use wiki/_system/p0_local_agent_invocation_policy.md as the compact P0 flow checklist.
Use read-only mode first.
Draft proposal content in response first.
Require explicit approval before proposal file creation.
Require separate approval before promotion.
Verify promoted reviewed memory through recall before PASS freeze.
Capture and remediate blockers before freezing PASS.
Avoid relying on long verification history unless policy files are missing or insufficient.
```

## Suggested Next Step

Recommended next milestone:

```text
M119 P0 Policy-to-Prompt Compact Bootstrap
```

Suggested purpose:

```text
Create a compact prompt block for future local governed agent sessions that references only hermes_runes_index.md and p0_local_agent_invocation_policy.md.
```

Alternative next milestone:

```text
M120 P0 Agent Bootstrap Regression Smoke
```

Suggested purpose:

```text
Run a small regression smoke confirming that the compact bootstrap prompt still leads the local governed agent to the correct policy and forbidden-operation summary.
```

## Final Lock

```text
M118 P0 Local Agent Policy Smoke Freeze
PASS / P0 local agent policy smoke baseline frozen
```
