# M93.5 M10 Thinking-model Smoke Token Budget

Status: PASS / LOCALLY VERIFIED
Date: 2026-06-06

## Purpose

M93.5 handles the remaining M10 smoke issue after M93.3 and M93.4.

After root/env resolution and Bearer auth were fixed, M10 reached the answer-generation path but failed because the local Qwen thinking model consumed the 512-token budget in `reasoning_content` and stopped with:

```text
finish_reason: length
```

This was a smoke-budget issue, not an auth or env issue.

## Implemented Change

Updated:

```text
tools/importer/smoke/eval_smoke_m10_observation.py
```

New smoke-local behavior:

```text
Default M10 smoke max tokens increased from 512 to 1536.
Local override is available through HERMES_M10_MAX_TOKENS.
The JSON output now reports max_tokens and finish_reason.
The subprocess timeout is increased from 120s to 180s.
```

This is intentionally limited to M10 smoke validation.

It does not change the global answer-generation defaults or introduce a model router.

## Local Verification Result

Developer checkout verification:

```text
repo: /home/eye/workspace/hermes-runes-md-wiki
M93 model env check: PASS / model_env_ready
M10 observation smoke: PASS
max_tokens: 1536
finish_reason: stop
selected_model_profile: qwen-forced-thinking
extraction_path: message.content
answer_chars: 57
issues: []
```

This confirms that the smoke-local token budget is sufficient for the current Qwen thinking-model path.

## Override

If a future local thinking model still stops with `finish_reason=length`, increase only the smoke override locally:

```bash
HERMES_M10_MAX_TOKENS=2048 python3 tools/importer/smoke/eval_smoke_m10_observation.py
```

## Boundaries

M93.5 does not introduce:

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
M93.5 M10 Thinking-model Smoke Token Budget
PASS / locally verified
```
