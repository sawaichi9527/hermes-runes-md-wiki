# Hermes Runes MD Wiki Roadmap

This roadmap tracks near-term work for making Hermes Runes MD Wiki usable as a governed, agent-facing Markdown memory tool while keeping implementation lightweight, local-first, and human-governed.

---

## M21 Runes Shield — P0 / Trial Run Agent-facing Boundary

Status: Planned
Priority: P0

### Name

Runes Shield

### Subtitle

A governed invocation boundary for trusted Markdown memory.

### Chinese positioning

Runes Shield 是 Hermes-agent 與 Hermes Runes MD Wiki 之間的治理護盾，負責提供可發現、可召喚、可驗證的受控工具介面，並阻止 agent 直接操作內部 Markdown wiki、proposal 狀態與資料庫內容。

### Core principle

Hermes-agent may invoke the runes, but must never breach the shield.

中文：Hermes-agent 可以召喚符文，但不得突破護盾。

### Purpose

Runes Shield defines the supported interaction boundary between Hermes-agent and Hermes Runes MD Wiki.

Hermes Runes MD Wiki remains a governed Markdown memory backend and source-of-truth. Hermes-agent remains the conversation, decision, and orchestration layer. Runes Shield provides the controlled interface that lets Hermes-agent discover, invoke, and verify Runes capabilities without directly mutating internal wiki files, proposal states, database records, importer artifacts, or trusted memory content.

### P0 design rule

Hermes-agent must interact with Hermes Runes only through Runes-provided interfaces.

Hermes-agent must not directly:

- read internal files as an operational shortcut
- write or edit `wiki/*.md`
- move proposal files between states
- approve, reject, promote, import, rebuild, or delete memory content
- write PostgreSQL / FTS / pgvector records
- mutate importer artifacts or trusted memory state

### P0 allowed agent-facing capabilities

The initial Runes Shield interface should expose only small, stable, JSON-friendly commands:

- `runes capabilities --json`
  - discover available Runes capabilities and safety boundaries
- `runes guidance --json`
  - read agent-facing policy, invocation rules, and usage guidance
- `runes propose --json`
  - create a governed draft proposal from user-provided material after user consent
- `runes proposal list --json`
  - list proposal states without mutating them
- `runes proposal show --json`
  - inspect a proposal without mutating it
- `runes recall --json`
  - retrieve already indexed trusted memory evidence
- `runes smoke --json`
  - verify tool health and baseline behavior

### P0 explicitly human-only operations

The following operations must remain human-only during P0 / trial run:

- approve proposal
- reject proposal
- promote reviewed proposal into curated wiki note
- direct wiki edit
- importer lifecycle changes beyond controlled wrapper behavior
- destructive delete / archive operations
- database rebuild / schema mutation

### Agent interaction pattern

Hermes-agent should learn Runes Shield capabilities through the exposed guidance/capabilities interface.

When a user provides material that looks like durable project knowledge, Hermes-agent should proactively ask whether the user wants to create a governed Runes proposal.

Example interaction:

> 這段內容看起來像是後續會重複使用的專案知識。要不要我幫你建立一筆 Hermes Runes governed proposal，先放入待審核區，之後由你確認後再固化成 Markdown wiki？

Hermes-agent should only call `runes propose` after user consent.

### M21 milestone breakdown

#### M21.1 Runes Shield Contract

Goal:

- Define Runes Shield as the official P0 agent-facing boundary.
- Replace earlier Facade / Gate / Field naming with Runes Shield.
- Document allowed and forbidden Hermes-agent behaviors.
- Document human-only approval boundaries.

Planned files:

- `wiki/_system/runes_shield_contract.md`
- `wiki/_system/runes_invocation_policy.md`
- `wiki/_system/runes_agent_guidance.md`

Success criteria:

- Hermes-agent can understand the Runes boundary without reading internal implementation code.
- The contract clearly states that Hermes-agent must not directly operate internal wiki files, proposal states, database records, or importer artifacts.

#### M21.2 Runes Shield capabilities / guidance CLI

Goal:

- Provide simple read-only CLI/JSON endpoints for agent discovery.
- Keep implementation local, deterministic, and easy to inspect.

Candidate commands:

- `runes capabilities --json`
- `runes guidance --json`

Success criteria:

- Output is stable enough for Hermes-agent to consume.
- Output includes capability list, safety boundaries, write limitations, and human-only operations.

#### M21.3 Agent interaction prompt pattern

Goal:

- Define when Hermes-agent should offer Runes knowledge solidification to the user.
- Avoid automatically turning every conversation into memory.

Trigger candidates:

- project decision
- baseline result
- verification result
- technical procedure
- durable service architecture
- future action item
- repeated troubleshooting knowledge
- user explicitly asks to remember or solidify knowledge

Non-trigger candidates:

- one-off casual chat
- unverified speculation
- sensitive secrets
- credentials / tokens / passwords
- raw logs with private data
- material that needs user review first

Success criteria:

- Hermes-agent can proactively ask whether to create a governed proposal.
- Hermes-agent does not silently persist knowledge.
- User consent is required before `runes propose`.

#### M21.4 Multi-proposal P0 trial run

Goal:

- Validate the full governed proposal flow with mixed proposal states.

Trial scenario:

1. Create proposal A.
2. Create proposal B.
3. Create proposal C.
4. Human approves A.
5. Human rejects B.
6. C remains draft.
7. Import reviewed/approved content.
8. Recall approved content.
9. Verify rejected and draft content are not visible as trusted memory.
10. Run smoke/regression checks.

Success criteria:

- Approved proposal becomes retrievable trusted evidence.
- Rejected proposal remains excluded.
- Draft proposal remains excluded.
- Trusted wiki ordering remains stable.
- Smoke/regression remains PASS.
- Observation remains lightweight and non-authoritative.

#### M21.5 Human-only curated promotion path

Goal:

- Define a manual or dry-run path for promoting reviewed proposals into curated wiki notes.
- Keep promotion human-controlled during P0.

Planned behavior:

- Runes may generate a promotion plan or dry-run diff.
- Human performs or approves final promotion.
- Hermes-agent may request status or evidence, but may not perform direct promotion.

Success criteria:

- Reviewed proposal can be converted into curated Markdown knowledge without giving Hermes-agent direct write authority over trusted wiki structure.

### Out of scope for M21 P0

- Autonomous trusted memory writer
- Agent direct wiki mutation
- Agent direct database mutation
- Full MCP server implementation
- Enterprise policy engine
- Multi-user permission model
- Automatic heuristic tuning
- P2/P3 observation-driven optimization
- Web dashboard
- Complex workflow engine

### P0 completion definition

M21 P0 is complete when Hermes-agent can:

1. Discover Runes capabilities through Runes Shield.
2. Understand the boundary between allowed invocation and forbidden direct mutation.
3. Ask the user whether durable knowledge should be solidified.
4. Create governed proposals only after user consent.
5. Read proposal status and trusted recall evidence through Runes interfaces.
6. Avoid direct manipulation of internal Markdown files, proposal state, importer artifacts, and database content.
7. Pass the multi-proposal trial run with approved / rejected / draft isolation verified.

---
