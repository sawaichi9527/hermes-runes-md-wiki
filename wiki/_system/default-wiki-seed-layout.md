# Default Wiki Seed Layout Policy

Status: P0 Runes Keystone policy extension
Scope: default wiki layout, owner-runes, workspace bootstrap guidance

## Purpose

This policy teaches agents how to interpret the default `wiki/` layout during trial run and first local deployment.

It also defines when agents should suggest workspace creation or migration through Runes Shield.

## Canonical Top-level Layers

```text
wiki/_system/        = system governance policy
wiki/owner-runes/    = owner preferences and personal operating data
wiki/<workspace>/    = project / workspace memory
wiki/*.md            = general flat-first memory
```

## System Governance Layer

`wiki/_system/` is reserved for governance policy, contracts, invocation rules, security policy, and deployment policy.

Normal owner knowledge must not be stored here.

## Owner Runes Layer

`wiki/owner-runes/` stores durable owner preferences and personal operating data.

Examples:

```text
preferences.md
operating-style.md
local-environment.md
rss-subscriptions.md
research-sources.md
```

This layer is agent-agnostic. Do not name the layer after Hermes-agent or any single future agent implementation.

Allowed content:

- language and tone preferences
- tooling preferences
- local operating habits
- non-secret source lists
- RSS subscription preferences
- research source watchlists

Forbidden content:

- passwords
- API keys
- tokens
- private keys
- secrets
- sensitive internal identifiers unless explicitly sanitized

## Workspace Layer

`wiki/<workspace>/` is a lifecycle boundary.

Use a workspace when memory concerns a machine, project, product, environment, or long-running objective.

A workspace may contain:

```text
README.md
deployment.md
operations.md
decisions.md
verification.md
baselines.md
next-actions.md
```

Fresh workspaces should start minimal:

```text
README.md
deployment.md
```

Do not create `sample.md` for the default workspace.

## Flat-first Layer

`wiki/*.md` stores standalone notes.

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

Migration fallback:

```text
If wiki/<default_project_sample>/ exists:
  do not auto-rename
  inspect first
  require human confirmation before migration
```

## Agent Reminder Behavior

When an agent observes that no workspace exists for the current host or deployment context, it may remind the user:

```text
I do not see a workspace for this host yet. Should I prepare a governed workspace proposal for wiki/<workspace-slug>/ ?
```

The agent must not directly create or rename folders without the governed workflow.

## Boundary

This policy does not grant direct mutation authority.

Workspace creation, rename, promotion, archive, and migration remain governed operations through Runes Shield / forge workflow.
