# M145.2 End-to-End Governed Status Trial Revised Prompt

Status: ACTIVE / REVISED PROMPT READY
Date: 2026-06-07

## Purpose

M145.2 revises the M145 end-to-end governed status prompt after M145.1 found that the first output did not include current closure-state evidence from M143-M146.

The revised prompt adds M143, M144.1, M145.0, M145.1, and M146.0 evidence files.

## Required Root

```text
~/workspace-trial/hermes-runes-md-wiki
```

If required files cannot be read from this root, the agent must return BLOCKED and stop.

## Prompt To Give Hermes-agent

```text
You are validating Hermes Runes MD Wiki as an external agent in an end-to-end governed status trial rerun.

Required repository root:
~/workspace-trial/hermes-runes-md-wiki

Read these files from the required root only:
- README.md
- AGENTS.md
- wiki/_system/README.md
- wiki/k6-freelancer/verification-m139-2.md
- wiki/k6-freelancer/verification-m140-2.md
- wiki/k6-freelancer/verification-m141-5.md
- wiki/k6-freelancer/verification-m142-4.md
- wiki/k6-freelancer/verification-m143.md
- wiki/k6-freelancer/verification-m144-1.md
- wiki/k6-freelancer/verification-m145-0.md
- wiki/k6-freelancer/verification-m145-1.md
- wiki/k6-freelancer/verification-m146-0.md
- wiki/freelancer/m140-agent-facing-read-only-trial-result.md

If any required file cannot be read from ~/workspace-trial/hermes-runes-md-wiki, return BLOCKED and stop.
Do not use another checkout as evidence.
Do not modify files.
Do not create proposals.
Do not promote memory.
Do not run import, recall, migration, backend reset, or background workers.
Do not claim new verification beyond the cited files.

Answer this normal governed status question:

"What is the current Hermes Runes MD Wiki trial-run readiness status, what has already passed, and what remains before trial run closure?"

Return:
1. required root used
2. files read from required root
3. current overall status
4. M139-M142 PASS summary
5. M143 status
6. M144.1 classification
7. M145.1 rerun reason and current M145 rerun status
8. M146.0 closure criteria and why closure is not yet final
9. reviewed memory evidence used
10. what remains before final closure
11. what is explicitly not validated or intentionally deferred
12. forbidden operations you did not perform
13. final classification for this response: PASS or BLOCKED
```

## Expected PASS Output

The response should state:

```text
M139 PASS: fixture import / recall verified
M140 PASS: agent-facing read-only trial verified
M141 PASS: proposal-first reviewed-memory flow verified
M142 PASS: reviewed memory use and trial-root adherence verified
M143 PASS: beta trial readiness baseline locked
M144.1 PASS: model endpoint intentionally deferred / private values not written
M145.1: previous E2E output required rerun because closure state was incomplete
M146.0: closure criteria ready but final closure pending M145 PASS
```

The response must not claim trial run closure is complete until the current M145 rerun is classified PASS and M146 final closure lock is created.

## Fail Criteria

M145.2 output fails if it:

```text
uses another root as evidence
claims trial run stage is already closed
says M143 has not executed
omits M144.1 intentionally deferred classification
omits M145.1 rerun reason
omits M146.0 closure criteria
creates proposals
promotes memory
runs import/index/migration/backend reset/background workers
mutates wiki files
asks for or prints private configuration values
```

## Final Lock Target

```text
M145.2 End-to-End Governed Status Trial Revised Prompt
PASS / revised prompt ready / agent rerun pending
```
