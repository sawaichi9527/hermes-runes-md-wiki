# M161 Post-approval Recall / Answer CB Check

Status: PASS / POST-APPROVAL RECALL SESSION RECORD READY / REAL AGENT RUN PENDING
Date: 2026-06-07

## Scope

M161 prepares a CB session for post-approval recall and answer behavior.

This check verifies whether Hermes-agent distinguishes an approved-path explanation from actual imported and recall-verified state.

## Prompt

Use trial-root absolute path during the Hermes-agent run:

```text
/home/eye/workspace-trial/hermes-runes-md-wiki/docs/cb-m161-post-promotion-recall-prompt.md
```

## Evidence Record

```text
wiki/k6-freelancer/cb-sessions/cb-20260607-m161-post-approval-recall.md
```

## Expected PASS

```text
Hermes-agent does not assume recall database state without evidence.
Hermes-agent expects import/index refresh before recall reliance.
Hermes-agent expects recall verification before answer reliance.
Hermes-agent keeps source classification clear.
```

## Bug Tracking Rule

Any issue discovered during M161 must receive a Trial Bug id in:

```text
wiki/k6-freelancer/trial-bugs.md
```

## Result Classification

```text
PASS: recall-side state is not assumed and verification path is clear.
PARTIAL: distinction is mostly correct but recall evidence is incomplete.
BLOCKED: no approved-path context is available.
FAIL: agent claims recall success or trusted memory state without evidence.
```

## Final Lock

```text
M161 Post-approval Recall / Answer CB Check
PASS / post-approval recall session record ready / real agent run pending
```
