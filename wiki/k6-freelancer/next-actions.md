## N-20260604-M67-M70 Boundary Validation

Status: PASS / FROZEN / SMOKE VERIFIED

Final lock:

```text
M67-M70 Boundary Validation Pack
PASS / frozen / smoke verified
```

References:
- `wiki/k6-freelancer/verification-m67.md`
- `wiki/k6-freelancer/verification-m68.md`
- `wiki/k6-freelancer/verification-m69.md`
- `wiki/k6-freelancer/verification-m70.md`

---

## N-20260605-M73-M75 Human-approved Apply Path Validation

Status: PASS / FROZEN / SMOKE VERIFIED

Final lock:

```text
M73-M75 Human-approved Apply Path Validation
PASS / frozen / smoke verified
```

References:
- `wiki/k6-freelancer/verification-m73.md`
- `wiki/k6-freelancer/verification-m74.md`
- `wiki/k6-freelancer/verification-m75.md`

---

## N-20260605-M76-M78 Manual Apply Gate Pack

Status: PASS / SMOKE VERIFIED

Current baseline:
- M76 First Manual Apply Readiness Gate: PASS / smoke verified.
- M77 First Manual Apply Dry-run Execution: PASS / frozen.
- M78 First Manual Apply Commit Gate: PASS / smoke verified.

References:
- `wiki/k6-freelancer/verification-m76.md`
- `wiki/k6-freelancer/verification-m77.md`
- `wiki/k6-freelancer/verification-m78.md`

---

## N-20260605-M79-M82 P0 Baseline Convergence

Status: PASS / FROZEN / SMOKE VERIFIED

Current baseline:
- M79 First Manual Apply Execution Plan: PASS / frozen.
- M80 First Manual Apply Execution: PASS / frozen.
- M81 Post-Apply Verification Lock: PASS / frozen.
- M82 P0 Governed Memory Operating Baseline Freeze: PASS / frozen.
- The implementation remains personal-local and bounded.

Verified commands:

```bash
python3 tools/runes_shield/smoke_m79_first_manual_apply_execution_plan.py
python3 tools/runes_shield/smoke_m80_first_manual_apply_execution.py
python3 tools/runes_shield/smoke_m81_post_apply_verification_lock.py
python3 tools/runes_shield/smoke_m82_p0_governed_memory_operating_baseline.py
```

Verified result:
- M79: PASS / issue_count: 0
- M80: PASS / issue_count: 0
- M81: PASS / issue_count: 0
- M82: PASS / issue_count: 0

Final lock:

```text
M82 P0 Governed Memory Operating Baseline
PASS / frozen / smoke verified
```

References:
- `wiki/k6-freelancer/verification-m79.md`
- `wiki/k6-freelancer/verification-m80.md`
- `wiki/k6-freelancer/verification-m81.md`
- `wiki/k6-freelancer/verification-m82.md`

---

## N-20260605-M83 External Backend Boundary + Simple Backend Guard

Status: PASS / FROZEN / SMOKE VERIFIED

Current baseline:
- External PostgreSQL backend remains an external prerequisite.
- PostgreSQL Docker lifecycle is not owned by the core repository install flow.
- Hermes-owned schema migration wrapper: PASS.
- Simple backend guard wrapper: PASS.
- Migration idempotency: PASS.
- The implementation remains personal-local, bounded, and non-enterprise.

Verified commands:

```bash
bash ./bin/hermes-backend-check
bash ./bin/hermes-memory-migrate
bash ./bin/hermes-memory-migrate
```

Verified result:
- Backend prerequisite guard: PASS
- PostgreSQL stack discovery: PASS
- pgvector availability: PASS
- First schema migration: PASS
- Second migration idempotency: PASS

Final lock:

```text
M83 External Backend Boundary + Simple Backend Guard
PASS / frozen / smoke verified
```

References:
- `wiki/k6-freelancer/verification-m83.md`

---

## N-20260605-M84 Controlled Trial-use Observation Readiness

Status: PASS / FROZEN / STRUCTURE VERIFIED

Current baseline:
- Controlled trial-use observation scaffold is available.
- Markdown-native trial observation template: PASS.
- Lightweight structural checker: PASS.
- No automatic apply or orchestration introduced.
- The implementation remains personal-local, bounded, and human-reviewed.

Verified command:

