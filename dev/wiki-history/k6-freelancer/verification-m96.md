# M96 Controlled Trial-run Execution Pack

Status: PASS / LOCALLY VERIFIED
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

## Developer Local Verification Result

Developer checkout verification:

```text
repo: /home/eye/workspace/hermes-runes-md-wiki
head: e73cff4 Add M96 controlled trial run execution pack
working tree: clean
```

Compile checks completed:

```text
python3 -m py_compile tools/importer/answer_generator.py
python3 -m py_compile tools/importer/smoke/eval_smoke_m10_observation.py
python3 -m py_compile tools/importer/promotion_governance_smoke.py
```

Model env check:

```text
suite: M93 Model Env Minimal Beta Setting
status: PASS
reason: model_env_ready
OPENAI_BASE_URL: configured
OPENAI_MODEL: qwen3.6-35B-A3B
OPENAI_API_KEY: set
```

M10 smoke result:

```text
suite: M10 Observation Log Smoke Test
profile: workspace-freelancer
status: PASS
issues: []
max_tokens: 1536
selected_model_profile: qwen-forced-thinking
extraction_path: message.content
finish_reason: stop
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

## Trial Local Verification Result

Trial checkout verification:

```text
repo: /home/eye/workspace-trial/hermes-runes-md-wiki
head: e73cff4 Add M96 controlled trial run execution pack
working tree: clean
```

Compile checks completed:

```text
python3 -m py_compile tools/importer/smoke/eval_smoke_m10_observation.py
python3 -m py_compile tools/importer/promotion_governance_smoke.py
```

Importer result:

```text
schema: public
import_scope: freelancer
M94 fixture path: skipped id=59 chunks=0 after prior import
imported_or_changed: 0
updated: 0
skipped: 59
chunks_written: 0
PASS: Markdown incremental import completed
```

M20.4 smoke result:

```text
suite: M20.4 Promotion Governance Smoke
profile: workspace-freelancer
status: PASS
failed: 0
total: 1
id: M20.4-TRIAL-A
summary: approved reviewed trial promotion fixture is retrieval-visible
path: wiki/freelancer/forge-inbox/m94-trial-promotion-fixture.md
trust_bias: 0
```

Forge metadata verified:

```text
status: approved
trust_class: reviewed
proposal_type: agent_memory
proposed_by: human
provenance: manual_cli
operation_id: M94-trial-promotion-fixture-20260606
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

M96 is marked PASS because:

```text
Developer command pack ran to expected PASS state.
Trial command pack ran to expected PASS state.
Both checkouts were clean and synced.
No secrets were committed.
M20.4 trial fixture remained retrieval-visible.
```

## Final Lock

```text
M96 Controlled Trial-run Execution Pack
PASS / locally verified
```
