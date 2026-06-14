# OPC Workspace Overlay Policy

Status: ACTIVE / OPTIONAL SYSTEM POLICY
Date: 2026-06-14

This policy records the optional OPC workspace overlay for Hermes Agent profile usage.

Single-agent use remains the default.

```text
agent -> Runes Shield -> Hermes Runes MD Wiki
```

When Hermes Agent OPC profiles are used, profile memory may be organized under:

```text
wiki/<workspace-slug>/opc/
```

Only `runes-holder` is expected to interact with Runes Shield.

`secretary` owns user-facing confirmation.

## Conceptual Paths

```text
a. user <-> secretary <-> coordinator <-> runes-holder <-> Runes Shield <-> Runes Wiki
b. user <-> secretary <-> researcher  <-> runes-holder <-> Runes Shield <-> Runes Wiki
c. user <-> secretary <-> builder     <-> runes-holder <-> Runes Shield <-> Runes Wiki
d. user <-> secretary <-> writer      <-> runes-holder <-> Runes Shield <-> Runes Wiki
e. user <-> secretary <-> runes-holder <-> Runes Shield <-> Runes Wiki
```

## Optional Layout

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

This is an organizational overlay only.

See:

```text
docs/opc-workspace-overlay.md
```
