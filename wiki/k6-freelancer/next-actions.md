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

## N-20260605-Realistic Fresh-user Trial-run

Status: NEXT / READY

Current baseline:
- P0 governed memory operating baseline is frozen.
- External backend prerequisite handling is frozen and smoke verified.
- Controlled trial-use observation scaffold is frozen and verified.
- First real controlled observation trial is complete and post-change verified.
- Trial-run environment isolation baseline is design ready and implemented.
- Keystone trial-run baseline is ready.
- The system remains personal-local, Markdown-native, deterministic, and simple.

Recommended next phase:
- Run a realistic fresh-user install trial from a separate trial clone.

Suggested trial:
- prepare isolated trial runtime database only
- do not modify shared PostgreSQL Docker stack
- clone into `~/workspace-trial/hermes-runes-md-wiki`
- configure trial runtime DB target
- run backend guard
- run schema migration twice
- run smoke / recall checks
- keep trial artifacts local unless explicitly promoted

---

## N-20260603-M50 Controlled Trial-run Governance

Status: HISTORICAL / SUPERSEDED BY N-20260605-M79-M82 P0 Baseline Convergence

Reference:
- `wiki/k6-freelancer/verification-m49.md`
