# M12.7 Release Boundary Decision

Status: PASS
Date: 2026-06-01
Scope: Release boundary and runtime access model for Hermes Runes MD Wiki after M12 repository readiness work.

---

## Decision

Hermes Runes MD Wiki is currently classified as:

```text
controlled-share baseline
```

It is technically stable enough for the owner to use, re-clone, test, and share with trusted collaborators, but it is not yet declared a full public open-source release.

---

## Runtime Assumption

Hermes Runes is designed for:

```text
single-owner / single-machine / local multi-agent read concurrency
```

This means:

- One human owner controls the machine and repository.
- Two to four local Hermes Agent personas may concurrently read from Hermes Runes.
- These local agent personas are treated as personas of the same owner, not separate security principals.
- The system does not introduce enterprise multi-user service boundaries.

---

## Supported Access Model

### Concurrent read access

Status: SUPPORTED

Allowed concurrent read-style operations:

```text
recall
FTS search
hybrid search
vector search
context build
governed answer generation
observation summary read
metadata inspection read
```

Rationale:
- PostgreSQL supports multiple local readers well.
- Local RAG usage may involve multiple Hermes Agent personas.
- Read concurrency is useful without adding enterprise service complexity.

### Single-writer governed mutation

Status: REQUIRED

Single-writer / governed operations:

```text
Markdown memory edits
importer runs
embedding refresh
stale purge --apply
future memory write workflows
retrieval profile mutation
configuration mutation
observation cleanup
Git commit / push operations
```

Rationale:
- Markdown remains the source-of-truth.
- Uncoordinated multi-agent writes can create conflicting edits, duplicate memories, memory pollution, and dirty Git state.
- Memory mutation should remain human-governed and auditable.

---

## Explicit Non-goals

Hermes Runes M12.7 does not introduce:

```text
multi-user SaaS
remote tenant isolation
enterprise RBAC
account system
admin dashboard
distributed lock service
background worker queue
multi-agent autonomous memory write
agent debate / planner / critic framework
LLM-as-judge evaluation platform
release automation
```

These are intentionally outside the current local-first personal RAG scope.

---

## Design Principle

```text
Hermes Runes supports local multi-agent read concurrency for one owner,
while keeping memory mutation single-writer and human-governed.
```

This preserves flexibility for 2-4 local Hermes Agent personas without turning the project into an enterprise multi-user platform.

---

## Release Boundary

Current public-readiness classification:

```text
Internal / controlled-share readiness: PASS
Full public open-source release readiness: DEFERRED
```

Deferred items:

```text
License selection
Release tag
Formal GitHub issue roadmap
CI workflow
Public release announcement
```

---

## Next Technical Work

The next technical track should be:

```text
M13 Retrieval Quality & Context Stability Layer
```

Recommended M13 scope:

```text
M13.1 same-path dedup
M13.2 sibling chunk merge
M13.3 context budget policy
M13.4 citation-preserving compression
M13.5 retrieval eval extension
M13.6 deterministic ordering / stable tie-break
```

M13 should improve retrieval quality and context stability for local multi-agent readers without introducing enterprise-scale orchestration.

---

## Next Integration Work

The next integration track should be:

```text
M14 Local Multi-Agent Read Access Layer
```

Recommended M14 scope:

```text
M14.1 read-only multi-agent access contract
M14.2 local tool contract for recall/context/answer
M14.3 single-writer maintenance lock
M14.4 Hermes Agent adapter MVP
M14.5 optional local memory service boundary
```

M14 should start read-only and add write capability only through curated, locked, human-governed workflows.

---

## Result

M12.7 Release Boundary Decision is considered:

```text
PASS
```

The repository is stable as a controlled-share baseline and ready to proceed into M13/M14 planning under the single-owner local multi-agent model.
