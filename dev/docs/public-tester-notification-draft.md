# Public Tester Notification Draft

Status: DRAFT / READY FOR REVIEW / NOT YET SENT
Date: 2026-06-08
Milestone: M215

## Purpose

Provide a reusable public tester notification draft for Hermes Runes MD Wiki Open Beta.

This is a draft only. It is not proof that the notification has been sent.

## Draft Message

```markdown
# Hermes Runes MD Wiki Open Beta

Hermes Runes MD Wiki is now available for Open Beta evaluation.

Repository:
https://github.com/sawaichi9527/hermes-runes-md-wiki

Version:
`0.1.0-beta.1`

Tag:
`v0.1.0-beta.1`

Hermes Runes MD Wiki is a local-first, agent-agnostic Markdown wiki memory layer for governed local RAG workflows. It uses curated Markdown files as the human-readable source of truth, with retrieval/indexing support from local tooling.

## What Open Beta means

This Open Beta is intended for personal/local evaluation, documentation review, installation testing, starter-path validation, and early feedback.

It is not a stable release, not a production guarantee, not an enterprise support commitment, and not an autonomous trusted-memory writer.

## Starter guide

Start here:

`docs/open-beta-starter.md`

Recommended first checks:

```bash
git clone https://github.com/sawaichi9527/hermes-runes-md-wiki.git
cd hermes-runes-md-wiki
cat VERSION
git tag -n --list "v0.1.0-beta.1"
```

## Workspace slug rule

Your workspace slug is derived from your installation PC hostname in lowercase.

Examples:

```text
Host name: Freelancer -> workspace slug: freelancer -> wiki/freelancer/
Host name: Chronos    -> workspace slug: chronos    -> wiki/chronos/
Host name: LabBox     -> workspace slug: labbox     -> wiki/labbox/
```

`freelancer` is only the current dogfood host example, not a universal default.

## Safety boundary

Do not put real secrets into Markdown wiki memory or git.

This includes API keys, database passwords, Telegram bot tokens, local service credentials, cloud credentials, and private customer data.

Use `.env` or local secret storage for real local values. `.env.example` is only a placeholder template.

## Feedback requested

Useful feedback areas:

- clone / first-run experience
- documentation clarity
- hostname-derived workspace slug behavior
- starter guide correctness
- `.env.example` clarity
- governed memory workflow clarity
- confusing legacy references
- installation or local tool errors

## Current limitations

This Open Beta focuses on personal/local governed memory workflows. It is not an enterprise orchestration platform, not a production memory service, and not an automatic wiki writer.

Please open feedback as GitHub issues or send notes with exact commands, logs, host OS, Python version, and the workspace slug used.
```

## Publication Notes

```text
notification_status: draft prepared
notification_sent: no
release_tag: v0.1.0-beta.1
workspace_slug_rule: lowercase(hostname)
secrets_policy: do not store real secrets in Markdown wiki or git
```

## Final Lock

```text
Public Tester Notification Draft
DRAFT / ready for review / not yet sent
```
