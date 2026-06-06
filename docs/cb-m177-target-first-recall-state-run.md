# M177 Target-first Recall-state Run Prompt

Status: READY / PROMPT LOCKED
Date: 2026-06-07

## Instruction

```text
Answer the target scenario first. Do not inspect unrelated fixtures before the target answer. Do not assume recall success without target-specific evidence.
```

## Required Result Format

```text
scenario:
target_answer:
evidence_seen:
boundary_result:
next_action:
```
