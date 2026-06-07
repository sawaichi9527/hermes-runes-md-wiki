# Security Policy

Status: runtime-clean-seed policy

## Purpose

This document defines baseline security expectations for Hermes Runes MD Wiki.

Hermes Runes is primarily intended for:

- local-first
- personal usage
- governed personal RAG
- self-hosted environments

It is not designed as an enterprise multi-tenant platform.

## Canonical Rule

Real secrets must never be committed into:

- Markdown source-of-truth
- Git repositories
- tracked configuration files
- observation logs
- sample fixtures

## Prohibited Content

Examples include:

- API keys
- Telegram bot tokens
- PostgreSQL passwords
- VPN credentials
- SSH private keys
- production secrets
- customer secrets
- private auth tokens

## Allowed Secret Location

Secrets belong in:

```text
tools/importer/.env
runtime environment variables
local secret stores
```

not in canonical memory.

## Observation Policy Interaction

Observation logs should avoid storing:

- full prompts
- full answers
- raw memory context
- secrets
- personally sensitive raw dumps

Observation exists for tuning and diagnostics, not full replay.

## Personal and Confidential Data

Not all sensitive information is a secret.

Future policy may distinguish:

```text
public
personal
confidential
secret-prohibited
```

P0 currently focuses on preventing obvious secret leakage.

## External Sources

Third-party notes and web sources may contain unsafe content.

Agents should not automatically solidify external content into canonical memory without approval.

## Repository Portability

Developer-only fixtures, milestone records, beta evidence, and historical retrieval samples should remain outside runtime wiki memory.

They belong under:

```text
dev/wiki-history/
dev/docs/
```

Runtime import should not ingest `dev/` by default.

## Change Log

- 2026-06-01: Initial security policy.
- 2026-06-08: Cleaned runtime seed boundary and moved developer fixtures/history outside `wiki/`.
