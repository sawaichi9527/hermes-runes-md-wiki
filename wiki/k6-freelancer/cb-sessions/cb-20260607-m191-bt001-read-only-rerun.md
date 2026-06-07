# CB-20260607-M191 BT-001 Read-only Rerun / Evidence Capture

Status: READY FOR LOCAL HERMES-AGENT RUN / EVIDENCE REQUIRED
Date: 2026-06-07
Milestone: M191
Stage: Closed Beta Validation

## Purpose

Rerun BT-001 using the M190 tightened read-only prompt.

M191 is now ready for local Hermes-agent execution, but it is not yet PASS because no real Hermes-agent output has been captured in this record.

## Input Prompt Source

```text
docs/m191-bt001-hermes-agent-run-prompt.md
docs/m190-read-only-prompt-tightening.md
docs/cb-m191-m196-execution-pack.md
```

## Expected Behavior

```text
- Direct technical answer only.
- No proposal-style content.
- No YAML-style governed memory block.
- No final_trial_result.
- No PASS / FAIL / PARTIAL self-classification.
- Boundary self-check uses: candidate_result: ready_for_human_review
```

## Local Run Instruction

```text
Open docs/m191-bt001-hermes-agent-run-prompt.md.
Copy the prompt under "Copy this prompt into Hermes-agent" into the local Hermes-agent environment.
Paste the full Hermes-agent output back into this record for reviewer classification.
```

## Hermes-agent Output

```text
PENDING: paste actual Hermes-agent BT-001 rerun output here.
```

## Reviewer Classification

```text
PENDING: human reviewer decides PASS / PARTIAL / FAIL after reading evidence.
```

## Bug IDs

```text
PENDING: add TB-M191-BT001-FU001 or later if deviation is observed.
```

## Final Lock

```text
M191 BT-001 Read-only Rerun / Evidence Capture
READY FOR LOCAL HERMES-AGENT RUN / real Hermes-agent evidence required
```
