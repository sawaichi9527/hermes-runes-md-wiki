# Freelancer Workspace

This is the active local workspace for this installation.

## Purpose

This workspace stores user-approved, durable Markdown memory for the current host/user context.

## Boundaries

- Store curated project notes, preferences, operating style, decisions, services, and long-term objectives.
- Do not store real secrets, tokens, passwords, API keys, private keys, or raw sensitive logs.
- Draft or unreviewed memory should enter through `forge-inbox/` first.

## Files

- `preferences.md` — user preferences and habits.
- `operating-style.md` — preferred working style and collaboration conventions.
- `local-environment.md` — non-secret local environment notes.
- `research-sources.md` — preferred source and research notes.
- `rss-subscriptions.md` — RSS or subscription source notes.
- `long-term-objectives.md` — long-term goals and direction.
- `services.md` — reviewed local service notes.
- `decisions.md` — reviewed decisions.
- `forge-inbox/` — governed draft proposal inbox.
- `opc/` — optional OPC profile memory overlay for installations using Hermes Agent OPC profiles.

## Optional OPC overlay

The `opc/` directory is optional. It is used only when this workspace is operated with Hermes Agent OPC profile agents.

Single-agent users can ignore this directory.

See:

```text
docs/opc-workspace-overlay.md
wiki/freelancer/opc/README.md
```

## Default workspace seed boundary

This directory is the current local workspace instance.

For documentation and fresh-install defaults, treat it as:

```text
wiki/<workspace slug>/
```

`freelancer` is only the workspace slug used by this demonstration PC.

Default workspace memory should include curated workspace files such as preferences, operating style, local environment, services, decisions, research sources, and long-term objectives.

Milestone files such as `verification-m*.md` are development / release evidence and should not be part of the default runtime workspace Markdown seed. Keep them under `dev/wiki-history/<workspace slug>/verification/` instead.
