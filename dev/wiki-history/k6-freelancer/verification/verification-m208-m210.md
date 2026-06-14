# Verification M208-M210 - Runes Wiki Migration Guard

Status: IMPLEMENTED ON GITHUB / LOCAL PULL VERIFICATION REQUIRED  
Version line: 0.7.2-dev

## Scope

M208-M210 introduce a minimal local safety helper:

```text
bin/runes-wiki-migration-guard
tools/wiki_migration_guard/migration_guard.py
docs/runes-wiki-migration-guard.md
```

The tool is intentionally small and low-frequency.

It is not:

- Runes Shield
- recall
- proposal governance
- a daemon
- a Git hook
- an enterprise migration framework

## Expected behavior

Default behavior protects the whole `wiki/` tree.

Classification is conservative:

```text
system-ish:
  wiki/_system/*.md
  wiki/README.md
  wiki/hermes_runes_index.md

user-ish:
  all other wiki/**/*.md
```

Unknown Markdown under `wiki/` is treated as possible user-owned Markdown.

## Verification commands

After pulling locally:

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
chmod +x bin/runes-wiki-migration-guard

python3 -m py_compile tools/wiki_migration_guard/migration_guard.py
./bin/runes-wiki-migration-guard --help
./bin/runes-wiki-migration-guard plan --no-fetch
./bin/runes-wiki-migration-guard preflight --no-fetch
./bin/runes-wiki-migration-guard update --dry-run --no-fetch
./bin/runes-wiki-migration-guard postflight
./bin/hermes-memory-smoke

git status
```

## Expected result

- Python compile PASS.
- Help displays CLI usage.
- `plan --no-fetch` reports SAFE / CAUTION / STOP without modifying tracked files.
- `preflight --no-fetch` creates a local backup under `backups/wiki-migration-guard/`.
- `update --dry-run --no-fetch` creates a backup and does not pull.
- `postflight` scans the current `wiki/` tree.
- Smoke remains PASS for core FTS.
- Git working tree is clean except possibly executable-bit update for `bin/runes-wiki-migration-guard`.

## Known GitHub API note

The GitHub Contents API may create `bin/runes-wiki-migration-guard` without executable mode.

If local verification shows the mode changed after `chmod +x`, commit that mode-only update separately:

```bash
git add bin/runes-wiki-migration-guard
git commit -m "Mark migration guard launcher executable"
git push
```

## PASS criteria

M208-M210 can be locked when:

```text
- CLI help works
- Python compile works
- plan/preflight/update dry-run/postflight work locally
- backup directory is created and ignored by Git
- no user-owned Markdown is overwritten
- core smoke remains PASS
```
