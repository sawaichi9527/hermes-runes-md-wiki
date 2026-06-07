# Beta-prep Model Endpoint Configuration Check

Status: ACTIVE / MODEL ENDPOINT CHECK READY
Date: 2026-06-06

## Purpose

This document defines the M136 beta-prep model endpoint configuration check.

The goal is to keep model-dependent smoke tests from blocking the beta-prep mainline when no local model endpoint is configured yet.

A missing model endpoint should be recorded as:

```text
SKIP / expected
```

not as a project failure.

## Added Checker

M136 adds:

```text
tools/importer/check_model_endpoint.py
bin/hermes-model-endpoint-check
```

The checker reads model endpoint settings from:

```text
tools/importer/.env
```

or from process environment variables.

It checks only whether the following are configured:

```text
OPENAI_BASE_URL
OPENAI_MODEL
OPENAI_AUTH_MODE
```

It does not print API keys.

It does not write files.

It does not import, index, apply, or promote memory.

## Expected Results

If model endpoint settings are missing:

```text
status: SKIP
expected: true
reason: OPENAI_BASE_URL and OPENAI_MODEL are required for model-dependent smoke.
```

If model endpoint settings are present:

```text
status: PASS
reason: model endpoint configuration present
```

If `--probe` is used and the endpoint probe fails:

```text
status: FAIL
```

The default check does not probe the network.

## Commands

Developer checkout:

```bash
cd ~/workspace/hermes-runes-md-wiki

bash ./bin/hermes-model-endpoint-check --json
```

Trial checkout:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

bash ./bin/hermes-model-endpoint-check --json
```

Optional endpoint probe when a local endpoint is expected to be running:

```bash
bash ./bin/hermes-model-endpoint-check --probe --json
```

## PASS / SKIP Interpretation

Acceptable beta-prep outcomes:

```text
PASS: model endpoint variables are configured.
SKIP / expected: model endpoint variables are not configured yet.
```

Blocking outcome:

```text
FAIL: invalid auth mode or configured endpoint probe failed.
```

## Mainline Relationship

M136 supports the M135 beta-prep mainline re-entry.

It verifies the first controllable gap:

```text
model endpoint configuration
```

It does not address the second gap:

```text
trial promotion fixture
```

That is reserved for M137.

## Personal-use Boundary

M136 remains:

```text
personal-local
simple
read-only
no secret output
no runtime mutation
no enterprise service dependency
no extra burden on Hermes-agent
```

## Final Lock

```text
Beta-prep Model Endpoint Configuration Check
ACTIVE / checker ready / SKIP expected when endpoint is absent
```
