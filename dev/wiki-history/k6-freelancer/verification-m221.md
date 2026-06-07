# M221 Beta Run Entry Criteria Lock / First Beta Smoke Plan

Status: PASS / ENTRY CRITERIA LOCKED / FIRST BETA SMOKE PLAN READY
Date: 2026-06-08

## Evidence Record

```text
docs/beta-run-entry-criteria.md
wiki/k6-freelancer/cb-sessions/cb-20260608-m221-beta-run-entry-criteria-lock.md
docs/open-beta-publication-checklist.md
wiki/k6-freelancer/verification-m220.md
```

## Scope

```text
Beta Run entry criteria
first beta smoke plan
no new runtime functionality
no release automation
```

## Result

```text
PASS
```

## Entry Criteria

```text
entry_version: 0.1.0-beta.1
entry_tag: v0.1.0-beta.1
working_tree_clean_required: yes
hostname_derived_slug_rule_required: yes
notification_sent_no_allowed: yes
m219_1_deferred_allowed: yes
```

## First Beta Smoke Plan

```text
git status / VERSION / tag check
documentation grep for hostname-derived workspace rule
publication grep for notification_sent: no and M219.1 deferred
lightweight Python syntax checks for active starter/runtime files
```

## Next Step

```text
M222 First Beta Smoke Execution / Evidence Capture
```

## Final Lock

```text
M221 Beta Run Entry Criteria Lock / First Beta Smoke Plan
PASS / entry criteria locked / first beta smoke plan ready
```
