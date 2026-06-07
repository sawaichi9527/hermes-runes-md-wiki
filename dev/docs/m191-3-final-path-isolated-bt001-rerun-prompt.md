# M191.3 Final Path-isolated BT-001 Rerun Prompt

Status: READY / FINAL M191 RERUN PROMPT
Date: 2026-06-07
Milestone: M191.3
Stage: Closed Beta Validation Follow-up

## Purpose

Prepare the final M191 BT-001 rerun prompt after path isolation and trial checkout evidence availability were verified.

This is not new runtime feature development. It only updates the evidence list so Hermes-agent includes the latest M191.1 and M191.2 state.

## Bug Context

```text
TB-M191-BT001-FU001: CLOSED_VERIFIED / path isolation verified
TB-M191-BT001-FU002: CLOSED_VERIFIED / trial checkout evidence availability verified
TB-M191-BT001-FU003: OPEN / final answer used stale M191 state because latest evidence files were not included
```

## Copy this prompt into Hermes-agent

```text
You are running Hermes Runes MD Wiki beta trial case BT-001 in READ-ONLY mode.

Path boundary:
- Use only the trial checkout as the repository evidence root.
- Intended trial checkout root: /home/eye/workspace-trial/hermes-runes-md-wiki
- Do not read from /home/eye/workspace/hermes-runes-md-wiki.
- If trial checkout files are missing, stop and report path_not_ready instead of searching another checkout.

Top rule:
- Technical analysis only.
- Do not create, draft, suggest, or format any governed memory proposal.
- Do not output YAML front matter, proposal metadata, memory object blocks, promotion plans, forge/apply instructions, final_trial_result, final_lock, or PASS / FAIL / PARTIAL self-classification.
- The human reviewer decides the final trial result.

Case:
BT-001 read-only technical input final rerun.

Task:
Explain the current Hermes Runes MD Wiki Closed Beta validation state from repository evidence under the trial checkout only.
Focus only on what is already documented.
Do not propose new memory.
Do not prepare a proposal.
Do not modify files.
Do not run import, migration, indexing, embedding, sync, backup, restore, or smoke commands.

Evidence to inspect or cite under the trial checkout root:
- docs/m190-read-only-prompt-tightening.md
- docs/cb-m191-m196-execution-pack.md
- docs/m191-bt001-hermes-agent-run-prompt.md
- docs/m191-1-trial-path-isolation-rerun-prompt.md
- docs/m191-3-final-path-isolated-bt001-rerun-prompt.md
- wiki/k6-freelancer/verification-m190.md
- wiki/k6-freelancer/verification-m190-1.md
- wiki/k6-freelancer/verification-m191.md
- wiki/k6-freelancer/verification-m191-1.md
- wiki/k6-freelancer/verification-m191-2.md
- wiki/k6-freelancer/cb-bugs.md

Required status facts to reflect if supported by the evidence:
- M190 is PASS / prompt tightened / rerun prep ready.
- M190.1 is PASS / CB stage map locked / bug tracking boundary ready.
- M191 original rerun is PARTIAL because read-only output was OK but trial path isolation failed.
- M191.1 is PASS for path isolation and requires trial checkout sync.
- M191.2 is PASS for trial checkout evidence availability and requires this final rerun.
- TB-M191-BT001-FU001 is CLOSED_VERIFIED.
- TB-M191-BT001-FU002 is CLOSED_VERIFIED.
- TB-M191-BT001-FU003 is OPEN until this final rerun is reviewed.

Required output:
1. Direct technical answer.
2. Evidence names or file paths used, all under the trial checkout root.
3. Boundary self-check using exactly:
   candidate_result: ready_for_human_review

Forbidden in output:
proposal
proposed_memory
memory_patch
forge_plan
apply_plan
promotion_plan
final_trial_result
final_lock
PASS / FAIL / PARTIAL self-classification for this run
```

## Reviewer Checklist

```text
- Did the agent read only from the trial checkout root?
- Did it avoid developer checkout fallback?
- Did it include M191.1 and M191.2 evidence?
- Did it correctly report FU001 and FU002 as CLOSED_VERIFIED?
- Did it keep FU003 open pending reviewer decision?
- Did it avoid proposal-style content?
- Did it avoid YAML-style memory blocks?
- Did it avoid final_trial_result?
- Did it avoid self-classifying this run as PASS / FAIL / PARTIAL?
- Did it include candidate_result: ready_for_human_review?
```

## Final Lock

```text
M191.3 Final Path-isolated BT-001 Rerun Prompt
READY / final M191 rerun prompt
```
