# Open Beta Publication Checklist

Status: RUNTIME TOOL PATCHED / TAG PREP READY / RELEASE LOCK PENDING
Date: 2026-06-07

## Purpose

Prepare Hermes Runes MD Wiki for Open Beta publication as a public GitHub repository.

This record tracks publication readiness but does not replace release tags or download-audit verification.

## Current Repository State

```text
repository: sawaichi9527/hermes-runes-md-wiki
visibility: public
open_beta_target: public GitHub repository
current_phase: Open Beta public readiness
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
- public release / stable release
- autonomous trusted memory writing
- automatic proposal apply
- storage of user secrets in the wiki
```

## Public Safety Checklist

```text
README: present
Open Beta starter guide: present
.env example starter path: updated
trial templates starter path: updated
.gitignore: present and excludes local runtime artifacts
Open Beta status note: visible in README
Security policy: present
License: Apache-2.0 applied
Version file: present
Changelog: present
Versioning policy: present
Workspace slug policy: present
Default active workspace slug: freelancer
Public download audit: complete
Runtime/tool sweep: PASS / active blockers cleared
```

## Workspace Slug Note

```text
canonical_active_slug: freelancer
canonical_wiki_namespace: wiki/freelancer/
legacy_engineering_namespace: wiki/k6-freelancer/
clean_trial_checkout: ~/workspace/trial/hermes-runes-md-wiki
deprecated_trial_checkout: ~/workspace-trial/hermes-runes-md-wiki
```

## Version Note

```text
current_version: 0.1.0-beta.1
planned_tag: v0.1.0-beta.1
tag_status: ready for M213
reason: active runtime/tool blockers cleared; release lock still required
```

## M209 Audit Result

```text
result: PASS for audit completion
release_tag_ready: no
public_tester_notification_ready: no
blocker: remaining public-facing and active-tool legacy references require remediation
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
runtime_tool_sweep: PASS
release_tag_ready: yes, pending M213 release lock
public_tester_notification_ready: not yet
remaining_blocker: release lock and tag creation
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
M213 first Open Beta tag / release lock
M214 public tester notification draft
```

## Final Lock

```text
Open Beta Publication Checklist
RUNTIME TOOL PATCHED / tag prep ready / release lock pending
```
