# M108.2 Local-only Runes Shield Access Boundary Lock

Status: PASS / LOCAL-ONLY AGENT RUNES SHIELD ACCESS BOUNDARY LOCKED
Date: 2026-06-06

## Purpose

M108.2 formally locks the local-only access boundary for Hermes Runes MD Wiki and Runes Shield.

This milestone corrects the M108 OpenAI-compatible adapter direction by clarifying that Hermes Runes MD Wiki is designed for local governed agent access, not external or public API access.

Hermes-agent is the current reference implementation, but the boundary is intentionally agent-agnostic. Future local agents such as OpenClaw or other third-party agents may be allowed if they operate through the same Runes Shield governed invocation boundary.

This is a governance/boundary lock only.

It does not change runtime behavior.

## Operator Clarification

The operator clarified:

```text
Runes can only be invoked by a local governed agent through Runes Shield.
The user must explicitly request the agent to connect to Runes.
Hermes-agent is the current implementation, but OpenClaw or other future third-party agents may also qualify if they obey the same local Runes Shield boundary.
At most, a bot connected through the agent can let the user call the agent, and the agent then operates through Runes Shield.
Bots must not directly access Runes Shield or Hermes Runes MD Wiki.
External/public API access is not part of the design intent.
```

## Correct Access Model

The correct access model is:

```text
User -> local governed agent -> Runes Shield -> Hermes Runes MD Wiki
```

Current concrete implementation:

```text
User -> local Hermes-agent -> Runes Shield -> Hermes Runes MD Wiki
```

Allowed future local-agent variants:

```text
User -> local OpenClaw or other approved local agent -> Runes Shield -> Hermes Runes MD Wiki
```

Allowed bot-mediated path:

```text
User -> approved bot channel -> local governed agent -> Runes Shield -> Hermes Runes MD Wiki
```

Current concrete bot-mediated implementation:

```text
User -> approved bot channel -> Hermes-agent -> Runes Shield -> Hermes Runes MD Wiki
```

The bot is only a user interaction channel into the approved local agent.

The bot is not a direct Runes client.

## In-scope Access Paths

In scope:

```text
Local governed agent invoking Runes Shield after explicit user request.
Hermes-agent invoking Runes Shield as the current reference implementation.
Future local OpenClaw or other approved third-party agent invoking Runes Shield under the same governed boundary.
Local CLI / generic CLI wrapper invoking approved local-agent behavior under governed boundary.
Approved bot channel invoking the approved local agent as a user-facing ingress path.
Approved local agent performing read-only recall or governed proposal drafting through Runes Shield.
Approved local agent stopping before persistence unless operator approval is explicit.
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
Any agent, bot, or wrapper bypassing Runes Shield to operate on wiki internals directly.
```

## OpenAI-compatible Wrapper Boundary

The M108 OpenAI-compatible adapter template remains useful as a theoretical smoke template, but its scope is restricted.

Allowed interpretation:

```text
A local-only, operator-controlled test harness that routes to an approved local governed agent and does not expose Runes directly.
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
M101 CLI baseline: local Hermes-agent reference channel / PASS frozen
M103 Lark bot baseline: bot-mediated Hermes-agent reference channel / PASS frozen
M107 Generic CLI wrapper baseline: local wrapper-mediated agent channel / PASS frozen
```

These baselines all preserve the same governing principle:

```text
Only an approved local governed agent may cross the Runes Shield boundary.
Hermes-agent is the current verified implementation, not the only possible future agent.
All other channels are ingress paths to the approved local agent, not direct Runes clients.
```

## Boundary Rule

Formal rule:

```text
Runes Shield is the governed invocation boundary.
Hermes Runes MD Wiki is local trusted memory substrate.
Only an approved local agent explicitly authorized by the user may invoke Runes Shield.
Hermes-agent is the current reference implementation.
OpenClaw or other third-party agents may be supported later only if they remain local, operator-controlled, and governed by Runes Shield.
Bots and wrappers may provide user interaction or local test harness behavior, but they must not bypass the approved local agent or directly operate on Runes Shield/wiki internals.
```

## Persistence Rule

Persistence remains governed:

```text
Read-only recall: allowed through agent/tool boundary.
Proposal draft in response: allowed after user asks an approved local agent to prepare it.
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
No agent-specific hard lock that prevents future local governed agents.
```

## Corrected M108 Interpretation

M108 should now be interpreted as:

```text
OpenAI-compatible adapter trial smoke template exists for local-only test harness exploration.
No live OpenAI-compatible endpoint is currently available.
No external/public API-facing channel is required for P0.
M108 remains pending/deferred unless a local-only operator-controlled harness is intentionally introduced later.
Such a harness must route to an approved local governed agent and must not expose Runes directly.
```

## PASS Meaning

M108.2 PASS means:

```text
The local-only access boundary is now documented and locked.
The project does not need an external OpenAI-compatible API channel for P0.
Bot channels are explicitly indirect: user -> bot -> approved local agent -> Runes Shield.
Runes Shield remains local agent-facing only.
Hermes-agent is the current verified implementation, while OpenClaw or other local governed agents remain future-compatible.
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
Promote the local-only, agent-agnostic access boundary from verification note into a concise system policy reference for future agent guidance.
```

## Final Lock

```text
M108.2 Local-only Runes Shield Access Boundary Lock
PASS / local-only agent Runes Shield access boundary locked
```
