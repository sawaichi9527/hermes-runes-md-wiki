# Beta Run Entry Criteria

Status: LOCKED / FIRST BETA SMOKE PLAN READY
Date: 2026-06-08
Milestone: M221

## Purpose

Define the entry criteria and first smoke plan for starting the Hermes Runes MD Wiki Beta Run after Open Beta publication preparation.

This document does not add new runtime features. It defines the minimum checks required before treating Beta Run as started.

## Entry Version

```text
entry_version: 0.1.0-beta.1
entry_tag: v0.1.0-beta.1
repository: sawaichi9527/hermes-runes-md-wiki
```

## Entry Criteria

```text
git working tree clean: required
VERSION equals 0.1.0-beta.1: required
tag v0.1.0-beta.1 exists: required
README Open Beta boundary present: required
open beta starter guide present: required
workspace slug policy uses lowercase(hostname): required
.env.example explains hostname-derived slug: required
public notification package prepared: required
notification_sent may remain no: allowed
M219.1 URL backfill may remain deferred: allowed
```

## First Beta Smoke Plan

```text
1. git pull
2. git status must be clean
3. cat VERSION must show 0.1.0-beta.1
4. git tag -n --list "v0.1.0-beta.1" must show the Open Beta tag
5. grep documentation for hostname-derived workspace slug rule
6. grep publication records for notification_sent: no and M219.1 deferred
7. run lightweight Python syntax checks for active starter/runtime files
```

## Suggested Smoke Commands

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status
cat VERSION
git tag -n --list "v0.1.0-beta.1"

grep -n "workspace_slug: lowercase(hostname)\|wiki_namespace: wiki/<lowercase-hostname>/\|freelancer_is_current_dogfood_instance_only" \
  wiki/k6-freelancer/verification-m220.md \
  docs/workspace-slug-policy.md \
  docs/open-beta-starter.md

grep -n "notification_sent: no\|M219.1 URL backfill\|m219_1_status: deferred" \
  wiki/k6-freelancer/verification-m220.md \
  docs/open-beta-publication-checklist.md \
  docs/public-notification-send-record.md

python3 -m py_compile \
  bin/hermes_memory_common.py \
  tools/importer/importer_preview.py \
  tools/importer/forge.py \
  tools/importer/forge/create_flat.py \
  tools/importer/memory_answer_generator.py \
  tools/importer/context_builder_v2.py \
  tools/importer/memory_adapter.py \
  tools/importer/retrieval_governance_smoke.py \
  tools/importer/smoke/eval_smoke_m6_6.py \
  tools/local_tools/hermes_memory_tools.py \
  tools/runes/runes.py
```

## Observation Focus

```text
starter path friction
hostname-derived workspace slug behavior
secret-safety messaging clarity
first-run documentation gaps
governed memory workflow clarity
runtime/tool syntax regressions
```

## Non-Goals

```text
no new runtime feature development
no release automation
no GitHub Release/Issue automation
no autonomous trusted memory writing
no enterprise orchestration
```

## Next Step

```text
M222 First Beta Smoke Execution / Evidence Capture
```

## Final Lock

```text
Beta Run Entry Criteria
LOCKED / first beta smoke plan ready
```
