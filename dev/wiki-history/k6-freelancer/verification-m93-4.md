# M93.4 Local Model Auth Mode Minimal Fix

Status: PASS / BEARER AUTH VERIFIED
Date: 2026-06-06

## Purpose

M93.4 records the local model authentication fix discovered during M93.3 developer M10 smoke validation.

The goal is to keep local model auth explicit and simple without adding a model router, daemon, or enterprise-grade secret system.

## Observed Failure

After M93.3 fixed M10 checkout-local env resolution, M10 no longer skipped for missing model env.

It then failed at the real model endpoint boundary:

```text
HTTP Error 401: Unauthorized
```

Endpoint diagnosis showed:

```text
models_no_auth: HTTP 401
models_bearer: HTTP 401 with stale/invalid token
models_x_api_key: HTTP 401
```

After refreshing the LM Studio token and using Bearer auth:

```text
models_bearer: HTTP 200
```

## Implemented Change

Updated:

```text
tools/importer/answer_generator.py
```

Added local auth mode support:

```text
OPENAI_AUTH_MODE=auto
OPENAI_AUTH_MODE=none
OPENAI_AUTH_MODE=bearer
```

Behavior:

```text
auto   = send Bearer only when OPENAI_API_KEY is not a placeholder
none   = do not send Authorization header
bearer = always send Authorization: Bearer <OPENAI_API_KEY>
```

For the current LM Studio server, the verified local setting is:

```text
OPENAI_AUTH_MODE=bearer
```

## Local Verification Result

Verified endpoint:

```text
/models with Bearer token: HTTP 200
```

Verified environment:

```text
M93 model env check: PASS / model_env_ready
```

M10 progressed past the previous auth failure. The remaining M10 issue is not authentication; it is Qwen thinking-model output length behavior and is handled separately under M93.5.

## Secret Handling

Real API tokens and database passwords remain local-only and must not be committed to git or Markdown memory.

If a token is pasted into chat or logs, treat it as exposed and rotate it at the model server.

## Boundaries

M93.4 does not introduce:

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
M93.4 Local Model Auth Mode Minimal Fix
PASS / bearer auth verified
```
