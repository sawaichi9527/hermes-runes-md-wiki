# M136 Beta-prep Model Endpoint Configuration Check

Status: PASS / TRIAL VERIFIED / SKIP EXPECTED
Date: 2026-06-06

## Purpose

M136 adds a lightweight model endpoint configuration check for the beta-prep mainline.

This milestone supports M135 by checking the first controllable beta-prep gap:

```text
model endpoint configuration
```

M136 makes missing model endpoint configuration a clear:

```text
SKIP / expected
```

instead of a blocking failure.

## Added Artifacts

M136 adds:

```text
tools/importer/check_model_endpoint.py
bin/hermes-model-endpoint-check
docs/beta-prep-model-endpoint-check.md
```

## Checker Behavior

The checker reads local OpenAI-compatible endpoint settings from:

```text
tools/importer/.env
```

or from process environment variables.

It reports whether the base URL and model name are configured.

It does not print credential values.

It does not write files.

It does not import, index, apply, or promote memory.

## Expected Outcomes

Acceptable outcomes:

```text
PASS: model endpoint variables are configured.
SKIP / expected: model endpoint variables are not configured yet.
```

Blocking outcome:

```text
FAIL: invalid auth mode or configured endpoint probe failed.
```

The default check does not probe the network.

Endpoint probing is optional via:

```text
--probe
```

## Verification Commands

Developer checkout:

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status
python3 -m py_compile tools/importer/check_model_endpoint.py
bash ./bin/hermes-model-endpoint-check --json
```

Trial checkout:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short
python3 -m py_compile tools/importer/check_model_endpoint.py
bash ./bin/hermes-model-endpoint-check --json
```

## Observed Local Result

Developer checkout pull/status and artifact existence were verified.

The developer `py_compile` command was inconclusive because the Python command resolved the path under the trial workspace during execution. This appears to be an execution environment/path mix-up, not a checker source issue.

Trial checkout verification completed:

```text
python3 -m py_compile tools/importer/check_model_endpoint.py
bash ./bin/hermes-model-endpoint-check --json
```

Observed checker result:

```json
{
  "auth_header_would_be_sent": false,
  "auth_mode": "auto",
  "base_url_configured": false,
  "check": "model-endpoint",
  "env_file_exists": true,
  "expected": true,
  "model_configured": false,
  "probe_requested": false,
  "reason": "OPENAI_BASE_URL and OPENAI_MODEL are required for model-dependent smoke.",
  "status": "SKIP",
  "write": false
}
```

## Current Classification Rule

The checker reported SKIP with expected=true.

This is acceptable for beta-prep because model-dependent smoke is optional until a model endpoint is configured.

## Relationship To M137

M136 only covers model endpoint configuration.

The next controllable gap remains:

```text
trial promotion fixture
```

That is reserved for M137.

## Personal-use Boundary

M136 preserves the personal-local boundary.

It does not add:

```text
enterprise orchestration
websocket bridge
centralized policy service
enterprise telemetry system
automatic proposal apply
autonomous promotion
direct wiki mutation by runtime wrappers
```

It keeps the project:

```text
personal-local
simple
read-only
no credential output
no runtime mutation
no extra burden on Hermes-agent
```

## Verification Scope

Static and local verification scope:

```text
checker exists
wrapper exists
documentation exists
checker compiles in trial checkout
checker returns SKIP / expected
no credential output
no write/import/index/apply/promote behavior
M137 remains next controllable gap
```

## Final Lock

```text
M136 Beta-prep Model Endpoint Configuration Check
PASS / trial verified / SKIP expected
```
