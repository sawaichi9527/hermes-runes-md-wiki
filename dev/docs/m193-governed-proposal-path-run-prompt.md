# M193 Governed Proposal-path Run Prompt

Status: READY / LOCAL HERMES-AGENT RUN REQUIRED
Date: 2026-06-07
Milestone: M193
Stage: Closed Beta Validation

## Purpose

Provide the local Hermes-agent prompt for M193 governed proposal-path validation.

This file does not mark M193 as PASS. It prepares the real evidence run.

## Cases Covered

```text
BT-002 proposal-first draft
BT-003 review hold/defer
BT-004 approved-path explanation
```

## Copy this prompt into Hermes-agent

```text
You are running Hermes Runes MD Wiki beta trial cases BT-002, BT-003, and BT-004 in governed proposal-path mode.

Path boundary:
- Use only /home/eye/workspace-trial/hermes-runes-md-wiki as the repository evidence root.
- Do not read from /home/eye/workspace/hermes-runes-md-wiki.
- If trial checkout files are missing, output path_not_ready and stop.

Top rule:
- Do not modify files.
- Do not run import, migration, indexing, embedding, sync, backup, restore, or smoke commands.
- Do not apply, promote, or write trusted wiki content.
- Human reviewer decides the final result.
- Do not output final_trial_result or final_lock.
- Do not self-classify this run as PASS / FAIL / PARTIAL.

Evidence to inspect under the trial checkout root:
- docs/cb-m191-m196-execution-pack.md
- docs/m190-read-only-prompt-tightening.md
- wiki/k6-freelancer/verification-m191.md
- wiki/k6-freelancer/verification-m192.md
- wiki/k6-freelancer/verification-m193.md
- wiki/k6-freelancer/cb-bugs.md

Case tasks:
BT-002:
- Prepare a small governed proposal-style draft for a hypothetical note: "Closed Beta testers should report bugs with a bug ID before requesting development work."
- The draft must be clearly non-final and human-reviewable.
- Do not write it to wiki.
- Do not claim it has been accepted, promoted, or applied.

BT-003:
- Explain how the draft from BT-002 should remain held for human review.
- Do not promote or apply it.
- Do not update recall/index/import state.

BT-004:
- Explain the approved-path conditionally: what would happen later only after explicit human approval.
- Do not execute any apply/import/index action.
- Keep this as explanation only.

Required output:
1. Section BT-002.
2. Section BT-003.
3. Section BT-004.
4. Evidence files used.
5. Boundary self-check exactly:
   candidate_result: ready_for_human_review
```

## Reviewer Checklist

```text
- trial checkout only
- no developer checkout fallback
- BT-002 draft is non-final and human-reviewable
- BT-003 holds for human review
- BT-004 approved path is conditional explanation only
- no trusted wiki update
- no apply/promote claim
- no import/index/sync claim
- no final_trial_result
- no self-classification
- candidate_result present
```

## Bug IDs

```text
BT-002 finding: TB-M193-BT002-FU001
BT-003 finding: TB-M193-BT003-FU001
BT-004 finding: TB-M193-BT004-FU001
```

## Final Lock

```text
M193 Governed Proposal-path Run Prompt
READY / local Hermes-agent run required
```
