# Agent / Subagent / Kanban Role Model

Status: ACTIVE GUIDANCE / v0.7.3-dev M223  
Scope: single-agent Hermes Runes MD Wiki operation on local finite compute

## Decision

The active `main` architecture is:

```text
single main agent
+ bounded Hermes native subagents
+ lightweight Kanban checkpoint layer
```

This replaces the abandoned profile-based OPC direction on `main`.

The archived OPC-capable baseline remains available only as history:

```text
archive/v0.7.2-opc
```

## Local compute assumptions

This role model is designed for local finite compute, not cloud-scale million-token context windows.

Current operating assumptions:

```text
maximum LLM context: 128K tokens
Hermes Agent compression threshold: about 50% context usage
practical live working window before compression pressure: about 64K tokens
```

The system should avoid depending on a long uncompressed conversation to recover task state.

## Role split

### Main agent

The main agent is the only user-facing governed runtime.

It owns:

- user intent interpretation
- final decision-making
- repo/tool/script execution decisions
- guarded write decisions
- human confirmation handoff
- final synthesis after delegated checks

The main agent remains responsible even when it asks a native subagent for help.

### Hermes native subagents

Native subagents are bounded delegated execution helpers.

They may be used for:

- focused code review
- scoped document inspection
- test-result interpretation
- one-shot research or comparison
- bounded patch planning

They are not long-lived profile personas and do not own wiki state.

A native subagent result returns to the main agent as bounded evidence. The main agent decides whether that evidence becomes a repo change, a proposal, a verification record, or no action.

### Kanban

Kanban is the compact task-state checkpoint layer.

It is useful when a session is long enough that context compression may hide earlier details.

Kanban tracks:

- current milestone
- one-line objective
- constraints
- current status
- next action
- blocker state
- last human decision
- evidence links or file paths

Kanban should store pointers and state, not large bodies.

## Four-layer memory model

```text
conversation = volatile working memory
Kanban       = compact task-state checkpoint
Runes Wiki   = governed durable source-of-truth
Git history  = exact change evidence
```

Meaning:

- conversation holds live reasoning and temporary discussion
- Kanban holds compact task state for resuming work after compression
- Runes Wiki holds governed durable knowledge
- Git history holds exact file-change evidence

Kanban must not compete with Runes Wiki as a knowledge store.

## Kanban card shape

A personal/local Kanban card should stay compact:

```yaml
id: Mxxx
status: proposed | active | blocked | ready_for_review | done
owner: main-agent
scope: hermes-runes-md-wiki
objective: <one-line objective>
constraints:
  - single-agent mainline
  - personal/local complexity only
  - no raw secrets or large logs
context_budget:
  max_context: 128K
  compression_threshold: ~50%
  kanban_role: compact checkpoint
last_human_decision: <latest explicit decision>
next_action: <single next action>
blockers:
  - <optional blocker>
evidence:
  - <file path / commit / verification path>
```

## Operating rule

At the start of a non-trivial session, the main agent should read the current task-state card or equivalent compact note before touching repo files.

At the end of a non-trivial session, the main agent should update compact task state only when it adds value and does not duplicate an existing verification record.

## Boundary

This guidance deliberately avoids enterprise workflow complexity.

Keep:

- small WIP
- explicit status
- explicit next action
- explicit blocker
- evidence links instead of copied evidence bodies
- human approval gate for durable changes

Do not add:

- workflow engines
- dispatch queues
- telemetry platforms
- profile-agent orchestration
- long-running broker daemons
- Kanban-owned wiki mutation authority

## Implementation consequence

M223 implements documentation and policy alignment only.

It does not add runtime daemons, databases, queues, or agent mesh behavior.

The active mainline remains simple:

```text
User -> main agent -> optional bounded native subagent -> main agent decision -> governed repo/wiki path
```

Kanban remains a checkpoint aid, not a second memory system and not an orchestration system.
