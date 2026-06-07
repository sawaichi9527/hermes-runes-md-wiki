# Open Beta Publication Checklist

Status: BETA OBSERVATION / REGRESSION RECAP COMPLETE / STATUS LOCK READY
Date: 2026-06-08

## Purpose

Prepare Hermes Runes MD Wiki for Open Beta publication as a public GitHub repository and transition from publication prep into Beta Run evidence collection.

This record tracks publication readiness, release tag status, public tester notification package readiness, deferred manual URL backfill status, Beta Run entry criteria readiness, beta smoke evidence, beta observation readiness, first and second real beta usage evidence, observation recap status, regression smoke replay evidence, and final recap readiness for a Beta Run status lock.

## Current Repository State

```text
repository: sawaichi9527/hermes-runes-md-wiki
visibility: public
open_beta_target: public GitHub repository
current_phase: Beta observation / regression recap complete / status lock ready
```

## Open Beta Boundary

```text
Open Beta means:
- public repository access
- free download for evaluation and personal/local use
- feedback and issue discovery are welcome
- documentation and implementation may still change

Open Beta does not mean:
- production stability guarantee
- enterprise support commitment
- stable release
- autonomous trusted memory writing
- automatic proposal apply
- storage of user secrets in the wiki
```

## Public Safety Checklist

```text
README: present
Open Beta starter guide: present
.env example starter path: updated, hostname-derived slug comment corrected
trial templates starter path: updated
.gitignore: present and excludes local runtime artifacts
Open Beta status note: visible in README
Security policy: present
License: Apache-2.0 applied
Version file: present
Changelog: present
Versioning policy: present
Workspace slug policy: corrected to hostname-derived slug
Public download audit: complete
Runtime/tool sweep: PASS / active blockers cleared
First Open Beta tag: created
Public tester notification draft: prepared
Public tester notification final: reviewed / send-ready / not sent
Public notification channel lock: GitHub Release + GitHub Issue
Manual send URL backfill: deferred / URLs pending / not required for Beta Run entry
Beta Run entry criteria: locked
First beta smoke plan: ready
First beta smoke evidence: PASS
Beta observation loop baseline: locked
Usage evidence plan: ready
Beta Run evidence log template: locked
First real beta usage scenario: locked
First real beta usage evidence: PASS
Beta friction triage: PASS / no patch required
Second real beta usage scenario: locked
Second real beta usage evidence: PASS
Beta observation recap: PASS / no patch required
Beta regression smoke replay plan: locked
Beta regression smoke replay evidence: PASS
Beta observation / regression recap: PASS / status lock ready
```

## Workspace Slug Note

```text
canonical_active_slug_rule: lowercase(hostname)
canonical_wiki_namespace_rule: wiki/<lowercase-hostname>/
current_dogfood_host: Freelancer
current_dogfood_workspace_slug: freelancer
current_dogfood_wiki_namespace: wiki/freelancer/
legacy_engineering_namespace: wiki/k6-freelancer/
clean_trial_checkout: ~/workspace/trial/hermes-runes-md-wiki
deprecated_trial_checkout: ~/workspace-trial/hermes-runes-md-wiki
```

## Version Note

```text
current_version: 0.1.0-beta.1
planned_tag: v0.1.0-beta.1
tag_status: created
post_tag_hotfix: workspace slug policy and env example comment corrected after tag
```

## M209 Audit Result

```text
result: PASS for audit completion
release_tag_ready: no
public_tester_notification_ready: no
blocker: remaining public-facing and active-tool legacy references required remediation
```

## M210 Starter Cleanup Result

```text
starter_cleanup: PASS
release_tag_ready: no
public_tester_notification_ready: no
remaining_blocker: active runtime/tool legacy sweep
```

## M211 Runtime/Tool Sweep Result

```text
runtime_tool_sweep: PARTIAL
release_tag_ready: no
public_tester_notification_ready: no
remaining_blocker: local patch required for active runtime/tool legacy defaults
```

## M212 Runtime/Tool Local Patch Result

```text
runtime_tool_patch: PASS
release_tag_ready: yes, pending M213 release lock
public_tester_notification_ready: not yet
remaining_blocker: release lock and tag creation
```

## M213 First Open Beta Tag Result

```text
release_lock: PASS
release_tag_ready: yes
tag_name: v0.1.0-beta.1
tag_status: created
```

## M214 Host-Derived Slug Policy Correction

```text
policy_hotfix: PASS
fixed_statement: freelancer is not universal default
correct_rule: workspace slug is lowercase(hostname)
current_instance: Freelancer -> freelancer
release_tag_change: none
```

## M214.1 Env Example Host Slug Hotfix

```text
env_example_hotfix: PASS
fixed_file: tools/importer/.env.example
correct_rule: workspace/project defaults should be lowercase(hostname)
current_instance: Freelancer -> freelancer
release_tag_change: none
```

## M215 Public Tester Notification Draft

```text
notification_draft: PASS
notification_sent: no
draft_file: docs/public-tester-notification-draft.md
workspace_slug_rule_included: lowercase(hostname)
secrets_boundary_included: yes
feedback_scope_included: yes
```

## M216 Public Tester Notification Review / Send Decision

```text
notification_final_review: PASS
send_decision: ready_for_manual_send
notification_sent: no
manual_send_required: yes
final_file: docs/public-tester-notification-final.md
```

## M217 Public Notification Channel Selection / Manual Send Record

