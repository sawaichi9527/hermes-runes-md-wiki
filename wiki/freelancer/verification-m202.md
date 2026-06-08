# M202 Post-release Public Docs Verification

Status: PASS / v0.5.0 public docs updated / committed / pushed  
Version line: 0.5.0  
Date: 2026-06-08

## Scope

M202 updates post-release public-facing documentation after the `v0.5.0` annotated tag was created and pushed.

This milestone does not move or recreate the `v0.5.0` tag.

## Release anchor

Final release tag:

- `v0.5.0`

Tag target:

- `3fa580b Promote v0.5.0 final version line`

Post-release documentation commit:

- `9366ccf Update public tester docs for v0.5.0`

This separation is intentional:

- `v0.5.0` tag remains locked on the final release version-line commit.
- Post-release public docs updates live after the tag on `main`.

## M202.1 Post-release docs inventory

Status: PASS / docs drift identified

Confirmed:

- `VERSION`: `0.5.0`
- `v0.5.0` tag exists.
- `v0.5.0` points to the final version-line commit.
- Some public-facing docs still referenced older Open Beta baselines.

Identified drift:

- `docs/open-beta-starter.md` still referenced `v0.3.0`.
- `docs/public-tester-notification-final.md` still referenced `v0.1.0-beta.1`.
- `docs/open-beta-feedback-issue-draft.md` still referenced `v0.1.0-beta.1`.

Historical docs intentionally retained:

- `docs/github-release-note-v0.1.0-beta.1.md`
- `docs/v0.3.0-tester-checklist.md`

## M202.2 Public tester docs update

Status: PASS / committed / pushed

Updated:

- `README.md`
- `docs/open-beta-starter.md`
- `docs/public-tester-notification-final.md`
- `docs/open-beta-feedback-issue-draft.md`

Added:

- `docs/v0.5.0-tester-checklist.md`
- `docs/github-release-note-v0.5.0.md`

Latest related commit:

- `9366ccf Update public tester docs for v0.5.0`

## Current public tester baseline

Recommended public tester baseline:

- `v0.5.0`

Expected version:

- `0.5.0`

Primary tester documents:

- `docs/open-beta-starter.md`
- `docs/v0.5.0-tester-checklist.md`
- `docs/github-release-note-v0.5.0.md`
- `docs/v0.5.0-release-readiness.md`
- `CHANGELOG.md`

## Accepted historical references

The following older references are allowed when they are explicitly historical or superseded:

- `v0.1.0-beta.1`
- `v0.3.0`

They must not appear as the current recommended public tester baseline.

## Verification result

M202 is locked as:

PASS / v0.5.0 public tester docs updated / release tag preserved / working tree clean
