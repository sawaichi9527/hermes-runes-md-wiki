# Public Tester Notification Final

Status: REVIEWED / SEND-READY / NOT SENT
Date: 2026-06-08
Milestone: M216

## Purpose

Provide the reviewed send-ready public tester notification text for Hermes Runes MD Wiki Open Beta.

This file is the final reviewed notification text. It does not mean the notification has been sent.

## Send Decision

```text
send_decision: ready_for_manual_send
notification_sent: no
manual_send_required: yes
```

## Final Message

```markdown
# Hermes Runes MD Wiki Open Beta

Hermes Runes MD Wiki v0.7.0 is the current Open Beta target for fresh-install evaluation.

Repository:
https://github.com/sawaichi9527/hermes-runes-md-wiki

Version:
`0.1.0-beta.1`

Tag:
`v0.7.0`

Hermes Runes MD Wiki is a local-first, agent-agnostic Markdown wiki memory layer for governed local RAG workflows. It treats curated Markdown files as the human-readable source of truth and uses local indexing/retrieval tooling to support recall and context assembly.

## Open Beta boundary

This Open Beta is intended for personal/local evaluation, documentation review, installation testing, starter-path validation, and early feedback.

It is not a stable release, not a production guarantee, not an enterprise support commitment, and not an autonomous trusted-memory writer.

## Start here

Starter guide:

`docs/open-beta-starter.md`

Recommended first checks:

```bash
git clone https://github.com/sawaichi9527/hermes-runes-md-wiki.git
cd hermes-runes-md-wiki
cat VERSION
git tag -n --list "v0.7.0"
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

This includes API keys, database passwords, Telegram bot tokens, local service credentials, cloud credentials, private customer data, and any other local credentials.

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

Please include exact commands, logs, host OS, Python version, and the workspace slug used when reporting issues.

## Current limitations

This Open Beta focuses on personal/local governed memory workflows. It is not an enterprise orchestration platform, not a production memory service, and not an automatic wiki writer.
```

## Review Checklist

```text
Open Beta boundary: included
version and tag: included
starter guide: included
hostname-derived workspace slug rule: included
freelancer not universal default: included
secrets safety boundary: included
feedback scope: included
notification_sent: no
```

## Final Lock

```text
Public Tester Notification Final
REVIEWED / send-ready / not sent
```
