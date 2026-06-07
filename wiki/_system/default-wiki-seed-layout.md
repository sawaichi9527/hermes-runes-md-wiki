# Default Wiki Seed Layout Policy

Status: runtime-clean-seed policy
Scope: default wiki layout and workspace bootstrap guidance

## Purpose

This policy teaches agents how to interpret the default `wiki/` layout during first local deployment.

It also defines when agents should suggest workspace creation or migration through Runes Shield.

## Canonical Top-level Layers

```text
wiki/_system/        = system governance policy
wiki/<workspace>/    = active workspace memory
wiki/*.md            = general flat-first runtime memory indexes or notes
```

Developer history belongs outside runtime wiki memory:

```text
dev/wiki-history/
dev/docs/
```

## System Governance Layer

`wiki/_system/` is reserved for governance policy, contracts, invocation rules, security policy, and deployment policy.

Normal owner knowledge must not be stored here.

## Workspace Layer

`wiki/<workspace>/` is a lifecycle boundary.

Use a workspace when memory concerns a machine, project, product, environment, or long-running objective.

For the current dogfood host, the active workspace is:

```text
wiki/freelancer/
```

For other installations, use the local hostname-derived workspace slug:

```text
wiki/<lowercase-hostname>/
```

A workspace may contain:

```text
README.md
preferences.md
operating-style.md
local-environment.md
research-sources.md
rss-subscriptions.md
long-term-objectives.md
services.md
decisions.md
forge-inbox/
```

Fresh workspaces should start minimal and grow through governed review.

## Flat-first Layer

`wiki/*.md` stores standalone runtime indexes or reviewed notes.

Use flat-first when the memory is a single topic and does not need lifecycle tracking.

## First-bootstrap Workspace Rule

During first local bootstrap, an agent may suggest creating a workspace from the OS hostname.

Example:

```text
Host display name: Freelancer
Workspace slug: freelancer
Path: wiki/freelancer/
```

The agent must normalize the hostname into a safe slug.

If the hostname appears sensitive, the agent should ask the user for a safer alias.

## Default Behavior

Primary path:

```text
If wiki/<workspace-slug>/ does not exist:
  propose creating wiki/<workspace-slug>/ through Runes Shield
```

Agents must not directly create, rename, or delete folders without the governed workflow.

## Boundary

This policy does not grant direct mutation authority.

Workspace creation, rename, promotion, archive, and migration remain governed operations through Runes Shield / forge workflow.
