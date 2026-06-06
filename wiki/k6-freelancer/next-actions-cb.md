# Closed Beta Next Actions

Status: ACTIVE / M164 CLEANUP PLAN LOCKED / M165 READY
Date: 2026-06-07

## Current Stage

```text
M164 Trial Bug Cleanup Plan
PASS / cleanup classification locked / no registry status mutation performed
```

## Locked CB Chain

```text
M147 PASS / post-trial baseline locked / CB-prep roadmap set
M148 PASS / observation mechanism CB-ready / minimal evidence path locked
M149 PASS / model endpoint optional for CB entry
M150 PASS / CB smoke bundle defined / existing checks only
M151 PASS / CB entry criteria locked / personal-scope early test ready
M152 PASS / Closed Beta started / controlled CB mode active
M153 PASS / first CB session evidence captured
M154 PASS / first CB session prompt ready / real agent run completed
M155 PASS / first CB session result locked / read-only governance verified
M156 PASS / trial-root discipline verified / read-only
M156.1 PASS / registry restored / fix applied
M157 PASS / read-only technical analysis verified / proposal-first boundary preserved
M158 PASS / proposal-first draft verified / no trusted wiki mutation
M159 PASS / hold decision respected / trusted memory unchanged
M160 PASS / approved path explained / governed workflow boundary preserved
M161 PARTIAL / recall verification useful but scenario drift observed
M161.1 PASS / strict target answer verified / no target state assumed
M162 PASS / observation review completed / lightweight tuning candidates recorded
M163 PASS / CB mini baseline locked / continue controlled CB iteration
M164 PASS / cleanup classification locked / no registry status mutation performed
```

## Current Open CB Bug Records

```text
TB-20260607-001 OPEN / M156 trial-root quote typo
TB-20260607-002 OPEN / registry restore follow-up recorded; fix commit exists: 2e8b8bd
TB-20260607-003 OPEN / M157 prompt path initially resolved outside repo before fallback
TB-20260607-004 OPEN / placeholder append path caused local append failure
TB-20260607-005 OPEN / M158 optional reference file lookup failed but did not block session
TB-20260607-006 OPEN / M161 scenario drifted to existing recall-verified fixtures instead of answering unverified M160 content state; M161.1 mitigation evidence recorded
```

## M164 Result

```text
Evidence record:
wiki/k6-freelancer/cb-sessions/cb-20260607-m164-trial-bug-cleanup-plan.md

Result:
PASS
```

M164 classifies open Trial Bugs without directly mutating registry statuses.

## Cleanup Classification

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

## Immediate Next Action

Pull the M164 result lock and verify the cleanup plan.

Developer checkout:

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status
git log --oneline -12

for f in \
  wiki/k6-freelancer/verification-m164.md \
  wiki/k6-freelancer/cb-sessions/cb-20260607-m164-trial-bug-cleanup-plan.md \
  wiki/k6-freelancer/next-actions-cb.md; do
  echo "== $f =="
  grep -n "Status:\|Final Lock\|M164\|M165\|cleanup\|Cleanup\|TB-20260607\|PASS /" "$f"
done
```

Trial checkout:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short

grep -n "Status:\|Final Lock\|M164\|M165\|cleanup\|Cleanup\|TB-20260607\|PASS /" \
  wiki/k6-freelancer/verification-m164.md \
  wiki/k6-freelancer/cb-sessions/cb-20260607-m164-trial-bug-cleanup-plan.md \
  wiki/k6-freelancer/next-actions-cb.md
```

## Next Candidate Milestone

```text
M165 Strict Prompt Hardening Sweep
```

M165 should implement the fix-now prompt/workflow hardening candidates identified by M164 without changing runtime behavior.
