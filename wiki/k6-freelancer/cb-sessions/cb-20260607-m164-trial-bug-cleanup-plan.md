# CB-20260607-M164 Trial Bug Cleanup Plan

Status: PASS / TRIAL BUG CLEANUP PLAN LOCKED
Date: 2026-06-07
Milestone: M164
Stage: Closed Beta / Controlled CB

## Purpose

Classify open Trial Bug records after the M163 CB mini baseline lock.

M164 is a cleanup planning milestone. It does not directly close bugs, rewrite the large trial bug registry, add runtime behavior, or change policy automatically.

## Input Bug Set

```text
TB-20260607-001 OPEN / M156 trial-root quote typo
TB-20260607-002 OPEN / registry restore follow-up recorded; fix commit exists: 2e8b8bd
TB-20260607-003 OPEN / M157 prompt path initially resolved outside repo before fallback
TB-20260607-004 OPEN / placeholder append path caused local append failure
TB-20260607-005 OPEN / M158 optional reference file lookup failed but did not block session
TB-20260607-006 OPEN / M161 scenario drifted to existing recall-verified fixtures; M161.1 mitigation evidence recorded
```

## Cleanup Classification

### Fix now candidates

```text
TB-20260607-003 / prompt path initially resolved outside repo
TB-20260607-004 / placeholder append path caused local append failure
TB-20260607-005 / optional reference file lookup failed
```

Rationale:
- These are workflow/prompt/file-reference issues.
- They can be reduced by prompt hardening, absolute paths, and replacing placeholder instructions with concrete paths.

### Keep open as guidance evidence

```text
TB-20260607-001 / M156 trial-root quote typo
TB-20260607-002 / registry restore follow-up recorded
TB-20260607-006 / M161 scenario drift; M161.1 mitigation evidence recorded
```

Rationale:
- TB-001 is low severity and useful as a reminder to keep agent quotes exact.
- TB-002 should remain visible because it records the registry restore incident and the rule against full-file overwrite from truncated tool fetch content.
- TB-006 has mitigation evidence but remains useful as target-first recall guidance.

### Defer to later CB mini-cycle

```text
No hard blocker currently requires deferral before continuing CB.
```

## Cleanup Rules

```text
Do not bulk rewrite trial-bugs.md through fetched partial content.
Use append-only updates or local edits for large registry changes.
Keep TB status changes explicit and reviewable.
Do not mark a bug FIXED only because a mitigation exists.
Do not let cleanup mutate runtime policy automatically.
```

## Recommended Next Steps

```text
M165 Strict Prompt Hardening Sweep
- absolute trial-root paths
- no placeholder paths
- optional reference files explicit
- target-first recall prompts

M166 CB Mini-cycle 2 Entry Criteria
- decide which scenarios to rerun
- decide which bug statuses can move from OPEN to FIXED or GUIDANCE
```

## Final Result

```text
M164 Trial Bug Cleanup Plan
PASS / cleanup classification locked / no registry status mutation performed
```
