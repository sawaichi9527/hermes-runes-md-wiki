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
- `runes guidance --json`
- `runes offer --text "..." --json`
- `tools/runes/trial_run_m21_4.py --json`
- `tools/runes/promotion_plan_m21_5.py --json`

### M23 Runes Attunement Workflow / Dry-run

Status: ACTIVE / HUMAN-READABLE PREVIEW ADDED
Priority: P0
Verification record: `wiki/k6-freelancer/verification-m23-runes-attunement.md`

### Goal

Provide a lightweight personal-use human-governed proposal attunement workflow with readable dry-run previews while preserving strict no-mutation boundaries.

### M23 milestone status

- M23.1 Runes Attunement Concept Lock: PASS
- M23.2 Attunement dry-run CLI: PASS
- M23.3 Human-readable Attunement Preview: PASS

### M23.3 additions

M23.3 upgrades the non-JSON attunement preview from a minimal status line into a human-readable review summary.

The readable preview now includes:

- proposal ID
- proposal title
- current state
- target state
- attunement meaning
- promotion boundary reminder
- mutation boundary summary
- attunement trail preview
- human confirmation reminder

### M23 boundary invariants

M23.3 still preserves:

- dry-run only
- no proposal mutation
- no trusted wiki mutation
- no database mutation
- no importer mutation
- no automatic promotion execution

### Human-readable preview philosophy

The readable preview is intended for:

- human review
- reasoning alignment
- memory governance clarity
- proposal risk visibility
- future promotion discussion

It is intentionally not:

- a workflow engine
- an approval executor
- a background automation system
- an enterprise review queue

---

---

## M23.5 Roadmap / Verification Lock

Status: PASS / STABLE P0 GOVERNED ATTUNEMENT BASELINE

Locked milestones:

- M23.1 Runes Attunement Concept Lock: PASS
- M23.2 Attunement dry-run CLI: PASS
- M23.3 Human-readable Attunement Preview: PASS
- M23.4 Attunement smoke test: PASS
- M23.5 Roadmap / verification lock: PASS

Locked boundaries:

- approve execution: not implemented
- reject execution: not implemented
- supersede execution: not implemented
- cleanup execution: not implemented
- promotion execution: not implemented
- trusted wiki mutation: forbidden
- direct database mutation: forbidden
- importer mutation: forbidden
- autonomous attunement execution: forbidden
- autonomous trusted-memory mutation: forbidden

Current baseline:

M23 Runes Attunement Workflow / Dry-run:
PASS / stable P0 governed attunement baseline

---

## M24 Runes Attunement Trail / Dry-run

Status: DESIGN LOCK / DRY-RUN SCOPE

Verification record:

- `wiki/k6-freelancer/verification-m24-attunement-trail.md`

Goal:

Define the append-only attunement trail model for human-governed proposal decisions while preserving strict no-mutation boundaries.

M24.1 scope:

- attunement trail terminology
- event schema design
- append-only trail principle
- dry-run-only boundary
- no trusted wiki mutation
- no database mutation
- no autonomous attunement execution

M24.1 non-goals:

- no real trail write
- no approve execution
- no reject execution
- no supersede execution
- no proposal state mutation
- no trusted wiki mutation
- no DB mutation
- no importer mutation
- no promotion execution

Current milestone:

- M24.1 Runes Attunement Trail Design Lock: PASS / design locked

Next:

- M24.2 Attunement trail dry-run CLI

---

## M24.3 Attunement Trail Markdown Preview

Status: PASS / PREVIEW-ONLY

Scope:

- Add Markdown rendering for attunement trail event previews.
- Keep JSON and terminal-readable previews intact.
- Preserve dry-run-only behavior.
- Do not write append-only trail files yet.

Boundary:

- no trail file write
- no proposal state mutation
- no trusted wiki mutation
- no database mutation
- no importer mutation
- no promotion execution

Current milestone:

- M24.3 Attunement Trail Markdown Preview: PASS / preview-only

Next:

- M24.4 Attunement trail smoke test


---

## M24.4 Attunement Trail Smoke Test

Status: PASS / REGRESSION BASELINE

Scope:

