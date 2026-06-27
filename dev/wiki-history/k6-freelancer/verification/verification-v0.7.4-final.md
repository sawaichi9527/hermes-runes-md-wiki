# Verification: v0.7.4 Final Release

Status: FINAL RELEASE RECORDED / tag pending  
Date: 2026-06-27  
Version line: 0.7.4

## Scope

v0.7.4 is a conservative PLUR runtime memory bridge documentation and governance-boundary release.

It records the optional PLUR reintegration boundary without adding runtime PLUR helpers, PLUR smoke tests, Hermes Agent core patches, Hermes Agent native configuration changes, PLUR memory reads, PLUR memory writes, PLUR migrations, PLUR deletions, or automatic PLUR-to-Runes Wiki promotion.

## Final scope state

```text
S1-S6  recorded as PLUR bridge scope / policy / hygiene
S7-S9  design-only
S10    paused
S11    candidate dry-run design-only
S12    verification/docs sync design-only
```

## Release artifacts

```text
docs/releases/v0.7.4.md
docs/plur-runtime-memory-bridge.md
CHANGELOG.md
dev/wiki-history/k6-freelancer/next-actions.md
dev/wiki-history/k6-freelancer/verification/verification-s1-s6-v0.7.4-dev-plur-runtime-memory-bridge.md
dev/wiki-history/k6-freelancer/verification/verification-s10-s12-v0.7.4-dev-design-only.md
```

## Local verification evidence

User local verification before final release marking:

```text
Repo head: e84972c
git status: clean
migration guard: SAFE
Core FTS smoke: PASS
PLUR helper: not added
PLUR smoke: not added
embedding profile: SKIP as expected
```

## Required release verification

After pulling the final release commit locally:

```bash
cd ~/workspace/hermes-runes-md-wiki
git pull
cat VERSION
git status
./bin/runes-wiki-migration-guard plan --no-fetch
./bin/hermes-memory-smoke
```

Expected:

```text
VERSION = 0.7.4 or 0.7.5-dev after post-release bump, depending on checked-out commit
working tree clean
migration guard SAFE
Core FTS smoke PASS
embedding profile skip acceptable when embedding profile is not installed
```

For exact v0.7.4 tagging, tag the release commit before the post-release `0.7.5-dev` bump.

## Result

```text
PASS: v0.7.4 final scope recorded.
PASS: PLUR runtime implementation remains paused/design-only beyond documented boundaries.
PASS: Core runtime surface remains unchanged.
PENDING: local pull verification and git tag creation.
```
