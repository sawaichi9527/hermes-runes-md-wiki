# M93 Model Env Minimal Beta Setting

Status: PASS / DEVELOPER MODEL ENV READY / TRIAL CLEAN SKIP VERIFIED
Date: 2026-06-06

## Purpose

M93 resolves the first controlled beta-prep gap recorded by M92: model environment setting.

The target is intentionally minimal:

```text
M10 observation smoke should PASS when a local OpenAI-compatible model endpoint is configured.
M10 observation smoke should remain a clean SKIP when no model endpoint is configured.
```

M93 does not make model availability mandatory for non-model smoke, backend checks, migration, import, or workspace validation.

## Scope

M93 remains:

```text
personal-local
bounded
explicit
non-enterprise
non-daemon
human-controlled
```

## Implemented Changes

### Safe local env example

Updated:

```text
tools/importer/.env.example
```

The example now documents:

```text
OPENAI_BASE_URL
OPENAI_MODEL
OPENAI_API_KEY
HERMES_WORKSPACE_SLUG
HERMES_PROJECT
```

Real `.env` files remain ignored by git and must stay local-only.

### M93 verifier

Added:

```text
tools/importer/smoke/eval_smoke_m93_model_env.py
```

The verifier:

```text
loads root .env and tools/importer/.env
checks required model env keys
validates OPENAI_BASE_URL structure
rejects obvious model-name placeholders
masks secret-like values in output
does not call the model endpoint
returns SKIP when env is absent
returns PASS when env is structurally ready
returns FAIL only for invalid configured env
```

### Command wrapper

Added:

```text
bin/hermes-model-env-check
```

Run with:

```bash
bash ./bin/hermes-model-env-check
```

The wrapper activates `tools/importer/.venv` when present and then runs the M93 verifier.

### Documentation

Added:

```text
docs/model-env-beta.md
```

The document records the local-only model env policy and expected verification behavior.

## Local Verification Result

Developer checkout:

```text
repo: /home/eye/workspace/hermes-runes-md-wiki
status: PASS
reason: model_env_ready
OPENAI_MODEL: qwen3.6-35B-A3B
```

Trial checkout:

```text
repo: /home/eye/workspace-trial/hermes-runes-md-wiki
status: SKIP
reason: missing_model_env
missing: OPENAI_BASE_URL, OPENAI_MODEL
```

This confirms the intended split:

```text
developer checkout can run model-dependent validation
trial checkout remains clean and non-blocking when model env is absent
```

## Expected Verification

Without local model env:

```text
status: SKIP
reason: missing_model_env
```

With local model env configured:

```text
status: PASS
reason: model_env_ready
```

Then M10 should move from expected SKIP to PASS when the configured endpoint is reachable:

```text
M10 Observation Log Smoke Test: PASS
```

## Boundaries

M93 does not introduce:

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
M93 Model Env Minimal Beta Setting
PASS / developer model env ready / trial clean skip verified
```
