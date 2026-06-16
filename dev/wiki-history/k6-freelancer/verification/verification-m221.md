# Verification M221 - De-OPC Mainline Rebaseline

Status: PASS / single-agent mainline restored / RSS local commit preserved  
Date: 2026-06-17  
Scope: return `main` to single-agent / agent-agnostic active baseline after archiving the v0.7.2 OPC-capable release state

## Decision

Hermes Agent profile-based OPC/A2A deployment is abandoned for this project because the profile-to-profile A2A behavior is not mature enough for the intended local governed memory workflow.

The `v0.7.2` OPC-capable state is preserved by:

```text
v0.7.2 tag
archive/v0.7.2-opc branch
```

`main` now proceeds as a single-agent / agent-agnostic baseline.

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

M221 preserves:

- `v0.7.2` tag
- `archive/v0.7.2-opc` branch
- migration guard
- existing-installation guarded update flow
- v0.7.2 release notes
- developer history under `dev/wiki-history/`
- regular workspace memory under `wiki/freelancer/`
- local RSS active feeds commit reapplied on top of the de-OPC baseline

## Local validation evidence

User local validation confirmed:

```text
main == origin/main
working tree clean
latest commit: 0d13a97 chore: update RSS subscriptions with active feeds (2026-06-14)
VERSION: 0.7.3-dev
```

Validation details:

```text
OPC active files absent:
- docs/opc-workspace-overlay.md
- wiki/_system/opc-workspace-overlay-policy.md
- wiki/freelancer/opc/README.md

operations.md:
- no diff after restore
- abandoned PLUR/OPC operations log was not merged into main

migration guard:
- ./bin/runes-wiki-migration-guard plan --no-fetch
- Status: SAFE
- Reason: no incoming changes detected

smoke:
- Core FTS Smoke Test PASS
```

Local RSS preservation:

```text
0d13a97 chore: update RSS subscriptions with active feeds (2026-06-14)
```

This local commit was cherry-picked after resetting to the M221 de-OPC origin/main baseline, then pushed to origin/main.

## Guard behavior note

M221 intentionally touched `wiki/` seed files and therefore correctly triggered migration guard STOP before the controlled developer sync. This was expected and aligned with migration guard policy.

The user preserved local state before reset:

```text
backups/manual-m221-*/local-operations-opc-plur.patch
backups/manual-m221-*/local-rss-commit.patch
backup/local-before-m221-*
```

The abandoned OPC/PLUR operations patch was intentionally not merged into active main.

## Non-goals

M221 did not:

- reset `main` history
- remove the `v0.7.2` tag
- remove the `archive/v0.7.2-opc` branch
- remove migration guard
- change Runes Shield schemas
- change VERSION
- remove ordinary workspace memory

## Final lock

M221 De-OPC Mainline Rebaseline is locked as:

```text
PASS / single-agent mainline restored / RSS local commit preserved
```

Post-M221 baseline:

```text
main: single-agent / agent-agnostic active baseline
archive/v0.7.2-opc: archived OPC-capable release baseline
VERSION: 0.7.3-dev
no immediate required action
```
