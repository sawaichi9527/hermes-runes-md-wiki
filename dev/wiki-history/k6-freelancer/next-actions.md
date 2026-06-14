## N-20260614-M213 v0.7.2 Release Candidate Decision

Status: READY

Current baseline:
- M205-M207 Optional OPC Workspace Overlay is released as v0.7.1.
- Development has reopened as VERSION `0.7.2-dev`.
- M208-M210 Runes Wiki Migration Guard Minimal MVP is PASS / locally verified / hotfix verified.
- M211 Migration Guard Dogfood Result Lock / README Update Flow Alignment is PASS / documentation aligned / minimal scope preserved.
- M212 Migration Guard Real Update Dogfood Decision is PASS / real safe update dogfood verified / minimal scope preserved.

M208-M212 locked result:
- `bin/runes-wiki-migration-guard` exists and is executable.
- `tools/wiki_migration_guard/migration_guard.py` passed py_compile.
- `docs/runes-wiki-migration-guard.md` documents the minimal guard.
- README recommends `./bin/runes-wiki-migration-guard update` for existing installations.
- Same-second backup collision is fixed and locally verified.
- Real safe update dogfood passed through the guard itself.
- Tool remains independent from Runes Shield.
- Tool scans the whole `wiki/` tree by default.
- Unknown `wiki/**/*.md` is treated as possible user-owned Markdown.
- Tool creates local backups under `backups/wiki-migration-guard/`.
- Tool does not automatically repair, restore, merge, delete, or overwrite user-owned Markdown.

M213 purpose:
- Decide whether the current `0.7.2-dev` state should be promoted toward a small v0.7.2 release candidate.
- Keep the release decision narrow: migration guard + documentation alignment only.
- Avoid expanding migration guard into repair, schema migration, hooks, daemon behavior, or enterprise migration management.

Suggested M213 checks:

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
- Guard sees no unsafe incoming `wiki/` changes.
- Python CLI compiles.
- Plan and dry-run remain stable.
- Core FTS smoke remains PASS.
- Working tree remains clean.

M213 non-goals:
- No new migration guard feature.
- No automatic restore.
- No automatic merge.
- No schema migration engine.
- No Shield integration.
- No Git hook.
- No daemon.
- No expansion into enterprise migration management.
- No release tagging unless explicitly decided after M213.

References:
- `README.md`
- `bin/runes-wiki-migration-guard`
- `tools/wiki_migration_guard/migration_guard.py`
- `docs/runes-wiki-migration-guard.md`
- `dev/wiki-history/k6-freelancer/verification/verification-m208-m210.md`
- `dev/wiki-history/k6-freelancer/verification/verification-m211.md`
- `dev/wiki-history/k6-freelancer/verification/verification-m212.md`

---
