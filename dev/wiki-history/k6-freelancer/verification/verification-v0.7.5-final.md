# Verification: v0.7.5 Final Release

Status: FINAL RELEASE RECORDED / tag pending  
Date: 2026-08-15  
Version line: 0.7.5

## Scope

v0.7.5 is a functional release that restores the Runes Shield runtime read-only tools and brings the OPC 8-profile governed wiki namespace into the formal mainline.

It records:

- PR #3: Restore runtime validator+fixtures so `tools/runes_shield/` no longer depends on `dev/`.
- PR #4: Add OPC v4.1 `opc` namespace (8 roles) + Plur slot in source-priority (M5), ported from the K6 local mainline.

## Runtime changes

```text
tools/runes_shield/validate_proposal_fixture.py   added (runtime copy, source = dev/.../validation/)
tools/runes_shield/fixtures/                       added (4 proposal samples)
tools/runes_shield/DEPENDENCY_NOTES.md             added (dev source mapping)
tools/runes_shield/runes_shield_tools_index.json   smoke.* entries removed (index_version -> m40.1)
wiki/freelancer/opc/<8 roles>/README.md            added
wiki/_system/source-priority.md                    Plur slot #4 inserted
```

## Release artifacts

```text
docs/releases/v0.7.5.md
CHANGELOG.md
VERSION (0.7.5)
dev/wiki-history/k6-freelancer/next-actions.md
dev/wiki-history/k6-freelancer/verification/verification-v0.7.5-final.md
```

## Verification evidence

Local (Acubens, Windows 10) and K6 verification of all read-only tools:

```text
proposal_registry.py list/show          PASS (4 fixtures: 1 valid + 3 negative)
proposal_review_queue.py list/show      PASS (1 pending)
proposal_draft_store.py list/show       PASS
build_proposal_draft.py dry-run         PASS
build_proposal_draft.py write-draft     PASS (validator re-validation PASS)
python -m compileall tools/runes_shield OK
K6 main converged to 3364607            registry 4 entries / queue 1 / 8 role READMEs
```

## Required release verification

After pulling the final release commit locally:

```bash
cd ~/workspace/hermes-runes-md-wiki
git pull
cat VERSION
git status
python3 tools/runes_shield/proposal_registry.py list --format json
```

Expected:

```text
VERSION = 0.7.5 (or 0.7.6-dev after post-release bump, depending on checked-out commit)
working tree clean
proposal_registry list: 4 entries
```

## Result

```text
PASS: v0.7.5 final scope recorded.
PASS: Runes Shield read-only tools restored and verified.
PASS: OPC 8-profile wiki namespace present in mainline.
PENDING: local pull verification and git tag creation.
```
