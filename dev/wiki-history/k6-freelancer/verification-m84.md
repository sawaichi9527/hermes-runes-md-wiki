# M84 Controlled Trial-use Observation Readiness

## Metadata

- Project: k6-freelancer
- Milestone: M84
- Status: PASS / FROZEN / STRUCTURE VERIFIED
- Date: 2026-06-05
- Scope: post-P0 controlled trial-use observation readiness
- Verification type: documentation + template + lightweight structural checker

---

## Summary

M84 establishes the minimal scaffold for controlled real trial-use observation after the P0 governed operating baseline freeze.

The goal is not to automate memory apply or infrastructure management.

The goal is to provide:

- a small Markdown-native trial workflow
- a reusable trial record template
- a lightweight structural checker
- clear review gates
- a bounded observation path for one small real candidate at a time

This preserves the personal-local design boundary while preparing for real-world observation.

---

## Implemented Files

```text
docs/trial-use-observation.md
templates/trial-observation-record.md
bin/hermes-trial-observation-check
```

---

## Design Boundary

M84 intentionally does not introduce:

```text
automatic proposal apply
automatic wiki mutation
hidden background workers
enterprise orchestration
queue systems
retry pipelines
multi-user approval systems
HA infrastructure
automatic backend repair
```

The implementation remains:

```text
Markdown-native
personal-local
bounded
human-reviewed
simple
explicit
```

---

## Trial Workflow

The intended controlled flow is:

```text
one small real candidate
→ one source reference
→ one target Markdown path
→ one manual review
→ one manual record
→ one post-change verification pass
```

The workflow remains governed and human-reviewed.

---

## Trial Structural Check

M84 introduces:

```bash
bash ./bin/hermes-trial-observation-check <trial-record.md>
```

The checker intentionally performs only:

```text
required-heading verification
obvious secret-marker detection
basic structural readiness validation
```

It does not:

```text
approve proposals
apply changes
write wiki
import memory
mutate databases
perform backend repair
```

---

## Verification Assessment

```text
trial observation guide: PASS
trial observation template: PASS
lightweight structural checker: PASS
personal-local scope preserved: PASS
no enterprise orchestration introduced: PASS
```

---

## Final Lock

```text
M84 Controlled Trial-use Observation Readiness
PASS / frozen / structure verified
```

The repository now contains:

```text
P0 governed operating baseline
external backend prerequisite handling
simple backend guard
Hermes-owned schema migration
controlled trial-use observation scaffold
```

This is sufficient to begin the first real small-scale observation trial.
