# M164 Trial Bug Cleanup Plan

Status: PASS / TRIAL BUG CLEANUP PLAN LOCKED
Date: 2026-06-07

## Scope

M164 classifies open Trial Bug records after the M163 CB mini baseline lock.

This is a cleanup planning milestone, not a runtime feature milestone and not a registry mutation milestone.

## Evidence Record

```text
wiki/k6-freelancer/cb-sessions/cb-20260607-m164-trial-bug-cleanup-plan.md
```

## Input Bugs

```text
TB-20260607-001 OPEN / M156 trial-root quote typo
TB-20260607-002 OPEN / registry restore follow-up recorded; fix commit exists: 2e8b8bd
TB-20260607-003 OPEN / M157 prompt path initially resolved outside repo before fallback
TB-20260607-004 OPEN / placeholder append path caused local append failure
TB-20260607-005 OPEN / M158 optional reference file lookup failed but did not block session
TB-20260607-006 OPEN / M161 scenario drifted to existing recall-verified fixtures; M161.1 mitigation evidence recorded
```

## Classification

```text
Fix now candidates:
- TB-20260607-003
- TB-20260607-004
- TB-20260607-005

Keep open as guidance evidence:
- TB-20260607-001
- TB-20260607-002
- TB-20260607-006

Defer to later CB mini-cycle:
- none as blocker
```

## Result

```text
PASS
```

## Cleanup Constraints

```text
No bulk rewrite of trial-bugs.md through fetched partial content.
Use append-only updates or local edits for large registry changes.
Do not mark bugs FIXED only because mitigation exists.
Do not mutate runtime policy automatically.
```

## Next Action

Proceed to:

```text
M165 Strict Prompt Hardening Sweep
```

## Final Lock

```text
M164 Trial Bug Cleanup Plan
PASS / cleanup classification locked / no registry status mutation performed
```
