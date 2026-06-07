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
```

`freelancer` is the current dogfood host slug. It is not a universal default for every tester.

## Public Tester Rule

```text
Public testers should use their own lowercase hostname as the workspace slug.
For example, a host named Chronos should use chronos.
A host named LabBox should use labbox.
```

## Runtime Wiki Boundary

Runtime memory belongs under:

```text
wiki/_system/
wiki/<workspace-slug>/
```

Developer history belongs under:

```text
dev/wiki-history/
dev/docs/
```

Public testers should not need to inspect or import `dev/` for normal runtime use.

## Policy

```text
Use lowercase(hostname) as the active workspace slug.
Use wiki/<lowercase-hostname>/ for that installation's active memory namespace.
Do not treat developer history under dev/ as runtime user memory.
Do not bulk-edit historical verification evidence only to rename old paths.
```

## Public Tester Boundary

```text
Public testers should not be told that freelancer is the universal default workspace.
Public testers should derive their workspace slug from their own installation PC hostname.
Public testers should work from wiki/ and docs/ only for normal installation and runtime use.
```

## Final Lock

```text
Workspace Slug Policy
ACTIVE / workspace slug is lowercase hostname / runtime memory stays under wiki/ / developer history stays under dev/
```
