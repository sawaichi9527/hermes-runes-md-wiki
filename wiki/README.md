# Hermes Runes Wiki Guide

Status: P0 Runes Keystone baseline

## Purpose

This document explains how knowledge should be organized under `wiki/`.

Agents should decipher this guide before proposing memory creation or restructuring.

## Layout Philosophy

Hermes Runes uses:

```text
flat-first
folder-when-needed
```

The goal is to keep local personal RAG:

- readable
- lightweight
- Git-friendly
- easy to inspect
- easy to maintain

## Top-level Wiki Layers

```text
wiki/_system/        = system governance policy
wiki/owner-runes/    = owner preferences and personal operating data
wiki/<workspace>/    = project / workspace memory
wiki/*.md            = general flat-first memory
```

### `wiki/_system/`

System governance rules only.

Normal user knowledge, personal preferences, RSS lists, project notes, and workspace memories must not be stored under `_system/`.

### `wiki/owner-runes/`

Owner-facing preferences and personal operating data.

Examples:

```text
wiki/owner-runes/preferences.md
wiki/owner-runes/operating-style.md
wiki/owner-runes/local-environment.md
wiki/owner-runes/rss-subscriptions.md
wiki/owner-runes/research-sources.md
```

This layer is agent-agnostic. It must not be named after a single agent implementation.

Owner-runes can influence presentation style, operating preferences, and reminder behavior, but must not override system governance, security policy, or human approval requirements.

### `wiki/<workspace>/`

Workspace namespace for a machine, project, product, environment, or long-running objective.

A workspace is not a sample folder. It is a lifecycle boundary for related memory.

Examples:

```text
wiki/freelancer/
wiki/chronos/
wiki/j18v154-automation/
wiki/k6-freelancer/
```

### `wiki/*.md`

General flat-first memory.

Use this for single-topic notes that do not need a workspace lifecycle.

## Flat-first Memory

General personal knowledge should start as:

```text
wiki/<category>-<topic>-<note_type>.md
```

Examples:

```text
wiki/specs-voip-softbank-sip-spec.md
wiki/engineering-rag-context-builder-design.md
wiki/products-platform-chronos-grace-c1-profile.md
```

Use flat-first memory when:

- the knowledge is a single topic
- no lifecycle tracking is needed
- no verification or operation history is expected
- the note can stand alone

## Workspace Namespace

Use a workspace namespace when:

- the topic represents a machine, project, product, environment, or long-running objective
- multiple related files are expected
- baseline, decision, operation, verification, or next-action tracking is useful
- recall should often be scoped to that workspace

Every workspace namespace should include:

```text
wiki/<workspace-slug>/README.md
```

A new local deployment workspace may start with:

```text
wiki/<workspace-slug>/README.md
wiki/<workspace-slug>/deployment.md
```

Optional files may be added later:

```text
wiki/<workspace-slug>/operations.md
wiki/<workspace-slug>/decisions.md
wiki/<workspace-slug>/verification.md
wiki/<workspace-slug>/baselines.md
wiki/<workspace-slug>/next-actions.md
```

## Workspace Bootstrap Guidance

During first local bootstrap, an agent may suggest creating a workspace derived from the OS hostname when available.

Example:

```text
Host display name: Freelancer
Workspace slug: freelancer
Path: wiki/freelancer/
```

The agent must normalize hostnames into safe slugs and ask for confirmation when a hostname may expose sensitive information.

Fresh install default:

```text
If wiki/<workspace-slug>/ does not exist:
  propose creating wiki/<workspace-slug>/ through Runes Shield
```

Legacy sample migration fallback:

```text
If wiki/<default_project_sample>/ exists:
  do not auto-rename
  inspect first
  require human confirmation before migration
```

Agents must not directly create, rename, or delete workspace folders as an operational shortcut.

Workspace creation, rename, promotion, archive, and migration should use governed Runes Shield / forge workflow.

## Baseline Categories

```text
specs
engineering
products
operations
references
personal
```

## Category Indexes

Planned indexes:

```text
wiki/specs-index.md
wiki/engineering-index.md
wiki/products-index.md
wiki/operations-index.md
wiki/references-index.md
wiki/personal-index.md
wiki/long-term-objectives-index.md
```

Indexes are intended to:

- help agents place knowledge
- help users browse memory layout
- support relationship consistency
- support future consistency probes

## Structural Changes

Structural changes include:

- create file
- create workspace namespace
- rename file
- archive file
- move file
- promote flat file to workspace namespace

Structural changes should use governed `forge` operations.

## Markdown-native Metadata

Hermes Runes currently uses Markdown-native metadata sections rather than YAML frontmatter.

The main solidified knowledge belongs in:

```markdown
## Canonical Memory
```

`Open Questions` should not be treated as confirmed truth.

## Change Log

- 2026-06-01: Initial wiki placement guide.
- 2026-06-05: Added owner-runes, workspace namespace semantics, and first-bootstrap workspace guidance.
