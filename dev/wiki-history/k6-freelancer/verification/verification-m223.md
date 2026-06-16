# M223 Agent / Subagent / Kanban Role Model

Status: PROPOSAL READY / pending user approval before implementation  
Target: v0.7.3-dev  
Scope: single-agent role model under local context limits

## Purpose

Prepare, but do not yet implement, the project role model for:

```text
main agent
Hermes native subagents
Kanban checkpoint layer
```

## Proposal file

```text
docs/agent-subagent-kanban-role-model-proposal.md
```

## Key proposal points

- Main agent remains the single user-facing governed runtime.
- Native subagents are bounded delegated execution helpers.
- Kanban is a task-state / checkpoint / observation layer.
- Kanban is not an A2A orchestration layer.
- Profile-based OPC agents remain abandoned and out of active mainline architecture.

## Local compute constraint

The proposal explicitly assumes:

```text
maximum LLM context: 128K tokens
Hermes Agent compression threshold: about 50% context usage
practical live working window before compression pressure: about 64K tokens
```

The proposed Kanban role is to reduce context pressure by holding compact task state, next action, blockers, and evidence links rather than long raw logs or full document bodies.

## Approval gate

Do not implement M223 active policy until the user approves the proposal.
