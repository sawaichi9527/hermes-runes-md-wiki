# Runes Shield Contract

Runes Shield  
A governed invocation boundary for trusted Markdown memory.

Runes Shield 是 Hermes-agent 與 Hermes Runes MD Wiki 之間的治理護盾，負責提供可發現、可召喚、可驗證的受控工具介面，並阻止 agent 直接操作內部 Markdown wiki、proposal 狀態與資料庫內容。

---

## Core Principle

Hermes-agent may invoke the runes, but must never breach the shield.

中文：Hermes-agent 可以召喚符文，但不得突破護盾。

---

## Purpose

Runes Shield defines the only supported agent-facing interaction boundary between Hermes-agent and Hermes Runes MD Wiki.

Hermes Runes MD Wiki is a governed Markdown memory backend and source-of-truth.

Hermes-agent is the conversation, reasoning, and orchestration layer.

Runes Shield is the protected interface between them.

Hermes-agent may discover, invoke, and verify Runes capabilities through this boundary, but must not directly mutate internal wiki files, proposal states, database records, importer artifacts, or trusted memory content.

---

## Boundary Model

```text
User
  ↓
Hermes-agent
  ↓ invoke only through Runes Shield
Runes Shield
  ↓ controlled internal operations
Hermes Runes MD Wiki
  ↓ derived index
PostgreSQL / FTS / pgvector
```

Hermes-agent is allowed to request governed memory operations.

Runes Shield decides how those requests are translated into safe internal actions.

Human approval remains the trust boundary for turning proposed knowledge into trusted memory.

---

## Supported P0 Interaction Classes

### 1. Discovery

Hermes-agent may ask what Runes can do.

Examples:

- capabilities
- available commands
- safety boundaries
- human-only operations
- proposal workflow summary

### 2. Guidance

Hermes-agent may ask how to use Runes safely.

Examples:

- when to propose durable memory
- what not to persist
- how to ask the user for consent
- what states exist in the proposal lifecycle

### 3. Proposal Creation

Hermes-agent may create a governed draft proposal only after user consent.

Proposal creation is not trusted memory insertion.

A draft proposal remains isolated until reviewed and approved by a human-controlled workflow.

### 4. Status Inspection

Hermes-agent may inspect proposal status through Runes-provided interfaces.

It must not move, rename, approve, reject, or promote proposal files directly.

### 5. Recall / Evidence Retrieval

Hermes-agent may ask Runes for already indexed trusted memory evidence.

Hermes-agent remains responsible for comparing Runes evidence with current user instructions, native memory, third-party RAG / notes, web search results, and other available sources.

### 6. Smoke / Verification

Hermes-agent may request tool health or smoke status through Runes-provided interfaces.

Smoke results are evidence of tool behavior, not automatic proof that every knowledge claim is true.

---

## Forbidden Hermes-agent Behaviors

Hermes-agent must not directly:

- read internal files as an operational shortcut
- write or edit `wiki/*.md`
- write or edit `wiki/_system/*.md`
- move proposal files between states
- approve proposals
- reject proposals
- promote reviewed proposals into curated wiki notes
- import reviewed content outside controlled wrapper behavior
- rebuild indexes outside controlled wrapper behavior
- delete, archive, or mutate trusted memory content
- write PostgreSQL / FTS / pgvector records
- mutate importer artifacts
- bypass human approval
- treat draft or rejected proposal content as trusted memory

---

## Human-only Operations During P0

The following operations remain human-only during P0 / trial run:

- approve proposal
- reject proposal
- promote reviewed proposal into curated wiki note
- direct wiki edit
- destructive delete / archive
- database rebuild / schema mutation
- policy mutation
- importer lifecycle changes beyond controlled wrapper behavior

Runes may later expose dry-run plans for these operations, but final state-changing authority remains human-controlled in P0.

---

## P0 Completion Criteria

Runes Shield P0 is complete when Hermes-agent can:

1. Discover Runes capabilities through the supported interface.
2. Understand allowed invocation versus forbidden direct mutation.
3. Ask the user whether durable knowledge should be solidified.
4. Create governed proposals only after user consent.
5. Read proposal status through Runes-provided interfaces.
6. Retrieve trusted recall evidence through Runes-provided interfaces.
7. Avoid direct manipulation of internal Markdown files, proposal state, importer artifacts, and database content.
8. Pass a multi-proposal trial run with approved / rejected / draft isolation verified.

---

## Design Bias

Keep Runes Shield small.

Prefer deterministic local interfaces over complex agent frameworks.

Prefer CLI/JSON contracts before MCP or server expansion.

Prefer human approval over autonomous trusted memory writes.

Prefer inspectable Markdown source-of-truth over opaque memory mutation.

---
