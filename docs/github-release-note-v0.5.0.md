# GitHub Release Note Draft - v0.5.0

## Title

Hermes Runes MD Wiki v0.5.0

## Tag

`v0.5.0`

## Summary

Hermes Runes MD Wiki v0.5.0 is the recommended Open Beta baseline for fresh public tester onboarding.

This release promotes the post-v0.3.0 runtime-readiness line after CPU embedding enablement, PostgreSQL / pgvector runtime validation, hybrid/vector recall restoration, fresh runtime smoke fixture alignment, and runtime CLI/tools surface cleanup.

## Highlights

- CPU-only embedding writer enabled for runtime use.
- PostgreSQL / pgvector backend verified.
- Hybrid and vector recall restored for the current runtime workspace.
- Fresh runtime smoke fixtures aligned to the `freelancer` workspace.
- Runtime support tools renamed to remove old milestone suffixes.
- Runtime CLI / tools surface cleaned:
  - user-facing wrappers remain under `bin/`
  - runtime/support tools remain under root `tools/`
  - development-only smoke, fixtures, regression, trial, and historical assets moved under `dev/`
- Security scan now resolves the current repository root.
- Final v0.5.0 release line verified and tagged.

## Accepted SKIP gates

The following SKIP gates are accepted for fresh runtime workspace evaluation:

- `TB-M1989-FS001`: local LLM endpoint unavailable for answer-generation smoke.
- `TB-M1989-FS002`: promotion governance fixture not present in fresh runtime workspace.
- `TB-M19810-RG001`: retrieval governance fixture not present in fresh runtime workspace.

## Quick verification

Run from a fresh checkout:

```bash
git fetch --tags
git checkout v0.5.0
cat VERSION
```

Expected version:

```text
0.5.0
```

Run the release smoke gate:

```bash
./bin/hermes-runes decipher freshness --json
./bin/hermes-runes probe policy --json
./bin/hermes-backend-check
./bin/hermes-memory-migrate
./bin/hermes-memory-security-scan
./bin/hermes-recall "forge inbox boundary" --project freelancer --mode hybrid --limit 5 --json
./bin/hermes-memory-smoke
./bin/hermes-retrieval-governance-smoke
```

Expected result:

- Main runtime checks should PASS.
- The accepted SKIP gates above may appear in a fresh runtime workspace.

## Boundary

This Open Beta release is intended for personal/local governed Markdown memory evaluation.

It is not:

- a production memory service
- an enterprise support commitment
- a multi-user SaaS platform
- an autonomous trusted memory writer

## Related documents

- `docs/open-beta-starter.md`
- `docs/v0.5.0-tester-checklist.md`
- `docs/v0.5.0-release-readiness.md`
- `CHANGELOG.md`
