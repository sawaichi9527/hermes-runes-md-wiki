# Second Real Beta Usage Scenario

Status: READY / SCENARIO LOCKED / EXECUTION PENDING
Date: 2026-06-08
Milestone: M227

## Purpose

Define the second bounded real Beta usage scenario for Hermes Runes MD Wiki.

This scenario is read-only and uses a clean trial checkout path to validate the Open Beta starter flow from a more realistic tester perspective. It does not add runtime functionality, does not write wiki memory, and does not create GitHub releases or issues.

## Scenario Identity

```text
observation_id: beta-obs-20260608-002
scenario: clean_checkout_starter_variant
version: 0.1.0-beta.1
tag: v0.1.0-beta.1
host: Freelancer
workspace_slug: freelancer
trial_checkout: ~/workspace/trial/hermes-runes-md-wiki
```

## Scenario Goal

Validate that a clean trial checkout can expose the expected Open Beta starter information and baseline signals:

```text
clean checkout path
VERSION visibility
tag visibility from cloned repository
starter guide visibility
workspace slug policy visibility
publication/deferred status visibility
no runtime mutation
```

## Preconditions

```text
network access to GitHub repository
trial checkout path may be removed/recreated
existing working repo remains untouched except for later evidence capture
tag v0.1.0-beta.1 exists in remote repository
```

## Execution Commands

```bash
mkdir -p ~/workspace/trial
rm -rf ~/workspace/trial/hermes-runes-md-wiki
cd ~/workspace/trial

git clone https://github.com/sawaichi9527/hermes-runes-md-wiki.git
cd hermes-runes-md-wiki

git status
cat VERSION
git tag -n --list "v0.1.0-beta.1"

printf 'host=%s\n' "$(hostname)"
printf 'workspace_slug=%s\n' "$(hostname | tr '[:upper:]' '[:lower:]')"

grep -n "Open Beta\|starter\|workspace" README.md docs/open-beta-starter.md | head -40

grep -n "workspace_slug: lowercase(hostname)\|wiki_namespace: wiki/<lowercase-hostname>/" \
  docs/workspace-slug-policy.md \
  docs/open-beta-starter.md

grep -n "notification_sent: no\|m219_1_status: deferred\|M219.1 URL backfill" \
  docs/open-beta-publication-checklist.md \
  docs/public-notification-send-record.md
```

## Expected Result

```text
clone: PASS
working_tree: clean
version: 0.1.0-beta.1
tag: v0.1.0-beta.1 Open Beta v0.1.0-beta.1
host: Freelancer
workspace_slug: freelancer
starter_docs_visible: yes
workspace_slug_rule_visible: yes
publication_deferred_state_visible: yes
runtime_mutation: no
```

## Evidence Capture Requirement

After execution, record the result using:

```text
docs/beta-run-evidence-log-template.md
```

## Classification Rule

```text
PASS: clean checkout and starter visibility complete without error
WARN: clean checkout completes but starter docs are confusing or incomplete
BLOCKED: clone, VERSION, tag, starter docs, or workspace rule checks fail
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
M227.1 Second Real Beta Usage Evidence Capture
```

## Final Lock

```text
Second Real Beta Usage Scenario
READY / scenario locked / execution pending
```
