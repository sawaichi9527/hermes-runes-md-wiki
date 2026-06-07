# Open Beta Publication Checklist

Status: AUDIT COMPLETE / REMEDIATION REQUIRED / FIRST TAG BLOCKED
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
.gitignore: present and excludes .env, keys, local logs, local databases, backups, and runtime artifacts
Open Beta status note: visible in README
Security policy: present
Secret scan quick check: no obvious keyword hits from repository code search
License: Apache-2.0 applied
Version file: present
Changelog: present
Versioning policy: present
Workspace slug policy: present
Default active workspace slug: freelancer
Public download audit: complete
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
tag_status: blocked
reason: public-facing legacy reference remediation is still required
```

## M209 Audit Result

```text
result: PASS for audit completion
release_tag_ready: no
public_tester_notification_ready: no
blocker: remaining public-facing and active-tool legacy references require remediation
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
M210 public download remediation / starter path cleanup
M211 first Open Beta tag / release lock
```

## Final Lock

```text
Open Beta Publication Checklist
AUDIT COMPLETE / remediation required / first tag blocked
```
