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

#### M21.2 Runes Shield capabilities / guidance CLI

Status: PASS / read-only / smoke verified

#### M21.3 Agent interaction prompt pattern

Status: PASS / read-only / smoke verified

#### M21.4 Multi-proposal P0 trial run

Status: PASS / sandbox-write-only / smoke verified

#### M21.5 Human-only curated promotion path

Status: PASS / dry-run-only / smoke verified

#### M21.6 P0 status recap / roadmap lock

Status: PASS / roadmap lock

---

## M22 Proposal Governance Loop

Status: PASS / P0 proposal governance loop established
Priority: P0
Verification record: `wiki/k6-freelancer/verification-m22-proposal-loop.md`

### Purpose

M22 extends the Runes Shield boundary from discovery/guidance into a governed proposal workflow suitable for P0 Hermes-agent trial-run usage.

The goal is to let Hermes-agent create, inspect, validate, and plan proposal cleanup operations without granting direct trusted-memory authority.

### M22 verified scope

The following proposal-governance loop is now implemented and verified:

- governed draft proposal creation
- proposal list inspection
- proposal show inspection
- proposal hygiene reporting
- proposal cleanup-plan dry-run generation
- CLI wrappers for hygiene and cleanup-plan

### M22 milestone breakdown

#### M22.1 Governed draft proposal writer

Status: PASS / draft-write-only / smoke verified

Verified command:

```bash
bin/runes propose --title "..." --text "..." --consent "go" --json
```

Verified properties:

- explicit user consent required
- creates draft proposal only
- trusted memory not created
- approval not executed
- promotion not executed
- importer/database not mutated

---

#### M22.2 Proposal list/show inspection

Status: PASS / read-only / smoke verified

Verified commands:

```bash
bin/runes proposal list --json
bin/runes proposal show --id "..." --json
```

Verified properties:

- proposal inspection without mutation
- no trusted-memory mutation
- no DB/importer mutation

---

#### M22.3 Proposal hygiene report

Status: PASS / read-only / smoke verified

Verified command:

```bash
python3 tools/runes/proposal_hygiene_m22_3.py --json
```

Verified properties:

- detects state mismatches
- detects metadata hygiene issues
- no mutation performed

---

#### M22.3b Hygiene CLI wiring

Status: PASS / read-only / smoke verified

Verified command:

```bash
bin/runes proposal hygiene --json
```

---

#### M22.4 Human cleanup plan dry-run

Status: PASS / dry-run-only / smoke verified

Verified command:

```bash
python3 tools/runes/cleanup_plan_m22_4.py --json
```

Verified properties:

- hygiene issues converted into planned cleanup actions
- execution disabled
- human review required
- no mutation performed

---

#### M22.5 Cleanup-plan CLI wiring

Status: PASS / dry-run-only / smoke verified

Verified command:

```bash
bin/runes proposal cleanup-plan --json
```

Verified properties:

- cleanup plan exposed through stable agent-facing CLI
- execution disabled
- agent may not execute cleanup
- no mutation performed

---

### M22 governance boundary

The following boundaries remain intentionally enforced:

- Hermes-agent must use Runes Shield interfaces only.
- Hermes-agent must not directly mutate wiki/.
- Hermes-agent must not directly approve proposals.
- Hermes-agent must not directly reject proposals.
- Hermes-agent must not directly promote curated notes.
- Hermes-agent must not autonomously execute cleanup.
- Draft/rejected proposals are not trusted memory.
- Human approval is required before trusted-memory creation.

### Explicitly not implemented in M22

The following operations intentionally remain outside the P0 boundary:

- approve execution
- reject execution
- curated promotion execution
- cleanup execution
- importer/index rebuild execution
- direct DB mutation
- autonomous trusted-memory mutation

### M22 result

M22 establishes a stable P0 proposal-governance loop suitable for:

- governed Hermes-agent proposal creation
- proposal inspection
- proposal hygiene validation
- human cleanup planning

without granting direct trusted-memory authority to Hermes-agent.

### Next stage after M22

The next stage should focus on:

- human approval workflow design
- human rejection workflow design
- human-reviewed state transition dry-run
- approval/rejection audit evidence

while preserving:

- explicit user consent
- human-only approval/rejection/promotion
- no autonomous trusted-memory mutation
- no direct Hermes-agent wiki/DB control

---