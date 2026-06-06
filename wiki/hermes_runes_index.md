# Hermes Runes Index

This is the canonical entry point for Hermes Runes MD Wiki.

這是 Hermes Runes MD Wiki 的標準入口檔。

---

## Purpose

Hermes Runes MD Wiki is a governed Markdown memory source-of-truth for local, agent-facing RAG memory.

This index defines the standard P0 / trial run entry path for agents and humans.

Agents must not infer operational behavior from arbitrary wiki files or incidental local development documents.

Agents should discover Runes capabilities through Runes Shield and its documented interface.

---

## Runes Shield

Runes Shield  
A governed invocation boundary for trusted Markdown memory.

Runes Shield 是 Hermes-agent 與 Hermes Runes MD Wiki 之間的治理護盾，負責提供可發現、可召喚、可驗證的受控工具介面，並阻止 agent 直接操作內部 Markdown wiki、proposal 狀態與資料庫內容。

Core principle:

> Hermes-agent may invoke the runes, but must never breach the shield.

中文：

> Hermes-agent 可以召喚符文，但不得突破護盾。

---

## Canonical P0 / Trial Run Files

For P0 / trial run, the canonical Markdown architecture is:

```text
wiki/hermes_runes_index.md
wiki/_system/runes_shield_contract.md
wiki/_system/runes_invocation_policy.md
wiki/_system/runes_agent_guidance.md
wiki/_system/p0_local_agent_invocation_policy.md
wiki/_system/p0_compact_agent_bootstrap_prompt.md
wiki/_system/p0_compact_bootstrap_regression_checklist.md
```

These files define the required P0 agent-facing knowledge boundary.

Other local wiki files may exist, including historical development notes, legacy policy drafts, project-specific notes, or implementation records. They may be useful as reference material, but they are not required P0 / trial run bootstrap dependencies unless explicitly promoted into the canonical architecture.

---

## Agent Bootstrap Rule

Agents should start from this index and then use the Runes Shield interface to discover operational capabilities.

Agents must not:

- treat arbitrary wiki files as operational authority
- directly read internal files as an operational shortcut
- directly write or edit Markdown wiki files
- directly move proposal states
- directly approve, reject, promote, import, rebuild, or delete memory content
- directly mutate PostgreSQL / FTS / pgvector records

Agents may:

- discover Runes capabilities through Runes Shield
- read Runes guidance through Runes Shield
- ask the user whether durable knowledge should be proposed
- create governed proposals only after user consent
- inspect proposal status through Runes-provided interfaces
- recall trusted indexed evidence through Runes-provided interfaces
- request smoke / diagnostic status through Runes-provided interfaces

---

## Required System Documents

### `wiki/_system/runes_shield_contract.md`

Defines the protected interaction boundary between Hermes-agent and Hermes Runes MD Wiki.

Use this to understand what Hermes-agent may invoke and what it must never directly mutate.

### `wiki/_system/runes_invocation_policy.md`

Defines how Hermes-agent may call Runes capabilities during P0 / trial run.

Use this to understand allowed interface classes, consent handling, proposal creation rules, recall rules, and human-only operations.

### `wiki/_system/runes_agent_guidance.md`

Defines practical interaction guidance for Hermes-agent.

Use this to understand when Hermes-agent should offer Runes knowledge solidification, how to ask the user for consent, and how to explain proposal results.

### `wiki/_system/p0_local_agent_invocation_policy.md`

Defines the repeated P0 practical local-agent invocation flow validated by M112 through M115.

Use this as the short checklist for read-only first, proposal draft first, explicit approval before file creation, separate approval before promotion, import/index refresh if needed, recall verification before PASS freeze, no autonomous writer behavior, no external/public Runes API, and no secrets.

### `wiki/_system/p0_compact_agent_bootstrap_prompt.md`

Defines a compact reusable bootstrap prompt for future Hermes-agent, OpenClaw, or other approved local governed agent sessions.

Use this when starting a new local governed session so the agent can bootstrap from `wiki/hermes_runes_index.md` and `wiki/_system/p0_local_agent_invocation_policy.md` instead of long milestone verification history.

### `wiki/_system/p0_compact_bootstrap_regression_checklist.md`

Defines a compact regression checklist for future edits to the P0 bootstrap index, local invocation policy, and compact bootstrap prompt.

Use this before and after modifying compact bootstrap policy files to confirm read-only-first, proposal-first, two-stage approval, recall-before-freeze, no autonomous writer, no external/public Runes authority, and no-secrets behavior remain intact.

---

## P0 Bootstrap Summary

A compliant P0 Hermes-agent should be able to answer:

1. What is Runes Shield?
2. What capabilities can be invoked?
3. Which operations are forbidden for the agent?
4. Which operations remain human-only?
5. When should the agent ask the user about knowledge solidification?
6. What does user consent look like?
7. What is the difference between draft proposal and trusted memory?
8. How should trusted recall evidence be used?
9. What is the repeated practical P0 local-agent invocation flow?
10. When is a practical P0 trial-run allowed to be frozen as PASS?
11. What compact bootstrap prompt should be used for a new local governed agent session?
12. Which checklist should be used before and after compact bootstrap policy edits?

---

## Non-authoritative Local Documents

Local or historical wiki documents may exist under `wiki/` or `wiki/_system/`.

They should not be treated as mandatory P0 bootstrap files unless they are listed in this index or in the current roadmap as canonical P0 architecture.

This prevents trial run behavior from accidentally depending on development-only local state.

---
