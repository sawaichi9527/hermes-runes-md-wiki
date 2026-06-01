# Runes Invocation Policy

This document defines how Hermes-agent may invoke Hermes Runes capabilities through Runes Shield during P0 / trial run.

It is intentionally small and conservative.

Runes Shield is a governed invocation boundary, not an autonomous trusted memory writer.

---

## Invocation Rule

Hermes-agent may only interact with Hermes Runes through Runes-provided interfaces.

Hermes-agent must not directly control or mutate Hermes Runes MD Wiki internals.

---

## P0 Interface Shape

The preferred P0 interface shape is small, local, deterministic, and JSON-friendly.

Candidate commands:

```bash
runes capabilities --json
runes guidance --json
runes propose --json
runes proposal list --json
runes proposal show --json
runes recall --json
runes smoke --json
```

The exact command implementation may evolve, but the policy boundary remains stable:

- discovery is allowed
- guidance is allowed
- proposal creation after user consent is allowed
- proposal inspection is allowed
- trusted recall is allowed
- smoke / diagnostics are allowed
- approval, rejection, promotion, destructive mutation, and direct internal writes are not allowed for Hermes-agent during P0

---

## Capability Classes

### `capabilities`

Purpose:

- Let Hermes-agent discover what Runes can do.
- Report allowed operations and forbidden operations.
- Report whether write-like operations require user consent and human approval.

Allowed:

- read-only
- stable JSON output
- no internal state mutation

Required information:

- capability list
- safety boundary summary
- human-only operation list
- proposal lifecycle summary

---

### `guidance`

Purpose:

- Let Hermes-agent learn how to use Runes safely.
- Provide user-facing prompt patterns.
- Explain when durable Markdown memory should or should not be proposed.

Allowed:

- read-only
- stable JSON or Markdown-derived summary
- no internal state mutation

Required information:

- trigger candidates
- non-trigger candidates
- consent requirement
- secret-handling warnings
- proposal isolation explanation

---

### `propose`

Purpose:

- Create a governed draft proposal from user-provided material.

Allowed only when:

1. The user has provided material or instructions to preserve.
2. Hermes-agent has identified the material as potentially durable knowledge.
3. Hermes-agent has asked the user whether to create a Runes proposal.
4. The user has consented.

Required behavior:

- create draft / quarantined proposal only
- do not create trusted memory directly
- do not update curated wiki notes directly
- do not bypass human approval
- return proposal id, status, path or opaque handle, and next human action

Forbidden input:

- credentials
- tokens
- passwords
- API keys
- private secrets
- raw logs containing sensitive data unless sanitized and approved by the user

---

### `proposal list`

Purpose:

- Let Hermes-agent inspect proposal status.

Allowed:

- read-only
- no state transition
- no file movement
- no approval / rejection

Expected states:

- draft
- pending_review
- approved
- rejected
- reviewed
- imported

The exact internal state names may evolve, but Hermes-agent must treat the returned status as authoritative and must not mutate it directly.

---

### `proposal show`

Purpose:

- Let Hermes-agent inspect a specific proposal.

Allowed:

- read-only
- no state transition
- no file movement
- no approval / rejection

Expected output:

- proposal id
- status
- safe summary
- source metadata when available
- next human action when applicable

---

### `recall`

Purpose:

- Retrieve already indexed trusted memory evidence.

Allowed:

- read-only retrieval
- context/evidence output
- citation/source metadata output

Rules:

- draft proposals are not trusted evidence
- rejected proposals are not trusted evidence
- unimported reviewed content is not trusted indexed evidence unless explicitly returned as non-trusted status
- Hermes-agent must compare Runes evidence with current user instructions and other available sources

---

### `smoke`

Purpose:

- Verify tool health and baseline behavior.

Allowed:

- read-only or controlled diagnostic behavior
- no destructive mutation
- no policy mutation

Expected output:

- status
- checked components
- pass/fail details
- safe logs or short summaries

---

## User Consent Requirement

Hermes-agent must not silently persist user-provided material.

Before creating a proposal, Hermes-agent should ask a clear question.

Example:

> 這段內容看起來像是後續會重複使用的專案知識。要不要我幫你建立一筆 Hermes Runes governed proposal，先放入待審核區，之後由你確認後再固化成 Markdown wiki？

Consent must be explicit enough for the current task.

Examples of sufficient consent:

- `go`
- `建立 proposal`
- `幫我固化`
- `寫進 Runes`
- `記到 wiki`
- `yes, create a proposal`

Examples that are not sufficient by themselves:

- casual agreement with the information
- asking a follow-up question
- continuing the technical discussion without persistence intent

---

## Human Approval Boundary

During P0, Hermes-agent may create proposals but may not approve or reject them.

Human approval is required before proposed content becomes trusted memory.

This preserves:

- reviewability
- source-of-truth integrity
- protection against hallucinated memory writes
- protection against prompt injection
- protection against accidental persistence of secrets

---

## Secret and Sensitive Data Rule

Runes Shield must treat real secrets as prohibited from Markdown memory and git.

Do not propose persistence of:

- API keys
- database passwords
- Telegram bot tokens
- LM Studio / OpenAI-compatible API keys
- Tavily keys
- private credentials
- private tokens
- raw secret-bearing logs

If user-provided content contains possible secrets, Hermes-agent should warn the user and ask for sanitized content instead of creating a proposal.

---

## P0 Non-goals

P0 does not implement:

- autonomous trusted memory writing
- unrestricted agent write access
- full MCP server
- complex workflow engine
- enterprise permission model
- web dashboard
- automatic heuristic tuning
- direct database mutation by agent

---
