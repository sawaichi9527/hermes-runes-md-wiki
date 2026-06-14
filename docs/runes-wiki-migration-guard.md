# Runes Wiki Migration Guard

Status: MVP design and CLI baseline  
Scope: local personal installation update safety

## Purpose

`runes-wiki-migration-guard` is a small local safety helper for existing Hermes Runes MD Wiki installations.

It protects the `wiki/` Markdown source-of-truth before repository updates.

It is intentionally small:

- no Runes Shield integration
- no daemon
- no Git hooks
- no automatic merge
- no automatic restore
- no enterprise migration framework
- no automatic user-owned Markdown edits

## Normal user command

Existing users should update with:

```bash
./bin/runes-wiki-migration-guard update
```

This command:

1. scans the whole `wiki/` tree
2. creates a local backup under `backups/wiki-migration-guard/`
3. runs `git fetch`
4. checks incoming changed files
5. stops before pull if incoming changes touch possible user-owned wiki Markdown
6. runs `git pull --ff-only` only when the update is safe or system/index-only
7. scans `wiki/` again after update

## Dry run

```bash
./bin/runes-wiki-migration-guard update --dry-run
```

Dry run creates the same safety backup and plan, but does not apply the repository update.

## Plan only

```bash
./bin/runes-wiki-migration-guard plan
```

`plan` fetches the remote and shows incoming update risk. It does not create a backup and does not pull.

## Advanced commands

```bash
./bin/runes-wiki-migration-guard preflight
./bin/runes-wiki-migration-guard postflight
./bin/runes-wiki-migration-guard repair --dry-run
```

`repair` is suggestion-only in the MVP. It does not change files.

## Classification rule

The guard uses a conservative rule:

```text
system-ish:
  wiki/_system/*.md
  wiki/README.md
  wiki/hermes_runes_index.md

user-ish:
  all other wiki/**/*.md
```

Unknown Markdown under `wiki/` is treated as possible user-owned Markdown.

## Update decision

```text
SAFE:
  incoming update does not touch wiki Markdown

CAUTION:
  incoming update only touches system/index wiki Markdown

STOP:
  incoming update touches possible user-owned wiki Markdown
  or local working tree has changes during update
```

`STOP` means no repository update is applied. A local backup is still created.

## Backup location

Backups are local-only and ignored by Git:

```text
backups/wiki-migration-guard/YYYYMMDD-HHMMSS/
  VERSION
  git-head.txt
  report.json
  wiki/
```

## Boundary

This tool is not the main Runes operation path.

It is only a low-frequency safety helper for version or layout updates.

For normal memory operations, continue to use the existing Runes Shield / proposal / recall flows.
