# Verification: S1-S6 v0.7.4-dev PLUR Runtime Memory Bridge

Status: DESIGN RECORDED / implementation scope aligned  
Date: 2026-06-27  
Version line: 0.7.4-dev

## Scope

This verification note records the v0.7.4-dev correction scope for optional PLUR runtime memory bridge reintegration.

It does not claim runtime PLUR integration is fully implemented. It verifies that the intended S1-S6 boundaries have been recorded without expanding the project into heavy Hermes Agent customization or enterprise workflow.

## Verified planning artifacts

```text
docs/plur-runtime-memory-bridge.md
CHANGELOG.md
dev/wiki-history/k6-freelancer/next-actions.md
```

## S1 — Detachable PLUR integration

Expected:

```text
PLUR is optional and detachable.
Core Hermes Runes MD Wiki workflows must remain usable when PLUR is unavailable.
```

Status: RECORDED

Evidence:

```text
docs/plur-runtime-memory-bridge.md
```

## S2 — Minimal Hermes Agent native customization

Expected:

```text
No Hermes Agent core patch.
No dependency on private Hermes Agent memory/compression/Kanban/subagent internals.
No repository-specific Hermes Agent configuration that makes the agent unusable for normal tasks.
```

Status: RECORDED

## S3 — PLUR runtime memory role and source priority

Expected:

```text
PLUR is runtime persistent working memory.
PLUR is not canonical long-term truth.
Runes Wiki remains governed canonical long-term memory evidence.
Hermes Agent / Lark bot remains the reasoning and candidate-proposal layer.
```

Status: RECORDED

## S4 — Engram / episode / checkpoint / candidate policy

Expected:

```text
Engram = compact behavioral/runtime memory.
Episode = timestamped history, not injected by default.
Checkpoint = current working state for recovery/handoff.
Candidate = proposed memory requiring user approval before forge.
```

Status: RECORDED

## S5 — Human-in-the-loop forge candidate flow

Expected:

```text
PLUR can hold candidates.
Hermes Agent / Lark bot proposes.
User explicitly approves.
Runes Shield protects the operation.
Runes Wiki receives canonical memory only after approved forge.
```

Status: RECORDED

## S6 — Minimal PLUR memory hygiene and deployed-memory caution

Expected:

```text
Scope required.
Episode injection disabled by default.
Governance hints require pointer and last_verified_at.
Candidates do not auto-promote.
Stale checkpoints are marked superseded/inactive instead of requiring heavy purge.
Existing deployed PLUR memory is not bulk migrated, bulk deleted, or assumed canonical.
```

Status: RECORDED

## Explicit non-goals

```text
No OPC profile-agent restoration.
No Hermes Agent core patch.
No daemon / queue / telemetry / enterprise approval workflow.
No heavy LLM judge.
No every-turn full PLUR scan.
No automatic PLUR-to-Runes Wiki promotion.
No bulk rewrite or deletion of existing deployed PLUR memory.
```

Status: RECORDED

## Follow-up verification still needed

Runtime verification should later confirm:

```text
1. Existing installation can pull the docs without touching local PLUR memory.
2. PLUR unavailable path remains harmless.
3. Any future PLUR status/check command is read-only by default.
4. Candidate forge cannot bypass human-in-the-loop approval.
5. Existing Runes smoke remains PASS after pull.
```

## Result

```text
PASS: v0.7.4-dev S1-S6 PLUR bridge scope recorded.
PASS: Heavy runtime enforcement is explicitly excluded.
PASS: Existing deployed PLUR memory caution is documented.
PENDING: Runtime PLUR adapter/status command implementation and smoke.
```
