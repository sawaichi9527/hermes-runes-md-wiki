# Wiki Operation Policy

Status: runtime-clean-seed policy

## Purpose

This document defines governed operations for the `wiki/` Markdown source-of-truth layer.

The goal is:

- keep local personal RAG simple
- keep wiki structure understandable
- prevent accidental corruption
- preserve deterministic retrieval behavior
- preserve relationship consistency

## Runtime Boundary

Runtime memory belongs under:

```text
wiki/_system/
wiki/<workspace-slug>/
wiki/*.md
```

Developer history belongs under:

```text
dev/wiki-history/
dev/docs/
```

Do not import `dev/` as runtime user memory by default.

## Structural Change vs Content Update

### Structural change

Structural changes affect wiki relationships.

Examples:

- create file
- create workspace namespace
- create workspace file
- rename file
- move file
- archive file
- delete file
- promote flat file to workspace
- split file
- merge files
- index repair

Structural changes may require:

- index update
- workspace README update
- change-history update
- import/index refresh
- consistency probes

### Content update

Content updates modify existing memory content without changing structure.

Examples:

- update Canonical Memory
- update Summary
- update Evidence section
- update Open Questions
- update Last reviewed

Content updates normally do not require structural index updates.

## Forge Vocabulary

| Operation | Status |
|---|---|
| create-flat | P0 |
| create-workspace | P0 |
| create-workspace-file | P0 |
| update-content | P0 |
| rename | P0 |
| archive | P0 |
| move | Reserved / P1 |
| promote | Reserved / P1 |
| restore | Reserved / P1 |
| purge | Reserved / P1 |
| resolve-conflict | Reserved / P1 |
| split | Reserved / P2 |
| merge | Reserved / P2 |

## Flat-first Naming

Baseline format:

```text
wiki/<category>-<topic>-<note_type>.md
```

Baseline categories:

```text
specs
engineering
products
operations
references
personal
```

Use flat-first memory for standalone reviewed notes.

## Workspace Namespace

Long-running machine/project/product/environment knowledge may use:

```text
wiki/<workspace-slug>/
```

Every workspace namespace must include:

```text
wiki/<workspace-slug>/README.md
```

Workspace README files act as local relationship indexes.

For the current dogfood host, the active workspace is:

```text
wiki/freelancer/
```

For other installations, use the local hostname-derived workspace slug.

## First-bootstrap Workspace Handling

During first local deployment, agents may suggest a workspace slug derived from the OS hostname.

Example:

```text
Host display name: Freelancer
Workspace slug: freelancer
Path: wiki/freelancer/
```

Rules:

- normalize hostnames into safe lower-case slugs
- ask the user for an alias if the hostname appears sensitive
- create a missing workspace through governed Runes Shield / forge workflow
- do not directly create folders as an operational shortcut

Primary bootstrap path:

```text
If wiki/<workspace-slug>/ does not exist:
  propose create-workspace through Runes Shield
```

## Index Consistency

Structural changes should update affected:

- category indexes
- long-term-objectives index
- workspace README references
- change-history

Broken relationships should be detectable by `probe`.

## Path Safety

Governed operations must reject:

- `../`
- absolute paths
- symlink escape
- writes outside repository wiki scope

Reserved namespaces:

```text
wiki/_system/
```

must not be treated as normal user knowledge.

## Active Workspace User Data

Personal preferences, operating style, local non-secret environment notes, research sources, RSS subscriptions, service notes, and decisions belong in the active workspace.

Example:

```text
wiki/freelancer/preferences.md
wiki/freelancer/operating-style.md
```

## Change History

Structural changes should append entries to:

```text
wiki/_system/change-history.md
```

Normal retrieval and ordinary answers must not append change-history.

## Approval Boundary

User approval is required before:

- creating workspace namespace
- creating new flat-first memory
- archiving/deleting memory
- importing external memory as canonical memory
- resolving memory conflicts

## Probe Expectations

Consistency probes should eventually support:

- missing index references
- missing workspace references
- broken links
- invalid metadata references
- invalid path layout
- missing required policy files

## Non-goals

This policy is intentionally simpler than enterprise CMS systems.

Hermes Runes should remain:

- local-first
- personal-RAG-oriented
- inspectable
- Git-friendly
- easy to maintain

## Change Log

- 2026-06-01: Initial wiki operation policy.
- 2026-06-08: Cleaned runtime seed policy and moved developer history outside `wiki/`.