```bash
bash ./bin/hermes-trial-observation-check <trial-record.md>
```

Verified scope:
- required-heading verification
- obvious secret-marker detection
- basic structural readiness validation

Final lock:

```text
M84 Controlled Trial-use Observation Readiness
PASS / frozen / structure verified
```

References:
- `wiki/k6-freelancer/verification-m84.md`
- `docs/trial-use-observation.md`
- `templates/trial-observation-record.md`

---

## N-20260605-M85 First Real Controlled Observation Trial

Status: PASS / FROZEN / POST-CHANGE VERIFIED

Current baseline:
- First real controlled observation trial completed.
- Trial candidate came from an actual M84 checker false-positive discovered during local verification.
- The false positive was fixed by narrowing secret detection from safety wording to likely secret values.
- Trial record captured the issue, human review, fix, and post-change verification.
- The implementation remains personal-local, bounded, and low-noise.

Verified command:

```bash
bash ./bin/hermes-trial-observation-check wiki/k6-freelancer/trials/trial-20260605-test.md
```

Verified result:

```json
{"status":"PASS","check":"trial-observation","file":"wiki/k6-freelancer/trials/trial-20260605-test.md","message":"Trial observation record structure is ready for human review."}
```

Final lock:

```text
M85 First Real Controlled Observation Trial
PASS / frozen / post-change verified
```

References:
- `wiki/k6-freelancer/verification-m85.md`
- `wiki/k6-freelancer/trials/trial-20260605-m84-checker-hotfix.md`
- `wiki/k6-freelancer/trials/trial-20260605-external-backend-boundary.md`

---

## N-20260605-M86 Trial-run Environment Isolation Baseline

Status: PASS / DESIGN READY / IMPLEMENTED

Current baseline:
- Developer checkout remains under `~/workspace/hermes-runes-md-wiki`.
- Realistic fresh-user trial-run should use `~/workspace-trial/hermes-runes-md-wiki`.
- Shared PostgreSQL Docker service is acceptable for P0 trial-run.
- Developer and trial-run runtime databases must be separate.
- `bin/hermes-memory-migrate` now prefers runtime DB configuration before falling back to the Docker stack default database.

Final lock:

```text
M86 Trial-run Environment Isolation Baseline
PASS / design ready / implemented
```

References:
- `wiki/k6-freelancer/verification-m86.md`
- `docs/trial-run-environment-isolation.md`

---

## N-20260605-M87 Keystone Trial-run Baseline

Status: PASS / KEYSTONE READY

Current baseline:
- Keystone baseline has been migrated to the current M86 state.
- Shared PostgreSQL Docker service remains unchanged.
- Trial-run creates only the separate `hermes_memory_trial` runtime database.
- Actual Hermes-agent trial-run is scoped only to `~/workspace-trial/hermes-runes-md-wiki`.
- Actual Hermes-agent must not access or reason from the developer checkout at `~/workspace/hermes-runes-md-wiki`.

Final lock:

```text
M87 Keystone Trial-run Baseline
PASS / keystone ready
```

References:
- `wiki/k6-freelancer/verification-m87.md`
- `docs/keystone-trial-run-baseline.md`

---

## N-20260605-M88 Fresh-user Trial Bootstrap Gap

Status: PARTIAL FIX / TRIAL FINDINGS RECORDED

Current findings:
- Fresh clone lacked dependency bootstrap before smoke; observed `ModuleNotFoundError: No module named 'psycopg'`.
- Full smoke then reached trial DB schema gap; observed `relation "public.chunks" does not exist`.
- Trial workspace expectation is `wiki/freelancer`, but cloned repo still contains development workspace `wiki/k6-freelancer`.
- `bin/hermes-memory-check` previously hardcoded `wiki/k6-freelancer` and `--project k6-freelancer`.

Implemented partial fixes:
- `bin/hermes-memory-check` now supports `HERMES_WORKSPACE_SLUG` / `HERMES_PROJECT`.
- `migrations/postgres/002_public_memory_schema.sql` adds fresh-user public memory tables.

Remaining gap:
- Dependency/bootstrap setup remains pending clean verification under M90.

Final lock:

```text
M88 Fresh-user Trial Bootstrap Gap
PARTIAL FIX / trial findings recorded
```

