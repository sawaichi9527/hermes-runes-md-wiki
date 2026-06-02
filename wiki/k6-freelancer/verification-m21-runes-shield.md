# M21 Runes Shield Verification Record

## V-20260602-M21 Runes Shield P0 / Trial Run Boundary

Status: PASS / P0 boundary baseline established
Scope: Hermes Runes MD Wiki / Runes Shield / agent-facing governed memory boundary
Date: 2026-06-02

## Summary

Runes Shield is verified as the governed invocation boundary between Hermes-agent and Hermes Runes MD Wiki for the P0 / trial-run stage.

The verified baseline allows Hermes-agent to discover Runes capabilities, read invocation guidance, classify whether durable user-provided knowledge should be offered for proposal creation, run isolated sandbox proposal-state trials, and generate human-only curated promotion plans.

The verified baseline does not allow Hermes-agent to directly write trusted Markdown wiki content, mutate proposal states, approve or reject proposals, promote curated notes, write PostgreSQL / FTS / pgvector records, rebuild importer state, or treat draft / rejected proposal content as trusted memory.

## Verified milestones

### M21.1a Runes Shield `_system` documents

Status: PASS

Verified files:

```text
wiki/_system/runes_shield_contract.md
wiki/_system/runes_invocation_policy.md
wiki/_system/runes_agent_guidance.md
```

Verified result:

- Runes Shield is documented as the official P0 agent-facing boundary.
- Hermes-agent must use Runes-provided interfaces.
- Hermes-agent must not directly operate internal Markdown wiki files, proposal states, importer artifacts, or database content.
- Human-only approval, rejection, and promotion boundaries are explicit.

### M21.1b Canonical Runes Markdown Architecture

Status: PASS

Verified files:

```text
wiki/hermes_runes_index.md
wiki/_system/runes_shield_contract.md
wiki/_system/runes_invocation_policy.md
wiki/_system/runes_agent_guidance.md
```

Verified result:

- P0 / trial-run bootstrap no longer depends on incidental local wiki documents.
- Hermes-agent can start from the canonical index and `_system` files.
- Arbitrary local wiki documents are not operational authority unless explicitly promoted into the canonical architecture.

### M21.2 Runes Shield capabilities / guidance CLI

Status: PASS / read-only / smoke verified

Verified commands:

```bash
bin/runes capabilities --json
bin/runes guidance --json
python3 tools/runes/smoke_runes_shield.py
```

Verified result:

- `capabilities` emits stable JSON discovery output.
- `guidance` emits stable JSON invocation guidance.
- Capability list, canonical files, forbidden operations, and human-only operations are visible to agent-facing callers.
- M21.2 did not create proposals, mutate trusted memory, or write database state.

### M21.3 Agent interaction offer-policy

Status: PASS / read-only / smoke verified

Verified command:

```bash
bin/runes offer --text "..." --json
python3 tools/runes/smoke_runes_shield.py
```

Verified result:

- Durable knowledge signals can trigger `should_offer: true`.
- Casual chat, secret-bearing content, and unverified speculation trigger `should_offer: false`.
- `offer` only recommends whether Hermes-agent should ask the user.
- `offer` does not create proposals and does not mutate memory.
- User consent remains required before any future proposal creation command.

### M21.4 Multi-proposal P0 sandbox trial

Status: PASS / sandbox-write-only / smoke verified

Verified command:

```bash
python3 tools/runes/trial_run_m21_4.py --json
python3 tools/runes/smoke_runes_shield.py
```

Verified scenario:

```text
create proposal A/B/C as draft in sandbox
approve A in sandbox
reject B in sandbox
leave C draft in sandbox
import approved A into sandbox trusted index
recall only sandbox trusted index
verify rejected and draft markers are excluded
```

Verified result:

- Approved proposal A is visible in the sandbox trusted index.
- Rejected proposal B is excluded from trusted visibility.
- Draft proposal C is excluded from trusted visibility.
- Trusted sandbox index contains only the approved proposal.
- Real trusted wiki content was not mutated.
- Real database state was not mutated.
- Real forge inbox was not mutated.

### M21.5 Human-only curated promotion path

Status: PASS / dry-run-only / smoke verified

Verified command:

```bash
python3 tools/runes/promotion_plan_m21_5.py --workspace tmp/runes-trial/m21-4 --json
python3 tools/runes/smoke_runes_shield.py
```

Verified result:

- Approved sandbox proposal can be converted into a curated-note promotion plan and preview.
- Promotion plan is dry-run only.
- `human_only: true`.
- `agent_may_promote: false`.
- `curated_write_performed: false`.
- `database_mutated: false`.
- `proposal_state_mutated: false`.
- Human final action is explicitly required before any curated wiki write.

## Final M21.6 baseline status

Status: PASS / roadmap lock candidate

Verified boundary:

```text
Hermes-agent may invoke the runes, but must never breach the shield.
```

Allowed during P0 / trial run:

- Discover Runes capabilities through `runes capabilities --json`.
- Read Runes guidance through `runes guidance --json`.
- Classify whether to ask the user about durable knowledge solidification through `runes offer --json`.
- Run sandbox-only multi-proposal state trial.
- Generate human-only curated promotion dry-run plans.

Forbidden during P0 / trial run:

- Direct trusted wiki writes by Hermes-agent.
- Direct proposal approve / reject / promote by Hermes-agent.
- Direct database mutation by Hermes-agent.
- Direct importer artifact mutation by Hermes-agent.
- Treating draft or rejected proposal content as trusted memory.
- Autonomous trusted memory writer mode.

## Current limitation / next stage

M21 establishes the P0 Runes Shield boundary and dry-run/sandbox behavior. It does not yet implement a production `runes propose` writer or real human-approved promotion command.

The next stage should move carefully from sandbox/dry-run into governed proposal creation while preserving:

- explicit user consent,
- human-only approval / rejection / promotion,
- no autonomous trusted memory writer,
- no direct Hermes-agent mutation of internal Markdown / DB state,
- smoke/regression checks before any trusted memory change.

## Result

M21 Runes Shield P0 / trial-run boundary is considered verified and ready to be used as the baseline for the next implementation stage.
