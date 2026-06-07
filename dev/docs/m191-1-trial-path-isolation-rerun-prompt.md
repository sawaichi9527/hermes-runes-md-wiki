# M191.1 Trial Path Isolation Rerun Prompt

Status: READY / PATH-ISOLATED RERUN PREP
Date: 2026-06-07
Milestone: M191.1
Stage: Closed Beta Validation Follow-up

## Purpose

Prepare a stricter rerun prompt for M191 after TB-M191-BT001-FU001.

This is not new runtime feature development. It only tightens the local run instruction so Hermes-agent uses the intended trial checkout evidence path.

## Bug Context

```text
id: TB-M191-BT001-FU001
summary: Hermes-agent satisfied read-only output rules but read evidence from developer checkout after trial-local path lookup failed.
```

## Required Pre-run Context

Before running Hermes-agent, confirm the intended CB/trial repository path.

Preferred trial path:

```text
/home/eye/workspace-trial/hermes-runes-md-wiki
```

If the local Hermes-agent runtime maps the repo to a different path, use that actual trial checkout path explicitly. Do not allow fallback to:

```text
/home/eye/workspace/hermes-runes-md-wiki
```

## Copy this prompt into Hermes-agent

```text
You are running Hermes Runes MD Wiki beta trial case BT-001 in READ-ONLY mode.

Path boundary:
- Use only the trial checkout as the repository evidence root.
- Intended trial checkout root: /home/eye/workspace-trial/hermes-runes-md-wiki
- Do not read from /home/eye/workspace/hermes-runes-md-wiki.
- If the trial checkout files are missing, stop and report path_not_ready instead of searching another checkout.

Top rule:
- Follow docs/m190-read-only-prompt-tightening.md.
- Technical analysis only.
- Do not create, draft, suggest, or format any governed memory proposal.
- Do not output YAML front matter, proposal metadata, memory object blocks, promotion plans, forge/apply instructions, final_trial_result, final_lock, or PASS / FAIL / PARTIAL self-classification.
- The human reviewer decides the final trial result.

Case:
BT-001 read-only technical input rerun for TB-M191-BT001-FU001.

Task:
Explain the current Hermes Runes MD Wiki Closed Beta validation state from repository evidence under the trial checkout only.
Focus only on what is already documented.
Do not propose new memory.
Do not prepare a proposal.
Do not modify files.
Do not run import, migration, indexing, embedding, sync, backup, restore, or smoke commands.

Evidence to inspect or cite if available under the trial checkout root:
- docs/m190-read-only-prompt-tightening.md
- docs/cb-m191-m196-execution-pack.md
- docs/m191-bt001-hermes-agent-run-prompt.md
- docs/m191-1-trial-path-isolation-rerun-prompt.md
- wiki/k6-freelancer/verification-m190.md
- wiki/k6-freelancer/verification-m190-1.md
- wiki/k6-freelancer/verification-m191.md
- wiki/k6-freelancer/cb-bugs.md

Required output:
1. Direct technical answer.
2. Evidence names or file paths used, all under the trial checkout root.
3. Boundary self-check using exactly:
   candidate_result: ready_for_human_review

If required evidence files are not present under the trial checkout root, output only:
path_not_ready: trial checkout evidence files missing
candidate_result: ready_for_human_review
```

## Reviewer Checklist

```text
- Did the agent read only from the trial checkout root?
- Did it avoid developer checkout fallback?
- Did the answer stay read-only?
- Did it avoid proposal-style content?
- Did it avoid YAML-style memory blocks?
- Did it avoid final_trial_result?
- Did it avoid self-classifying PASS / FAIL / PARTIAL?
- Did it include candidate_result: ready_for_human_review?
```

## Final Lock

```text
M191.1 Trial Path Isolation Rerun Prompt
READY / path-isolated rerun prep
```
