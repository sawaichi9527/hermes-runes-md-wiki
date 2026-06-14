# M212 Migration Guard Real Update Dogfood Decision

Status: READY FOR LOCAL DOGFOOD / safe upstream prepared  
Date: 2026-06-14  
Scope: documentation/status-only upstream change for real `runes-wiki-migration-guard update` dogfood

---

## Purpose

M212 validates the normal-user update path for the minimal migration guard.

The important behavior is not another synthetic `--no-fetch` run. The target behavior is:

```bash
./bin/runes-wiki-migration-guard update
```

This command should:

1. Back up the local `wiki/` tree.
2. Fetch incoming upstream changes.
3. Classify incoming changes conservatively.
4. Apply the update only if incoming changes do not touch possible user-owned `wiki/**/*.md` files.
5. Leave user-owned Markdown untouched.

---

## Dogfood setup

This M212 setup intentionally creates a safe upstream update that does not touch `wiki/`.

Changed files in the prepared upstream update are expected to be limited to development/history documentation such as:

- `dev/wiki-history/k6-freelancer/verification/verification-m212.md`
- `dev/wiki-history/k6-freelancer/next-actions.md`

Because no `wiki/` Markdown is changed by this setup, the guard should classify the update as safe and allow the pull.

---

## Required local verification

Run from an existing local checkout that is behind this M212 setup commit:

```bash
cd ~/workspace/hermes-runes-md-wiki

./bin/runes-wiki-migration-guard update

git status
git log --oneline -10
```

Expected result:

```text
Status: SAFE
Reason: no incoming wiki changes detected
Update applied.
working tree clean
```

The exact wording may differ slightly, but the required behavior is:

- backup directory is created under `backups/wiki-migration-guard/`
- incoming update is allowed because no possible user-owned `wiki/**/*.md` files are touched
- local branch advances to the M212 setup commit
- working tree remains clean

---

## Non-goals

M212 must not expand the tool scope.

Non-goals:

- no automatic restore
- no automatic merge
- no schema migration engine
- no Shield integration
- no Git hook
- no daemon
- no enterprise migration framework
- no artificial user-owned overwrite test in the main repo

---

## Result lock

Pending local dogfood.

After the local `./bin/runes-wiki-migration-guard update` verification passes, this file should be updated to:

```text
M212 Migration Guard Real Update Dogfood Decision
PASS / real safe update dogfood verified / minimal scope preserved
```