- Verify trail dry-run JSON payload.
- Verify terminal-readable trail preview renderer.
- Verify Markdown trail preview renderer.
- Verify no trail/proposal/wiki/database/importer mutation boundary.

Boundary:

- no trail file write
- no proposal state mutation
- no trusted wiki mutation
- no database mutation
- no importer mutation
- no promotion execution

Current milestone:

- M24.4 Attunement Trail Smoke Test: PASS / regression baseline

Next:

- M24.5 Roadmap / verification lock


---

## M24.5 Roadmap / Verification Lock

Status: PASS / STABLE GOVERNED ATTUNEMENT-HISTORY BASELINE

Locked milestones:

- M24.1 Runes Attunement Trail Design Lock: PASS
- M24.2 Attunement trail dry-run CLI: PASS
- M24.3 Attunement trail Markdown preview: PASS
- M24.4 Attunement trail smoke test: PASS
- M24.5 Roadmap / verification lock: PASS

Locked boundaries:

- append-only design only
- trail write execution: not implemented
- approve execution: not implemented
- reject execution: not implemented
- supersede execution: not implemented
- proposal mutation: forbidden
- trusted wiki mutation: forbidden
- direct database mutation: forbidden
- importer mutation: forbidden
- promotion execution: forbidden
- autonomous attunement execution: forbidden
- autonomous trusted-memory mutation: forbidden

Current baseline:

M24 Runes Attunement Trail / Dry-run:
PASS / stable governed attunement-history baseline

Next:

- M25 Curated promotion patch preview / dry-run


---

## M25 Curated Promotion Patch Preview / Dry-run

Status: DESIGN LOCK / DRY-RUN CLI BASELINE

Verification record:

- `wiki/k6-freelancer/verification-m25-curated-promotion-preview.md`

Goal:

Define and implement a preview-only curated promotion patch model that lets Hermes-agent recommend Markdown wiki changes without mutating trusted memory.

Completed milestones:

- M25.1 Curated Promotion Patch Design Lock: PASS
- M25.2 Promotion Patch Dry-run CLI: PASS

Locked boundaries:

- proposal is not trusted memory
- patch preview is not wiki mutation
- forge preview is not promotion execution
- no trusted wiki mutation
- no proposal state mutation
- no database mutation
- no importer mutation
- no autonomous promotion execution

Next:

- M25.3 Promotion patch smoke test


---

## M25.3 Promotion Patch Smoke Test

Status: PASS / REGRESSION BASELINE

Verification target:

- `tools/runes/smoke_m25_3_promotion_patch.py`

Scope:

- validate promotion patch helper payload
- validate JSON preview
- validate Markdown preview
- validate CLI route through `bin/runes promotion preview`
- validate target Markdown hash remains unchanged
- validate no trusted wiki mutation
- validate no database mutation
- validate no importer mutation
- validate no promotion execution

Boundary:

M25.3 is still dry-run only. It does not apply any promotion patch.

Next:

- M25.4 Roadmap / verification lock


---

## M25.4 Roadmap / Verification Lock

Status: PASS / M25 STABLE DRY-RUN BASELINE

Verification record:

- `wiki/k6-freelancer/verification-m25-curated-promotion-preview.md`

Locked milestone:

```text
M25 Curated Promotion Patch Preview / Dry-run:
PASS / stable governed forge-preview baseline
```

Completed M25 scope:

- M25.1 Curated Promotion Patch Design Lock: PASS
- M25.2 Promotion Patch Dry-run CLI: PASS
- M25.3 Promotion Patch Smoke Test: PASS
- M25.4 Roadmap / Verification Lock: PASS

Locked boundaries:

- proposal is not trusted memory
- patch preview is not wiki mutation
- forge preview is not forge execution
- promotion preview is not promotion execution
- no trusted wiki mutation
- no proposal state mutation
- no database mutation
- no importer mutation
- no autonomous promotion execution

Not implemented in M25:

- actual patch apply
- trusted wiki write
- proposal promotion state mutation
- database mutation
- importer/index mutation
- autonomous trusted-memory promotion

Next possible milestone:

- M26 Human-approved Promotion Apply / Dry-run-to-Apply Boundary

