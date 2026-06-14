## N-20260614-M208-M210 Runes Wiki Migration Guard

Status: IMPLEMENTED ON GITHUB / LOCAL PULL VERIFICATION REQUIRED

Current baseline:
- M205-M207 Optional OPC Workspace Overlay is released as v0.7.1.
- Development has reopened as VERSION `0.7.2-dev`.
- Existing installations may already contain user-owned Markdown knowledge under `wiki/`.
- Future updates should protect that local Markdown before repository version/layout updates.

M208-M210 result:
- Added minimal local CLI: `bin/runes-wiki-migration-guard`.
- Added implementation: `tools/wiki_migration_guard/migration_guard.py`.
- Added documentation: `docs/runes-wiki-migration-guard.md`.
- Added verification plan: `dev/wiki-history/k6-freelancer/verification/verification-m208-m210.md`.
- Tool remains independent from Runes Shield.
- Tool scans the whole `wiki/` tree by default.
- Unknown `wiki/**/*.md` is treated as possible user-owned Markdown.
- Tool creates local backups under `backups/wiki-migration-guard/`.
- Tool performs conservative incoming-update risk reporting.

Current position:
- GitHub implementation is present.
- Local pull verification is required on the active workstation.
- GitHub API may not preserve executable bit for the new `bin/` launcher; local `chmod +x` may be needed and should be committed if required.

Recommended local verification:
- Pull latest main.
- Run the M208-M210 commands in the verification file.
- Confirm backup directory is ignored by Git.
- Confirm core smoke remains PASS.

Recommended next milestone after verification:
- M211 Migration Guard Dogfood Result Lock / v0.7.2-dev Next Actions

References:
- `bin/runes-wiki-migration-guard`
- `tools/wiki_migration_guard/migration_guard.py`
- `docs/runes-wiki-migration-guard.md`
- `dev/wiki-history/k6-freelancer/verification/verification-m208-m210.md`

---
