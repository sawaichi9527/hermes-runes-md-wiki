## N-20260614-M212 Migration Guard Real Update Dogfood Decision

Status: READY

Current baseline:
- M205-M207 Optional OPC Workspace Overlay is released as v0.7.1.
- Development has reopened as VERSION `0.7.2-dev`.
- M208-M210 Runes Wiki Migration Guard Minimal MVP is PASS / locally verified / hotfix verified.
- M211 Migration Guard Dogfood Result Lock / README Update Flow Alignment is PASS / documentation aligned / minimal scope preserved.

M208-M210 locked result:
- Added minimal local CLI: `bin/runes-wiki-migration-guard`.
- Added implementation: `tools/wiki_migration_guard/migration_guard.py`.
- Added documentation: `docs/runes-wiki-migration-guard.md`.
- Added verification record: `dev/wiki-history/k6-freelancer/verification/verification-m208-m210.md`.
- Launcher executable bit is committed.
- Same-second backup collision is fixed.
- Tool remains independent from Runes Shield.
- Tool scans the whole `wiki/` tree by default.
- Unknown `wiki/**/*.md` is treated as possible user-owned Markdown.
- Tool creates local backups under `backups/wiki-migration-guard/`.
- Tool performs conservative incoming-update risk reporting.
- Tool does not automatically repair, restore, merge, delete, or overwrite user-owned Markdown.

M211 locked result:
- Added README `Existing Installation Updates` section.
- README now recommends `./bin/runes-wiki-migration-guard update` for existing installations where `wiki/` may contain local knowledge.
- `docs/runes-wiki-migration-guard.md` is aligned with dogfood verified / minimal scope locked status.
- Added `dev/wiki-history/k6-freelancer/verification/verification-m211.md`.
- M211 keeps the guard small and avoids enterprise migration scope expansion.

Verified local behavior:
- `python3 -m py_compile tools/wiki_migration_guard/migration_guard.py`: PASS.
- `./bin/runes-wiki-migration-guard --help`: PASS.
- `plan --no-fetch`: PASS.
- `preflight --no-fetch`: PASS.
- `update --dry-run --no-fetch`: PASS.
- repeated backup creation in the same second: PASS.
- `postflight`: PASS.
- `./bin/hermes-memory-smoke`: core FTS PASS.
- local working tree clean after verification.

Recommended next milestone:
- M212 Migration Guard Real Update Dogfood Decision

M212 purpose:
- Decide whether to run one real `./bin/runes-wiki-migration-guard update` dogfood against a safe upstream change.
- If no safe upstream change exists, record that dry-run and no-fetch dogfood are sufficient for the minimal MVP.
- Keep the tool low-frequency, local, and conservative.

M212 non-goals:
- No automatic restore.
- No automatic merge.
- No schema migration engine.
- No Shield integration.
- No Git hook.
- No daemon.
- No expansion into enterprise migration management.

References:
- `README.md`
- `bin/runes-wiki-migration-guard`
- `tools/wiki_migration_guard/migration_guard.py`
- `docs/runes-wiki-migration-guard.md`
- `dev/wiki-history/k6-freelancer/verification/verification-m208-m210.md`
- `dev/wiki-history/k6-freelancer/verification/verification-m211.md`

---
