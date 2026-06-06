# M150 Closed Beta Smoke Bundle

Status: PASS / CB SMOKE BUNDLE DEFINED / EXISTING CHECKS ONLY
Date: 2026-06-07

## Scope

M150 defines the minimal Closed Beta smoke bundle using existing checks and existing behavior.

This milestone intentionally avoids adding a new test framework or long-running automation layer.

## Bundle Principle

```text
Run the smallest useful set of checks before a CB session.
Prefer existing scripts.
Allow model-dependent checks to SKIP when the endpoint is not configured.
Do not block CB on optional model quality tests.
Do not mutate trusted memory except through explicitly human-approved proposal/promotion flow.
```

## Minimal CB Smoke Bundle

Developer checkout:

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status

python3 -m py_compile tools/importer/context_builder.py || true
python3 -m py_compile tools/runes_shield/*.py || true

./bin/hermes-memory-check
./bin/hermes-memory-smoke
```

Trial checkout:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short

export HERMES_WORKSPACE_SLUG=freelancer
export HERMES_PROJECT=freelancer

./bin/hermes-memory-check
./bin/hermes-memory-smoke
```

Observation readiness:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

bash ./bin/hermes-trial-observation-check <trial-record.md>
./bin/hermes-observe stats || true
```

Governed recall sample:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

./bin/hermes-recall "M140 agent-facing read-only trial verified" \
  --project freelancer \
  --limit 5 \
  --json
```

## Expected Outcome Classes

```text
PASS: required local and trial checks pass
SKIP: allowed for model-dependent checks when endpoint is intentionally unconfigured
WARN: allowed for optional observation logs when no CB session has produced records yet
FAIL: workspace boundary, trusted mutation boundary, missing core scripts, broken import/recall, or secret leakage
```

## What This Bundle Does Not Do

```text
does not create a proposal automatically
does not promote memory automatically
does not reset backend state
does not start a daemon
does not configure a model endpoint
does not run enterprise-scale tests
does not require OpenClaw or external runtime availability
```

## CB Smoke Interpretation

A CB session may begin when:

```text
core smoke passes
trial workspace smoke passes
model-dependent checks are either PASS or explicitly SKIP
observation record path is available
trusted mutation still requires human review
```

## Verification Commands

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status

grep -n "Status:\|M150\|CB SMOKE BUNDLE\|Minimal CB Smoke\|Expected Outcome\|does not" \
  wiki/k6-freelancer/verification-m150.md
```

## Final Lock

```text
M150 Closed Beta Smoke Bundle
PASS / CB smoke bundle defined / existing checks only
```
