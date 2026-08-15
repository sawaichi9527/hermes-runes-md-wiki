# Changelog

All notable Hermes Runes MD Wiki Open Beta changes are recorded here.

This project uses SemVer-style versioning during Open Beta.

## [0.7.6-dev] - Unreleased

### Planned

- Continue from the v0.7.5 functional release (Runes Shield runtime restoration + OPC namespace).
- Connect the runes-holder / coordinator / secretary Runes approval workflow (P3) using the **forge native wrappers** (`tools/importer/forge.py create-flat|approve|reject` + `bin/hermes-agent-propose-memory`). The restored `tools/runes_shield/` read-only tools cover discovery / inspection only — they cannot change proposal state.
- Keep smoke / regression / trial assets under `dev/` (developer-only).
- Keep the active mainline single-agent / agent-agnostic.

### Notes (P3 wiring correction, 2026-08-15)

- The v0.7.5 fix restored the read-only Runes Shield tools, but those tools (`proposal_registry.py`, `proposal_review_queue.py`, `proposal_draft_store.py`) read **test surfaces only** (`tools/runes_shield/fixtures/*.json`, `tools/runes_shield/drafts/*.json`). They are NOT the real proposal lifecycle.
- The real governed write lifecycle is `tools/importer/forge.py` (M18–M20): `create-flat` writes `wiki/<project>/forge-inbox/<slug>-<op>.md` (status: draft), `approve`/`reject` change status to `approved`/`rejected`, every operation writes an operation manifest under `var/operations/<op_id>.json`, and `tools/importer/write_guard.py` restricts writes to `forge-inbox/`.
- The forge write path is governed by its own `write_guard` and is intentionally **outside** the read-only tool index (`runes_shield_tools_index.json`); the shield boundary contract is two-layer: read/discovery via the index, write via the controlled forge wrappers.
- The legacy `bin/hermes-runes forge|evoke|inscribe` CLI remains an M15.3 scaffold and must not be used as the write path.

## [0.7.5] - 2026-08-15

### Added

- Added `wiki/freelancer/opc/` governed namespace with 8 role READMEs (secretary, coordinator, researcher, writer, builder, runes-holder, aeon-builder, nim-researcher) for the OPC 8-profile agent set (v4.1).
- Inserted Plur slot at #4 in `wiki/_system/source-priority.md` (OPC v4.1 §4): Plur is learned conventions that may decay; when conflicting with Runes, Runes wins and the engram is flagged for manual prune.
- Added `tools/runes_shield/validate_proposal_fixture.py` and `tools/runes_shield/fixtures/` (4 proposal samples) to the runtime so `tools/runes_shield/` is self-contained and no longer depends on `dev/`.
- Added `tools/runes_shield/DEPENDENCY_NOTES.md` mapping each runtime copy to its `dev/` source for future maintenance.
- Added `docs/releases/v0.7.5.md` release notes.
- Added v0.7.5 verification notes under `dev/wiki-history/k6-freelancer/verification/`.

### Changed

- Removed `smoke.*` tool entries from `tools/runes_shield/runes_shield_tools_index.json`; smoke scripts remain under `dev/` as developer-only assets (index_version → m40.1).
- Ported the M5 OPC namespace from the K6 local mainline (commit `c16c96b`) into the formal mainline via PR #4.

### Fixed

- Fixed broken P0 read-only Runes Shield tools (`proposal_registry.py`, `proposal_review_queue.py`). Root cause: commit `e1cb587` moved `validate_proposal_fixture.py` and the proposal fixtures under `dev/`, but the runtime CLIs (`build_proposal_manifest.py`, `build_proposal_draft.py`, `proposal_draft_store.py`) still imported `validate_proposal_fixture` from the same directory, causing `ModuleNotFoundError`.

### Boundaries

- No Hermes Agent core patch.
- No Hermes Agent native configuration change.
- No daemon, queue, telemetry platform, enterprise approval workflow, heavy LLM judge, or every-turn full-memory scan.
- No automatic PLUR-to-Runes Wiki promotion.
- Smoke / regression / trial assets remain in `dev/` (developer-only) and are not part of the runtime surface.

### Verification

- Local (Acubens, Windows) + K6 verification: `proposal_registry` list/show, `proposal_review_queue` list/show, `proposal_draft_store` list/show, `build_proposal_draft` dry-run and write-draft all PASS.
- `python -m compileall tools/runes_shield` OK.
- K6 `git merge origin/main` converged to `3364607`; registry 4 entries / queue 1 / 8 OPC role READMEs present.

## [0.7.4] - 2026-06-27

### Added

- Added `docs/plur-runtime-memory-bridge.md` as the primary v0.7.4 PLUR bridge planning artifact.
- Added `docs/releases/v0.7.4.md` release notes.
- Added final v0.7.4 verification notes under `dev/wiki-history/k6-freelancer/verification/`.

### Changed

- Reframed v0.7.4 around optional PLUR runtime persistent memory bridge reintegration for the current single-agent / agent-agnostic mainline.
- Preserved Runes Wiki as the governed canonical long-term memory source.
- Preserved Runes Shield as the protected forge gate / operation protection layer, not the memory judge.
- Recorded S1-S6 as the PLUR bridge scope / policy / hygiene boundary.
- Recorded S7-S9 as design-only until a future implementation is explicitly approved.
- Paused S10 because PLUR read-only context summary value is unclear.
- Recorded S11 candidate dry-run flow as proposal-only.
- Recorded S12 smoke / verification / docs sync as manual consistency checking.

### Boundaries

- No OPC profile-agent restoration.
- No Hermes Agent core patch.
- No Hermes Agent native configuration change.
- No daemon, queue, telemetry platform, enterprise approval workflow, heavy LLM judge, or every-turn full-memory scan.
- No automatic PLUR-to-Runes Wiki promotion.
- No bulk migration or deletion of existing deployed PLUR memory.
- No new PLUR runtime helper or smoke test.

### Verification

- Local working tree clean at final design-only verification.
- Migration guard plan SAFE.
- Core FTS smoke PASS.
- Embedding profile skip accepted when embedding profile is not installed.

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
- License: Apache-2.0 applied.
- Current version file: `VERSION`

### Notable Boundaries

- This is not a stable release.
- This is not a production support commitment.
- This is not an enterprise support commitment.
- Governed memory safety boundaries remain unchanged.

### Tagging Note

The `v0.1.0-beta.1` tag should not be used for fresh tester onboarding. It was superseded before release tag lock by the v0.3.0 readiness cleanup path.
