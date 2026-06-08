# M208 v0.7.1-dev Agent Onboarding Prompt

Status: PASS candidate / local validation ready
Version line: 0.7.1-dev
Date: 2026-06-08

## Scope

M208 starts the post-v0.7.0 development line and adds a simple Hermes-agent onboarding prompt to the fresh install guide.

This milestone does not move or recreate the `v0.7.0` tag.

## Starting state

Confirmed before M208:

- `v0.7.0` tag exists.
- GitHub Release `v0.7.0` is published.
- post-release docs alignment completed.
- backend check PASS.
- FTS recall PASS.
- core smoke PASS.
- embedding profile skip accepted for core profile.

## Hermes-agent onboarding prompt validation

The simple onboarding prompt was manually tested against Hermes-agent.

Observed behavior:

- Hermes-agent read the requested guide files.
- Hermes-agent summarized project purpose.
- Hermes-agent described governed access through Runes Shield.
- Hermes-agent identified readable files and prohibited direct mutations.
- Hermes-agent explained memory proposal / review / promotion flow.
- Hermes-agent explained recall and smoke checks.
- Hermes-agent preserved the no-direct-trusted-write and no-secrets boundaries.

## Changes

Applied:

- `VERSION`: `0.7.0` -> `0.7.1-dev`
- `docs/fresh-install-manual.md`: added Hermes-agent onboarding prompt
- `wiki/freelancer/verification-m208.md`: added validation note

## Result

Pending commit / push.
