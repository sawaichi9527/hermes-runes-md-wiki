# M34 — Runes Shield Invocation Integration

Status: PASS / DESIGN LOCK
Stage: P0 / Trial-run Integration Planning
Subsystem: Runes Shield Invocation Boundary
Date: 2026-06-03

---

## Objective

Define how the frozen M33 observation invocation semantics are integrated into the Runes Shield boundary.

M34 does not grant autonomous write authority. It defines the governed routing contract between an agent-facing invocation request and the existing Hermes Runes MD Wiki governance layers.

---

## Baseline Inputs

M34 depends on the frozen M33 chain:

- M33.7 boundary smoke verified the four-state behavior.
- M33.8 observe lock froze invocation semantics and observation scope.
- M33.9 governance documentation freeze made those semantics documentation-stable.

---

## Runes Shield Positioning

Runes Shield is the governed invocation boundary for trusted Markdown memory.

It is responsible for:

- exposing safe, discoverable operations to agents
- enforcing invocation boundaries
- preserving human-governed write and promotion policy
- preventing direct agent mutation of wiki content, proposal state, or database content

Runes Shield is not:

- a direct Markdown editor
- an autonomous forge engine
- a bypass around proposal governance
- a replacement for human review

---

## M34 Integration Contract

The M33 observation invocation output is mapped into Runes Shield as a governed routing decision.

| M33 State | Runes Shield Routing | Write Authority |
|---|---|---|
| MATCH | allow observation bundle invocation | none |
| CONFIRM | return confirmation challenge | none |
| CONFIRM_MATCH | allow observation bundle invocation | none |
| NO_MATCH | do not invoke observation bundle | none |

The integration deliberately preserves observation-only authority.

---

## Allowed Operations

When M33 resolves to MATCH or CONFIRM_MATCH, Runes Shield may route to observation operations such as:

- source health observation
- Markdown structure diagnostics
- forge readiness observation
- evidence inventory lookup
- governance status summary

These operations are read-only or proposal-aware diagnostic operations.

---

## Blocked Operations

M34 explicitly blocks the following through this integration path:

- direct wiki mutation
- autonomous apply
- autonomous proposal approval
- hidden promotion into trusted memory
- direct database mutation
- background write worker behavior

Any future write path must remain under the separate human-approved apply and attunement governance path.

---

## Agent-Facing Behavior

An agent using Runes Shield must treat M33 as a routing signal, not as authority escalation.

Required behavior:

1. classify the request against the frozen M33 boundary
2. route observation-only requests when allowed
3. ask for confirmation when the boundary returns CONFIRM
4. refuse or answer normally when the boundary returns NO_MATCH
5. never convert observation access into write access

---

## Trust Boundary

M34 preserves the existing trust hierarchy:

```text
trusted Markdown wiki
>
reviewed proposals
>
draft proposals
>
raw agent observations
```

Observation output may provide evidence for future proposals, but it must not become trusted memory automatically.

---

## Regression Requirements

Any future implementation of M34 runtime routing must include smoke coverage for:

- MATCH routes to observation only
- CONFIRM returns confirmation challenge
- CONFIRM_MATCH routes to observation only
- NO_MATCH does not invoke observation bundle
- observation routing does not mutate wiki files
- observation routing does not alter proposal status
- observation routing does not write to the database

---

## Completion Criteria

M34 design lock is complete when:

- M33 output states are mapped to Runes Shield routing
- observation-only authority is preserved
- blocked write operations are documented
- agent-facing behavior is defined
- regression requirements are listed
- future runtime implementation remains constrained by human-governed apply policy

---

## Result

M34 establishes the Runes Shield integration contract for the M33 observation invocation layer.

The system can now proceed toward runtime routing implementation without weakening the P0 governed memory boundary.

---
