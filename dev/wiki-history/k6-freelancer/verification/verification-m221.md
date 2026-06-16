# Verification M221 - De-OPC Mainline Rebaseline

Status: READY FOR LOCAL DE-OPC CHECK  
Date: 2026-06-14  
Scope: return `main` to single-agent / agent-agnostic active baseline after archiving the v0.7.2 OPC-capable release state

## Decision

Hermes Agent profile-based OPC/A2A deployment is abandoned for this project because the profile-to-profile A2A behavior is not mature enough for the intended local governed memory workflow.

The `v0.7.2` OPC-capable state is preserved by:

```text
v0.7.2 tag
archive/v0.7.2-opc branch
```

`main` should now proceed as a single-agent / agent-agnostic baseline.

## Implementation changes

M221 removes active OPC overlay material from `main`:

```text
README.md
wiki/_system/README.md
docs/releases/v0.7.2.md
docs/opc-workspace-overlay.md
wiki/_system/opc-workspace-overlay-policy.md
wiki/freelancer/opc/README.md
```

Expected mainline behavior after M221:

- `README.md` no longer advertises active OPC workspace overlay usage.
- `wiki/_system/README.md` no longer lists OPC overlay policy in the required runtime policy read order.
- `docs/opc-workspace-overlay.md` is no longer active on main.
- `wiki/_system/opc-workspace-overlay-policy.md` is no longer active on main.
- `wiki/freelancer/opc/README.md` is no longer an active workspace seed on main.
- `docs/releases/v0.7.2.md` records that the OPC-capable v0.7.2 state is archived.

## Preserved items

M221 must preserve:

- `v0.7.2` tag
- `archive/v0.7.2-opc` branch
- migration guard
- existing-installation guarded update flow
- v0.7.2 release notes
- developer history under `dev/wiki-history/`
- regular workspace memory under `wiki/freelancer/`

## Guard expectation

Unlike normal docs-only updates, M221 intentionally touches `wiki/` seed files to remove the active OPC overlay from main.

Therefore `./bin/runes-wiki-migration-guard update` may return STOP before pull. This is expected if the incoming changed files are limited to the M221 de-OPC cleanup set.

For this controlled developer sync only, after confirming the incoming files match M221, it is acceptable to apply:

```bash
git pull --ff-only
```

This does not change the general rule: existing users should still use the migration guard for normal updates.

## Non-goals

M221 does not:

- reset `main`
- remove the `v0.7.2` tag
- remove the `archive/v0.7.2-opc` branch
- remove migration guard
- change Runes Shield schemas
- change VERSION
- mutate ordinary user-owned memory files

## Local validation plan

Run from a local checkout:

```bash
cd ~/workspace/hermes-runes-md-wiki

./bin/runes-wiki-migration-guard update
# If the guard stops because of the intentional M221 wiki seed cleanup,
# inspect the incoming file list, then run:
# git pull --ff-only

cat VERSION

test ! -e docs/opc-workspace-overlay.md
test ! -e wiki/_system/opc-workspace-overlay-policy.md
test ! -e wiki/freelancer/opc/README.md

python3 -m py_compile tools/wiki_migration_guard/migration_guard.py
./bin/runes-wiki-migration-guard plan --no-fetch
./bin/hermes-memory-smoke

git status
git log --oneline -12

grep -n "Status:\|READY FOR LOCAL DE-OPC CHECK\|M221" \
  dev/wiki-history/k6-freelancer/verification/verification-m221.md \
  dev/wiki-history/k6-freelancer/next-actions.md
```

Expected result:

```text
VERSION = 0.7.3-dev
OPC active files are absent from main
migration guard still works
Core FTS smoke PASS
working tree clean
```

## Lock rule

M221 may be locked as PASS only after local validation confirms the de-OPC mainline baseline.
