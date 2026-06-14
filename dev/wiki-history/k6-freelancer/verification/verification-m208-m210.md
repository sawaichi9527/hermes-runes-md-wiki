# Verification M208-M210 - Runes Wiki Migration Guard

Status: PASS / locally verified / hotfix verified  
Version line: 0.7.2-dev  
Verification date: 2026-06-14

## Scope

M208-M210 introduced a minimal local safety helper:

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

The tool does not automatically repair, restore, merge, delete, or overwrite user-owned Markdown.

## Implemented commits

```text
2d14fb0 Add minimal Runes wiki migration guard CLI
2ef1b29 Add runes wiki migration guard launcher
2b79372 Document minimal Runes wiki migration guard
6e9cffc Record M208-M210 wiki migration guard verification plan
1f79a02 Update next actions for M208-M210 migration guard
12a2d94 Allow migration guard options after subcommands
5376fe3 Mark migration guard launcher executable
b62b6b4 Fix migration guard backup collision
```

## Local verification commands

Executed on the active workstation:

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
git log --oneline -8
```

## Initial local verification result

Result:

```text
CLI help: PASS
plan --no-fetch: PASS
preflight --no-fetch: PASS
postflight: PASS
Core FTS smoke: PASS
launcher executable bit: required local mode fix
```

The GitHub Contents API created `bin/runes-wiki-migration-guard` as mode `100644`. The local launcher was marked executable and committed as:

```text
5376fe3 Mark migration guard launcher executable
```

## Hotfix result

Initial `update --dry-run --no-fetch` exposed a backup directory collision when multiple backup-producing commands ran within the same second:

```text
FileExistsError: backups/wiki-migration-guard/YYYYMMDD-HHMMSS already exists
```

The fix adds a deterministic suffix when the timestamp directory already exists:

```text
backups/wiki-migration-guard/YYYYMMDD-HHMMSS
backups/wiki-migration-guard/YYYYMMDD-HHMMSS-02
backups/wiki-migration-guard/YYYYMMDD-HHMMSS-03
```

Hotfix commit:

```text
b62b6b4 Fix migration guard backup collision
```

Hotfix verification commands:

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull

python3 -m py_compile tools/wiki_migration_guard/migration_guard.py

./bin/runes-wiki-migration-guard preflight --no-fetch
./bin/runes-wiki-migration-guard update --dry-run --no-fetch
./bin/runes-wiki-migration-guard update --dry-run --no-fetch

git status
git log --oneline -8
```

Hotfix verification result:

```text
python3 py_compile: PASS
preflight --no-fetch: PASS
update --dry-run --no-fetch: PASS
repeated backup collision handling: PASS
working tree clean: PASS
```

Confirmed backup directories:

```text
backups/wiki-migration-guard/20260614-212925
backups/wiki-migration-guard/20260614-212925-02
backups/wiki-migration-guard/20260614-212925-03
```

Confirmed repository state after verification:

```text
main == origin/main
working tree clean
latest commit: b62b6b4 Fix migration guard backup collision
VERSION: 0.7.2-dev
```

## PASS criteria

M208-M210 are locked as PASS because:

```text
- CLI help works
- Python compile works
- plan/preflight/update dry-run/postflight work locally
- backup directory is created and ignored by Git
- repeated backup creation in the same second is safe
- no user-owned Markdown is overwritten
- core smoke remains PASS
- launcher executable bit is committed
- working tree is clean after verification
```

## Final lock

```text
M208-M210 Runes Wiki Migration Guard Minimal MVP
PASS / locally verified / hotfix verified
```
