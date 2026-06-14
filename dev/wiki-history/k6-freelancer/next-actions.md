## N-20260614-M212 Migration Guard Real Update Dogfood Decision

Status: READY FOR LOCAL DOGFOOD

Current baseline:
- M205-M207 Optional OPC Workspace Overlay is released as v0.7.1.
- Development has reopened as VERSION `0.7.2-dev`.
- M208-M210 Runes Wiki Migration Guard Minimal MVP is PASS / locally verified / hotfix verified.
- M211 Migration Guard Dogfood Result Lock / README Update Flow Alignment is PASS / documentation aligned / minimal scope preserved.

M208-M211 locked result:
- `bin/runes-wiki-migration-guard` exists and is executable.
- `tools/wiki_migration_guard/migration_guard.py` passed py_compile.
- `docs/runes-wiki-migration-guard.md` documents the minimal guard.
- README now recommends `./bin/runes-wiki-migration-guard update` for existing installations.
- Same-second backup collision is fixed and locally verified.
- Tool remains independent from Runes Shield.
- Tool scans the whole `wiki/` tree by default.
- Unknown `wiki/**/*.md` is treated as possible user-owned Markdown.
- Tool creates local backups under `backups/wiki-migration-guard/`.
- Tool does not automatically repair, restore, merge, delete, or overwrite user-owned Markdown.

M212 setup:
- A safe upstream update has been prepared for real dogfood.
- The prepared update intentionally changes only development/history documentation.
- The prepared update does not modify `wiki/`.
- Existing local checkout should pull this prepared update through the guard, not through bare `git pull`.

Required local dogfood command:

```bash
cd ~/workspace/hermes-runes-md-wiki

./bin/runes-wiki-migration-guard update

git status
git log --oneline -10
```

Expected result:
- Guard creates a `backups/wiki-migration-guard/<timestamp>/` backup.
- Incoming update is classified as SAFE because no `wiki/` files are touched.
- Update is applied.
- Working tree remains clean.

M212 non-goals:
- No automatic restore.
- No automatic merge.
- No schema migration engine.
- No Shield integration.
- No Git hook.
- No daemon.
- No expansion into enterprise migration management.

After local dogfood passes:
- Update `dev/wiki-history/k6-freelancer/verification/verification-m212.md` to PASS.
- Update this file to the next small milestone.

References:
- `README.md`
- `bin/runes-wiki-migration-guard`
- `tools/wiki_migration_guard/migration_guard.py`
- `docs/runes-wiki-migration-guard.md`
- `dev/wiki-history/k6-freelancer/verification/verification-m208-m210.md`
- `dev/wiki-history/k6-freelancer/verification/verification-m211.md`
- `dev/wiki-history/k6-freelancer/verification/verification-m212.md`

---
