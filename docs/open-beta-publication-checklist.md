# Open Beta Publication Checklist

Status: MANUAL SEND URL BACKFILL BLOCKED / RELEASE AND FEEDBACK URLS PENDING / NOT SENT
Date: 2026-06-08

## Purpose

Prepare Hermes Runes MD Wiki for Open Beta publication as a public GitHub repository.

This record tracks publication readiness, release tag status, public tester notification draft/final review status, channel selection status, and remaining manual URL backfill work.

## Current Repository State

```text
repository: sawaichi9527/hermes-runes-md-wiki
visibility: public
open_beta_target: public GitHub repository
current_phase: waiting for manual GitHub Release and feedback issue URLs
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
Manual send URL backfill: blocked / URLs pending
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
public_tester_notification_ready: not yet
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
selected_channel: pending
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
url_backfill_template: BLOCKED
release_url: missing
feedback_issue_url: missing
notification_sent: no
next_step: M219.1 manual send result backfill after URLs are available
```

## License Note

```text
LICENSE file: present
selected_license: Apache License, Version 2.0
copyright_holder: Chehan Lin
year: 2026
```

## Remaining Before Public Notification Send Record Completion

```text
Create GitHub Release using docs/github-release-note-v0.1.0-beta.1.md.
Create GitHub Issue using docs/open-beta-feedback-issue-draft.md.
Backfill release_url and feedback_issue_url in M219.1.
```

## Final Lock

```text
Open Beta Publication Checklist
MANUAL SEND URL BACKFILL BLOCKED / release and feedback URLs pending / notification not recorded as sent
```
