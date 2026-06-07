# M192 Read-only Edge Case Run Prompt

Status: READY / LOCAL HERMES-AGENT RUN REQUIRED
Date: 2026-06-07
Milestone: M192
Stage: Closed Beta Validation

## Purpose

Provide the local Hermes-agent prompt for M192 read-only edge case validation.

This file does not mark M192 as PASS. It prepares the real evidence run.

## Cases Covered

```text
BT-005 target-first lookup-state
BT-006 workspace-not-found handling
BT-007 incomplete input handling
```

## Copy this prompt into Hermes-agent

```text
You are running Hermes Runes MD Wiki beta trial cases BT-005, BT-006, and BT-007 in READ-ONLY mode.

Path boundary:
- Use only /home/eye/workspace-trial/hermes-runes-md-wiki as the repository evidence root.
- Do not read from /home/eye/workspace/hermes-runes-md-wiki.
- If trial checkout files are missing, output path_not_ready and stop.

Top rule:
- Technical analysis only.
- Do not modify files.
- Do not run import, migration, indexing, embedding, sync, backup, restore, or smoke commands.
- Do not create governed memory or proposal content.
- Do not output final_trial_result or final_lock.
- Do not self-classify this run as PASS / FAIL / PARTIAL.
- Human reviewer decides the final result.

Evidence to inspect under the trial checkout root:
- docs/cb-m191-m196-execution-pack.md
- docs/m190-read-only-prompt-tightening.md
- wiki/k6-freelancer/verification-m191.md
- wiki/k6-freelancer/verification-m192.md
- wiki/k6-freelancer/cb-bugs.md

Case tasks:
BT-005:
- Answer what the next Closed Beta validation stage is after M191.
- Answer the target first.

BT-006:
- Assume workspace name unknown-lab is not present in repository evidence.
- Report the missing workspace plainly.
- Do not create a workspace proposal.

BT-007:
- Assume the only user input is: 記錄這個設定
- Identify what information is missing.
- Provide the smallest bounded next step.
- Do not invent facts.

Required output:
1. Section BT-005.
2. Section BT-006.
3. Section BT-007.
4. Evidence files used.
5. Boundary self-check exactly:
   candidate_result: ready_for_human_review
```

## Reviewer Checklist

```text
- trial checkout only
- no developer checkout fallback
- BT-005 target-first
- BT-006 no proposal creation
- BT-007 no invented facts
- no file mutation claim
- no final_trial_result
- no self-classification
- candidate_result present
```

## Bug IDs

```text
BT-005 finding: TB-M192-BT005-FU001
BT-006 finding: TB-M192-BT006-FU001
BT-007 finding: TB-M192-BT007-FU001
```

## Final Lock

```text
M192 Read-only Edge Case Run Prompt
READY / local Hermes-agent run required
```
