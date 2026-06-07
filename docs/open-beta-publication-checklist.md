# Open Beta Publication Checklist

Status: POST-TAG POLICY HOTFIX / HOST-DERIVED SLUG CORRECTED / TESTER NOTICE PENDING
Date: 2026-06-08

## Purpose

Prepare Hermes Runes MD Wiki for Open Beta publication as a public GitHub repository.

This record tracks publication readiness, release tag status, and remaining public tester notification work.

## Current Repository State

```text
repository: sawaichi9527/hermes-runes-md-wiki
visibility: public
open_beta_target: public GitHub repository
current_phase: Open Beta tag created with post-tag workspace slug policy correction
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
.env example starter path: updated, dogfood example still uses freelancer
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
post_tag_hotfix: workspace slug policy corrected after tag
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

## License Note

```text
LICENSE file: present
selected_license: Apache License, Version 2.0
copyright_holder: Chehan Lin
year: 2026
```

## Remaining Before Tester Notification

```text
M215 public tester notification draft
```

## Final Lock

```text
Open Beta Publication Checklist
POST-TAG POLICY HOTFIX / hostname-derived slug corrected / public tester notification pending
```
