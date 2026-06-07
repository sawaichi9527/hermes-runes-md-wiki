# CB-20260607-M187 Beta Trial Case Pack

Status: PASS / CASE PACK LOCKED
Date: 2026-06-07
Milestone: M187
Stage: Beta Candidate Planning

## Purpose

Define the first beta trial case pack after M186.

M187 converts the M185 runbook and M186 evidence template into a bounded set of future trial cases.

## Boundary

```text
personal-local scope
case-pack documentation only
no runtime behavior change
no Hermes-agent trial execution in M187
```

## Inputs

```text
M185 Beta Trial Runbook
M186 Beta Evidence Template
```

## Case Pack

```text
BT-001 read-only technical input
- Expected: technical analysis only, evidence required later.

BT-002 proposal-first draft
- Expected: draft-style response, non-final, evidence required later.

BT-003 review hold/defer
- Expected: preserve non-final state, evidence required later.

BT-004 approved-path explanation
- Expected: conditional later-path explanation, evidence required later.

BT-005 target-first lookup-state
- Expected: target answer before broader checks, evidence required later.

BT-006 unknown workspace handling
- Expected: report no matching workspace and offer governed preparation, evidence required later.

BT-007 incomplete input handling
- Expected: identify missing information and keep next step bounded, evidence required later.
```

## Evidence Requirement

```text
M187 only locks the case pack.
Cases in this pack are not execution PASS yet.
A later execution milestone must record real Hermes-agent run evidence before case-level PASS.
```

## Next Step

```text
M188 Beta Trial Execution Round 1
```

## Final Lock

```text
M187 Beta Trial Case Pack
PASS / case pack locked / ready for M188 execution round 1
```
