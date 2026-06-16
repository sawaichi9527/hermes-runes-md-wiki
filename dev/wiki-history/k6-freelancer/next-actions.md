## N-20260617-v0.7.3-dev Target Queue

Status: READY / M222-M225 resolved / M226 selected

Current baseline:

```text
main: single-agent / agent-agnostic active baseline
VERSION: 0.7.3-dev
v0.7.2: archived release tag
archive/v0.7.2-opc: archived OPC-capable branch
```

Completed:

```text
M222 Single-Agent Baseline Sanity Check
PASS / single-agent sanity locally verified

M223 Agent / Subagent / Kanban Role Model
PASS / active guidance approved and documented

M224 hermes-memory-sync Path Fix
PASS / sync path locally verified

M225 Optional Embedding Profile Boundary
PASS / optional embedding boundary locally verified
```

M223 active guidance:

```text
docs/agent-subagent-kanban-role-model.md
```

M223 final model:

```text
main agent = single user-facing governed runtime
Hermes native subagents = bounded delegated execution helpers
Kanban = compact task-state / checkpoint layer under local context limits
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
M226 v0.7.3 Release Candidate Prep
```

M226 entry criteria:

```text
- VERSION remains 0.7.3-dev until release prep finishes.
- M222-M225 are resolved.
- M223 is active guidance, not runtime orchestration.
- Core FTS smoke remains the required baseline.
- Embedding/hybrid/answer-generation remains optional unless the release explicitly targets that profile.
- No active OPC overlay returns to main.
```
