# M108.1 OpenAI-compatible Adapter Availability Check

Status: PASS / OPENAI-COMPATIBLE ADAPTER NOT CURRENTLY AVAILABLE
Date: 2026-06-06

## Purpose

M108.1 records the availability check for the OpenAI-compatible / API-facing adapter required by M108.

M108 has already created the smoke template, but actual execution requires a live OpenAI-compatible endpoint or wrapper path that can route API-style requests to Hermes-agent and Hermes Runes MD Wiki.

This milestone is an availability/status check only.

It does not change runtime behavior.

## Baseline Reference

Current M108 status:

```text
M108 OpenAI-compatible Adapter Trial Smoke
IMPLEMENTED / pending OpenAI-compatible adapter smoke
baseline commit: f86a1fa Add M108 OpenAI-compatible adapter trial smoke
```

## Check Scope

The operator checked:

```text
Developer repo state
Trial repo state
Repository files related to openai/compatible/api/server/wrapper/gateway
Listening local ports
Hermes gateway service status
```

Real secrets, tokens, and service credentials are intentionally not recorded in this file.

## Developer Repo Check

Developer repo:

```text
~/workspace/hermes-runes-md-wiki
```

Observed state:

```text
working tree clean
branch aligned with origin/main
latest commit: f86a1fa Add M108 OpenAI-compatible adapter trial smoke
M108 status: IMPLEMENTED / PENDING OPENAI-COMPATIBLE ADAPTER SMOKE
```

## Trial Repo Check

Trial repo:

```text
~/workspace-trial/hermes-runes-md-wiki
```

Observed state:

```text
working tree clean
branch aligned with origin/main
forge-inbox contains only wiki/freelancer/forge-inbox/m94-trial-promotion-fixture.md
```

This means the trial repo is clean and ready for a future M108 smoke, but it does not prove the API-facing adapter exists.

## Artifact Search Result

Repository search found historical/static wrapper-related artifacts, including:

```text
fixtures/m63/openai-compatible-wrapper-validation.json
fixtures/m63/generic-cli-wrapper-validation.json
fixtures/m65/wrapper-interpretation-regression.json
fixtures/m66/wrapper-drift-observation.json
tools/runes_shield/agent_profiles/generic-openai-agent.json
tools/runes_shield/smoke_m63_openai_compatible_wrapper_validation.py
tools/runes_shield/smoke_m63_generic_cli_wrapper_validation.py
tools/runes_shield/smoke_m65_wrapper_interpretation_regression.py
tools/runes_shield/smoke_m66_wrapper_drift_observation.py
```

Interpretation:

```text
These are historical/static validation artifacts and smoke scripts.
They do not prove a live OpenAI-compatible /v1/chat/completions adapter endpoint is currently running.
```

## Port / Service Observation

Observed listening endpoint:

```text
127.0.0.1:8088
```

Interpretation:

```text
This matches the local SearXNG service path, not a known OpenAI-compatible /v1/chat/completions adapter endpoint.
```

Hermes gateway service was active and running, but observed role was messaging platform integration, including Lark/RSS MCP style processes.

Interpretation:

```text
Hermes gateway is active.
It does not currently demonstrate a live OpenAI-compatible API endpoint for M108 smoke.
```

## Availability Decision

M108.1 availability decision:

```text
Live OpenAI-compatible adapter endpoint: NOT FOUND
Historical/static OpenAI-compatible wrapper artifacts: FOUND
M108 actual smoke execution: DEFERRED
M108 template status: KEEP IMPLEMENTED / PENDING
```

## Why M108 Cannot Be Marked PASS Yet

M108 cannot be marked PASS because:

```text
No live /v1/chat/completions style adapter endpoint was identified.
No API-facing request/response smoke was executed.
No four-prompt M108 API response set exists yet.
Only the post-smoke clean check precondition is currently satisfied.
```

## Safe Current State

The safe current state is:

```text
M108 template exists.
M108 execution is pending.
M108.1 availability check confirms no current live OpenAI-compatible endpoint.
No trial repo mutation occurred.
No secrets are recorded in wiki/git.
```

## Future Requirements Before M108 Execution

Before resuming M108 actual smoke, one of the following must exist:

```text
A live local OpenAI-compatible endpoint such as /v1/chat/completions.
A documented adapter command that routes API-style requests to Hermes-agent.
A wrapper process with clear host, port, path, and model routing behavior.
A safe test harness that does not expose real secrets to wiki/git.
```

## Suggested Next Step

Recommended next milestone:

```text
M108.2 OpenAI-compatible Adapter Bring-up Plan
```

Suggested purpose:

```text
Define the minimal local-only adapter bring-up requirements for a future /v1/chat/completions compatible Hermes-agent channel, without implementing enterprise server behavior.
```

Alternative next milestone:

```text
M110 Adapter Channel Governance Recap
```

Suggested purpose:

```text
Summarize frozen CLI, Lark, and generic CLI baselines, plus the deferred OpenAI-compatible adapter status, before broader P0 trial-run usage.
```

## Final Lock

```text
M108.1 OpenAI-compatible Adapter Availability Check
PASS / OpenAI-compatible adapter not currently available
```
