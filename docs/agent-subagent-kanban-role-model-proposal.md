# Agent / Subagent / Kanban Role Model Proposal

Status: PROPOSAL / pending user approval before implementation  
Target: v0.7.3-dev M223  
Scope: single-agent Hermes Runes MD Wiki operation on local finite compute

## Problem

The active mainline has returned to a single-agent / agent-agnostic baseline.

The abandoned profile-based OPC model should not be reintroduced as active architecture. However, the project still needs a practical way to manage long-running work without overloading a local LLM context window.

Current local constraints:

```text
maximum LLM context: 128K tokens
Hermes Agent compression threshold: about 50% context usage
practical live working window before compression pressure: about 64K tokens
```

Therefore, the system needs an external, simple, durable task-state layer that helps the single main agent recover intent, status, evidence, and next action without relying on a long uncompressed conversation.

## Proposed role split

### 1. Main agent

The main agent is the only user-facing governed runtime.

Responsibilities:

- interpret user intent
- decide whether to read, propose, validate, or modify repo content
- call tools and scripts
- request human confirmation for governed writes
- summarize work into durable records when appropriate

Non-goals:

- no profile-agent mesh
- no autonomous multi-agent organization
- no direct unsupervised wiki mutation

### 2. Hermes native subagents

Native subagents are bounded delegated execution helpers.

They may be used for:

- focused code review
- scoped document inspection
- test-result interpretation
- one-shot research or comparison
- bounded patch planning

They are not:

- independent long-lived personas
- persistent profile agents
- separate owners of wiki state
- A2A orchestration endpoints

A subagent result should return to the main agent as bounded evidence, not as a competing authority.

### 3. Kanban

Kanban is the task-state and checkpoint window.

It is not an A2A orchestration layer.

It should track:

- current milestone
- objective
- constraints
- status
- next action
- evidence links or file paths
- blocker state
- last human decision

Kanban should not store raw large logs, full documents, secrets, or long conversation bodies.

## Why Kanban is useful under local context limits

With a 128K context limit and early compression pressure around 50%, the useful live conversation window can shrink during long technical work.

Kanban acts as a compact state register:

```text
conversation = volatile working memory
Kanban = compact task-state checkpoint
Runes Wiki = governed durable source-of-truth
Git history = exact code/document change evidence
```

This allows the main agent to resume safely after context compression by reading a short task card instead of reconstructing everything from a long chat.

## Mature-practice mapping without enterprise complexity

This proposal borrows only the lightweight parts of mature Kanban and incident/change management practice:

- small WIP
- explicit status
- explicit next action
- explicit blocker
- evidence link instead of copied evidence body
- done criteria
- human approval gate for durable changes

It deliberately avoids:

- enterprise workflow engines
- multi-user permission systems
- automated dispatch queues
- SLA dashboards
- telemetry platforms
- profile-agent orchestration

## Proposed Kanban card shape

```yaml
id: M223
status: proposed | active | blocked | ready_for_review | done
owner: main-agent
scope: hermes-runes-md-wiki
objective: clarify agent/subagent/kanban relationship
constraints:
  - single-agent mainline
  - no OPC profile agents
  - personal/local complexity only
  - no raw secrets or large logs
context_budget:
  max_context: 128K
  compression_threshold: ~50%
  kanban_role: compact checkpoint
last_human_decision: pending approval
next_action: wait for user approval before implementation
links:
  repo_docs:
    - docs/agent-subagent-kanban-role-model-proposal.md
  verification:
    - dev/wiki-history/k6-freelancer/verification/verification-m223.md
```

## Proposed operating rule

At the start of a non-trivial session, the main agent should read the current Kanban card or equivalent compact task-state note before touching repo files.

At the end of a non-trivial session, the main agent should update the task-state summary only when the user approves or when the repo change itself already records the state in `dev/wiki-history`.

## Proposed implementation boundary

After user approval, M223 should implement only documentation/policy alignment:

- document this role model as active guidance
- keep profile-based OPC excluded from `main`
- clarify that native subagents are bounded helpers
- clarify that Kanban is checkpoint state, not orchestration
- avoid adding daemons, queues, databases, or enterprise workflow components

No runtime daemon or multi-agent broker should be added for M223.

## Approval question

Approve M223 as:

```text
single main agent + bounded native subagents + lightweight Kanban checkpoint layer
```

and explicitly keep abandoned OPC profile agents out of active mainline architecture.
