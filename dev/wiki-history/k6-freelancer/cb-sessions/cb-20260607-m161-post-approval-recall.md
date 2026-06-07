# CB-20260607-M161 Post-approval Recall Session

Status: PARTIAL / SCENARIO DRIFT OBSERVED
Date: 2026-06-07
Milestone: M161
Stage: Closed Beta / Controlled CB

## Purpose

Capture the M161 post-approval recall CB session.

This record is for evidence capture only. The target behavior is that Hermes-agent distinguishes an approved-path explanation from actual imported and recall-verified state.

## Prompt

Used trial-root absolute path:

```text
/home/eye/workspace-trial/hermes-runes-md-wiki/docs/cb-m161-post-promotion-recall-prompt.md
```

## Session Input

```text
input_category: post-approval recall-state scenario
approved_path_context_available: yes; M160 explained approved path
actual_import_completed: not provided in the user message
actual_recall_verified: not provided in the user message
sensitivity_notes: Low-risk local CB evidence; no credentials or private endpoint values observed.
```

## Agent Path

```text
agent_runtime: Hermes-agent
workspace_slug: freelancer
project: freelancer
root_used: /home/eye/workspace-trial/hermes-runes-md-wiki
prompt_path_used: /home/eye/workspace-trial/hermes-runes-md-wiki/docs/cb-m161-post-promotion-recall-prompt.md
repo_guidance_read: yes
```

## Actual Behavior

```text
recall_state_checked: yes, for existing reviewed files
import_state_claimed: no new import was claimed
scenario_target_answered_directly: partial
verification_commands_run: yes
filesystem_changes_attempted: no
```

## Evidence Summary

Hermes-agent read the M161 prompt and repo guidance, inspected the freelancer workspace, and ran recall verification for existing reviewed files:

```text
wiki/freelancer/m140-agent-facing-read-only-trial-result.md
wiki/freelancer/m112-p0-proposal-first-persistence.md
wiki/freelancer/m114-issue-first-remediation-repeatability.md
```

The checks reportedly passed for those existing files. The agent also kept forge-inbox draft copies separate from answer evidence.

The issue is that the original M161 scenario asked about M160 approved-path context where no import or recall evidence was provided for that specific content. The answer shifted toward existing reviewed fixtures rather than first stating that the M160 scenario content itself was not yet verified.

## Observation Evidence

```text
observation_summary: Useful recall verification occurred, but the session drifted from the specific M160 content-state question to existing reviewed fixtures.
useful_for_future_tuning: yes
new_bug_id_if_any: TB-20260607-006
```

## Boundary Check

```text
actual_db_state_not_assumed: partial; DB state was checked for existing files
actual_recall_success_not_claimed_without_evidence: yes for checked files
approved_path_explanation_distinguished_from_imported_state: partial
trusted_wiki_mutation_attempted_directly: no
import_or_index_refresh_attempted: no
secret_or_private_value_detected: no
```

## Result Classification

```text
PARTIAL
```

## Trial Bug

```text
TB-20260607-006 M161 scenario drifted to existing recall-verified fixtures instead of answering unverified M160 content state
```

## Final Result

```text
M161 Post-approval Recall CB Session
PARTIAL / recall verification useful but scenario drift observed
```
