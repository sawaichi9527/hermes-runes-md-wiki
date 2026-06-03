# M34.4 — Invocation Registry Draft

Status: PASS / REGISTRY DRAFT LOCK
Stage: P0 / Trial-run Invocation Registry Definition
Subsystem: Runes Shield Invocation Registry
Date: 2026-06-03

---

## Objective

Define the first draft structure for the Runes Shield invocation registry.

The registry acts as a governed mapping layer between:

- invocation state
- discoverable tool classes
- routing policy
- authority scope
- confirmation requirements
- runtime eligibility

This milestone defines the registry shape only.

It does not implement autonomous execution.

---

## Registry Principle

The invocation registry exists to:

- normalize routing semantics
- centralize invocation metadata
- make runtime behavior reviewable
- expose governance-visible routing rules
- preserve authority boundaries

The registry must not:

- bypass governance
- grant hidden write authority
- expose internal storage layout
- expose direct DB mutation operations
- enable silent escalation

---

## Registry Layer Position

```text
agent request
-> invocation classification
-> invocation registry
-> governed routing
-> observable result
```

The registry is a metadata and routing layer.

It is not a direct execution engine.

---

## Registry Entry Shape

Each registry entry should contain:

```yaml
id: <stable registry id>
state: MATCH | CONFIRM | CONFIRM_MATCH | NO_MATCH
tool: observe | propose | confirm | apply
routing_enabled: true | false
write: true | false
requires_confirmation: true | false
authority: observe | propose | confirm | apply
risk: low | medium | high
allowed_outputs: []
blocked_behaviors: []
notes: <human-readable governance note>
```

---

## Initial Registry Draft

### MATCH

```yaml
id: m34.match.observe
state: MATCH
tool: observe
routing_enabled: true
write: false
requires_confirmation: false
authority: observe
risk: low
```

Purpose:

- allow observation-layer diagnostics
- allow governance visibility
- preserve read-only routing

Blocked:

- no trusted-memory mutation
- no proposal approval
- no DB mutation

---

### CONFIRM

```yaml
id: m34.confirm.challenge
state: CONFIRM
tool: confirm
routing_enabled: true
write: false
requires_confirmation: false
authority: confirm
risk: low
```

Purpose:

- return explicit confirmation challenge
- preserve human intent priority
- block silent escalation

Blocked:

- no implicit routing continuation
- no hidden invoke
- no write authority

---

### CONFIRM_MATCH

```yaml
id: m34.confirm_match.observe
state: CONFIRM_MATCH
tool: observe
routing_enabled: true
write: false
requires_confirmation: false
authority: observe
risk: low
```

Purpose:

- unlock observation routing after explicit user continuation
- preserve observation-only authority

Blocked:

- no autonomous apply
- no proposal approval
- no trusted-memory promotion

---

### NO_MATCH

```yaml
id: m34.no_match.none
state: NO_MATCH
tool: none
routing_enabled: false
write: false
requires_confirmation: false
authority: none
risk: low
```

Purpose:

- preserve normal assistant behavior
- prevent mythology/game/fiction false invocation

Blocked:

- no observation invocation
- no escalation
- no hidden registry routing

---

## Reserved Registry Space

The following registry namespaces remain reserved:

| Namespace | Status |
|---|---|
| `m34.apply.*` | reserved |
| `m34.admin.*` | reserved |
| `m34.system.*` | reserved |

These namespaces must not become runtime-enabled during current P0 trial-run stages.

---

## Runtime Safety Rules

The registry must preserve:

- explicit human intent priority
- deterministic routing
- observation-only routing for M33/M34 flows
- no hidden escalation
- no write leakage
- no internal storage exposure
- governance-visible routing behavior

---

## Registry Visibility

The registry is intended to be:

- discoverable
- reviewable
- governance-visible
- regression-testable

but not:

- directly mutable by agents
- self-modifying
- dynamically self-authorizing

---

## Integration Chain

```text
M34.2 tool contract skeleton
-> M34.3 discovery contract
-> M34.4 invocation registry draft
-> future runtime registry implementation
```

---

## Completion Criteria

M34.4 is PASS when:

- registry entry shape is defined
- all four routing states have draft entries
- reserved namespaces are documented
- runtime safety rules are documented
- registry visibility rules are documented
- registry remains aligned with M33/M34 governance boundaries

---

## Result

M34.4 establishes the first governed invocation registry draft for Runes Shield.

The system now has a stable routing metadata vocabulary for future runtime integration while preserving the P0 governed memory boundary.

---
