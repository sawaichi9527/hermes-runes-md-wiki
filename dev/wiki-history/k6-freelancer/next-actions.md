## N-20260617-v0.7.3-dev Target Queue

Status: READY / v0.7.3-dev target queue defined

Current baseline:

```text
main: single-agent / agent-agnostic active baseline
VERSION: 0.7.3-dev
v0.7.2: archived release tag
archive/v0.7.2-opc: archived OPC-capable branch
```

M221 result:

```text
M221 De-OPC Mainline Rebaseline
PASS / single-agent mainline restored / RSS local commit preserved
```

Decisions:

- Hermes Agent profile-based OPC/A2A deployment is abandoned for this project.
- Active OPC overlay docs and workspace seed are removed from `main`.
- `v0.7.2` and `archive/v0.7.2-opc` preserve the old OPC-capable release baseline.
- Migration guard remains active.
- Existing-installation guarded update flow remains active.
- Local RSS active feeds commit is preserved on top of the de-OPC baseline.
- Abandoned OPC/PLUR operations log was not merged into active main.
- Repository location remains unchanged for now: `~/workspace/hermes-runes-md-wiki`.

v0.7.3-dev target queue:

1. `M222 Single-Agent Baseline Sanity Check`
   - Confirm README, wiki system entry, fresh-install docs, and workspace seed all describe the single-agent / agent-agnostic baseline.
   - Confirm no active OPC overlay wording remains in mainline docs.
   - Preserve archived v0.7.2 OPC references as historical release/archive context only.

2. `M223 Agent / Subagent / Kanban Role Model`
   - Define the project-level relationship among the main agent, Hermes native subagents, and Kanban.
   - Treat the main agent as the single user-facing governed runtime.
   - Treat native subagents as bounded delegated execution helpers, not independent profile agents.
   - Treat Kanban as an observation / task-state / checkpoint window, not an A2A orchestration layer.
   - Explicitly exclude abandoned OPC profile agents from the active architecture.

3. `M224 hermes-memory-sync Path Fix`
   - Inspect whether `./bin/hermes-memory-sync` still uses stale `hermes-memory` paths.
   - Patch wrappers to derive the current repo root dynamically where appropriate.
   - Keep `./bin/hermes-memory-import` as the known-good import entrypoint.

4. `M225 Optional Embedding Profile Boundary`
   - Clarify that Core FTS smoke is the required baseline.
   - Keep embedding / hybrid recall / answer generation as optional profile checks unless dependencies are installed.
   - Document dependency expectations without making optional embedding a core failure.

5. `M226 v0.7.3 Release Candidate Prep`
   - Enter only after M222-M225 are resolved or explicitly deferred.
   - Confirm single-agent baseline, guarded update flow, and release notes are aligned.

Out of scope for active `main`:

- OPC profile overlay.
- Profile-based secretary / runes-holder / coordinator / researcher / builder / writer architecture.
- PLUR shared memory as active mainline dependency.
- Lark-to-profile A2A handoff.
- Any direct Lark-to-wiki write path.

Next selected work:

```text
M222 Single-Agent Baseline Sanity Check
```
