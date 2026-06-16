# Agent / Subagent / Kanban Role Model Proposal

Status: APPROVED / superseded by active guidance  
Target: v0.7.3-dev M223  
Scope: single-agent Hermes Runes MD Wiki operation on local finite compute

## Result

This proposal was approved by the user and implemented as active guidance:

```text
docs/agent-subagent-kanban-role-model.md
```

## Approved role model

```text
single main agent
+ bounded Hermes native subagents
+ lightweight Kanban checkpoint layer
```

## Preserved decision boundary

The active mainline remains single-agent / agent-agnostic.

The abandoned profile-based OPC model is not active on `main`.

Native subagents are bounded delegated helpers, not persistent profile agents.

Kanban is a compact task-state checkpoint layer, not an orchestration layer.

## Local compute assumptions

The approved model assumes local finite compute:

```text
maximum LLM context: 128K tokens
Hermes Agent compression threshold: about 50% context usage
practical live working window before compression pressure: about 64K tokens
```

Kanban is used to reduce context pressure by preserving compact state, blockers, next action, and evidence links rather than long raw logs or full document bodies.

## Implementation boundary

M223 implementation is documentation and policy alignment only.

No runtime daemon, queue, database, profile-agent mesh, or enterprise workflow component was added.

See the active guidance document for the current policy.
