# Wiki Operation Policy

Status: P0 Runes Keystone baseline

## Purpose

This document defines governed operations for the `wiki/` Markdown source-of-truth layer.

The goal is:

- keep local personal RAG simple
- keep wiki structure understandable
- prevent accidental corruption
- preserve deterministic retrieval behavior
- preserve relationship consistency

## Structural Change vs Content Update

### Structural change

Structural changes affect wiki relationships.

Examples:

- create file
- create workspace namespace
- create workspace file
- create objective namespace
- create objective file
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
- objective README update
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
| create-objective | P0 |
| create-objective-file | P0 |
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

Use flat-first memory for standalone notes.

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

A fresh deployment workspace may start with:

```text
wiki/<workspace-slug>/README.md
wiki/<workspace-slug>/deployment.md
```

Do not create `sample.md` as the default workspace content.

## Objective Namespace

Long-running engineering/project/domain knowledge may also use:

```text
wiki/<objective-slug>/
```

For P0 Runes Keystone usage, workspace namespace and objective namespace share the same governed structural rules.

Every objective namespace must include:

```text
wiki/<objective-slug>/README.md
```

Objective README files act as local relationship indexes.

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
- do not auto-rename template or sample folders
- treat sample-folder migration as human-confirmed migration only

Primary bootstrap path:

```text
If wiki/<workspace-slug>/ does not exist:
  propose create-workspace through Runes Shield
```

Migration fallback:

```text
If wiki/<default_project_sample>/ exists:
  inspect first
  require human confirmation
  then use governed rename / migration workflow if approved
```

## Index Consistency

Structural changes should update affected:

- category indexes
- long-term-objectives index
- workspace README references
- objective README references
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

## Owner Runes Boundary

`wiki/owner-runes/` is reserved for owner preferences and personal operating data.

It is not system policy and does not override governance, security, or human approval requirements.

## Change History

Structural changes should append entries to:

```text
wiki/_system/change-history.md
```

Normal retrieval and ordinary answers must not append change-history.

## Approval Boundary

User approval is required before:

- creating workspace namespace
- creating objective namespace
- creating new flat-first memory
- archiving/deleting memory
- importing external memory as canonical memory
- resolving memory conflicts
- renaming or migrating a sample/template workspace

## Probe Expectations

Consistency probes should eventually support:

- missing index references
- missing workspace references
- missing objective references
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
- 2026-06-05: Added owner-runes, workspace namespace, and first-bootstrap workspace handling.
