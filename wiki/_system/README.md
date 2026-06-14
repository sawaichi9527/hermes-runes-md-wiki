# Hermes Runes System Policy Index

Status: runtime-clean-seed policy baseline  
Scope: Hermes Runes MD Wiki system governance

## Purpose

`wiki/_system/` contains canonical governance policy for Hermes Runes MD Wiki.

These files are intended for:

- Hermes Agent
- compatible future agents
- the human owner/developer
- direct tooling and smoke verification

Normal user knowledge must not be stored under `_system/`.

## Hermes Runes Role

Hermes Runes MD Wiki is a governed personal RAG memory substrate.

It provides:

- Markdown source-of-truth
- deterministic policy and index reads
- governed wiki mutations
- RAG recall evidence
- import / embedding lifecycle
- diagnostics and consistency checks

It does not replace agent decision-making.

## Required Policy Read Order

Agents should decipher this policy bundle before performing Hermes Runes operations:

1. `wiki/_system/README.md`
2. `wiki/_system/memory-policy.md`
3. `wiki/_system/source-priority.md`
4. `wiki/_system/access-boundary.md`
5. `wiki/_system/wiki-operation-policy.md`
6. `wiki/_system/default-wiki-seed-layout.md`
7. `wiki/_system/opc-workspace-overlay-policy.md`
8. `wiki/_system/agent-operation-guide.md`
9. `wiki/_system/ingestion-policy.md`
10. `wiki/_system/security-policy.md`
11. `wiki/_system/observation-policy.md`
12. `wiki/_system/developer-policy.md`
13. `wiki/README.md`
14. `wiki/hermes_runes_index.md`

## Command Vocabulary

| Rune term | Plain meaning | Scope |
|---|---|---|
| `decipher` | deterministic read | Read policy, guides, indexes, and objective README files. |
| `forge` | governed write | Create, update, rename, archive, or otherwise mutate Markdown wiki structure. |
| `evoke` | recall / retrieve | Query indexed personal RAG memory. |
| `inscribe` | index / embed | Import Markdown source-of-truth into searchable PostgreSQL / FTS / vector indexes. |
| `probe` | diagnose / check | Check retrieval, context, links, indexes, metadata, locks, policy, and consistency. |
| `chronicle` | change history | Record structural Markdown wiki changes, normally written by `forge`. |

Rune terms are interface names. Documentation and CLI help must include plain-language meaning.

## Runtime Wiki Layout

- `default-wiki-seed-layout.md`
  - Defines the canonical top-level wiki layers:
    - `wiki/_system/`
    - `wiki/<workspace>/`
    - `wiki/*.md`
  - Defines first-bootstrap workspace suggestion behavior.
  - Keeps developer history outside runtime wiki memory under `dev/`.
- `opc-workspace-overlay-policy.md`
  - Defines optional OPC profile memory organization under `wiki/<workspace>/opc/`.
  - Preserves the default single-agent workspace seed.
  - Keeps OPC support as an optional workspace overlay, not a runtime requirement.

## Runes Shield Discovery

- `runes_shield_contract.md`
  - Defines the governed invocation boundary between agents and Hermes Runes MD Wiki.
- `runes_invocation_policy.md`
  - Defines how controlled Runes Shield operations should be invoked.
- `runes_agent_guidance.md`
  - Defines agent-facing operating guidance for proposal, review, approval, and trusted-memory boundaries.

## Developer Boundary

Developer history, old milestone records, beta observations, trial evidence, and sample fixtures belong outside runtime wiki memory:

```text
dev/wiki-history/
dev/docs/
```

Do not import `dev/` as runtime user memory by default.

## Non-goals

Hermes Runes is not:

- an enterprise multi-user CMS
- a distributed cloud memory platform
- a full autonomous self-modifying agent framework
- a replacement for agent judgment

## Change Log

- 2026-06-01: Initial P0 system policy index.
- 2026-06-05: Registered default wiki seed layout policy in the required policy read order.
- 2026-06-08: Cleaned runtime seed boundary and moved developer history outside `wiki/`.
- 2026-06-14: Registered optional OPC workspace overlay policy in the required policy read order.

## Runtime Seed Boundary

`wiki/_system/` is the runtime system-policy seed for normal users and agent-facing guidance.

Milestone implementation records and historical P0/M-series development notes are retained under:

```text
dev/wiki-history/_system/
```

Normal users and fresh Open Beta testers should not need to read or import `dev/wiki-history/_system/` for routine operation.

The runtime `_system` directory should remain focused on active policies, source priorities, invocation boundaries, memory rules, observation policy, and wiki operation guidance.
