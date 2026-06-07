# CB-20260608-M221 Beta Run Entry Criteria Lock / First Beta Smoke Plan

Status: PASS / ENTRY CRITERIA LOCKED / FIRST BETA SMOKE PLAN READY
Date: 2026-06-08
Milestone: M221
Stage: Beta Run Entry

## Purpose

Lock the Beta Run entry criteria and first smoke plan after Open Beta publication preparation is complete.

## Inputs

```text
M220 Open Beta publication final recap: PASS
entry_version: 0.1.0-beta.1
entry_tag: v0.1.0-beta.1
M219.1 URL backfill: deferred / not blocking Beta Run entry
```

## Created File

```text
docs/beta-run-entry-criteria.md
```

## Entry Criteria Summary

```text
clean working tree
VERSION equals 0.1.0-beta.1
tag v0.1.0-beta.1 exists
hostname-derived workspace slug rule documented
.env.example clarifies hostname-derived slug
notification package prepared
notification_sent may remain no
M219.1 URL backfill may remain deferred
```

## First Beta Smoke Plan Summary

```text
git pull / status / VERSION / tag check
documentation grep for workspace slug rule
publication grep for notification_sent no and M219.1 deferred
lightweight Python syntax checks for active starter/runtime files
```

## Non-Goals

```text
no new runtime functionality
no release automation
no GitHub Release/Issue automation
no autonomous trusted memory writing
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
