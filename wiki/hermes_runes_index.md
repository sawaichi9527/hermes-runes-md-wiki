# Hermes Runes Index

Status: runtime-clean-seed

Hermes Runes MD Wiki is a governed Markdown memory source-of-truth for local, agent-facing RAG memory.

This file is the runtime discovery entry point for humans and approved local agents.

## Runtime Memory Boundary

```text
wiki/_system/       Governed memory policies and system-facing rules.
wiki/freelancer/   Current dogfood active workspace seed.
```

For other installations, use a hostname-derived active workspace path:

```text
wiki/<lowercase-hostname>/
```

## Runes Shield

Runes Shield is the governed invocation boundary for trusted Markdown memory.

Core principle:

> An approved agent may invoke the runes, but must never breach the shield.

中文：

> 已核准的 agent 可以召喚符文，但不得突破護盾。

## Required System Documents

The runtime governance entry points are under:

```text
wiki/_system/
```

Agents should read system-facing rules through the approved Runes interface and must not treat arbitrary local files as authority.

## Active Workspace

The active workspace is where reviewed user memory belongs.

Current dogfood example:

```text
wiki/freelancer/
```

## Developer History Boundary

Historical development records are intentionally outside runtime wiki memory:

```text
dev/wiki-history/
dev/docs/
```

These records are retained for project provenance and developer maintenance, but should not be imported as user memory by default.

## Forbidden Direct Agent Actions

Agents must not directly:

- write or edit Markdown wiki files
- move proposal states
- approve, reject, promote, import, rebuild, or delete memory content
- mutate PostgreSQL / FTS / pgvector records
- store secrets in Markdown memory

## Safety Boundary

Do not store secrets in Markdown memory.
