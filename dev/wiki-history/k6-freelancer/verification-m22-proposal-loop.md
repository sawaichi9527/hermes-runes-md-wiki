# M22 Proposal Governance Loop Verification

Status: PASS / P0 proposal governance loop baseline established

## V-20260602-M22 Proposal Governance Loop

This document freezes the P0 / trial-run proposal governance boundary implemented through M22.1 ~ M22.5.

The goal of M22 is to provide a governed agent-facing proposal workflow through Runes Shield while preventing Hermes-agent from directly mutating trusted Markdown memory.

---

## Verified Components

### M22.1 Governed draft proposal writer

Status:

PASS / draft-write-only / smoke verified

Verified properties:

- explicit user consent required
- creates draft proposal only
- proposal remains unapproved
- trusted memory not created
- importer not executed
- database not mutated

---

### M22.2 Proposal list/show inspection

Status:

PASS / read-only / smoke verified

Verified properties:

- proposal list available
- proposal show available
- no proposal mutation
- no trusted memory mutation

---

### M22.3 Proposal hygiene report

Status:

PASS / read-only / smoke verified

Verified properties:

- detects proposal status mismatches
- detects metadata hygiene problems
- reports issues without mutation
- no importer/database mutation

---

### M22.3b Hygiene CLI wiring

Status:

PASS / read-only / smoke verified

Verified command:

```bash
bin/runes proposal hygiene --json
```

---

### M22.4 Cleanup plan dry-run

Status:

PASS / dry-run-only / smoke verified

Verified properties:

- hygiene issues converted into planned cleanup actions
- execution disabled
- human review required
- no mutation performed

---

### M22.5 Cleanup-plan CLI wiring

Status:

PASS / dry-run-only / smoke verified

Verified command:

```bash
bin/runes proposal cleanup-plan --json
```

---

## P0 Governance Boundary

The following boundaries are intentionally enforced:

- Hermes-agent must use Runes Shield interfaces only.
- Hermes-agent must not directly mutate wiki/ content.
- Hermes-agent must not directly approve proposals.
- Hermes-agent must not directly reject proposals.
- Hermes-agent must not directly promote curated notes.
- Hermes-agent must not autonomously execute cleanup operations.
- Draft or rejected proposals are not trusted memory.
- Human approval is required before trusted memory creation.

---

## Explicitly Not Implemented In M22

The following operations remain intentionally outside the P0 boundary:

- approve execution
- reject execution
- curated promotion execution
- cleanup execution
- importer/index rebuild execution
- direct database mutation
- autonomous trusted-memory mutation

These operations remain human-only or future dry-run targets.

---

## Trial-Run Readiness

M22 establishes a stable proposal-governance loop suitable for:

- P0 Hermes-agent trial run
- governed proposal creation
- proposal inspection
- hygiene validation
- cleanup planning

without granting direct trusted-memory authority to Hermes-agent.
