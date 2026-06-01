# Source Priority Policy

Status: P0 baseline

## Purpose

This document defines how Hermes Runes evidence should relate to other sources.

Hermes Runes provides governed memory evidence.

Hermes Agent performs final source comparison and judgment.

## Baseline Priority

Suggested baseline order:

1. Current user instruction
2. Current conversation context
3. Hermes Agent runtime/native memory
4. Hermes Runes MD Wiki
5. Third-party RAG / third-party notes / Obsidian
6. Web/external sources

## Native Memory Role

Hermes Agent native memory may contain:

- runtime state
- temporary working context
- preferences
- operation skill cache
- recent tasks

Native memory is not canonical long-term truth.

## Hermes Runes Role

Hermes Runes MD Wiki is the primary governed personal/project long-term memory substrate.

Hermes Runes should expose:

- source path
- source status
- memory quality
- retrieval evidence
- relationship metadata
- warning signals

Hermes Runes should not silently decide final truth.

## Third-party RAG / Notes

Third-party systems such as Obsidian may be used as:

- auxiliary evidence
- explicit-use search targets
- comparison sources
- import candidates

Third-party systems should not silently override Hermes Runes canonical memory.

Hermes Runes should not silently override external notes either.

Hermes Agent compares and explains differences when necessary.

## Web / External Sources

Web/external sources are important for:

- current facts
- version-sensitive information
- public references
- latest updates

Hermes Runes should not attempt to replace live web knowledge.

## Conflict Handling

If sources conflict:

- Hermes Runes should expose the conflict
- Hermes Agent should explain the conflict
- user approval may be required for memory resolution

Hermes Runes should not automatically merge conflicting memory.

## Change Log

- 2026-06-01: Initial source priority policy.
