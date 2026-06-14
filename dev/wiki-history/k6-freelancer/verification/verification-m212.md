# M212 Migration Guard Real Update Dogfood Decision

Status: PASS / real safe update dogfood verified / minimal scope preserved  
Date: 2026-06-14  
Scope: real `runes-wiki-migration-guard update` dogfood for a safe upstream change

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

The M212 setup intentionally created a safe upstream update that did not touch `wiki/`.

Prepared upstream changed files:

- `dev/wiki-history/k6-freelancer/verification/verification-m212.md`
- `dev/wiki-history/k6-freelancer/next-actions.md`

Because no `wiki/` Markdown was changed by this setup, the guard was expected to classify the update as safe and allow the pull.

---

## Local verification command

The local dogfood was executed from an existing checkout at commit `bb73aaa`:

```bash
cd ~/workspace/hermes-runes-md-wiki

./bin/runes-wiki-migration-guard update

git status
git log --oneline -10
```

---

## Observed result

The guard reported:

```text
Runes Wiki Migration Guard
Version: 0.7.2-dev
Repo head: bb73aaa
Wiki root: wiki
Backup: backups/wiki-migration-guard/20260614-215044

Detected workspaces:
- freelancer

Status: SAFE
Reason: incoming update does not touch wiki Markdown

Incoming changed files:
- dev/wiki-history/k6-freelancer/next-actions.md
- dev/wiki-history/k6-freelancer/verification/verification-m212.md

Policy:
- Unknown wiki/**/*.md is treated as possible user-owned Markdown.
- This tool never overwrites user-owned Markdown.
- This tool is not part of Runes Shield.
Applying safe repository update with: git pull --ff-only
```

After the safe update, the guard postflight scan reported the new head:

```text
Repo head: 53ac087
Status: SCAN
```

`git status` confirmed:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

`git log --oneline -10` confirmed the local checkout advanced through the prepared M212 setup commits:

```text
53ac087 Update next actions for M212 dogfood
ea5c6d6 Prepare M212 real update dogfood
bb73aaa Update next actions after M211 lock
0650768 Record M211 migration guard dogfood lock
84093c6 Align migration guard docs with dogfood lock
c3ebbbf Document migration guard update flow
a0c7f7f Update next actions after M208-M210 lock
19898bd Lock M208-M210 migration guard verification
b62b6b4 Fix migration guard backup collision
5376fe3 Mark migration guard launcher executable
```

---

## Result assessment

PASS.

Verified behavior:

- Backup directory was created under `backups/wiki-migration-guard/`.
- Incoming update was classified as SAFE because no `wiki/` Markdown files were touched.
- Guard applied the update with `git pull --ff-only`.
- Local checkout advanced from `bb73aaa` to `53ac087`.
- Working tree remained clean.
- User-owned Markdown was not touched.
- Tool scope remained minimal.

---

## Non-goals preserved

M212 did not expand the tool scope.

Non-goals preserved:

- no automatic restore
- no automatic merge
- no schema migration engine
- no Shield integration
- no Git hook
- no daemon
- no enterprise migration framework
- no artificial user-owned overwrite test in the main repo

---

## Final lock

```text
M212 Migration Guard Real Update Dogfood Decision
PASS / real safe update dogfood verified / minimal scope preserved
```
