# Trial Observation Record: External Backend Boundary

## Metadata

- Trial ID: trial-20260605-external-backend-boundary
- Date: 2026-06-05
- Project: k6-freelancer
- Status: PASS / manually reviewed / post-change verified
- Scope: personal-local controlled trial-use observation
- Candidate type: baseline
- Source type: current implementation verification and user-approved design discussion
- Target Markdown path: wiki/k6-freelancer/verification-m83.md
- Review owner: human

---

## Candidate Summary

This trial observes one small real project-memory candidate: the external backend boundary for Hermes Runes MD Wiki.

The PostgreSQL / pgvector Docker service remains an external prerequisite. Hermes Runes MD Wiki owns backend guard, Hermes schema migration, importer / recall verification, and governed Markdown memory workflows.

Hermes-agent should verify and report backend state, but it should not become a PostgreSQL / Docker infrastructure operator.

---

## Source Reference

Source references:

```text
AGENTS.md
docs/reference-postgres-backend.md
QUICKSTART.md
wiki/k6-freelancer/verification-m83.md
observed command output from Freelancer host backend guard and migration verification
```

No secrets, `.env` contents, database passwords, API keys, or local credentials are included.

---

## Target Markdown Path

Target already recorded:

```text
wiki/k6-freelancer/verification-m83.md
```

This trial does not require creating a new workspace.

---

## Proposed Memory Content

Canonical candidate:

```text
Hermes Runes MD Wiki treats PostgreSQL / pgvector as the P0 reference memory backend, but the PostgreSQL Docker service lifecycle remains external to the core repository install flow.

The repository provides a simple backend guard and Hermes-owned schema migration entrypoint. Agents must verify the backend before DB-dependent operations, run Hermes-owned migrations from the repository, and fail safely if the backend is unavailable.

Agents must not automatically repair, reset, recreate, or replace the backend. The design remains personal-local, bounded, and non-enterprise.
```

---

## Governance Checks

- [x] Candidate is small and bounded.
- [x] Source reference is known.
- [x] No secrets are included.
- [x] Target path is explicit.
- [x] Existing workspace status is checked.
- [x] Direct wiki mutation is not performed without governed approval.
- [x] Backend guard is PASS before import / recall / smoke.
- [x] Manual human review is required before final apply.

---

## Manual Review

Human review decision:

```text
approved
```

Reviewer notes:

```text
The candidate reflects the M83 verified implementation boundary and matches the intended personal-local scope.
```

---

## Manual Record

Recorded apply:

```text
No hidden automatic apply was performed.
The canonical boundary was already recorded in wiki/k6-freelancer/verification-m83.md.
This trial record observes and confirms that the verified M83 memory candidate can be represented through the controlled trial-use observation scaffold.
```

Applied evidence:

```text
- target file changed: wiki/k6-freelancer/verification-m83.md already exists
- summary of change: external backend prerequisite boundary and simple backend guard verified
- method: prior governed documentation + verification lock, followed by controlled observation record
- timestamp: 2026-06-05
```

---

## Post-change Verification

Relevant observed checks:

```bash
bash ./bin/hermes-backend-check
bash ./bin/hermes-memory-migrate
bash ./bin/hermes-memory-migrate
bash ./bin/hermes-trial-observation-check wiki/k6-freelancer/trials/trial-20260605-test.md
```

Observed results:

```text
backend guard: PASS
first migration: PASS / applied: 1 / skipped: 0
second migration: PASS / applied: 0 / skipped: 1
trial observation structural checker: PASS after false-positive hotfix
```

This real trial record should also pass:

```bash
bash ./bin/hermes-trial-observation-check wiki/k6-freelancer/trials/trial-20260605-external-backend-boundary.md
```

---

## Observation Notes

Observed learning:

```text
The trial observation scaffold is usable for a small real memory candidate.
The first structural checker was too noisy because it matched safety guidance words such as PostgreSQL passwords and Telegram tokens.
The checker was improved to detect likely secret values instead of secret-related documentation wording.
This keeps the tool simple and low-noise while preserving human review.
```

The controlled observation path remains lightweight and does not introduce automatic apply, background workers, or enterprise orchestration.

---

## Final Status

```text
PASS
```

Final lock:

```text
Trial trial-20260605-external-backend-boundary
PASS / manually reviewed / post-change verified
```
