## N-20260614-M213 v0.7.2 Release Candidate Decision

Status: READY FOR LOCAL RC CHECK

Current baseline:
- M205-M207 Optional OPC Workspace Overlay is released as v0.7.1.
- Development has reopened as VERSION `0.7.2-dev`.
- M208-M210 Runes Wiki Migration Guard Minimal MVP is PASS / locally verified / hotfix verified.
- M211 Migration Guard Dogfood Result Lock / README Update Flow Alignment is PASS / documentation aligned / minimal scope preserved.
- M212 Migration Guard Real Update Dogfood Decision is PASS / real safe update dogfood verified / minimal scope preserved.

M213 setup result:
- `dev/wiki-history/k6-freelancer/verification/verification-m213.md` records the RC decision plan.
- M213 is not a release tag milestone.
- M213 must not bump VERSION.
- M213 must not add migration guard features.
- M213 should only determine whether the current `0.7.2-dev` baseline is ready to move toward v0.7.2 release prep.

Suggested local RC checks:

```bash
cd ~/workspace/hermes-runes-md-wiki

./bin/runes-wiki-migration-guard update
python3 -m py_compile tools/wiki_migration_guard/migration_guard.py
./bin/runes-wiki-migration-guard plan --no-fetch
./bin/runes-wiki-migration-guard update --dry-run --no-fetch
./bin/hermes-memory-smoke

git status
git log --oneline -12

grep -n "Status:\|READY FOR LOCAL RC CHECK\|VERSION:\|M213" \
  dev/wiki-history/k6-freelancer/verification/verification-m213.md \
  dev/wiki-history/k6-freelancer/next-actions.md
```

Expected result:
- Guard update is SAFE or reports no incoming changes.
- Python CLI compiles.
- Plan and dry-run remain stable.
- Core FTS smoke remains PASS.
- Optional embedding smoke may be skipped if dependencies are not installed.
- Working tree remains clean.
- VERSION remains `0.7.2-dev`.

M213 PASS criteria:
- Local RC checks pass.
- No user-owned `wiki/` content is modified.
- No migration guard feature expansion is introduced.
- No VERSION bump is performed.
- No release tag is created.

M213 non-goals:
- No release tagging.
- No release note finalization.
- No VERSION bump.
- No migration guard feature expansion.
- No automatic restore.
- No automatic merge.
- No schema migration engine.
- No Shield integration.
- No Git hook.
- No daemon.
- No enterprise migration management.

Possible next milestone after local PASS:
- M214 v0.7.2 Release Prep Decision / Release Notes Draft

References:
- `VERSION`
- `README.md`
- `docs/runes-wiki-migration-guard.md`
- `dev/wiki-history/k6-freelancer/verification/verification-m208-m210.md`
- `dev/wiki-history/k6-freelancer/verification/verification-m211.md`
- `dev/wiki-history/k6-freelancer/verification/verification-m212.md`
- `dev/wiki-history/k6-freelancer/verification/verification-m213.md`

---
