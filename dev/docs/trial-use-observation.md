# Controlled Trial-use Observation Guide

Status: M84 readiness scaffold

This guide describes the first post-P0 controlled real trial-use observation flow for Hermes Runes MD Wiki.

The goal is to observe one small real memory candidate through the governed workflow without adding enterprise-grade automation, hidden background workers, automatic proposal apply, automatic wiki mutation, or database lifecycle management.

---

## Scope

A controlled trial should use exactly one small candidate at a time:

```text
one small real project-memory candidate
one source reference
one target Markdown path
one manual review
one manual record
one post-change verification pass
```

This is a personal-local observation workflow, not an enterprise ingestion pipeline.

---

## Preconditions

Before starting a trial, verify:

```bash
bash ./bin/hermes-backend-check
bash ./bin/hermes-memory-migrate
```

The repository should already have:

```text
M82 P0 Governed Memory Operating Baseline: PASS / frozen / smoke verified
M83 External Backend Boundary + Simple Backend Guard: PASS / frozen / smoke verified
```

---

## Trial record location

Trial records should live under:

```text
wiki/k6-freelancer/trials/
```

Recommended filename format:

```text
trial-YYYYMMDD-<short-slug>.md
```

Example:

```text
wiki/k6-freelancer/trials/trial-20260605-small-memory-candidate.md
```

---

## Trial record template

Use:

```text
templates/trial-observation-record.md
```

Copy it to a concrete trial record path, then fill in the fields manually.

The template is intentionally Markdown-native and simple. It is not a queue item, not an automation job, and not a hidden agent instruction.

---

## Required review gates

A trial record should include these sections:

```text
## Metadata
## Candidate Summary
## Source Reference
## Target Markdown Path
## Proposed Memory Content
## Governance Checks
## Manual Review
## Manual Record
## Post-change Verification
## Observation Notes
## Final Status
```

A trial should not be marked PASS until post-change verification is complete.

---

## Allowed actions

Agents may:

- read the candidate and source reference provided by the user
- draft a trial observation record
- suggest a target Markdown path
- run read-only checks
- run backend guard
- run schema migration entrypoint
- prepare a governed proposal draft if needed
- report blocked states clearly

---

## Forbidden actions

Agents must not:

- automatically apply a proposal
- directly mutate `wiki/` as a hidden side effect
- import arbitrary content into memory without review
- treat backend unavailable as empty memory
- write secrets into trial records
- ingest `.env` or local credentials
- spawn background workers
- build enterprise queue / retry / orchestration systems

---

## Observation principle

The trial should answer:

```text
Can a small real memory candidate move through the governed workflow clearly, safely, and with enough evidence for later improvement?
```

It should not attempt to solve:

```text
bulk ingestion
multi-user approval
enterprise audit
high availability
automatic promotion
background synchronization
```

---

## Minimal verification command

Before treating a trial record as structurally ready, run:

```bash
bash ./bin/hermes-trial-observation-check wiki/k6-freelancer/trials/<trial-file>.md
```

This check is intentionally shallow. It verifies required sections and obvious forbidden secret markers only. Human review remains required.
