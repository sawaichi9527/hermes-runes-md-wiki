# First Real Beta Usage Scenario

Status: READY / SCENARIO LOCKED / EXECUTION PENDING
Date: 2026-06-08
Milestone: M225

## Purpose

Define the first bounded real Beta usage scenario for Hermes Runes MD Wiki.

This scenario is intentionally read-only. It does not add runtime functionality, does not write wiki memory, and does not create GitHub releases or issues.

## Scenario Identity

```text
observation_id: beta-obs-20260608-001
scenario: starter_followthrough
version: 0.1.0-beta.1
tag: v0.1.0-beta.1
host: Freelancer
workspace_slug: freelancer
```

## Scenario Goal

Simulate a first beta user following the starter path far enough to verify:

```text
repository sync
version/tag visibility
starter documentation visibility
hostname-derived workspace slug rule
Open Beta notification/deferred-publication clarity
basic active Python syntax health
```

## Preconditions

```text
working tree should be clean
VERSION should be 0.1.0-beta.1
tag v0.1.0-beta.1 should exist
M219.1 URL backfill may remain deferred
notification_sent may remain no
```

## Execution Commands

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status
cat VERSION
git tag -n --list "v0.1.0-beta.1"

printf 'host=%s\n' "$(hostname)"
printf 'workspace_slug=%s\n' "$(hostname | tr '[:upper:]' '[:lower:]')"

grep -n "workspace_slug: lowercase(hostname)\|wiki_namespace: wiki/<lowercase-hostname>/" \
  docs/workspace-slug-policy.md \
  docs/open-beta-starter.md \
  wiki/k6-freelancer/verification-m220.md

grep -n "notification_sent: no\|m219_1_status: deferred\|M219.1 URL backfill" \
  docs/open-beta-publication-checklist.md \
  docs/public-notification-send-record.md \
  wiki/k6-freelancer/verification-m220.md

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
host: Freelancer
workspace_slug: freelancer
workspace_slug_rule: visible
publication_deferred_state: visible
py_compile: PASS
```

## Evidence Capture Requirement

After execution, record the result using:

```text
docs/beta-run-evidence-log-template.md
```

## Classification Rule

```text
PASS: all checks complete without error
WARN: checks complete but docs are confusing or ambiguous
BLOCKED: any command fails or required starter path evidence is missing
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
M225.1 First Real Beta Usage Evidence Capture
```

## Final Lock

```text
First Real Beta Usage Scenario
READY / scenario locked / execution pending
```
