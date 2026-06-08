# GitHub Release Note Draft - v0.7.0

Release title:

```text
Hermes Runes MD Wiki v0.7.0
```

Tag:

```text
v0.7.0
```

## Summary

Hermes Runes MD Wiki v0.7.0 advances the Open Beta baseline with a verified fresh-install core path.

This release focuses on fresh public tester onboarding, PostgreSQL / pgvector setup clarity, clean reinstall safety, and tooling defaults that work without manual runtime overrides.

## Highlights

- Fresh-install manual consolidated and hardened.
- PostgreSQL / pgvector stack initialization flow documented and validated.
- Strict clean reinstall reset path added.
- PostgreSQL data removal separated from repository / venv removal.
- Docker CE and normal-user Docker access checks added.
- Local port 5433 preflight added.
- Backend check aligned with fresh-install stack defaults.
- Import wrapper no longer points to the old `~/workspace/hermes-memory` path.
- Core FTS smoke no longer false-fails against `sample-project` during fresh install.
- Fresh-install core path verified without `HERMES_MEMORY_ROOT` or `HERMES_SMOKE_*` workarounds.

## Recommended checkout

```bash
git clone https://github.com/sawaichi9527/hermes-runes-md-wiki.git
cd hermes-runes-md-wiki
git checkout v0.7.0
cat VERSION
```

Expected:

```text
0.7.0
```

## Validation gate

```bash
./bin/hermes-backend-check
./bin/hermes-memory-migrate
./bin/hermes-memory-import
./bin/hermes-recall "forge inbox boundary" --project freelancer --mode fts --limit 5 --json
./bin/hermes-memory-smoke
```

Expected:

- backend check PASS
- migration PASS
- import PASS
- FTS recall PASS
- core smoke PASS

## Accepted skips

The core fresh-install profile does not require embedding dependencies or a local LLM endpoint.

This message is accepted:

```text
Embedding profile not installed: skipping hybrid and answer-generation smoke suites
```

Install embedding dependencies only when testing hybrid/vector/answer-generation paths.

## Open Beta boundary

This release remains personal/local Open Beta software.

It is not a production service, hosted platform, enterprise orchestration system, or autonomous trusted memory writer.

## Primary documents

- `README.md`
- `docs/open-beta-starter.md`
- `docs/fresh-install-manual.md`
- `docs/v0.7.0-tester-checklist.md`
- `docs/v0.7.0-release-readiness.md`
