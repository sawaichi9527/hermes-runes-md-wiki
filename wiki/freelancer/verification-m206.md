# M206 Promote Open Beta Target to v0.7.0

Status: IN PROGRESS / M206.2 final release gate
Version line: 0.7.0
Date: 2026-06-08

## Scope

M206 promotes the Open Beta target from the v0.5.x public tester baseline to the v0.7.0 fresh-install hardened baseline.

This milestone must not move or rewrite historical tags.

## Starting state

Confirmed before M206.1:

- `VERSION`: `0.7.0-dev`
- latest commit: `06607ed Align fresh install tooling defaults`
- working tree: clean
- `main == origin/main`
- fresh-install core path: PASS without runtime override
- backend check: PASS
- import: PASS
- core smoke: PASS
- embedding profile skip: accepted for core profile

## M206.1 Release-prep docs

Status: PASS / pushed

Planned additions:

- `docs/v0.7.0-release-readiness.md`
- `docs/v0.7.0-tester-checklist.md`
- `docs/github-release-note-v0.7.0.md`

Planned updates:

- `README.md`
- `docs/open-beta-starter.md`
- `docs/public-tester-notification-final.md`
- `docs/open-beta-feedback-issue-draft.md`
- `docs/fresh-install-manual.md`

## M206.2 Final release gate

Status: IN PROGRESS / final-ready version line prepared.

Expected final gate:

- `VERSION`: `0.7.0-dev` -> `0.7.0`
- `CHANGELOG.md` updated with `[0.7.0]`
- backend check PASS
- migration PASS
- import PASS
- direct FTS recall PASS
- core smoke PASS

## M206.3 Tag / release

Pending.

Expected:

- annotated tag `v0.7.0`
- GitHub Release published
- v0.7.0 marked as current Open Beta baseline


## M206.2 Prepared changes

Status: PRE-GATE / local validation required

Prepared files:

- `VERSION`
- `CHANGELOG.md`
- `docs/v0.7.0-release-readiness.md`
- `docs/v0.7.0-tester-checklist.md`
- `docs/github-release-note-v0.7.0.md`
- `wiki/freelancer/verification-m206.md`

Required validation before commit:

```bash
cat VERSION
git diff --check
./bin/hermes-backend-check
./bin/hermes-memory-migrate
./bin/hermes-memory-import
./bin/hermes-recall "forge inbox boundary" --project freelancer --mode fts --limit 5 --json
./bin/hermes-memory-smoke
```

M206.3 tag / release remains pending until the final gate is committed and pushed.
