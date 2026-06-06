# M108.2 Local-only Runes Shield Access Boundary Lock

Status: PASS / LOCAL-ONLY RUNES SHIELD ACCESS BOUNDARY LOCKED
Date: 2026-06-06

## Purpose

M108.2 formally locks the local-only access boundary for Hermes Runes MD Wiki and Runes Shield.

This milestone corrects the M108 OpenAI-compatible adapter direction by clarifying that Hermes Runes MD Wiki is designed for local Hermes-agent governed access, not external or public API access.

This is a governance/boundary lock only.

It does not change runtime behavior.

## Operator Clarification

The operator clarified:

```text
Runes can only be invoked by a local agent through Runes Shield.
The user must explicitly request the agent to connect to Runes.
At most, a bot connected through the agent can let the user call the agent, and the agent then operates through Runes Shield.
Bots must not directly access Runes Shield or Hermes Runes MD Wiki.
External/public API access is not part of the design intent.
```

## Correct Access Model

The correct access model is:

```text
User -> local Hermes-agent -> Runes Shield -> Hermes Runes MD Wiki
```

Allowed bot-mediated path:

```text
User -> approved bot channel -> Hermes-agent -> Runes Shield -> Hermes Runes MD Wiki
```

The bot is only a user interaction channel into Hermes-agent.

The bot is not a direct Runes client.

## In-scope Access Paths

In scope:

```text
Local Hermes-agent invoking Runes Shield after explicit user request.
Local CLI / generic CLI wrapper invoking Hermes-agent behavior under governed boundary.
Approved bot channel invoking Hermes-agent as a user-facing ingress path.
Hermes-agent performing read-only recall or governed proposal drafting through Runes Shield.
Hermes-agent stopping before persistence unless operator approval is explicit.
```

## Out-of-scope Access Paths

Out of scope:

```text
External/public API access to Runes Shield.
Remote third-party adapter access to Hermes Runes MD Wiki.
Bot direct access to Runes Shield.
Bot direct file access to wiki content.
Bot direct proposal creation, import, index, apply, promote, approve, reject, or state mutation.
OpenAI-compatible public service endpoint for external clients.
Enterprise API gateway / orchestration daemon / websocket bridge.
```

## OpenAI-compatible Wrapper Boundary

The M108 OpenAI-compatible adapter template remains useful as a theoretical smoke template, but its scope is restricted.

Allowed interpretation:

```text
A local-only, operator-controlled test harness that routes to Hermes-agent and does not expose Runes directly.
```

Disallowed interpretation:

```text
A public or external OpenAI-compatible API server for third-party clients to access Runes Shield or wiki memory.
```

Therefore, M108 actual smoke remains:

```text
IMPLEMENTED / pending
```

and should not be treated as a required P0 runtime channel.

## Relationship to Existing Baselines

Existing verified channels remain valid:

```text
M101 CLI baseline: local Hermes-agent channel / PASS frozen
M103 Lark bot baseline: bot-mediated Hermes-agent channel / PASS frozen
M107 Generic CLI wrapper baseline: local wrapper-mediated agent channel / PASS frozen
```

These baselines all preserve the same governing principle:

```text
Only Hermes-agent may cross the Runes Shield boundary.
All other channels are ingress paths to the agent, not direct Runes clients.
```

## Boundary Rule

Formal rule:

```text
Runes Shield is the governed invocation boundary.
Hermes Runes MD Wiki is local trusted memory substrate.
Only a local agent explicitly authorized by the user may invoke Runes Shield.
Bots and wrappers may provide user interaction or local test harness behavior, but they must not bypass Hermes-agent or directly operate on Runes Shield/wiki internals.
```

## Persistence Rule

Persistence remains governed:

```text
Read-only recall: allowed through agent/tool boundary.
Proposal draft in response: allowed after user asks agent to prepare it.
Actual proposal file creation: requires explicit operator approval.
Import/index/apply/promote/approve/reject/state mutation: operator-gated and tool-governed.
Direct wiki mutation: not allowed for agents/bots/wrappers.
```

## Security Rule

Security remains local-first:

```text
No public Runes endpoint.
No direct bot-to-Runes access.
No third-party remote direct memory access.
No secrets in wiki/git/logs.
No runtime authority escalation through wrapper choice.
```

## Corrected M108 Interpretation

M108 should now be interpreted as:

```text
OpenAI-compatible adapter trial smoke template exists for local-only test harness exploration.
No live OpenAI-compatible endpoint is currently available.
No external/public API-facing channel is required for P0.
M108 remains pending/deferred unless a local-only operator-controlled harness is intentionally introduced later.
```

## PASS Meaning

M108.2 PASS means:

```text
The access boundary is now documented and locked.
The project does not need an external OpenAI-compatible API channel for P0.
Bot channels are explicitly indirect: user -> bot -> Hermes-agent -> Runes Shield.
Runes Shield remains local agent-facing only.
The M108 pending state is not a blocker for local P0/trial-run usage.
```

## Suggested Next Step

Recommended next milestone:

```text
M110 Adapter Channel Governance Recap
```

Suggested purpose:

```text
Summarize the frozen local/bot/wrapper channel baselines and the corrected OpenAI-compatible out-of-scope boundary before broader P0 trial-run usage.
```

Alternative next milestone:

```text
M109 Local Agent Runes Invocation Policy Lock
```

Suggested purpose:

```text
Promote the local-only access boundary from verification note into a concise system policy reference for future agent guidance.
```

## Final Lock

```text
M108.2 Local-only Runes Shield Access Boundary Lock
PASS / local-only Runes Shield access boundary locked
```
