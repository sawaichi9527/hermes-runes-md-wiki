# M96 Controlled Trial-run Execution Pack

Status: IMPLEMENTED / PENDING LOCAL VERIFICATION
Date: 2026-06-06

## Purpose

M96 defines the manual execution pack for the controlled trial-run stage after M95 beta-prep readiness closure.

This milestone is documentation-only.

It does not add runtime behavior, background services, automatic apply behavior, or new fixture data.

## Scope

M96 covers:

```text
developer checkout command pack
trial checkout command pack
expected PASS / SKIP outputs
basic failure triage notes
operator-driven execution boundary
```

M96 does not replace the existing smoke scripts. It records a stable command sequence so controlled trial-run execution is repeatable.

## Preconditions

Expected repository state:

```text
M95 Beta-prep Closure / Trial-run Readiness Lock: PASS
Developer checkout clean and synced
Trial checkout clean and synced
Trial checkout uses HERMES_WORKSPACE_SLUG=freelancer
Trial checkout uses HERMES_PROJECT=freelancer
Trial database remains isolated
Real secrets remain local-only in .env
```

## Developer Checkout Command Pack

Use the developer checkout for model-dependent and repo-authoring verification.

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status
git log --oneline -8

python3 -m py_compile tools/importer/answer_generator.py
python3 -m py_compile tools/importer/smoke/eval_smoke_m10_observation.py
python3 -m py_compile tools/importer/promotion_governance_smoke.py

bash ./bin/hermes-model-env-check
python3 tools/importer/smoke/eval_smoke_m10_observation.py
```

Expected developer results:

```text
git status: clean
M93 model env check: PASS / model_env_ready
M10 observation smoke: PASS
M10 max_tokens: 1536
M10 finish_reason: stop
```

Developer notes:

```text
If M93 model env check fails, inspect tools/importer/.env locally.
If M10 returns 401, refresh the local model server token and keep OPENAI_AUTH_MODE=bearer.
If M10 returns finish_reason=length, try HERMES_M10_MAX_TOKENS=2048 for smoke verification only.
Do not commit .env.
```

## Trial Checkout Command Pack

Use the trial checkout for isolated trial workspace verification.

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status
git log --oneline -8

python3 -m py_compile tools/importer/smoke/eval_smoke_m10_observation.py
python3 -m py_compile tools/importer/promotion_governance_smoke.py

bash ./bin/hermes-memory-import
python3 tools/importer/promotion_governance_smoke.py
```

Expected trial results:

```text
git status: clean
import_scope: freelancer
M94 fixture path imported or skipped if already indexed
M20.4 Promotion Governance Smoke: PASS
profile: workspace-freelancer
id: M20.4-TRIAL-A
summary: approved reviewed trial promotion fixture is retrieval-visible
```

Trial notes:

```text
If M20.4 returns SKIP, confirm wiki/freelancer/forge-inbox/m94-trial-promotion-fixture.md exists.
If the fixture exists but M20.4 still SKIPs, rerun bash ./bin/hermes-memory-import.
If import does not include the fixture, confirm HERMES_WORKSPACE_SLUG=freelancer and HERMES_PROJECT=freelancer.
If M20.4 returns FAIL, inspect forge metadata on the retrieved result.
```

## Optional Full Trial Smoke

After the focused checks pass, the operator may run the existing full smoke entrypoint:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki
bash ./bin/hermes-memory-smoke
```

Expected controlled-trial behavior:

```text
Core non-model checks: PASS
M20.4 promotion governance: PASS when fixture is imported
Model-dependent checks: PASS only if trial model env is configured, otherwise clean SKIP where applicable
```

## Controlled Boundary

This execution pack is intentionally manual and bounded:

```text
operator starts each command
local .env remains outside git
fixture is human-reviewed
smoke output is inspected by operator
no production deployment is implied
```

Out of scope:

```text
background orchestration
automatic proposal application
unattended workflow execution
enterprise telemetry expansion
runtime permission expansion
```

## Completion Criteria

M96 can be marked PASS when:

```text
Developer command pack runs to expected PASS state.
Trial command pack runs to expected PASS state.
Both checkouts are clean and synced.
No secrets are committed.
M20.4 trial fixture remains retrieval-visible.
```

## Final Lock

```text
M96 Controlled Trial-run Execution Pack
IMPLEMENTED / pending local verification
```
