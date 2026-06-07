# M191.1 Trial Path Isolation Prompt / Environment Rerun Prep

Status: READY / PATH-ISOLATED RERUN PREP
Date: 2026-06-07

## Evidence Record

```text
wiki/k6-freelancer/verification-m191.md
wiki/k6-freelancer/cb-sessions/cb-20260607-m191-bt001-read-only-rerun.md
wiki/k6-freelancer/cb-bugs.md
docs/m191-1-trial-path-isolation-rerun-prompt.md
```

## Scope

```text
TB-M191-BT001-FU001 follow-up
trial checkout path isolation
read-only BT-001 rerun prep
no runtime feature development
```

## Result

```text
READY
```

## Rerun Rule

```text
Use only the intended trial checkout evidence root.
Do not fall back to the developer checkout.
If trial evidence files are missing, report path_not_ready instead of searching another checkout.
```

## Bug State

```text
id: TB-M191-BT001-FU001
state_after_M191_1: FIX READY / RERUN REQUIRED
closure_rule: close only after rerun evidence confirms path-isolated read-only behavior
```

## Next Step

```text
Rerun BT-001 using docs/m191-1-trial-path-isolation-rerun-prompt.md.
```

## Final Lock

```text
M191.1 Trial Path Isolation Prompt / Environment Rerun Prep
READY / path-isolated rerun prep
```
