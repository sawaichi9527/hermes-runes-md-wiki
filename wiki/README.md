# Hermes Runes Wiki

Status: runtime-clean-seed

This directory is the runtime Markdown memory seed for Hermes Runes MD Wiki.

## Runtime Layout

```text
wiki/
  _system/       System governance rules and governed memory policy.
  freelancer/   Active workspace seed for the current dogfood host.
```

For other installations, the active workspace slug should be derived from the local hostname, for example `wiki/<lowercase-hostname>/`.

## Active Workspace

The current dogfood workspace is:

```text
wiki/freelancer/
```

This workspace stores reviewed, durable, user-approved memory such as preferences, operating style, decisions, service notes, research sources, and long-term objectives.

## Developer History Boundary

Developer milestones, historical verification files, trial evidence, sample fixtures, beta observations, and release-planning records are not runtime memory seed.

They are retained outside `wiki/` under:

```text
dev/wiki-history/
dev/docs/
```

Runtime import should not ingest `dev/` by default.

## Safety Boundary

Do not store real secrets in Markdown memory. This includes passwords, API keys, bot tokens, database credentials, private keys, and raw sensitive logs.
