# M214 Host-Derived Workspace Slug Policy Correction

Status: PASS / HOST-DERIVED SLUG POLICY CORRECTED / POST-TAG HOTFIX
Date: 2026-06-08

## Evidence Record

```text
wiki/k6-freelancer/cb-sessions/cb-20260608-m214-host-derived-slug-policy-correction.md
README.md
docs/open-beta-starter.md
docs/workspace-slug-policy.md
docs/open-beta-publication-checklist.md
```

## Scope

```text
workspace slug policy correction
public starter documentation correction
post-tag documentation hotfix
no runtime feature development
no tag rewrite
```

## Result

```text
PASS
```

## Corrected Rule

```text
workspace_slug: lowercase(hostname)
wiki_namespace: wiki/<lowercase-hostname>/
```

## Current Instance

```text
current_dogfood_host: Freelancer
current_dogfood_workspace_slug: freelancer
current_dogfood_wiki_namespace: wiki/freelancer/
```

## Correction Summary

```text
freelancer is not the universal default workspace slug.
freelancer is the lowercase hostname-derived slug for the current dogfood host.
Public testers should derive their workspace slug from their own installation PC hostname.
```

## Tag Boundary

```text
existing_tag: v0.1.0-beta.1
release_tag_change: none
policy_hotfix: post-tag documentation correction
```

## Next Step

```text
M215 Public Tester Notification Draft
```

## Final Lock

```text
M214 Host-Derived Workspace Slug Policy Correction
PASS / lowercase hostname rule restored / freelancer is current host instance only
```