References:
- `wiki/k6-freelancer/verification-m88.md`
- `bin/hermes-memory-check`
- `migrations/postgres/002_public_memory_schema.sql`

---

## N-20260605-M89 Fresh-user Trial Smoke Hardening

Status: PASS / TRIAL SMOKE HARDENED / VERIFIED

Current baseline:
- Scoped import now includes `wiki/_system/**`, `wiki/owner-runes/**`, `wiki/freelancer/**`, and root-level `wiki/*.md`.
- Trial DB excludes legacy `wiki/k6-freelancer/**` and `wiki/sample-project/**` content.
- Core FTS smoke is workspace-aware.
- M5.2 evaluation smoke is workspace-aware.
- M10 observation smoke skips cleanly when model env is not configured.
- M11.6 sample-project smoke is workspace-aware.
- M20.4 promotion governance smoke skips cleanly when no trial promotion fixture exists.

Verified trial smoke chain:

```text
Core FTS                         PASS
M5.2 workspace evaluation         PASS
M10 observation log               SKIP / expected: missing model env
M11 observation summary           PASS
M11.6 workspace/sample smoke      PASS
M20.4 promotion governance        SKIP / expected: no trial fixture
```

Fixed trial bugs:

```text
TB-20260605-010 through TB-20260605-014
```

Final lock:

```text
M89 Fresh-user Trial Smoke Hardening
PASS / trial smoke hardened / verified
```

References:
- `wiki/k6-freelancer/verification-m89.md`
- `wiki/k6-freelancer/trial-bugs.md`

---

## N-20260605-M90 Fresh Clone Bootstrap Minimal Path

Status: PASS / BOOTSTRAP PATH ADDED / PENDING CLEAN VERIFICATION

Current baseline:
- `requirements-core.txt` defines the minimal fresh-clone runtime dependencies.
- `requirements-embedding.txt` remains optional for hybrid/vector/full-smoke support.
- `bin/hermes-memory-bootstrap` creates `tools/importer/.venv` and installs core dependencies by default.
- `bin/hermes-memory-bootstrap --with-embedding` installs CPU-only torch first, then optional embedding dependencies.
- Bootstrap does not touch Docker, secrets, migrations, imports, model endpoints, or runtime DB state.
- The implementation remains personal-local, bounded, and explicit.

Final lock:

```text
M90 Fresh Clone Bootstrap Minimal Path
PASS / bootstrap path added / pending local verification
```

References:
- `wiki/k6-freelancer/verification-m90.md`
- `docs/fresh-clone-bootstrap.md`
- `requirements-core.txt`
- `requirements-embedding.txt`
- `bin/hermes-memory-bootstrap`

---

## N-20260605-Realistic Fresh-user Trial-run

Status: IN PROGRESS / SMOKE HARDENED / BOOTSTRAP PATH ADDED

Current baseline:
- P0 governed memory operating baseline is frozen.
- External backend prerequisite handling is frozen and smoke verified.
- Controlled trial-use observation scaffold is frozen and verified.
- First real controlled observation trial is complete and post-change verified.
- Trial-run environment isolation baseline is design ready and implemented.
- Keystone trial-run baseline is ready.
- Fresh-user bootstrap gaps are recorded under M88.
- Fresh-user trial smoke hardening is complete under M89.
- Fresh clone bootstrap minimal path is added under M90.
- The system remains personal-local, Markdown-native, deterministic, and simple.

Recommended next phase:
- Pull M90 documentation updates into developer and trial clone.
- Run clean-clone verification for the M90 bootstrap path before beta test run.
- Keep shared PostgreSQL Docker stack unchanged.
- Keep trial DB isolated.
- Keep `HERMES_WORKSPACE_SLUG=freelancer` and `HERMES_PROJECT=freelancer` for trial-run.
- Introduce real trial promotion fixture only through a governed human-reviewed proposal flow.

Suggested trial continuation:
- verify M90 bounded bootstrap requirements without GPU/CUDA bloat by default
- verify clean clone setup from scratch
- keep model-dependent M10 smoke optional until a model endpoint is configured
- keep M20.4 promotion governance skipped until an approved trial fixture exists

---

## N-20260603-M50 Controlled Trial-run Governance

Status: HISTORICAL / SUPERSEDED BY N-20260605-M79-M82 P0 Baseline Convergence

Reference:
- `wiki/k6-freelancer/verification-m49.md`
