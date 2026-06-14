# Verification M213 - v0.7.2 Release Candidate Decision

Status: READY FOR LOCAL RC CHECK  
Scope: release-candidate decision only; no release tag; no VERSION bump

## Purpose

M213 decides whether the current `0.7.2-dev` baseline is ready to move toward a small v0.7.2 release candidate.

This milestone is intentionally narrow. It does not add new migration guard features and does not create a release tag.

## Current candidate baseline

Current expected baseline before local verification:

- VERSION: `0.7.2-dev`
- M205-M207 Optional OPC Workspace Overlay: released as v0.7.1
- M208-M210 Runes Wiki Migration Guard Minimal MVP: PASS / locally verified / hotfix verified
- M211 README Update Flow Alignment: PASS / documentation aligned / minimal scope preserved
- M212 Real Safe Update Dogfood: PASS / real safe update dogfood verified / minimal scope preserved

## Candidate scope

The v0.7.2 candidate scope should remain limited to:

- minimal `runes-wiki-migration-guard` update safety helper
- README update flow alignment for existing installations
- documentation and verification locks for M208-M212
- no Shield integration
- no daemon
- no Git hook
- no automatic restore
- no automatic merge
- no schema migration framework
- no enterprise migration management

## Local RC check procedure

Run from repo root:

```bash
cd ~/workspace/hermes-runes-md-wiki

./bin/runes-wiki-migration-guard update
python3 -m py_compile tools/wiki_migration_guard/migration_guard.py
./bin/runes-wiki-migration-guard plan --no-fetch
./bin/runes-wiki-migration-guard update --dry-run --no-fetch
./bin/hermes-memory-smoke

git status
git log --oneline -12
```

Expected result:

- guard update path is SAFE or reports no incoming changes
- Python CLI compiles
- plan and dry-run remain stable
- core FTS smoke remains PASS
- embedding profile may be skipped if optional dependencies are not installed
- working tree remains clean
- VERSION remains `0.7.2-dev`

## Release candidate decision rule

M213 may be locked as PASS only if:

- all local RC checks pass
- no new migration guard functionality is added during M213
- no `wiki/` user-owned content is modified
- no release tag is created
- no VERSION bump is performed

If PASS, the next milestone may decide whether to prepare v0.7.2 release notes and version bump.

## Non-goals

- No v0.7.2 tag in M213
- No VERSION change in M213
- No release note finalization in M213
- No migration guard feature expansion
- No auto-restore behavior
- No repair/apply behavior
- No Git hook
- No daemon
- No Shield integration

## References

- `VERSION`
- `README.md`
- `bin/runes-wiki-migration-guard`
- `tools/wiki_migration_guard/migration_guard.py`
- `docs/runes-wiki-migration-guard.md`
- `dev/wiki-history/k6-freelancer/verification/verification-m208-m210.md`
- `dev/wiki-history/k6-freelancer/verification/verification-m211.md`
- `dev/wiki-history/k6-freelancer/verification/verification-m212.md`

---
