# CB-20260608-M214 Host-Derived Slug Policy Correction

Status: PASS / HOST-DERIVED SLUG POLICY CORRECTED / POST-TAG HOTFIX
Date: 2026-06-08
Milestone: M214
Stage: Open Beta Publication Hotfix

## Purpose

Correct the Open Beta workspace slug policy after identifying that `freelancer` was incorrectly described as a universal default.

## Correction

```text
wrong_statement: freelancer is the default workspace slug
correct_rule: workspace slug is lowercase(hostname)
current_dogfood_host: Freelancer
current_dogfood_slug: freelancer
current_dogfood_namespace: wiki/freelancer/
```

## Updated Files

```text
README.md
docs/open-beta-starter.md
docs/workspace-slug-policy.md
docs/open-beta-publication-checklist.md
```

## Tag Boundary

```text
existing_tag: v0.1.0-beta.1
release_tag_change: none
reason: this is a post-tag documentation/policy hotfix
future_option: create v0.1.0-beta.2 if public tester package should include corrected policy tag
```

## Remaining Work

```text
tools/importer/.env.example still uses freelancer as the dogfood example.
It should be clarified locally if the public package requires a beta.2 cleanup.
```

## Next Step

```text
M215 Public Tester Notification Draft
```

## Final Lock

```text
M214 Host-Derived Slug Policy Correction
PASS / lowercase hostname rule restored / freelancer is current host instance only
```
