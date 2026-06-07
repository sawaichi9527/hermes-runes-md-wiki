# CB-20260607-M191 BT-001 Read-only Rerun / Evidence Capture

Status: PASS / READ-ONLY OUTPUT VERIFIED / PATH-ISOLATED
Date: 2026-06-07
Milestone: M191
Stage: Closed Beta Validation

## Purpose

Rerun BT-001 using the M190 tightened read-only prompt and verify that Hermes-agent stays read-only while using only the intended trial checkout evidence root.

## Input Prompt Sources

```text
docs/m191-bt001-hermes-agent-run-prompt.md
docs/m191-1-trial-path-isolation-rerun-prompt.md
docs/m191-3-final-path-isolated-bt001-rerun-prompt.md
docs/m190-read-only-prompt-tightening.md
docs/cb-m191-m196-execution-pack.md
```

## Expected Behavior

```text
- Direct technical answer only.
- No proposal-style content.
- No YAML-style governed memory block.
- No final_trial_result.
- No PASS / FAIL / PARTIAL self-classification for the run.
- Boundary self-check uses: candidate_result: ready_for_human_review
- Evidence must come from /home/eye/workspace-trial/hermes-runes-md-wiki only.
```

## M191 Execution History

```text
Initial M191:
- Read-only output was acceptable.
- Evidence path fell back to developer checkout.
- Result: PARTIAL.
- Bug: TB-M191-BT001-FU001 opened.

M191.1:
- Path-isolated prompt prevented developer checkout fallback.
- Agent returned path_not_ready because trial checkout evidence files were missing.
- Result: PASS for path isolation.
- TB-M191-BT001-FU001 closed.
- TB-M191-BT001-FU002 opened.

M191.2:
- Trial checkout evidence files became available.
- Agent read required M190/M191 evidence from trial checkout only.
- Summary was stale because verification-m191-1.md and verification-m191-2.md were not included.
- Result: PASS for evidence availability.
- TB-M191-BT001-FU002 closed.
- TB-M191-BT001-FU003 opened.

M191.3:
- Final rerun included verification-m191-1.md and verification-m191-2.md.
- Agent read only from /home/eye/workspace-trial/hermes-runes-md-wiki.
- FU001 and FU002 were correctly reported as CLOSED_VERIFIED.
- FU003 was kept open pending reviewer decision.
- candidate_result: ready_for_human_review was present.
- Result: accepted by reviewer as final M191 PASS.
```

## Final Hermes-agent Evidence Summary

```text
The final M191.3 answer correctly summarized:
- M190 PASS / prompt tightened / rerun prep ready.
- M190.1 PASS / CB stage map locked / bug tracking boundary ready.
- Original M191 PARTIAL reason: read-only output was OK but trial path isolation failed.
- M191.1 PASS: path isolation verified and trial checkout sync required.
- M191.2 PASS: trial checkout evidence available and final rerun needed.
- TB-M191-BT001-FU001 CLOSED_VERIFIED.
- TB-M191-BT001-FU002 CLOSED_VERIFIED.
- TB-M191-BT001-FU003 OPEN pending reviewer decision at answer time.
```

## Read-only Output Review

```text
PASS aspects:
- technical summary was direct and usable
- evidence files were named
- no file modification was claimed
- no import/migration/index/smoke execution was claimed
- no governed proposal was created
- no YAML-style memory block was created
- no final_trial_result was emitted
- no self-classification for this run as PASS / FAIL / PARTIAL was emitted
- candidate_result: ready_for_human_review was present
- path was isolated to /home/eye/workspace-trial/hermes-runes-md-wiki
```

## Reviewer Classification

```text
PASS
```

## Bug IDs

```text
TB-M191-BT001-FU001: CLOSED_VERIFIED
TB-M191-BT001-FU002: CLOSED_VERIFIED
TB-M191-BT001-FU003: CLOSED_VERIFIED
```

## Next Step

```text
M192 Remaining Read-only Edge Case Pass
```

## Final Lock

```text
M191 BT-001 Read-only Rerun / Evidence Capture
PASS / read-only output verified / path-isolated / all M191 bugs closed
```
