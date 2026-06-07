# M93.1 Model Env Check Root Resolution Hardening

Status: PASS / LOCALLY VERIFIED
Date: 2026-06-06

## Purpose

M93.1 hardens the `bin/hermes-model-env-check` wrapper after local verification showed that a stale exported `HERMES_MEMORY_ROOT` could redirect the checker from the developer checkout to the trial checkout.

This is a wrapper-only hardening step.

It does not change:

```text
M10 observation smoke logic
M93 verifier logic
local .env policy
model endpoint policy
secret handling policy
```

## Observed Issue

When running from the developer checkout, the command attempted to load the M93 verifier from the trial checkout because the shell environment still contained:

```text
HERMES_MEMORY_ROOT=/home/eye/workspace-trial/hermes-runes-md-wiki
```

This caused the command to reference the wrong checkout.

## Implemented Change

Updated:

```text
bin/hermes-model-env-check
```

New behavior:

```text
Default root = repository checkout containing the wrapper.
Ignore stale HERMES_MEMORY_ROOT for this wrapper by default.
Use HERMES_MODEL_ENV_CHECK_ROOT only when an explicit override is needed.
Pass HERMES_MEMORY_ROOT to the Python verifier as a command-scoped value after resolving the intended root.
Fail early with a clear error if the M93 verifier is missing under the resolved root.
```

Explicit override example:

```bash
HERMES_MODEL_ENV_CHECK_ROOT=/path/to/repo bash ./bin/hermes-model-env-check
```

## Local Verification Result

Developer checkout:

```text
repo: /home/eye/workspace/hermes-runes-md-wiki
status: PASS
reason: model_env_ready
env_files path correctly points to developer checkout
```

Trial checkout:

```text
repo: /home/eye/workspace-trial/hermes-runes-md-wiki
status: SKIP
reason: missing_model_env
env_files path correctly points to trial checkout
```

This confirms that stale `HERMES_MEMORY_ROOT` no longer redirects the checker to the wrong clone.

## Expected Verification

From developer checkout:

```bash
cd ~/workspace/hermes-runes-md-wiki
bash ./bin/hermes-model-env-check
```

Expected with developer model env:

```text
status: PASS
reason: model_env_ready
```

From trial checkout:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki
bash ./bin/hermes-model-env-check
```

Expected without trial model env:

```text
status: SKIP
reason: missing_model_env
```

The `env_files` paths in the JSON output should match the checkout where the command is executed.

## Boundaries

M93.1 does not introduce:

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
M93.1 Model Env Check Root Resolution Hardening
PASS / locally verified
```
