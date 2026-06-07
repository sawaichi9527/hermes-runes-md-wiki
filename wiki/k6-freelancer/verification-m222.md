# M222 First Beta Smoke Execution / Evidence Capture

Status: PASS / FIRST BETA SMOKE EXECUTED / EVIDENCE CAPTURED
Date: 2026-06-08

## Evidence Record

```text
docs/beta-run-first-smoke-evidence.md
wiki/k6-freelancer/cb-sessions/cb-20260608-m222-first-beta-smoke-evidence.md
docs/beta-run-entry-criteria.md
```

## Scope

```text
first Beta Run smoke execution
version and tag check
hostname-derived workspace slug rule check
notification/deferred-publication check
Python syntax checks
no new runtime functionality
```

## Result

```text
PASS
```

## Smoke Result

```text
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
m219_1_status: deferred until manual URLs exist
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
