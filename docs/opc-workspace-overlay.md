# Optional OPC Workspace Overlay

Status: ACTIVE / OPTIONAL OPC OVERLAY POLICY
Date: 2026-06-14
Scope: optional `wiki/<workspace-slug>/opc/` memory organization for Hermes Agent OPC profile usage

## Purpose

This document defines an optional workspace overlay for installations that use Hermes Agent OPC profile agents.

The overlay adds profile-oriented Markdown memory organization without changing Hermes Runes MD Wiki access rules, Runes Shield schemas, runtime behavior, or the default single-agent workspace layout.

## Baseline Rule

Hermes Runes MD Wiki keeps the existing governed access model:

```text
agent -> Runes Shield -> Hermes Runes MD Wiki
```

For normal single-agent use, the default workspace remains:

```text
wiki/<workspace-slug>/
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

The optional OPC overlay does not replace this layout.

## OPC Access Principle

In OPC usage, Hermes Runes MD Wiki still only sees governed access through Runes Shield.

The only profile expected to interact with Runes Shield is:

```text
runes-holder
```

The `secretary` profile owns user-facing consent. Other OPC profiles may need Runes context, but Runes access still goes through `runes-holder` and Runes Shield.

## OPC Runes Access Paths

OPC Runes access is not a fixed coordinator-only path. It is consent-gated through `secretary` and Shield-gated through `runes-holder`.

Supported conceptual paths:

```text
a. user <-> secretary <-> coordinator <-> runes-holder <-> Runes Shield <-> Runes Wiki
b. user <-> secretary <-> researcher  <-> runes-holder <-> Runes Shield <-> Runes Wiki
c. user <-> secretary <-> builder     <-> runes-holder <-> Runes Shield <-> Runes Wiki
d. user <-> secretary <-> writer      <-> runes-holder <-> Runes Shield <-> Runes Wiki
e. user <-> secretary <-> runes-holder <-> Runes Shield <-> Runes Wiki
```

Communication between OPC profiles after `runes-holder` receives Runes results is outside the Hermes Runes MD Wiki contract.

## Optional Overlay Layout

OPC users may add this optional workspace overlay through governed proposal/review:

```text
wiki/<workspace-slug>/opc/
  README.md
  profile-memory-map.md
  secretary.md
  coordinator.md
  researcher.md
  writer.md
  builder.md
  runes-holder.md
```

This overlay is optional. Forkers and users who run a single agent do not need it.

## Profile Memory Scope

- `secretary.md` stores user-facing preferences, consent habits, response style, and reply conventions.
- `coordinator.md` stores task routing preferences, handoff discipline, and one-profile-at-a-time constraints.
- `researcher.md` stores source validation habits, freshness policy, citation policy, uncertainty marking, and comparison rules.
- `writer.md` stores documentation style, Traditional Chinese phrasing preferences, and source-status wording.
- `builder.md` stores repo operation habits, verification commands, smoke-test conventions, deployment checklists, local limitations, and known repair paths.
- `runes-holder.md` stores Runes Shield usage habits, policy read order, proposal status interpretation, trusted/draft/rejected boundaries, and workspace placement guidance.

## Creation Rule

The optional `opc/` overlay is a workspace memory structure. Creating or modifying it remains a governed operation through Runes Shield / forge workflow.

## Non-goals

This policy does not introduce a new Runes Shield schema, new OPC runtime, parallel profile dispatch, enterprise memory management, direct Hermes native-memory changes, direct Hermes Kanban changes, gateway control, or autonomous trusted memory writing.

## M205-M207 Lock

```text
M205 Optional OPC Workspace Overlay Seed
M206 OPC Overlay Layout Smoke
M207 README / _system Link Alignment

Resulting policy:
- Single-agent workspace defaults remain unchanged.
- OPC profile memory organization is optional.
- Only runes-holder should touch Runes Shield in OPC usage.
- Secretary owns user-facing consent.
- Hermes Runes MD Wiki remains agent-agnostic and Shield-governed.
```
