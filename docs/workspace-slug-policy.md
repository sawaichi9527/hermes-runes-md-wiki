# Workspace Slug Policy

Status: ACTIVE / HOST-DERIVED WORKSPACE SLUG BASELINE
Date: 2026-06-08

## Purpose

Define how a workspace slug is selected for Hermes Runes MD Wiki installations.

## Canonical Rule

```text
workspace_slug: lowercase(hostname)
wiki_namespace: wiki/<lowercase-hostname>/
```

The workspace slug is derived from the installation PC hostname and normalized to lowercase.

Example:

```text
hostname: Freelancer
workspace_slug: freelancer
wiki_namespace: wiki/freelancer/
```

## Current Dogfood Instance

```text
current_development_host: Freelancer
current_dogfood_workspace_slug: freelancer
current_dogfood_wiki_namespace: wiki/freelancer/
main_checkout: ~/workspace/hermes-runes-md-wiki
clean_trial_checkout: ~/workspace/trial/hermes-runes-md-wiki
```

`freelancer` is the current dogfood host slug. It is not a universal default for every tester.

## Public Tester Rule

```text
Public testers should use their own lowercase hostname as the workspace slug.
For example, a host named Chronos should use chronos.
A host named LabBox should use labbox.
```

## Deprecated Paths

```text
old_trial_checkout: ~/workspace-trial/hermes-runes-md-wiki
legacy_engineering_namespace: wiki/k6-freelancer/
```

## Policy

```text
Use lowercase(hostname) as the active workspace slug.
Use wiki/<lowercase-hostname>/ for that installation's active memory namespace.
Keep wiki/k6-freelancer/ as legacy engineering history unless a specific migration task requires moving curated content.
Do not bulk-edit historical verification evidence only to rename old paths.
```

## Active Default Rule

```text
Active runtime defaults and public examples should describe the hostname-derived slug rule.
The repository's dogfood example may show freelancer only as an example for the Freelancer host.
Legacy k6-freelancer references in historical verification records are allowed but must not be presented as the default user path.
```

## Trial Checkout Rule

```text
Clean external-user simulation should use ~/workspace/trial/hermes-runes-md-wiki.
The old ~/workspace-trial/hermes-runes-md-wiki path is deprecated.
```

## Public Tester Boundary

```text
Public testers should not be told that freelancer is the universal default workspace.
Public testers should derive their workspace slug from their own installation PC hostname.
Public testers should not need to know the old k6-freelancer engineering namespace unless reading historical project logs.
```

## Final Lock

```text
Workspace Slug Policy
ACTIVE / workspace slug is lowercase hostname / freelancer is current dogfood host instance only
```
