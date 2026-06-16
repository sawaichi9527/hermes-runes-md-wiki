# M223 Agent / Subagent / Kanban Role Model

Status: PASS / active guidance approved and documented  
Target: v0.7.3-dev  
Scope: single-agent role model under local context limits

## Purpose

Implement the approved project role model for:

```text
main agent
Hermes native subagents
Kanban checkpoint layer
```

## User decision

User approved the M223 proposal with the intended model:

```text
single main agent
+ bounded native subagents
+ lightweight Kanban checkpoint layer
```

The approval explicitly keeps abandoned OPC profile agents out of active mainline architecture.

## Active guidance

Implemented active guidance:

```text
docs/agent-subagent-kanban-role-model.md
```

The proposal record remains for history:

```text
docs/agent-subagent-kanban-role-model-proposal.md
```

Its status is now approved and superseded by active guidance.

## Final role model

- Main agent is the single user-facing governed runtime.
- Native subagents are bounded delegated execution helpers.
- Kanban is a compact task-state / checkpoint layer.
- Kanban is not an A2A orchestration layer.
- Profile-based OPC agents remain abandoned and out of active mainline architecture.

## Local compute constraint

The active guidance explicitly assumes:

```text
maximum LLM context: 128K tokens
Hermes Agent compression threshold: about 50% context usage
practical live working window before compression pressure: about 64K tokens
```

Kanban reduces context pressure by holding compact task state, next action, blocker state, last human decision, and evidence links rather than long raw logs or full document bodies.

## Complexity boundary

M223 adds documentation and policy alignment only.

It does not add:

```text
runtime daemon
queue
database
profile-agent mesh
enterprise workflow component
```

## Final lock

M223 Agent / Subagent / Kanban Role Model

PASS / active guidance approved and documented
