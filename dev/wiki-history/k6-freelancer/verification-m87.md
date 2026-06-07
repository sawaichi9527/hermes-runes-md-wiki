# M87 Keystone Trial-run Baseline

## Metadata

- Project: k6-freelancer
- Milestone: M87
- Status: PASS / KEYSTONE READY
- Date: 2026-06-05
- Scope: realistic fresh-user trial-run keystone boundary
- Verification type: baseline document + trial-run scope lock

---

## Summary

M87 establishes the keystone baseline immediately before the realistic fresh-user trial-run.

It records three hard requirements:

```text
1. migrate the keystone baseline to the current M86 state
2. do not modify docker-stacks/hermes-memory-postgres; create only the trial DB
3. during trial-run, the real Hermes-agent may use only ~/workspace-trial/hermes-runes-md-wiki and must not access or reason from ~/workspace/hermes-runes-md-wiki
```

---

## Implemented File

```text
docs/keystone-trial-run-baseline.md
```

---

## Keystone Requirement 1

Current baseline migrated to:

```text
M82 P0 governed memory operating baseline: PASS / frozen
M83 external backend boundary: PASS / frozen / smoke verified
M84 controlled trial-use observation readiness: PASS / frozen
M85 first real controlled observation trial: PASS / frozen / post-change verified
M86 trial-run environment isolation baseline: PASS / design ready / implemented
```

Next phase:

```text
Realistic Fresh-user Trial-run
```

---

## Keystone Requirement 2

Do not modify the shared PostgreSQL Docker stack:

```text
~/docker-stacks/hermes-memory-postgres
```

Allowed:

```text
verify existing service
connect to existing service
create separate trial DB only
```

Forbidden:

```text
change compose.yaml
change stack local runtime files
reset volumes
recreate containers
replace image
automatic backend repair or failover
```

Trial DB:

```text
hermes_memory_trial
```

Developer DB:

```text
hermes_memory
```

---

## Keystone Requirement 3

The real Hermes-agent trial-run scope is limited to:

```text
~/workspace-trial/hermes-runes-md-wiki
```

The real Hermes-agent must not access or reason from:

```text
~/workspace/hermes-runes-md-wiki
```

That developer checkout remains available only for maintainer / assistant-guided hotfix work outside the actual trial-run agent context.

---

## Governance Boundary

M87 does not introduce:

```text
automatic apply
automatic DB repair
hidden background worker
multi-service orchestration
trial artifact promotion
```

M87 preserves:

```text
personal-local scope
explicit backend prerequisite
developer / trial-run separation
single shared PostgreSQL service with separated runtime databases
human-controlled promotion
```

---

## Final Lock

```text
M87 Keystone Trial-run Baseline
PASS / keystone ready
```

The repository is ready for isolated realistic fresh-user trial-run preparation.
