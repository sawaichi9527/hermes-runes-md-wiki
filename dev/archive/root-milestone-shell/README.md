# Root Milestone Shell Archive

Status:
- M31.4 archive move lock enabled
- Historical root milestone shell scripts archived
- No deletion performed

Scope:
This archive stores root-level M24/M25/M26 shell scripts that were used during
early governed promotion, attunement, and rollback milestone implementation.

Rules:
- Files in this directory are historical relics.
- Do not execute archived shell scripts as active workflow entrypoints.
- Do not add new active tooling here.
- Do not move files out of this archive unless explicitly performing a governed restoration.
- New smoke tests and active CLI tools should live under `smoke/`, `bin/`, or `tools/`.

Verification:
- `smoke/m31_4_archive_lock_smoke.sh` checks that:
  - root has no active M24/M25/M26 shell scripts
  - archive contains 13 root milestone shell scripts
  - active `tools/runes/` no longer contains archived milestone-era tooling
  - archived Python milestone tooling remains under `tools/archive/milestone-shell/`
