# Open Beta Publication Checklist

Status: READY / MANUAL PUBLIC VISIBILITY CHANGE REQUIRED
Date: 2026-06-07

## Purpose

Prepare Hermes Runes MD Wiki for Open Beta publication as a public GitHub repository.

This record does not itself change GitHub repository visibility. The repository owner must switch visibility from private to public in GitHub settings.

## Current Repository State

```text
repository: sawaichi9527/hermes-runes-md-wiki
current_visibility_before_manual_change: private
open_beta_target: public GitHub repository
current_phase: Open Beta readiness
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
Open Beta status note: should be visible in README
Security policy: should be present
Secret scan quick check: no obvious keyword hits from repository code search
License: not selected yet
```

## License Note

```text
A public repository can be viewed and downloaded, but reuse rights are clearer only after a LICENSE file is selected.
The owner should choose a license before advertising broad reuse.
Suggested simple options to review: MIT or Apache-2.0.
No license is added by this checklist.
```

## Manual Visibility Change

```text
GitHub UI:
Repository -> Settings -> General -> Danger Zone -> Change repository visibility -> Make public
```

## Final Lock

```text
Open Beta Publication Checklist
READY / manual public visibility change required
```
