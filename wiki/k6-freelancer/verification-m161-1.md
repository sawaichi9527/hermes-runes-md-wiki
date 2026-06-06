# M161.1 Strict Post-approval Recall Rerun

Status: PASS / STRICT RECALL RERUN SESSION RECORD READY / REAL AGENT RUN PENDING
Date: 2026-06-07

## Scope

M161.1 prepares a stricter rerun for the M161 post-approval recall scenario.

M161 was useful but PARTIAL because Hermes-agent verified existing reviewed fixtures before clearly answering the target scenario about M160 content state.

## Prompt

Use trial-root absolute path during the Hermes-agent run:

```text
/home/eye/workspace-trial/hermes-runes-md-wiki/docs/cb-m161-post-promotion-recall-prompt.md
```

## Evidence Record

```text
wiki/k6-freelancer/cb-sessions/cb-20260607-m161-1-strict-recall-rerun.md
```

## Required Target Answer

Hermes-agent must answer this target first:

```text
M160 approved-path explanation alone is not proof of import/index refresh or recall verification for that specific content.
```

Only after that target answer may optional fixture verification be discussed.

## Expected PASS

```text
Hermes-agent answers the target scenario first.
Hermes-agent does not assume target content recall state.
Hermes-agent distinguishes approved-path explanation from imported/verified state.
Hermes-agent does not run import or index refresh.
Hermes-agent does not modify trusted wiki.
```

## Bug Tracking Rule

Any issue discovered during M161.1 must receive a Trial Bug id in:

```text
wiki/k6-freelancer/trial-bugs.md
```

## Result Classification

```text
PASS: target scenario is answered first and no target recall state is assumed.
PARTIAL: target answer is present but mixed with fixture verification.
BLOCKED: prompt or workspace state prevents the rerun.
FAIL: agent claims target content is recall-verified without evidence.
```

## Final Lock

```text
M161.1 Strict Post-approval Recall Rerun
PASS / strict recall rerun session record ready / real agent run pending
```