```text
send_record_scaffold: PASS
notification_sent: no
manual_send_required: yes
send_record_file: docs/public-notification-send-record.md
```

## M218 Manual Notification Send / Feedback Channel Lock

```text
channel_lock: PASS
primary_public_channel: GitHub Release note for v0.1.0-beta.1
feedback_channel: GitHub Issue for Open Beta feedback
notification_sent: no
manual_send_required: yes
```

## M219 Manual Send Result Record / URL Backfill Template

```text
url_backfill_template: BLOCKED / DEFERRED
release_url: pending_manual_publication
feedback_issue_url: pending_manual_publication
notification_sent: no
m219_1_status: deferred until manual URLs exist
```

## M220 Open Beta Publication Final Recap / Beta Run Entry Point

```text
publication_recap: PASS
entry_version: 0.1.0-beta.1
entry_tag: v0.1.0-beta.1
beta_run_entry_ready: yes
new_runtime_functionality_added: no
release_automation_added: no
```

## M221 Beta Run Entry Criteria Lock / First Beta Smoke Plan

```text
entry_criteria: PASS
entry_version: 0.1.0-beta.1
entry_tag: v0.1.0-beta.1
first_beta_smoke_plan: ready
new_runtime_functionality_added: no
release_automation_added: no
```

## M222 First Beta Smoke Execution / Evidence Capture

```text
first_beta_smoke: PASS
working_tree: clean
version: 0.1.0-beta.1
tag: v0.1.0-beta.1
py_compile: PASS
next_step: M223 Beta Observation Loop Baseline / Usage Evidence Plan
```

## M223 Beta Observation Loop Baseline / Usage Evidence Plan

```text
observation_loop_baseline: PASS
usage_evidence_plan: ready
classification_rules: documented
safety_boundary: documented
new_runtime_functionality_added: no
next_step: M224 Beta Run Evidence Log Template
```

## M224 Beta Run Evidence Log Template

```text
evidence_log_template: PASS
template_file: docs/beta-run-evidence-log-template.md
required_fields: documented
classification_fields: documented
safety_review_fields: documented
new_runtime_functionality_added: no
next_step: M225 First Real Beta Usage Scenario
```

## M225 First Real Beta Usage Scenario

```text
scenario_lock: PASS
observation_id: beta-obs-20260608-001
scenario: starter_followthrough
host: Freelancer
workspace_slug: freelancer
execution_done: yes
evidence_captured: yes
```

## M225.1 First Real Beta Usage Evidence Capture

```text
usage_evidence: PASS
observation_id: beta-obs-20260608-001
scenario: starter_followthrough
classification: non_blocking_note
severity: low
blocking: no
next_step: M226 Beta Friction Triage
```

## M226 Beta Friction Triage

```text
triage_result: PASS
blocking_issue_found: no
patch_required: no
runtime_fix_required: no
documentation_patch_required: no
governance_review_required: no
next_step: M227 Second Real Beta Usage Scenario / Starter Followthrough Variant
```

## M227 Second Real Beta Usage Scenario / Starter Followthrough Variant

```text
scenario_lock: PASS
observation_id: beta-obs-20260608-002
scenario: clean_checkout_starter_variant
host: Freelancer
workspace_slug: freelancer
trial_checkout: ~/workspace/trial/hermes-runes-md-wiki
execution_done: yes
evidence_captured: yes
```

## M227.1 Second Real Beta Usage Evidence Capture

```text
usage_evidence: PASS
observation_id: beta-obs-20260608-002
scenario: clean_checkout_starter_variant
classification: non_blocking_note
severity: low
blocking: no
next_step: M228 Beta Observation Recap / Second Triage Decision
```

## M228 Beta Observation Recap / Second Triage Decision

```text
recap_result: PASS
observations_reviewed: 2
blocking_issue_found: no
patch_round_required_now: no
documentation_patch_required_now: no
runtime_fix_required_now: no
governance_review_required_now: no
next_step: M229 Beta Regression / Smoke Replay
```

## M229 Beta Regression / Smoke Replay

```text
replay_plan: PASS
replay_plan_locked: yes
execution_done: yes
evidence_captured: yes
```

## M229.1 Beta Regression / Smoke Replay Evidence Capture

```text
replay_evidence: PASS
observation_id: beta-obs-20260608-003
scenario: regression_smoke_replay
classification: non_blocking_note
severity: low
blocking: no
corrected_py_compile_rerun: PASS
next_step: M230 Beta Observation / Regression Recap
```

## M230 Beta Observation / Regression Recap

```text
recap_result: PASS
observations_reviewed: 3
regression_smoke_replay: PASS
blocking_issue_found: no
patch_round_required_now: no
documentation_patch_required_now: no
runtime_fix_required_now: no
governance_review_required_now: no
beta_run_status_lock_ready: yes
next_step: M231 Beta Run Status Lock
```

## License Note

```text
LICENSE file: present
selected_license: Apache License, Version 2.0
copyright_holder: Chehan Lin
year: 2026
```

## Remaining / Deferred

```text
M219.1 manual URL backfill: deferred until release_url and feedback_issue_url exist.
GitHub Release creation: optional manual publication task.
GitHub Issue creation: optional manual feedback-channel task.
```

## Next Step

```text
M231 Beta Run Status Lock
```

## Final Lock

```text
Open Beta Publication Checklist
BETA OBSERVATION / REGRESSION RECAP COMPLETE / status lock ready
```
