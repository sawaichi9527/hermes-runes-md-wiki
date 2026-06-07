# Model Env Minimal Beta Setting

Status: M93 beta-prep helper

## Purpose

This document defines the minimal local model environment required for beta-prep model-dependent smoke validation.

The goal is intentionally small:

```text
M10 observation smoke should PASS when a local OpenAI-compatible model endpoint is configured.
M10 observation smoke should remain a clean SKIP when no model endpoint is configured.
```

This does not make model availability mandatory for normal memory, import, backend, or non-model smoke checks.

## Boundary

M93 remains:

```text
personal-local
bounded
explicit
non-enterprise
non-daemon
```

M93 does not introduce:

```text
no orchestration daemon
no model router
no secret manager
no enterprise telemetry
no automatic proposal apply
no direct wiki mutation by agent
```

## Local-only configuration

The repository provides only a safe example file:

```text
tools/importer/.env.example
```

Real local configuration must be copied to:

```text
tools/importer/.env
```

The real `.env` file is ignored by git and must not be committed.

## Minimal model variables

Required for M10 model-dependent smoke:

```text
OPENAI_BASE_URL=http://127.0.0.1:1234/v1
OPENAI_MODEL=your-local-model-name
```

Optional:

```text
OPENAI_API_KEY=not-needed
```

For local LM Studio or local OpenAI-compatible endpoints, `OPENAI_API_KEY=not-needed` is acceptable when the endpoint does not require authentication.

## Trial-run workspace variables

For clean beta-prep trial validation, keep:

```text
HERMES_WORKSPACE_SLUG=freelancer
HERMES_PROJECT=freelancer
```

## Verification commands

From the repository root:

```bash
bash ./bin/hermes-model-env-check
```

Expected when no local model env exists:

```text
status: SKIP
reason: missing_model_env
```

Expected after local model env is configured:

```text
status: PASS
reason: model_env_ready
```

Then run the model-dependent smoke:

```bash
bash ./bin/hermes-memory-smoke
```

Expected M10 result when the endpoint is configured and reachable:

```text
M10 Observation Log Smoke Test: PASS
```

## Notes

`hermes-model-env-check` does not call the model endpoint. It only verifies that the local environment is present and structurally sane.

`eval_smoke_m10_observation.py` remains the actual model-dependent smoke and performs the answer generation validation.
