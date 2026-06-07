# Beta Observation Loop Baseline

Status: LOCKED / USAGE EVIDENCE PLAN READY
Date: 2026-06-08
Milestone: M223

## Purpose

Define the Beta Run observation loop for Hermes Runes MD Wiki after the first beta smoke passed.

This baseline does not add runtime functionality. It defines how real beta usage evidence should be captured, classified, and fed into later documentation or small-fix decisions.

## Observation Principle

```text
observe first, tune later
record evidence before changing behavior
separate documentation friction from runtime bugs
preserve personal/local scope
avoid enterprise telemetry complexity
```

## Evidence Units

Each beta observation should record one bounded event:

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

## Required Fields

```text
observation_id: required
observed_at: required
host: required
workspace_slug: required
version: required
tag: required
scenario: required
status: PASS | WARN | BLOCKED
summary: required
evidence: required
classification: required
next_action: required
```

## Classification

```text
documentation_friction: command unclear, path confusing, stale wording, missing note
runtime_bug: command fails, Python error, incorrect output, broken script
governance_issue: unsafe write path, unclear trust boundary, missing human-review gate
workspace_slug_issue: hostname-derived slug mismatch, legacy path confusion
publication_issue: release/issue/manual announcement status confusion
security_issue: secrets handling ambiguity, unsafe example, accidental sensitive data risk
non_blocking_note: improvement idea, wording preference, optional enhancement
```

## Status Meaning

```text
PASS: scenario completed and evidence captured
WARN: scenario completed but friction or ambiguity was observed
BLOCKED: scenario could not complete without a fix, clarification, or missing prerequisite
```

## Evidence Safety Boundary

```text
no real secrets
no API keys
no database passwords
no Telegram bot tokens
no private customer data
no raw full prompt/answer/context by default
sanitize logs before committing
```

## Observation Loop

```text
1. Run a bounded beta scenario.
2. Capture exact command/output summary.
3. Classify the result.
4. Decide whether the next action is doc patch, runtime bug fix, deferred note, or no action.
5. Only patch after evidence exists.
6. Re-run a smoke/regression check after any patch.
```

## First Target Scenarios

```text
M224 evidence log template
M225 first real beta usage scenario
M226 beta friction triage
M227 minimal documentation patch round, only if evidence justifies it
M228 second beta smoke/regression
```

## Non-Goals

```text
no new runtime feature development
no automatic heuristic tuning
no automatic wiki write
no enterprise telemetry system
no database observation pipeline
no release automation
```

## Next Step

```text
M224 Beta Run Evidence Log Template
```

## Final Lock

```text
Beta Observation Loop Baseline
LOCKED / usage evidence plan ready
```
