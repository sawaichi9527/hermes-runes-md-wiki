# CB-20260608-M214.1 Env Example Host Slug Hotfix

Status: PASS / ENV EXAMPLE SLUG COMMENT CORRECTED
Date: 2026-06-08
Milestone: M214.1
Stage: Open Beta Publication Hotfix

## Purpose

Clarify that `freelancer` in `tools/importer/.env.example` is the current dogfood host example, not a universal default workspace slug.

## Correct Rule

```text
workspace_slug: lowercase(hostname)
project: lowercase(hostname)
```

## Current Dogfood Example

```text
current_dogfood_host: Freelancer
example_slug: freelancer
example_project: freelancer
```

## Patched File

```text
tools/importer/.env.example
```

## Tag Boundary

```text
existing_tag: v0.1.0-beta.1
release_tag_change: none
policy_hotfix: post-tag documentation/comment correction
```

## Next Step

```text
M215 Public Tester Notification Draft
```

## Final Lock

```text
M214.1 Env Example Host Slug Hotfix
PASS / .env.example comment corrected / freelancer remains dogfood example only
```
