# M34.2 — Tool Contract Skeleton

Status: PASS / CONTRACT SKELETON LOCK
Stage: P0 / Trial-run Boundary Definition
Subsystem: Agent-Facing Tool Contract
Date: 2026-06-03

---

## Objective

Define the smallest agent-facing contract skeleton for the governed memory boundary.

This milestone creates a stable contract vocabulary that future agents can discover and call without receiving direct control over Markdown files, proposal state, or database content.

This is a contract skeleton only. It does not introduce autonomous write behavior.

---

## Design Principle

The boundary exposes governed operations, not internal implementation access.

Agents should interact through narrow operations with explicit authority classes.

```text
agent request
-> governed tool contract
-> governed operation
-> observable result
```

Agents must not directly operate:

- source Markdown files
- proposal state internals
- database rows
- importer internals
- trusted-memory promotion state

---

## Authority Classes

| Authority Class | Meaning | Write Access |
|---|---|---|
| `observe` | read-only diagnostics and evidence collection | no |
| `propose` | create or preview governed proposal material | draft/quarantine only |
| `confirm` | request explicit human approval signal | no |
| `apply` | execute controlled write after approval | human-governed only |

M34.2 only locks the skeleton for `observe`, `propose`, and `confirm`.

`apply` remains reserved for a separate controlled-write milestone.

---

## Tool Skeleton

### 1. observe

Purpose:

- Run observation-layer diagnostics.
- Inspect source health, structure, evidence, and readiness.

Allowed output:

- diagnostic summary
- evidence references
- source health report
- readiness report
- recommended next actions

Blocked behavior:

- no Markdown mutation
- no proposal approval
- no trusted-memory promotion
- no database mutation

---

### 2. propose

Purpose:

- Create or preview a governed proposal candidate.
- Keep output in draft / quarantine state until reviewed.

Allowed output:

- proposal preview
- candidate Markdown
- target path recommendation
- risk summary
- required confirmation metadata

Blocked behavior:

- no direct trusted wiki write
- no automatic approval
- no automatic promotion
- no silent apply

---

### 3. confirm

Purpose:

- Ask for explicit human confirmation when a boundary requires it.
- Preserve human intent priority.

Allowed output:

- confirmation challenge
- pending operation summary
- required approval token or equivalent approval signal

Blocked behavior:

- no operation execution
- no hidden escalation
- no auto-confirm

---

## Reserved Operation

`apply` is reserved and not enabled by M34.2.

Reason:

- Controlled writes require a separate human-governed path.
- That path must include visible diff, approval evidence, operation record, rollback evidence, and post-operation verification.

---

## Result Shape

Every tool result should include:

```yaml
status: PASS | BLOCKED | CONFIRM_REQUIRED | ERROR
tool: <tool name>
authority: observe | propose | confirm | apply
write: true | false
risk: low | medium | high
summary: <human-readable summary>
evidence: []
next_actions: []
```

For M34.2:

```text
observe.write = false
propose.write = false for trusted wiki
confirm.write = false
```

---

## Integration With M34.1

| Routing State | Tool Class |
|---|---|
| MATCH | observe |
| CONFIRM | confirm |
| CONFIRM_MATCH | observe |
| NO_MATCH | no governed tool invocation |

Proposal generation may be introduced only through explicit propose calls and must remain draft/quarantine scoped.

---

## Governance Rules

The tool contract skeleton must preserve:

- human intent priority
- observation-only invocation for the M34 routing path
- proposal quarantine for untrusted generated content
- no direct trusted-memory write through observation paths
- no autonomous apply
- no hidden authority escalation

---

## Completion Criteria

M34.2 is PASS when:

- tool authority classes are defined
- initial tool skeletons are named
- allowed outputs are documented
- blocked behaviors are documented
- result shape is defined
- apply remains reserved
- M34 routing remains observation-only

---

## Result

M34.2 establishes the first agent-facing tool contract skeleton.

The system now has a stable vocabulary for future runtime implementation while preserving the governed P0 memory boundary.

---
