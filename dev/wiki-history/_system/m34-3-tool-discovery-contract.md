# M34.3 — Tool Discovery Contract

Status: PASS / DISCOVERY CONTRACT LOCK
Stage: P0 / Trial-run Boundary Definition
Subsystem: Agent-Facing Tool Discovery
Date: 2026-06-03

---

## Objective

Define how an agent discovers the governed memory boundary and its available tool classes.

M34.3 builds on M34.2 by adding a discovery contract. The goal is to make the boundary self-describing without exposing internal file paths, proposal internals, database internals, or unrestricted write capability.

This milestone is a documentation and contract lock. It does not add runtime implementation.

---

## Discovery Principle

Tool discovery must reveal what an agent may request, not how internal memory is implemented.

Discovery output should provide:

- tool names
- authority class
- write capability flag
- short purpose
- allowed result type
- blocked behavior summary
- required human confirmation status

Discovery output must not provide:

- direct file mutation instructions
- database connection details
- secret paths
- private credentials
- bypass instructions for proposal review
- internal state mutation details

---

## Discovery Result Shape

The discovery response should use a simple structured shape:

```yaml
status: PASS
tool_boundary: runes_shield
discovery_version: m34.3-p0
write_default: false
tools:
  - name: observe
    authority: observe
    write: false
    purpose: diagnostics and evidence visibility
    requires_confirmation: false
  - name: propose
    authority: propose
    write: false
    purpose: draft candidate generation or preview
    requires_confirmation: true
  - name: confirm
    authority: confirm
    write: false
    purpose: explicit human confirmation challenge
    requires_confirmation: false
reserved:
  - name: apply
    enabled: false
    reason: reserved for separate human-governed controlled-write path
```

---

## Discoverable Tool Classes

### observe

Discoverable: yes

Authority: read-only observation

Purpose:

- diagnostics
- evidence visibility
- source health summary
- structure readiness summary

Write capability:

```text
false
```

---

### propose

Discoverable: yes

Authority: draft proposal creation or preview

Purpose:

- candidate material preparation
- target recommendation
- risk summary
- human-review handoff

Write capability:

```text
false for trusted wiki
```

Notes:

- Proposal output must remain untrusted until reviewed.
- Proposal output must not become trusted memory automatically.

---

### confirm

Discoverable: yes

Authority: confirmation challenge only

Purpose:

- ask for explicit human intent
- preserve boundary semantics
- prevent silent escalation

Write capability:

```text
false
```

---

## Reserved Tool Class

### apply

Discoverable: reserved only

Enabled:

```text
false in M34.3
```

Reason:

- Controlled writes require a separate milestone.
- Future implementation must preserve visible diff, approval evidence, operation record, rollback evidence, and post-operation verification.

---

## Discovery Safety Rules

Discovery must preserve the following rules:

- default write flag is false
- unavailable tools are shown as reserved, not executable
- internal implementation details remain hidden
- human confirmation requirements are visible
- no authority escalation is implied by discovery
- discovery itself is read-only

---

## Integration With M34.2

M34.3 makes the M34.2 tool contract discoverable.

M34.2 defined the contract skeleton.

M34.3 defines how an agent learns that skeleton safely.

```text
M34.2 contract skeleton
-> M34.3 discovery contract
-> future runtime registry
```

---

## Completion Criteria

M34.3 is PASS when:

- discovery result shape is defined
- discoverable tool classes are listed
- reserved tool class is explicitly disabled
- discovery safety rules are documented
- discovery does not expose internal mutation paths
- discovery remains aligned with M34.2 authority classes

---

## Result

M34.3 establishes the safe discovery contract for the Runes Shield tool boundary.

Agents can now discover the governed operation vocabulary without gaining direct access to trusted memory internals.

---
