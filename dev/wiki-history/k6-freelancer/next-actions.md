## N-20260617-v0.7.3-dev Target Queue

Status: READY / M222-M225 partially resolved

Current baseline:

```text
main: single-agent / agent-agnostic active baseline
VERSION: 0.7.3-dev
v0.7.2: archived release tag
archive/v0.7.2-opc: archived OPC-capable branch
```

Completed in this pass:

```text
M222 Single-Agent Baseline Sanity Check
PASS / single-agent sanity locally verified

M224 hermes-memory-sync Path Fix
PASS / sync path locally verified

M225 Optional Embedding Profile Boundary
PASS / optional embedding boundary locally verified
```

Pending decision:

```text
M223 Agent / Subagent / Kanban Role Model
Status: PROPOSAL READY / pending user approval before implementation
Proposal: docs/agent-subagent-kanban-role-model-proposal.md
```

M223 proposal summary:

```text
main agent = single user-facing governed runtime
Hermes native subagents = bounded delegated execution helpers
Kanban = compact task-state / checkpoint layer under local context limits
```

M223 assumptions:

```text
local maximum context: 128K tokens
compression pressure begins around 50% context usage
Kanban should store compact task state, blockers, next action, and evidence links
Kanban should not become an A2A orchestration layer
```

Deferred until M223 decision:

```text
M226 v0.7.3 Release Candidate Prep
```

Repository location decision:

```text
Keep current path for now: ~/workspace/hermes-runes-md-wiki
```

Out of active mainline scope:

```text
profile-agent OPC overlay
profile-based secretary / runes-holder / coordinator / researcher / builder / writer architecture
PLUR as active mainline dependency
Lark-to-profile A2A handoff
direct Lark-to-wiki write path
```

Next selected work:

```text
Review and decide M223 proposal.
```
