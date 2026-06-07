# First Beta Smoke Evidence

Status: PASS / FIRST BETA SMOKE EXECUTED / EVIDENCE CAPTURED
Date: 2026-06-08
Milestone: M222

## Purpose

Capture the first Beta Run smoke execution evidence after M221 entry criteria were locked.

This evidence records the first Beta Run smoke. It does not add runtime functionality.

## Smoke Scope

```text
git sync / clean working tree
VERSION check
tag check
hostname-derived workspace slug documentation check
publication notification/deferred URL status check
lightweight Python syntax checks for active starter/runtime files
```

## Execution Result

```text
status: PASS
working_tree: clean
version: 0.1.0-beta.1
tag: v0.1.0-beta.1 Open Beta v0.1.0-beta.1
py_compile: PASS
```

## Version / Tag Evidence

```text
git pull: already latest
git status: working tree clean
cat VERSION: 0.1.0-beta.1
git tag -n --list "v0.1.0-beta.1": v0.1.0-beta.1 Open Beta v0.1.0-beta.1
```

## Workspace Slug Evidence

```text
wiki/k6-freelancer/verification-m220.md: workspace_slug: lowercase(hostname)
wiki/k6-freelancer/verification-m220.md: wiki_namespace: wiki/<lowercase-hostname>/
wiki/k6-freelancer/verification-m220.md: freelancer_is_current_dogfood_instance_only: true
docs/workspace-slug-policy.md: workspace_slug: lowercase(hostname)
docs/workspace-slug-policy.md: wiki_namespace: wiki/<lowercase-hostname>/
```

## Publication Deferred Evidence

```text
wiki/k6-freelancer/verification-m220.md: notification_sent: no
wiki/k6-freelancer/verification-m220.md: M219.1 URL backfill: deferred until manual Release/Issue URLs exist
docs/open-beta-publication-checklist.md: notification_sent: no
docs/open-beta-publication-checklist.md: m219_1_status: deferred until manual URLs exist
docs/public-notification-send-record.md: notification_sent: no
```

## Python Syntax Check Evidence

```text
python3 -m py_compile completed with no output and no error.
```

Checked files:

```text
bin/hermes_memory_common.py
tools/importer/importer_preview.py
tools/importer/forge.py
tools/importer/forge/create_flat.py
tools/importer/memory_answer_generator.py
tools/importer/context_builder_v2.py
tools/importer/memory_adapter.py
tools/importer/retrieval_governance_smoke.py
tools/importer/smoke/eval_smoke_m6_6.py
tools/local_tools/hermes_memory_tools.py
tools/runes/runes.py
```

## Observation Focus For Next Beta Runs

```text
starter path friction
hostname-derived workspace slug behavior
notification/deferred-publication clarity
secret-safety messaging clarity
first-run documentation gaps
governed memory workflow clarity
runtime/tool syntax regressions
```

## Next Step

```text
M223 Beta Observation Loop Baseline / Usage Evidence Plan
```

## Final Lock

```text
First Beta Smoke Evidence
PASS / first beta smoke executed / evidence captured
```
