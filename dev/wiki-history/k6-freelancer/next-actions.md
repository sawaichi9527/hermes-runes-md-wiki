## N-20260614-M214 v0.7.2 Release Prep Decision

Status: READY

Current baseline:
- VERSION remains `0.7.2-dev`.
- M208-M210 Migration Guard Minimal MVP is PASS / locally verified / hotfix verified.
- M211 README Update Flow Alignment is PASS / documentation aligned / minimal scope preserved.
- M212 Real Safe Update Dogfood is PASS / real safe update dogfood verified / minimal scope preserved.
- M213 v0.7.2 Release Candidate Decision is PASS / release candidate ready / no release tag created.

M214 purpose:
- Decide whether to prepare v0.7.2 release notes.
- Decide whether to bump `VERSION` from `0.7.2-dev` to `0.7.2`.
- Keep v0.7.2 focused on the minimal migration guard, documentation alignment, and verification locks.

Suggested M214 local check:

```bash
cd ~/workspace/hermes-runes-md-wiki

./bin/runes-wiki-migration-guard update
cat VERSION
python3 -m py_compile tools/wiki_migration_guard/migration_guard.py
./bin/runes-wiki-migration-guard plan --no-fetch
./bin/runes-wiki-migration-guard update --dry-run --no-fetch
./bin/hermes-memory-smoke

git status
git log --oneline -12
```

M214 allowed scope:
- Draft `docs/releases/v0.7.2.md`.
- Optionally bump `VERSION` to `0.7.2` after explicit release-prep decision.
- Update README release references only if needed.
- Record release-prep verification.

M214 non-goals:
- No release tag by default.
- No migration guard feature expansion.
- No user-owned `wiki/` changes.

Possible next milestone:
- M215 v0.7.2 Release Finalization / Tag Decision

References:
- `VERSION`
- `README.md`
- `docs/runes-wiki-migration-guard.md`
- `dev/wiki-history/k6-freelancer/verification/verification-m213.md`

---
