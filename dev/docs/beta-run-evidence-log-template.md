# Beta Run Evidence Log Template

Status: TEMPLATE LOCKED / READY FOR BETA OBSERVATIONS
Date: 2026-06-08
Milestone: M224

## Purpose

Provide a consistent template for recording Hermes Runes MD Wiki Beta Run observations.

This template is for evidence capture only. It does not add runtime functionality.

## Usage

Copy this template for each bounded beta observation. Keep each entry small, sanitized, and tied to one scenario.

## Template

```markdown
# Beta Observation - <observation_id>

Status: <PASS | WARN | BLOCKED>
Date: <YYYY-MM-DD>
Version: 0.1.0-beta.1
Tag: v0.1.0-beta.1
Host: <hostname>
Workspace Slug: <lowercase(hostname)>
Scenario: <scenario_type>

## Summary

<One to three sentences summarizing what was tested and what happened.>

## Command / Action

```text
<Exact command, user action, or doc step followed. Remove secrets before committing.>
```

## Evidence

```text
<Relevant output summary. Do not include secrets, tokens, passwords, private customer data, or raw full prompt/context.>
```

## Classification

```text
classification: <documentation_friction | runtime_bug | governance_issue | workspace_slug_issue | publication_issue | security_issue | non_blocking_note>
severity: <low | medium | high>
```

## Result

```text
status: <PASS | WARN | BLOCKED>
blocking: <yes | no>
reproducible: <yes | no | unknown>
```

## Next Action

```text
next_action: <no_action | doc_patch | runtime_fix | governance_review | defer | rerun_smoke>
owner: <human | future_milestone | none>
```

## Safety Review

```text
secrets_removed: yes
private_data_removed: yes
raw_full_prompt_or_context_included: no
safe_to_commit: yes
```

## Final Lock

```text
Beta Observation <observation_id>
<status> / evidence captured / next action recorded
```
```

## Scenario Types

```text
smoke_run
starter_followthrough
clean_checkout_trial
hostname_slug_trial
first_recall_trial
governance_path_trial
documentation_friction
runtime_error
secret_safety_review
```

## Status Rules

```text
PASS: scenario completed and evidence was captured
WARN: scenario completed but friction or ambiguity was observed
BLOCKED: scenario could not complete without a fix, clarification, or missing prerequisite
```

## Safety Boundary

```text
Do not commit real secrets.
Do not commit API keys.
Do not commit database passwords.
Do not commit Telegram bot tokens.
Do not commit private customer data.
Do not commit raw full prompt/answer/context by default.
Sanitize logs before committing.
```

## Next Step

```text
M225 First Real Beta Usage Scenario
```

## Final Lock

```text
Beta Run Evidence Log Template
TEMPLATE LOCKED / ready for beta observations
```
