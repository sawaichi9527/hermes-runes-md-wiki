# M36.3 — Runtime Conversation Adapter

Status: PASS / MVP CANDIDATE
Stage: P0 Runtime Conversation Layer
Subsystem: Runes Shield Conversation Adapter
Date: 2026-06-03

## Objective

Implement the first conversation adapter that converts user-facing text into the frozen four-state runtime path.

M36.3 does not redefine the incantation.

It adapts conversation text into the already locked runtime states:

- MATCH
- CONFIRM
- CONFIRM_MATCH
- NO_MATCH

## Important Boundary Note

The observation handler is the runtime action after a valid invocation.

It is not a new incantation grammar.

The adapter must not introduce a new trigger phrase such as adding an observation keyword into the ritual wording.

## Implemented Components

| Component | Path |
|---|---|
| Conversation adapter | `tools/runes_shield/adapt_conversation.py` |
| Adapter smoke | `tools/runes_shield/smoke_conversation_adapter.py` |

## Runtime Flow

```text
user message
-> conversation adapter
-> classified state
-> integration runtime
-> governed response
```

## Expected State Behavior

| Case | State | Response |
|---|---|---|
| core incantation + activation + Hermes Runes context | MATCH | governed_observation |
| core incantation + activation, unclear context | CONFIRM | confirmation_challenge |
| pending confirmation + user affirmation | CONFIRM_MATCH | governed_observation |
| mythology / fiction / generic diagnostics | NO_MATCH | normal_handling |

## Boundary

M36.3 remains read-only.

Frozen guarantees:

```text
write=false
autonomous_apply=false
hidden_escalation=false
trusted_memory_mutation=false
```

## Verification

Run:

```bash
python3 tools/runes_shield/smoke_conversation_adapter.py
```

Expected:

```text
PASS: conversation adapter validation completed
```

## Result

M36.3 establishes the first conversational entry point into the governed Runes Shield runtime chain while preserving the M33 four-state boundary.
