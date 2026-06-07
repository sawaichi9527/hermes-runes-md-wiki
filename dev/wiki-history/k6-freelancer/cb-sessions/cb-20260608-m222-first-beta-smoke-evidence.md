# CB-20260608-M222 First Beta Smoke Execution / Evidence Capture

Status: PASS / FIRST BETA SMOKE EXECUTED / EVIDENCE CAPTURED
Date: 2026-06-08
Milestone: M222
Stage: Beta Run

## Purpose

Capture the first Beta Run smoke execution evidence using the M221 entry criteria and smoke plan.

## Inputs

```text
M221 Beta Run entry criteria: PASS
entry_version: 0.1.0-beta.1
entry_tag: v0.1.0-beta.1
```

## Evidence Location

```text
docs/beta-run-first-smoke-evidence.md
```

## Smoke Result

```text
status: PASS
git_pull: already latest
working_tree: clean
version: 0.1.0-beta.1
tag: v0.1.0-beta.1 Open Beta v0.1.0-beta.1
py_compile: PASS
```

## Confirmed Rules

```text
workspace_slug: lowercase(hostname)
wiki_namespace: wiki/<lowercase-hostname>/
freelancer_is_current_dogfood_instance_only: true
notification_sent: no
M219.1 URL backfill: deferred until manual Release/Issue URLs exist
```

## Next Step

```text
M223 Beta Observation Loop Baseline / Usage Evidence Plan
```

## Final Lock

```text
M222 First Beta Smoke Execution / Evidence Capture
PASS / first beta smoke executed / evidence captured
```
