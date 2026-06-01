# Hermes Agent Operation Guide

Status: P0 baseline

## Purpose

This document defines how Hermes Agent should interact with Hermes Runes MD Wiki.

Hermes Runes is a governed personal RAG substrate.

Hermes Agent is the decision-making layer.

## Core Boundary

Hermes Runes:

- provides governed memory evidence
- provides source metadata
- provides source status
- provides operational safety
- provides deterministic wiki operations

Hermes Agent:

- compares sources
- decides final answer behavior
- decides whether to ask follow-up questions
- decides whether to solidify memory
- decides whether web or external evidence is more appropriate

Hermes Runes does not decide truth for Hermes Agent.

## Source Relationship

Hermes Agent should treat:

1. current user instruction
2. current conversation
3. Hermes Agent runtime/native memory
4. Hermes Runes MD Wiki
5. third-party RAG / notes / Obsidian
6. web/external sources

as separate evidence layers.

Hermes Runes should normally be the primary governed personal memory source.

Third-party RAG / notes / Obsidian are auxiliary, explicit-use, comparison, or import-candidate sources.

Hermes Agent performs the comparison.

## Native Memory Skill Cache

Hermes Agent may learn Hermes Runes usage patterns as native-memory operational skill.

Examples:

- how to use `forge`
- how to use `evoke`
- how to place knowledge into objective namespaces
- how to update indexes

Native-memory skill cache is allowed.

However:

- native memory is not authoritative policy
- cached behavior may become stale
- structural wiki changes may invalidate assumptions

Before structural Runes operations, Hermes Agent should check freshness or decipher relevant policy again.

## Structural Operations

Structural operations include:

- create file
- create objective namespace
- create objective file
- rename file
- archive file
- delete file
- promote file
- move file
- split file
- merge file

Structural operations should go through governed `forge` workflows.

Hermes Agent should not freely mutate `wiki/` structure outside the governed interface.

## Recommended Operation Flow

### Ordinary memory retrieval

```text
check freshness if needed
↓
decipher minimal required guidance
↓
evoke memory
↓
compare with other sources if necessary
↓
answer user
```

### Memory solidification

```text
receive user request or candidate knowledge
↓
decipher placement/index/policy guidance
↓
decide objective vs flat-first placement
↓
ask user for approval when required
↓
forge Markdown source-of-truth
↓
inscribe import/index updates
↓
probe consistency
↓
report result
```

## Approval Boundary

Hermes Agent should ask the user before:

- creating objective namespace
- creating new flat-first file
- creating new objective file
- changing draft to active
- archiving/deleting memory
- promoting/moving/splitting/merging memory
- importing external notes into canonical memory
- resolving conflicting memory

## Freshness Awareness

Hermes Agent should pay attention to:

- `_system` policy updates
- `change-history.md`
- objective README changes
- category index changes

Policy freshness should override cached assumptions.

## Non-goals

Hermes Agent should not:

- treat Hermes Runes as the only source
- automatically trust archived/superseded memory
- automatically solidify web content into canonical memory
- silently rewrite canonical memory without approval
- bypass governed forge workflows

## Change Log

- 2026-06-01: Initial Hermes Agent operation guide.
