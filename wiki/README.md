# Hermes Runes Wiki Guide

Status: P0 baseline

## Purpose

This document explains how knowledge should be organized under `wiki/`.

Hermes Agent should decipher this guide before creating or restructuring memory.

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

## Two Main Knowledge Shapes

### Flat-first files

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

### Objective namespaces

Long-running projects/domains may use:

```text
wiki/<objective-slug>/
```

Example:

```text
wiki/k6-freelancer/
```

Objective namespaces are intended for:

- engineering projects
- product investigations
- platform baselines
- long-running operational domains

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

- help Hermes Agent place knowledge
- help users browse memory layout
- support relationship consistency
- support future consistency probes

## Objective Placement Guidance

Hermes Agent should consider objective namespaces when:

- a topic becomes long-running
- multiple related files are expected
- lifecycle tracking matters
- baseline / verification / operations history matters

Otherwise:

- prefer flat-first layout

## Structural Changes

Structural changes include:

- create file
- create objective namespace
- rename file
- archive file
- move file
- promote flat file to objective namespace

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
