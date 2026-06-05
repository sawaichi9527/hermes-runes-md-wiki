# M93.3 Developer M10 Model Smoke Verification

Status: HOTFIX IMPLEMENTED / PENDING LOCAL VERIFICATION
Date: 2026-06-06

## Purpose

M93.3 attempts to verify that developer checkout M10 observation smoke can move from clean SKIP to PASS when model env is configured.

Initial local execution showed:

```text
M93 model env check: PASS / model_env_ready
M10 observation smoke: SKIP / missing_model_env
```

This exposed an env/root-resolution mismatch between the M93 checker and direct M10 smoke execution.

## Observed Gap

The developer checkout had model env configured:

```text
OPENAI_BASE_URL: configured
OPENAI_MODEL: qwen3.6-35B-A3B
OPENAI_API_KEY: set
```

But `tools/importer/smoke/eval_smoke_m10_observation.py` still reported:

```text
status: SKIP
reason: missing_model_env
missing: OPENAI_BASE_URL, OPENAI_MODEL
```

This indicated that M10 was not resolving the same checkout-local env as M93.

## Implemented Hotfix

Updated:

```text
tools/importer/smoke/eval_smoke_m10_observation.py
```

New behavior:

```text
M10 smoke defaults to the repository checkout containing the script.
M10 no longer relies on stale exported HERMES_MEMORY_ROOT by default.
Use HERMES_M10_SMOKE_ROOT only for explicit override.
M10 reports root, importer, env_files, and loaded_keys in JSON output.
```

This aligns M10 smoke with the M93 checker root behavior while keeping the implementation simple and local-only.

## Expected Verification

From developer checkout:

```bash
cd ~/workspace/hermes-runes-md-wiki
bash ./bin/hermes-model-env-check
python3 tools/importer/smoke/eval_smoke_m10_observation.py
```

Expected first command:

```text
status: PASS
reason: model_env_ready
```

Expected second command after this hotfix:

```text
M10 should no longer SKIP because of missing_model_env when developer .env is configured.
```

If the endpoint and answer generation are healthy, M10 should return:

```text
status: PASS
```

If M10 returns FAIL, the failure should now represent a real endpoint, answer generation, citation, or observation issue rather than env-root mismatch.

## Trial Behavior

Trial checkout may remain:

```text
status: SKIP
reason: missing_model_env
```

This remains expected until trial model env is explicitly configured.

## Boundaries

M93.3 does not introduce:

```text
no orchestration daemon
no model router
no secret manager
no enterprise telemetry
no automatic proposal apply
no direct wiki mutation by agent
no runtime authority escalation
```

## Final Lock

```text
M93.3 Developer M10 Model Smoke Verification
HOTFIX IMPLEMENTED / pending local verification
```
