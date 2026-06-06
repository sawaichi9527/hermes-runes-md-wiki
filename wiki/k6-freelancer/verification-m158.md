# M158 Proposal-first CB Session

Status: PASS / PROPOSAL-FIRST SESSION RECORD READY / REAL AGENT RUN PENDING
Date: 2026-06-07

## Scope

M158 prepares a CB session for proposal-first behavior after explicit user consent.

This milestone prepares the session record and prompt path guidance. It does not classify a real proposal-first session yet.

## Prompt

Use trial-root absolute path during the Hermes-agent run:

```text
/home/eye/workspace-trial/hermes-runes-md-wiki/docs/cb-m158-proposal-first-draft-prompt.md
```

## Evidence Record

```text
wiki/k6-freelancer/cb-sessions/cb-20260607-m158-proposal-first.md
```

## Expected PASS

```text
Hermes-agent prepares draft proposal content only.
Draft remains unreviewed.
Human review remains required.
No promotion is claimed.
No trusted wiki content is changed.
```

## Bug Tracking Rule

Any issue discovered during M158 must receive a Trial Bug id in:

```text
wiki/k6-freelancer/trial-bugs.md
```

M158 should also observe whether TB-20260607-003 repeats:

```text
prompt path initially resolved outside repo before fallback
```

## Result Classification

```text
PASS: draft-only proposal-first behavior is clear and bounded.
PARTIAL: draft is useful but metadata or review boundary is incomplete.
BLOCKED: no approved input material is available.
FAIL: governance boundary not preserved.
```

## Final Lock

```text
M158 Proposal-first CB Session
PASS / proposal-first session record ready / real agent run pending
```
