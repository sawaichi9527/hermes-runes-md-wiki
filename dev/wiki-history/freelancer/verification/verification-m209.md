# M209 Hermes-agent Onboarding Smoke / Read-only Trial Lock

Status: PASS candidate / local validation required
Version line: 0.7.1-dev
Date: 2026-06-08

## Scope

M209 converts the Hermes-agent onboarding prompt into a reusable read-only smoke target.

The smoke validates repository readiness for Hermes-agent onboarding without:

- starting Hermes-agent
- modifying trusted Markdown memory
- modifying `_system/` policy
- touching PostgreSQL
- promoting or mutating proposals

## Starting state

Confirmed before M209:

- M208 added the Hermes-agent onboarding prompt to `docs/fresh-install-manual.md`.
- `VERSION` is `0.7.1-dev`.
- backend check PASS.
- FTS recall PASS.
- core smoke PASS.
- embedding profile skip accepted for core profile.

## Added files

- `tools/runes_shield/smoke_agent_onboarding_readonly.py`
- `bin/hermes-agent-onboarding-smoke`

## Updated files

- `docs/fresh-install-manual.md`

## Validation commands

```bash
python3 -m py_compile tools/runes_shield/smoke_agent_onboarding_readonly.py
./bin/hermes-agent-onboarding-smoke
git diff --check
```

## Expected behavior

The smoke should return:

```json
{
  "suite": "M209 Hermes-agent Onboarding Read-only Smoke",
  "status": "PASS",
  "write": false,
  "mutates_trusted_memory": false,
  "starts_agent": false,
  "touches_database": false
}
```

## Result

Pending local validation / commit.
