# Workspace Slug Policy

Status: ACTIVE / OPEN BETA SLUG BASELINE
Date: 2026-06-07

## Purpose

Define the default workspace slug and the role of legacy engineering evidence before public Open Beta tester notification.

## Canonical Open Beta Workspace

```text
workspace_slug: freelancer
wiki_namespace: wiki/freelancer/
main_checkout: ~/workspace/hermes-runes-md-wiki
clean_trial_checkout: ~/workspace/trial/hermes-runes-md-wiki
```

## Deprecated Paths

```text
old_trial_checkout: ~/workspace-trial/hermes-runes-md-wiki
legacy_engineering_namespace: wiki/k6-freelancer/
```

## Policy

```text
Use freelancer as the default active workspace slug.
Use wiki/freelancer/ for dogfood and public Open Beta user-facing memory.
Keep wiki/k6-freelancer/ as legacy engineering history unless a specific migration task requires moving curated content.
Do not bulk-edit historical verification evidence only to rename old paths.
```

## Active Default Rule

```text
Active runtime defaults and public examples should prefer freelancer.
Legacy k6-freelancer references in historical verification records are allowed but must not be presented as the default user path.
```

## Trial Checkout Rule

```text
Clean external-user simulation should use ~/workspace/trial/hermes-runes-md-wiki.
The old ~/workspace-trial/hermes-runes-md-wiki path is deprecated.
```

## Public Tester Boundary

```text
Public testers should see freelancer as the default workspace.
Public testers should not need to know the old k6-freelancer engineering namespace unless reading historical project logs.
```

## Final Lock

```text
Workspace Slug Policy
ACTIVE / freelancer is default / k6-freelancer is legacy engineering history
```
