# OPC Workspace Overlay

Status: OPTIONAL / WORKSPACE-SCOPED PROFILE MEMORY OVERLAY
Scope: `wiki/freelancer/opc/`

## Purpose

This optional overlay stores workspace-scoped memory notes for Hermes Agent OPC profile usage.

It does not replace the default single-agent workspace files under `wiki/freelancer/`.

## Boundary

Hermes Runes MD Wiki remains Shield-governed.

In OPC usage:

```text
secretary owns user-facing consent
runes-holder owns Runes Shield access
requesting profile owns the reason for the memory request
```

Only `runes-holder` is expected to interact with Runes Shield.

## Conceptual Access Paths

```text
a. user <-> secretary <-> coordinator <-> runes-holder <-> Runes Shield <-> Runes Wiki
b. user <-> secretary <-> researcher  <-> runes-holder <-> Runes Shield <-> Runes Wiki
c. user <-> secretary <-> builder     <-> runes-holder <-> Runes Shield <-> Runes Wiki
d. user <-> secretary <-> writer      <-> runes-holder <-> Runes Shield <-> Runes Wiki
e. user <-> secretary <-> runes-holder <-> Runes Shield <-> Runes Wiki
```

## Files

- `profile-memory-map.md` — summary map for the six OPC profile memory scopes.
- `secretary.md` — user-facing consent, reply style, and preference memory.
- `coordinator.md` — task routing and profile handoff memory.
- `researcher.md` — source validation, freshness, and evidence comparison memory.
- `writer.md` — documentation and final-output style memory.
- `builder.md` — repo operation, verification, and deployment memory.
- `runes-holder.md` — Runes Shield usage and proposal boundary memory.

## Non-goal

This overlay does not add an OPC runtime, worker scheduler, enterprise memory manager, or a new Runes Shield schema.
