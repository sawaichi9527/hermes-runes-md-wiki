# Changelog

All notable Hermes Runes MD Wiki Open Beta changes are recorded here.

This project uses SemVer-style versioning during Open Beta.

## [0.7.4-dev] - Unreleased

### Planned

- Reintroduce PLUR as an optional runtime persistent memory bridge for the current single-agent / agent-agnostic mainline.
- Keep PLUR detachable: Hermes Runes MD Wiki must remain usable when PLUR is absent, disabled, unavailable, or replaced by a future provider.
- Keep Hermes Agent native customization minimal: do not patch Hermes Agent core or depend on private memory, compression, Kanban, or subagent internals.
- Define PLUR memory roles for engram, episode, checkpoint, and forge candidate use.
- Preserve Runes Wiki as the governed canonical long-term memory source.
- Preserve Runes Shield as the protected forge gate / operation protection layer, not the memory judge.
- Require human-in-the-loop approval before any PLUR candidate is forged into Runes Wiki.
- Add minimal PLUR memory hygiene suitable for personal/local use: required scope, no default episode injection, governance hint pointers, no auto-promotion, superseded checkpoints, and cautious handling of already-deployed PLUR memory.

### Non-goals

- No OPC profile-agent restoration.
- No Hermes Agent core patch.
- No daemon, queue, telemetry platform, enterprise approval workflow, heavy LLM judge, or every-turn full-memory scan.
- No automatic PLUR-to-Runes Wiki promotion.
- No bulk migration or deletion of existing deployed PLUR memory.

### Documentation

- Added `docs/plur-runtime-memory-bridge.md` as the primary v0.7.4-dev planning artifact.
- Updated `dev/wiki-history/k6-freelancer/next-actions.md` with S1-S6 PLUR bridge scope.

## [0.7.0] - 2026-06-08

### Added

- v0.7.0 fresh-install release-readiness documentation.
- v0.7.0 public tester checklist.
- v0.7.0 GitHub release note draft.
- Standalone fresh-install manual path for current Open Beta onboarding.

### Changed

- Open Beta target advanced from the historical v0.5.0 baseline to the v0.7.0 fresh-install hardened line.
- Fresh-install public tester path now centers on `docs/fresh-install-manual.md` and `docs/v0.7.0-tester-checklist.md`.
- PostgreSQL stack/data removal and repository/venv removal are documented as separate reset paths.
- Core smoke defaults align with the fresh-install `freelancer` workspace instead of the historical `sample-project` fixture.
- `bin/hermes-memory-import` resolves the repository root from the wrapper location instead of the old `~/workspace/hermes-memory` path.

### Fixed

- Fresh-install backend check no longer fails when backend stack `.env` omits `POSTGRES_PORT`; it defaults to local port `5433`.
- Fresh-install import and core smoke no longer require manual `HERMES_MEMORY_ROOT` or `HERMES_SMOKE_*` runtime overrides.
- Public Open Beta starter and tester notification now point to the v0.7.0 target while preserving v0.5.0 as historical baseline.

### Verification

- M204 Fresh Install Runbook Dry-run Review: core path verified.
- M205 Fresh Install Tooling Alignment: PASS / pushed / clean-run verified.
- M206.1 v0.7.0 release-prep docs: PASS / pushed.
- M206.2 final release gate: pending at section creation.

### Release status

- This is the final-ready v0.7.0 release line.
- Final `v0.7.0` tag may be created only after the M206.2 final gate passes.

## [0.5.0] - 2026-06-08

### Added

- CPU-only embedding writer for runtime use.
- Runtime release-readiness documentation for the v0.5.0 line.
- Accepted SKIP gates for local-only unavailable LLM endpoint and absent fresh-workspace governance fixtures.

### Changed

- Runtime seed smoke fixtures were realigned to the current `freelancer` workspace.
- Hybrid/vector recall was restored for the current PostgreSQL/pgvector runtime.
- Runtime CLI and tools surface were cleaned:
  - user-facing wrappers remain in `bin/`
  - runtime/support tools remain in root `tools/`
  - development-only smoke, fixture, regression, trial, and historical assets moved under `dev/`
- Runtime support tool filenames no longer carry old milestone suffixes.

### Fixed

- `security_scan.py` now resolves the current repository root instead of the old `~/workspace/hermes-memory` default.
- Executable bits were restored for runtime check scripts.

### Release status

- This is the final v0.5.0 release line.
- Final `v0.5.0` tag may be created after the final smoke gate passes.


## [0.3.0] - 2026-06-08

Status: RELEASE CANDIDATE / DOCS PREPARED / TAG PENDING

### Added

- v0.3.0 readiness review and release gate documentation.
- Fresh-clone deployment rehearsal evidence.
- User support evidence / observation / Ragnarok verification evidence.
- M193 root developer layout consolidation inventory.

### Changed

- Default dependency profile is now lightweight by default.
- `requirements.txt` now aliases `requirements-core.txt`.
- `requirements-dev.txt` no longer pulls embedding dependencies by default.
- QUICKSTART now recommends `bash ./bin/hermes-memory-bootstrap` for normal fresh clone setup.
- Developer-only root assets were moved under `dev/`:
  - `db/` -> `dev/db/`
  - `fixtures/` -> `dev/fixtures/`
  - `smoke/` -> `dev/smoke/`
  - `templates/` -> `dev/templates/`
  - `reports/m29-runes-seal-local-inventory/` -> `dev/reports/m29-runes-seal-local-inventory/`
- `bin/hermes-observe` now resolves the repository root from its own wrapper location instead of falling back to the old `~/workspace/hermes-memory` path.

### Preserved

- `migrations/postgres/` remains at root because it is still the runtime migration default path.
- `reports/m33-markdown-source-health/` remains at root because it is still used by Ragnarok / markdown health support tooling.
- Observation, support evidence, and Ragnarok-style diagnostic tooling remain user-facing support features, not developer-only fixtures.

### Verification

- M191 Readiness Review: PASS / boundary clarified.
- M192 Default Dependency Footprint Cleanup: PASS / default install lightweight.
- M193 Root Developer Layout Consolidation: PASS / developer-only root assets moved under `dev/`.
- M194 User Support Evidence Bundle Check: PASS / wrapper fix verified.
- M195 Fresh Clone Deployment Rehearsal: PASS / clean-env rerun verified.

### Release Boundary

`v0.3.0` means a cleaner personal-local Open Beta baseline for fresh clone evaluation. It does not mean stable production support, enterprise readiness, multi-user SaaS readiness, or autonomous trusted memory writing.

## [0.1.0-beta.1] - 2026-06-07

Status: SUPERSEDED / NOT RECOMMENDED FOR TESTER ONBOARDING

### Superseded By

Use `v0.3.0` or later for public tester onboarding.

### Added

- Public Open Beta repository visibility confirmed.
- Apache License, Version 2.0 applied.
- Open Beta safety policy added.
- Open Beta publication checklist added.
- First Open Beta version file added.
- Versioning policy added.

### Baseline

- Repository: `sawaichi9527/hermes-runes-md-wiki`
- Visibility: public
- License: Apache-2.0
- Current version file: `VERSION`

### Notable Boundaries

- This is not a stable release.
- This is not a production support commitment.
- This is not an enterprise support commitment.
- Governed memory safety boundaries remain unchanged.

### Tagging Note

The `v0.1.0-beta.1` tag should not be used for fresh tester onboarding. It was superseded before release tag lock by the v0.3.0 readiness cleanup path.
