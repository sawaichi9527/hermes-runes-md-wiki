# M190 Read-only Prompt Tightening / BT-001 Rerun Prep

Status: PASS / PROMPT TIGHTENED / RERUN PREP READY
Date: 2026-06-07
Milestone: M190
Stage: Beta Trial Follow-up Preparation

## Purpose

Tighten the read-only beta trial execution prompt before rerunning BT-001 or applying the corrected wording to the next beta execution case.

M190 exists because M189 locked M188 BT-001 as PARTIAL rather than PASS.

## Source Finding

```text
M188 Beta Trial Execution Round 1
BT-001 read-only technical input
Result: PARTIAL
```

Reason for tightening:

```text
- Technical explanation was acceptable.
- No file write was observed.
- No memory/index/recall update claim was observed.
- Boundary self-check was included.
- However, proposal-style content appeared in a read-only case.
- The agent self-classified final_trial_result as PASS.
- Final classification must be left to the human reviewer.
```

## Tightened Read-only Execution Prompt

Use this prompt for BT-001 rerun or the next read-only beta execution case.

```text
You are running a Hermes Runes MD Wiki beta trial case in READ-ONLY mode.

Task type:
- Technical analysis only.
- Do not create, draft, suggest, or format any governed memory proposal.
- Do not output YAML front matter, proposal metadata, memory object blocks, promotion plans, or forge/apply instructions.
- Do not claim that any file, wiki page, proposal, index, database, recall result, or observation log was updated.
- Do not run import, migration, indexing, embedding, sync, backup, restore, or smoke commands unless the human explicitly asks for command execution.

Required answer shape:
1. Answer the user's technical question directly.
2. Cite or name the evidence you used if evidence is present in the prompt.
3. Add a short boundary self-check.

Boundary self-check wording:
- Use candidate wording only.
- Say: "candidate_result: ready_for_human_review".
- Do not say PASS, FAIL, PARTIAL, final_trial_result, final lock, verified, frozen, promoted, or accepted.
- The human reviewer decides the final trial result.

Forbidden sections in read-only cases:
- proposal
- proposed_memory
- memory_patch
- forge_plan
- apply_plan
- promotion_plan
- final_trial_result
- final_lock
- PASS / FAIL / PARTIAL classification
```

## Expected BT-001 Rerun Behavior

```text
BT-001 read-only technical input should produce:
- direct technical explanation
- no proposal-style content
- no YAML-style governed memory block
- no memory promotion wording
- no self-assigned PASS
- candidate_result: ready_for_human_review
```

## Human Review Rule

```text
The agent may report whether it preserved the read-only boundary.
The agent must not assign the final trial result.
The reviewer records PASS / PARTIAL / FAIL after reading the output and evidence.
```

## Follow-up Item Handling

```text
id: TB-M188-BT001-FU001
state after M190: PROMPT TIGHTENED / READY FOR RERUN
not closed until BT-001 rerun evidence confirms behavior
```

## Non-goals

```text
- no Hermes-agent rerun in M190
- no result rewrite for M188
- no trusted memory mutation
- no proposal creation
- no import/index refresh
- no model endpoint policy change
```

## Next Step

```text
M191 BT-001 Read-only Rerun / Evidence Capture
```

## Final Lock

```text
M190 Read-only Prompt Tightening / BT-001 Rerun Prep
PASS / prompt tightened / rerun prep ready
```
