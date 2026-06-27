# PLUR Runtime Memory Bridge

Status: PLANNED / v0.7.4-dev correction scope  
Scope: optional PLUR reintegration for single-agent Hermes usage

## Purpose

v0.7.4-dev focuses on reintroducing PLUR as a detachable runtime persistent memory bridge for the current single-agent / agent-agnostic mainline.

The goal is cross-session continuity for Hermes Agent / Lark bot usage and future bounded subagent handoff, without turning PLUR into the canonical memory authority and without making Hermes Agent native configuration heavily customized for this repository.

## Operating boundary

```text
PLUR = optional runtime persistent working memory
Runes Wiki = governed canonical long-term memory source
Runes Shield = protected forge gate / operation protection layer
Hermes Agent / Lark bot = candidate proposer and task reasoner
User = human-in-the-loop approval authority
```

PLUR may help the agent remember working state, stable interaction preferences, governance hints, and short checkpoints. It must not directly forge Markdown wiki memory, bypass user approval, override Runes Wiki canonical memory, or require invasive Hermes Agent core changes.

## S1 — Detachable PLUR integration

PLUR integration must be optional.

PASS criteria:

- Hermes Runes MD Wiki remains usable without PLUR installed.
- Existing import, recall, smoke, migration guard, and governed wiki operation documentation remain valid without PLUR.
- PLUR failure or absence degrades to no runtime bridge instead of blocking core Runes operation.
- The integration does not require patching Hermes Agent core.

## S2 — Minimal Hermes Agent native customization

PLUR may be enabled through the normal Hermes Agent plugin/provider path, but the Runes project must not require deep Hermes Agent native customization.

Allowed:

- Enable an existing PLUR plugin/provider when available.
- Store small runtime memory records such as engrams, checkpoints, governance hints, and candidates.
- Let Hermes Agent call Runes/Shield/CLI interfaces when user-approved work requires it.

Avoid:

- Patching Hermes Agent core.
- Depending on private Hermes Agent internals for memory, compression, Kanban, or subagent behavior.
- Making Hermes Agent configuration usable only for Hermes Runes MD Wiki.
- Adding daemon, queue, telemetry, enterprise workflow, or multi-profile mesh requirements.

## S3 — PLUR memory role and source priority

PLUR is runtime memory, not canonical truth.

Suggested priority when sources conflict:

```text
1. Current user instruction / current conversation
2. Hermes Agent runtime memory
   - native memory
   - PLUR engrams / checkpoints
   - active session state
   - not canonical long-term truth
3. Hermes Runes MD Wiki
   - governed canonical long-term memory evidence
4. Third-party RAG / notes / Obsidian
5. Web / external public sources
```

Hermes Agent performs final source comparison. Runes provides governed evidence and safe operations. PLUR provides runtime continuity only.

## S4 — Engram / episode / checkpoint / candidate policy

PLUR memory should remain compact and personal-use oriented.

Engram:

- Stable or semi-stable short memory that may influence behavior.
- Examples: user preference, interaction rule, active architecture direction, governance hint.

Episode:

- Timestamped history or operational timeline.
- Examples: a test was run, a Lark bot interaction happened, a gateway issue was observed.
- Episodes must not be injected by default and must not automatically become formal memory.

Checkpoint:

- Current working state for session recovery or handoff.
- Short-lived or supersedable.

Candidate:

- A proposed memory item that Hermes Agent / Lark bot believes may deserve formal forge.
- Requires explicit user approval before Runes Shield can perform a protected forge operation.

## S5 — Human-in-the-loop forge candidate flow

PLUR can hold candidates, but cannot promote them by itself.

```text
PLUR checkpoint / engram / candidate
        ↓
Hermes Agent / Lark bot proposes formal memory
        ↓
User explicitly approves forge
        ↓
Runes Shield protects the operation
        ↓
Markdown Runes Wiki is updated
        ↓
PLUR candidate is marked forged and keeps only a short pointer
```

Forbidden:

- PLUR directly writes `wiki/**/*.md`.
- PLUR episode automatically becomes canonical memory.
- Subagent directly forges Runes Wiki memory.
- Hermes Agent forges memory without explicit user approval.
- Runes Shield is treated as the memory judge; it is the protected forge gate.

## S6 — Minimal PLUR memory hygiene

Personal-use hygiene should stay lightweight and cheap.

Rules:

1. Scope is required for PLUR records.
2. Episode injection is disabled by default.
3. Governance hints require a source pointer and `last_verified_at`.
4. Candidates do not auto-promote.
5. Stale checkpoints are marked `superseded` or `inactive`; heavy purge is not required.
6. Existing deployed PLUR memory is treated as pre-existing runtime state and must not be bulk migrated, bulk deleted, or assumed canonical.

Non-goals:

- Heavy LLM judge.
- Multi-level approval workflow.
- Enterprise governance engine.
- Every-turn full-memory scan.
- Automatic policy mutation.
- Automatic Runes Wiki writes.

## Existing deployed PLUR memory caution

v0.7.4-dev is being developed after Hermes Agent + Hermes Runes MD Wiki + PLUR were already deployed together.

Therefore:

- Existing PLUR memory may already contain runtime rules, checkpoints, or old observations.
- Existing PLUR memory must be treated as non-authoritative unless backed by current user instruction or Runes Wiki evidence.
- The first integration pass should inspect/status-check PLUR gently, not rewrite it.
- Any cleanup should prefer marking stale records as superseded over deletion.
- No existing PLUR record should be promoted into Runes Wiki without human-in-the-loop approval.

## Verification target

A v0.7.4-dev verification pass should confirm:

- PLUR is optional and detachable.
- No Hermes Agent core patch is required.
- No Runes Wiki write can occur from PLUR alone.
- Candidate forge requires explicit user approval.
- Existing PLUR memory is not bulk migrated or deleted.
- Core Runes workflows remain usable when PLUR is unavailable.
