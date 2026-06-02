# Hermes Runes MD Wiki Roadmap

This roadmap tracks near-term work for making Hermes Runes MD Wiki usable as a governed, agent-facing Markdown memory tool while keeping implementation lightweight, local-first, and human-governed.

---

## M21 Runes Shield — P0 / Trial Run Agent-facing Boundary

Status: PASS / P0 boundary baseline established
Priority: P0
Verification record: `wiki/k6-freelancer/verification-m21-runes-shield.md`

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

### Canonical P0 Markdown architecture

P0 / trial run must use the canonical Markdown architecture files defined by this roadmap, not incidental local wiki documents accumulated during development.

Canonical P0 / trial run files:

```text
wiki/hermes_runes_index.md
wiki/_system/runes_shield_contract.md
wiki/_system/runes_invocation_policy.md
wiki/_system/runes_agent_guidance.md
```

Other local wiki files may exist and may be useful references, but they are not required P0 bootstrap dependencies unless explicitly promoted into this canonical architecture.

Agents must not infer operational behavior from arbitrary wiki files.

### P0 allowed agent-facing capabilities

The initial Runes Shield interface exposes small, stable, JSON-friendly commands and scripts:

- `runes capabilities --json`
  - discover available Runes capabilities and safety boundaries
- `runes guidance --json`
  - read agent-facing policy, invocation rules, and usage guidance
- `runes offer --text "..." --json`
  - deterministically decide whether Hermes-agent should ask the user about creating a governed proposal
- `tools/runes/trial_run_m21_4.py --json`
  - run an isolated multi-proposal sandbox trial with approved / rejected / draft visibility checks
- `tools/runes/promotion_plan_m21_5.py --json`
  - generate a human-only curated promotion dry-run plan and preview

Planned future commands remain outside the completed M21 P0 boundary baseline:

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

Hermes-agent should only call future proposal-writing commands after user consent.

### M21 milestone breakdown

#### M21.1 Runes Shield Contract

Status: PASS

Goal:

- Define Runes Shield as the official P0 agent-facing boundary.
- Replace earlier Facade / Gate / Field naming with Runes Shield.
- Document allowed and forbidden Hermes-agent behaviors.
- Document human-only approval boundaries.
- Establish the canonical P0 Markdown entry path instead of relying on incidental local wiki files.

Verified files:

- `wiki/hermes_runes_index.md`
- `wiki/_system/runes_shield_contract.md`
- `wiki/_system/runes_invocation_policy.md`
- `wiki/_system/runes_agent_guidance.md`

Result:

- M21.1a Runes Shield `_system` documents: PASS.
- M21.1b Canonical Runes Markdown Architecture: PASS.

#### M21.2 Runes Shield capabilities / guidance CLI

Status: PASS / read-only / smoke verified

Goal:

- Provide simple read-only CLI/JSON endpoints for agent discovery.
- Keep implementation local, deterministic, and easy to inspect.

Verified commands:

```bash
bin/runes capabilities --json
bin/runes guidance --json
python3 tools/runes/smoke_runes_shield.py
```

Success criteria:

- Output is stable enough for Hermes-agent to consume.
- Output includes capability list, safety boundaries, write limitations, and human-only operations.
- No proposal creation, trusted memory mutation, or DB mutation occurs.

#### M21.3 Agent interaction prompt pattern

Status: PASS / read-only / smoke verified

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

Verified command:

```bash
bin/runes offer --text "..." --json
python3 tools/runes/smoke_runes_shield.py
```

Success criteria:

- Hermes-agent can proactively ask whether to create a governed proposal.
- Hermes-agent does not silently persist knowledge.
- User consent is required before future `runes propose`.
- Casual chat, secret-bearing content, and unverified speculation do not trigger proposal offers.

#### M21.4 Multi-proposal P0 trial run

Status: PASS / sandbox-write-only / smoke verified

Goal:

- Validate the governed proposal flow with mixed proposal states without mutating real trusted wiki content or database state.

Verified command:

```bash
python3 tools/runes/trial_run_m21_4.py --json
python3 tools/runes/smoke_runes_shield.py
```

Verified scenario:

1. Create proposal A in sandbox.
2. Create proposal B in sandbox.
3. Create proposal C in sandbox.
4. Approve A in sandbox.
5. Reject B in sandbox.
6. C remains draft in sandbox.
7. Import approved A into sandbox trusted index.
8. Recall approved content from sandbox trusted index.
9. Verify rejected and draft content are not visible as trusted memory.
10. Run smoke/regression checks.

Success criteria:

- Approved proposal becomes retrievable sandbox trusted evidence.
- Rejected proposal remains excluded.
- Draft proposal remains excluded.
- Trusted sandbox index contains only the approved proposal.
- Real trusted wiki is not mutated.
- Real database state is not mutated.
- Real forge inbox is not mutated.

#### M21.5 Human-only curated promotion path

Status: PASS / dry-run-only / smoke verified

Goal:

- Define a dry-run path for promoting reviewed proposals into curated wiki notes.
- Keep promotion human-controlled during P0.

Verified command:

```bash
python3 tools/runes/promotion_plan_m21_5.py --workspace tmp/runes-trial/m21-4 --json
python3 tools/runes/smoke_runes_shield.py
```

Verified behavior:

- Runes may generate a promotion plan and preview.
- Human performs or approves final promotion.
- Hermes-agent may request status or evidence, but may not perform direct promotion.

Success criteria:

- Approved proposal can be converted into a curated Markdown promotion plan without giving Hermes-agent direct write authority over trusted wiki structure.
- `human_only: true`.
- `agent_may_promote: false`.
- `curated_write_performed: false`.
- `database_mutated: false`.
- `proposal_state_mutated: false`.

#### M21.6 P0 status recap / roadmap lock

Status: PASS / roadmap lock

Goal:

- Record M21.1 through M21.5 as the verified Runes Shield P0 / trial-run boundary baseline.
- Link roadmap state to a dedicated verification record.
- Make the next implementation stage explicit.

Verified record:

```text
wiki/k6-freelancer/verification-m21-runes-shield.md
```

Result:

- M21 Runes Shield P0 / trial-run boundary is established.
- Hermes-agent can invoke Runes discovery, guidance, offer-policy, sandbox proposal trial, and human-only promotion dry-run capabilities.
- Hermes-agent still cannot directly write trusted wiki content, approve / reject / promote proposals, mutate proposal states, mutate DB/index state, or treat draft / rejected content as trusted memory.

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

M21 P0 is complete because Hermes-agent can:

1. Discover Runes capabilities through Runes Shield.
2. Understand the boundary between allowed invocation and forbidden direct mutation.
3. Ask the user whether durable knowledge should be solidified.
4. Keep governed proposal creation behind explicit user consent and future controlled interfaces.
5. Run multi-proposal sandbox verification with approved / rejected / draft isolation.
6. Generate human-only curated promotion dry-run plans.
7. Avoid direct manipulation of internal Markdown files, proposal state, importer artifacts, and database content.
8. Bootstrap from `wiki/hermes_runes_index.md` and the canonical Runes Shield `_system` files without depending on incidental local wiki documents.

### Next stage after M21

The next implementation stage should move from verified sandbox / dry-run behavior toward governed proposal creation while preserving:

- explicit user consent,
- human-only approval / rejection / promotion,
- no autonomous trusted memory writer,
- no direct Hermes-agent mutation of internal Markdown / DB state,
- smoke/regression checks before any trusted memory change.

---
