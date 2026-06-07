# Beta Regression / Smoke Replay - M229

Status: READY / REGRESSION SMOKE REPLAY PLAN LOCKED / EXECUTION PENDING
Date: 2026-06-08
Milestone: M229

## Purpose

Define the Beta regression / smoke replay after two real Beta observations passed and M228 determined that no patch round is required.

This plan does not add runtime functionality and does not patch documentation. It replays the core smoke checks to confirm the Beta evidence loop did not break the baseline.

## Replay Scope

```text
repo sync and clean tree
VERSION check
tag check
workspace slug rule visibility
publication deferred state visibility
observation evidence visibility
Python syntax check for active files
```

## Preconditions

```text
M228: PASS / two observations pass / no patch required
working repo: ~/workspace/hermes-runes-md-wiki
version: 0.1.0-beta.1
tag: v0.1.0-beta.1
```

## Execution Commands

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status
cat VERSION
git tag -n --list "v0.1.0-beta.1"

grep -n "workspace_slug: lowercase(hostname)\|wiki_namespace: wiki/<lowercase-hostname>/" \
  docs/workspace-slug-policy.md \
  docs/open-beta-starter.md \
  wiki/k6-freelancer/verification-m220.md

grep -n "notification_sent: no\|m219_1_status: deferred\|M219.1 URL backfill" \
  docs/open-beta-publication-checklist.md \
  docs/public-notification-send-record.md \
  wiki/k6-freelancer/verification-m220.md

grep -n "Status:\|beta-obs-20260608-001\|beta-obs-20260608-002\|patch_round_required_now\|regression_smoke_replay" \
  docs/beta-observation-recap-m228.md \
  docs/beta-observations/beta-obs-20260608-001-starter-followthrough.md \
  docs/beta-observations/beta-obs-20260608-002-clean-checkout-starter-variant.md \
  wiki/k6-freelancer/verification-m228.md

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

## Expected Result

```text
working_tree: clean
version: 0.1.0-beta.1
tag: v0.1.0-beta.1 Open Beta v0.1.0-beta.1
workspace_slug_rule_visible: yes
publication_deferred_state_visible: yes
observation_evidence_visible: yes
py_compile: PASS
```

## Classification Rule

```text
PASS: all replay checks complete without error
WARN: replay completes but evidence wording is ambiguous
BLOCKED: any replay command fails or required evidence is missing
```

## Safety Boundary

```text
no real secrets
no API keys
no database passwords
no Telegram bot tokens
no private customer data
sanitize logs before committing
```

## Next Step

```text
M229.1 Beta Regression / Smoke Replay Evidence Capture
```

## Final Lock

```text
Beta Regression / Smoke Replay M229
READY / regression smoke replay plan locked / execution pending
```
