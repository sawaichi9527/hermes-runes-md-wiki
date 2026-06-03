# Hermes Runes System Policy Index

Status: P0 policy baseline  
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

It does not replace Hermes Agent decision-making.

Hermes Agent remains responsible for comparing Hermes Runes evidence with current user instructions, native memory, third-party RAG / notes, Obsidian, web search, and other sources.

## Required Policy Read Order

Hermes Agent should decipher this policy bundle before performing Hermes Runes operations:

1. `wiki/_system/README.md`
2. `wiki/_system/memory-policy.md`
3. `wiki/_system/source-priority.md`
4. `wiki/_system/access-boundary.md`
5. `wiki/_system/wiki-operation-policy.md`
6. `wiki/_system/agent-operation-guide.md`
7. `wiki/_system/ingestion-policy.md`
8. `wiki/_system/security-policy.md`
9. `wiki/_system/observation-policy.md`
10. `wiki/_system/developer-policy.md`
11. `wiki/README.md`
12. `wiki/long-term-objectives-index.md`

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

## Policy Freshness

Hermes Agent may cache Hermes Runes usage as native-memory skill.

Before real Runes operations, Hermes Agent must check policy freshness or decipher the relevant policy bundle again.

`change-history.md` is part of freshness awareness because structural wiki changes may invalidate cached assumptions.

## Non-goals

Hermes Runes is not:

- an enterprise multi-user CMS
- a distributed cloud memory platform
- a full autonomous self-modifying agent framework
- a replacement for Hermes Agent judgment

## Change Log

- 2026-06-01: Initial P0 system policy index.

## Agent Style Overlay

- `agent-style-overlay.md`
  - Optional presentation guidance for Hermes-agent when interacting with Hermes Runes MD Wiki through Runes Shield.
  - Defines Runes-themed terms such as forge, attunement, relic, seal, resonance, and inscription.
  - Style only; does not override `soul.md`, governance policy, security policy, or human approval requirements.

## Runes Shield Discovery

- `runes_shield_contract.md`
  - Defines the governed invocation boundary between Hermes-agent and Hermes Runes MD Wiki.
- `runes_invocation_policy.md`
  - Defines how controlled Runes Shield operations should be invoked.
- `runes_agent_guidance.md`
  - Defines agent-facing operating guidance for proposal, review, approval, and trusted-memory boundaries.

## Runes Markdown Source Health

- `runes_markdown_source_health.md`
  - Defines Markdown source-of-truth health semantics.
  - Defines Runes Shield Forge Readiness Check / Runes 符文鑄造前適性檢查.
  - Defines refinement levels `+0` to `+9`.
  - Clarifies that PostgreSQL is a replaceable recall/index backend, not the authoritative memory layer.
