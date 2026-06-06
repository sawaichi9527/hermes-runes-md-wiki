# M149 Model Endpoint Policy Decision

Status: PASS / POLICY DECIDED / MODEL ENDPOINT OPTIONAL FOR CB ENTRY
Date: 2026-06-07

## Scope

M149 decides the Closed Beta model endpoint policy.

This milestone does not configure a private model endpoint and does not write secrets, hostnames, tokens, ports, or local private values into the repository.

## Decision

```text
Closed Beta does not depend on a configured model endpoint as an entry blocker.
```

Reason:

```text
The trial-run scope validated governed memory behavior, proposal-first persistence, reviewed memory recall, and read-only agent-facing answer behavior.
The model endpoint affects answer quality and convenience, but it is not required to validate the governed memory control path.
```

## Policy

Model-backed runs are allowed during CB when a local/private endpoint is configured by the tester.

Model-backed runs are not required for CB entry when the session focuses on:

```text
workspace discovery
trial-root adherence
proposal-first behavior
human-review boundary
trusted memory mutation prevention
observation record creation
smoke bundle readiness
entry criteria validation
```

## Required Safety Boundary

```text
no private endpoint URL in wiki/git
no API key in wiki/git
no database password in wiki/git
no Telegram token in wiki/git
no model provider credential in wiki/git
no assumption that one tester's endpoint is a stable project resource
```

## Classification

```text
Model endpoint configured: optional enhancement for richer CB answer sessions
Model endpoint missing: allowed; model-dependent checks may SKIP
Model endpoint unstable: record as CB observation, not as core memory-path failure
Model endpoint secrets: remain in local .env / local secret storage only
```

## Practical CB Rule

```text
CB can start without a model endpoint.
A model endpoint should be treated as a local tester capability, not an enterprise resource.
Model-dependent answer quality findings should be labeled separately from governed memory path findings.
```

## Boundary Confirmation

```text
no new model router
no endpoint auto-discovery
no secret template with real values
no enterprise SLA requirement
no cloud dependency requirement
no model benchmark gate before CB entry
```

## Verification Commands

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status

grep -n "Status:\|M149\|MODEL ENDPOINT OPTIONAL\|Decision\|Policy\|Safety Boundary\|CB can start" \
  wiki/k6-freelancer/verification-m149.md
```

## Final Lock

```text
M149 Model Endpoint Policy Decision
PASS / policy decided / model endpoint optional for CB entry
```
