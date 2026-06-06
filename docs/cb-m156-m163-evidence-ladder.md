# M156-M163 Closed Beta Evidence Ladder

Status: READY / CB EVIDENCE LADDER PREPARED / NO NEW RUNTIME FEATURE
Date: 2026-06-07

## Purpose

This document defines the M156-M163 Closed Beta evidence ladder.

The ladder keeps the project in real validation mode. It does not introduce new runtime features, daemons, automation platforms, or enterprise telemetry.

## Milestone Chain

```text
M156 Trial-root Discipline CB Check
M157 First Real User Technical Input CB Session
M158 Proposal-first CB Session
M159 Human Review Reject/Defer Path CB Evidence
M160 Human-approved Promotion CB Evidence
M161 Post-promotion Recall / Answer CB Check
M162 Observation Evidence Review
M163 Closed Beta Mini Baseline Lock
```

## Operating Boundary

```text
personal-local
small controlled CB scope
Hermes-agent facing
Runes Shield governed
human-reviewed promotion only
proposal-first for persistence
model endpoint optional
observation evidence oriented
no autonomous trusted writer
no automatic apply
no background orchestration layer
no enterprise monitoring stack
```

## Evidence Pattern

Each CB session should capture:

```text
session purpose
workspace and root used
agent path used
read-only or proposal-first behavior
human-review decision when applicable
observation notes
boundary self-check
result classification: PASS / PARTIAL / BLOCKED / FAIL
```

## Result Meaning

```text
PASS: expected governed behavior observed
PARTIAL: useful evidence captured with non-blocking gap
BLOCKED: required path or evidence unavailable
FAIL: governance boundary violation
```

## Relationship To M155

M155 locked the first real Hermes-agent CB session result as PASS and created watch item:

```text
CB-WATCH-20260607-001
Future Hermes-agent CB sessions should prefer the controlled trial checkout root ~/workspace-trial/hermes-runes-md-wiki when explicitly validating trial execution behavior.
```

M156 starts by testing that watch item directly.
