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

## S7 — Read-only PLUR discovery / status check design

S7 is design-only for now. It should define how a future read-only status check may work, but v0.7.4-dev should not add a new runtime helper until there is a clear need.

A future status check, if implemented, should only inspect safe local availability signals:

- Python module names discoverable through a non-invasive check.
- CLI command names discoverable on `PATH`.
- PLUR-related environment variable prefixes, without printing values.

It must not:

- import PLUR modules merely for discovery
- execute PLUR commands
- read PLUR memory
- write PLUR memory
- print environment variable values
- mutate Hermes Agent settings
- become part of every normal Hermes Agent interaction

## S8 — Runtime memory provider abstraction / Noop provider design

S8 is design-only for now.

The intended future provider boundary is intentionally tiny:

```text
RuntimeMemoryProvider.status() -> ProviderStatus
```

Potential providers:

- `noop`: safe fallback, always available, no memory read/write.
- `plur`: read-only detector first; no memory read/write until explicitly approved in a later step.

The Noop provider is a design requirement to preserve detachable behavior when PLUR is absent, disabled, unavailable, or intentionally not selected.

## S9 — PLUR memory schema mapping design

S9 is design-only for now.

The schema should map the runtime roles:

```text
engram     = compact behavioral/runtime memory
episode    = timestamped history, not injected by default
checkpoint = current working state for recovery/handoff
candidate  = proposed memory requiring user approval before forge
```

Global rules:

- scope is required
- episode injection is disabled by default
- governance hints require source pointer and `last_verified_at` when available
- candidates do not auto-promote
- stale checkpoints are marked `superseded` or `inactive` instead of heavy purge
- existing deployed PLUR memory is not bulk migrated, bulk deleted, or assumed canonical

## S10 — Read-only PLUR context summary pause

S10 is paused.

The value of a dedicated PLUR read-only context summary is not clear enough yet. Until there is a concrete use case, v0.7.4-dev should not add a context-summary helper, automatic prompt injection, every-turn PLUR scan, or additional Hermes Agent burden.

Current decision:

```text
Do not implement S10.
Do not add a read-only PLUR context summary tool.
Do not inject PLUR context by default.
Revisit only if a concrete user-visible failure shows native Hermes Agent runtime memory is insufficient.
```

## S11 — Candidate dry-run flow design

S11 is design-only.

The goal is to define a plain candidate proposal format before any runtime integration exists. A candidate dry-run is only a proposal that says, "this information may deserve formal Runes Wiki memory later." It does not write PLUR, write Runes Wiki, run forge, or promote anything automatically.

Candidate dry-run flow:

```text
Current conversation / runtime observation / possible PLUR checkpoint
        ↓
Hermes Agent or Lark bot notices a possible durable memory candidate
        ↓
Agent presents a candidate proposal only
        ↓
User accepts, rejects, or asks to revise
        ↓
Only after explicit approval can a future Runes Shield / forge path be used
```

Suggested candidate card:

```text
Candidate:
- Type: decision | preference | project-state | warning | procedure | open-question
- Scope: <project/workspace/user scope>
- Source: current-conversation | user-instruction | PLUR-checkpoint | Runes-Wiki-reference | other
- Proposed target: wiki/<workspace>/... or undecided
- Proposal: <short memory statement>
- Why preserve: <why this should survive the current session>
- Risk: low | medium | high
- Approval state: pending
- Writes performed: none
```

Rules:

- Candidate dry-run is proposal-only.
- No wiki write occurs during dry-run.
- No PLUR write occurs during dry-run.
- No PLUR read is required for the design.
- No automatic promotion is allowed.
- User approval is necessary but not equal to forge completion.
- Runes Shield remains the protected forge gate if the candidate later becomes a durable wiki change.

## S12 — Smoke / verification / docs sync design

S12 is design-only and is about keeping the repo honest.

It does not add a new smoke suite. It defines the manual verification checklist for this PLUR bridge line:

```bash
cd ~/workspace/hermes-runes-md-wiki
git pull
git status
./bin/runes-wiki-migration-guard plan --no-fetch
./bin/hermes-memory-smoke
```

Expected result:

```text
git status clean
migration guard SAFE
Core FTS smoke PASS
no PLUR runtime helper required
no PLUR smoke required
embedding profile SKIP remains acceptable when not installed
```

Documentation consistency checks:

- `CHANGELOG.md` says S10 is paused and S11-S12 are design-only.
- `dev/wiki-history/k6-freelancer/next-actions.md` points to design-only S11-S12, not runtime implementation.
- No documentation claims PLUR memory was read, written, migrated, deleted, or promoted.
- No documentation claims a new Hermes Agent tool was added.
- No documentation treats PLUR as canonical memory.

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
- S7-S9 remain design-only until a future implementation is explicitly approved.
- S10 is paused because value is not clear enough.
- S11-S12 are design-only and add no runtime helper.
- No new runtime helper is required for normal Hermes Runes MD Wiki use.
