# M36.5 — Conversation Chain Regression Lock

Status: PASS / REGRESSION LOCK
Stage: P0 Runtime Conversation Chain Lock
Subsystem: Runes Shield Conversation Runtime
Date: 2026-06-03

## Objective

Freeze the M36 conversation runtime chain with a single regression smoke.

M36.5 verifies that the M36.0 to M36.4 runtime path remains stable.

## Locked M36 Chain

| Milestone | Status | Result |
|---|---|---|
| M36 | PASS | real read-only observation handler |
| M36.1 | PASS | observation summary formatter |
| M36.2 | PASS | invocation-to-observation integration |
| M36.3 | PASS | runtime conversation adapter |
| M36.4 | PASS | user-facing response renderer |
| M36.5 | PASS | conversation chain regression lock |

## Regression Smoke

| Smoke | Path |
|---|---|
| Observe handler | `tools/runes_shield/smoke_observe_handler.py` |
| Formatter | `tools/runes_shield/smoke_formatter.py` |
| Integration | `tools/runes_shield/smoke_integration.py` |
| Conversation adapter | `tools/runes_shield/smoke_conversation_adapter.py` |
| Response renderer | `tools/runes_shield/smoke_response_renderer.py` |
| Boundary regression | `tools/runes_shield/smoke_boundary_regression.py` |
| M36.5 chain smoke | `tools/runes_shield/smoke_conversation_chain.py` |

## Runtime Chain

```text
conversation input
-> conversation adapter
-> integration runtime
-> dispatcher
-> observe / confirm / none
-> formatter
-> response renderer
-> user-facing governed response
```

## Frozen Boundary

M36.5 preserves the P0 governed runtime boundary:

```text
write=false
autonomous_apply=false
hidden_escalation=false
trusted_memory_mutation=false
```

## Verification

Run:

```bash
python3 tools/runes_shield/smoke_conversation_chain.py
```

Expected:

```text
PASS: conversation chain regression completed
```

## Result

M36 is frozen as the first complete read-only governed conversation runtime chain for Runes Shield.
