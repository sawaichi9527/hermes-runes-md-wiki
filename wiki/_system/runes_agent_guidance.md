# Runes Agent Guidance

This document gives Hermes-agent practical guidance for deciding when and how to offer Hermes Runes knowledge solidification to the user.

Runes Shield is the boundary.

Hermes-agent may invoke Runes, but must never breach the shield.

---

## Role Separation

### Hermes-agent

Hermes-agent is responsible for:

- understanding user intent
- comparing current instructions with available evidence
- deciding whether Runes may be useful
- asking the user whether to create a governed proposal
- invoking Runes only through the supported interface
- explaining Runes results back to the user

Hermes-agent is not responsible for directly writing trusted Markdown memory.

### Runes Shield

Runes Shield is responsible for:

- exposing Runes capabilities
- exposing safe usage guidance
- creating governed proposals when requested
- exposing proposal status
- exposing trusted recall evidence
- exposing smoke / diagnostic status
- preventing direct agent mutation of internal memory state

### Human

The human user remains responsible for:

- deciding whether proposed knowledge should be persisted
- approving or rejecting proposals
- promoting reviewed content into curated wiki notes during P0
- reviewing sensitive or ambiguous material

---

## When Hermes-agent Should Offer Runes

Hermes-agent should consider offering Runes when the user provides or confirms durable knowledge.

Good trigger candidates:

- project decisions
- architecture decisions
- frozen baselines
- verification results
- PASS / FAIL markers
- service layout decisions
- command procedures
- troubleshooting outcomes
- future action items
- naming decisions
- governance rules
- repeated knowledge that the user is likely to ask about later
- user says to remember, solidify, write into Runes, write into wiki, or make it part of long-term memory

---

## When Hermes-agent Should Not Offer Runes

Hermes-agent should avoid offering Runes for:

- casual one-off conversation
- unverified speculation
- brainstorming that the user has not accepted
- raw logs with secrets
- credentials / tokens / passwords
- private keys or API keys
- personal data that has not been clearly approved for persistence
- transient debugging output that is not useful later
- content that conflicts with existing trusted memory without review
- content that may require sanitization first

---

## Suggested User Prompt

When durable knowledge is detected, Hermes-agent should ask before invoking Runes.

Recommended Chinese prompt:

> 這段內容看起來像是後續會重複使用的專案知識。要不要我幫你建立一筆 Hermes Runes governed proposal，先放入待審核區，之後由你確認後再固化成 Markdown wiki？

Shorter variant:

> 這看起來值得固化成長期專案記憶。要不要我透過 Runes Shield 建立一筆 governed proposal？

Recommended English prompt:

> This looks like durable project knowledge that may be useful later. Would you like me to create a governed Hermes Runes proposal for human review before it becomes trusted Markdown memory?

---

## Consent Handling

Hermes-agent should call `runes propose` only after consent.

Clear consent examples:

- `go`
- `好`
- `可以`
- `建立 proposal`
- `寫進 Runes`
- `寫進 roadmap`
- `固化`
- `記到 wiki`
- `yes, create the proposal`

Ambiguous cases should be treated conservatively.

If the user continues discussing the topic but does not indicate persistence intent, Hermes-agent should not create a proposal silently.

---

## What to Send to Runes Proposal

A good proposal should include:

- concise title
- source context
- accepted decision or fact
- rationale when available
- scope
- non-goals / exclusions
- suggested target domain or project
- sensitivity notes
- user consent marker

Do not send:

- secrets
- raw credentials
- raw API keys
- full unfiltered logs with private data
- unsupported claims as trusted facts
- model speculation without user acceptance

---

## How to Explain Proposal Result

After creating a proposal, Hermes-agent should tell the user:

- proposal id or handle
- current status
- that it is not trusted memory yet
- what the next human action is

Example:

```text
已建立 Runes governed proposal。
Status: draft / pending review
Next: 你可以 review 後再 approve，approve 後才會進入 trusted Markdown memory / import / recall 流程。
```

---

## Recall Behavior

When using Runes recall, Hermes-agent should treat results as governed memory evidence, not as the only truth.

Hermes-agent should compare Runes evidence with:

- current user instruction
- current conversation context
- native memory
- third-party notes or RAG
- web search results when freshness matters
- direct user corrections

Runes recall supports evidence; it does not replace reasoning.

---

## Multi-source Comparison

When a task involves current facts, external facts, or possibly changed information, Hermes-agent should not rely only on Runes.

Recommended pattern:

```text
Runes trusted memory
+ current user instruction
+ external search / source when needed
+ other available notes or RAG
→ Hermes-agent final judgment
```

Runes should provide memory evidence and provenance.

Hermes-agent performs final comparison and explanation.

---

## P0 Safety Summary

Hermes-agent may:

- discover Runes capabilities
- read Runes guidance
- ask user whether to create proposal
- create governed proposal after consent
- inspect proposal status
- recall trusted indexed memory
- request smoke / diagnostic status

Hermes-agent must not:

- directly write Markdown wiki files
- directly edit `_system` policy files
- directly move proposal state
- approve or reject proposals
- promote reviewed proposals
- import content outside controlled wrappers
- rebuild or mutate database state
- persist secrets
- silently create memory without user consent

---

## Operating Slogan

Hermes-agent may invoke the runes, but must never breach the shield.

中文：Hermes-agent 可以召喚符文，但不得突破護盾。

---
