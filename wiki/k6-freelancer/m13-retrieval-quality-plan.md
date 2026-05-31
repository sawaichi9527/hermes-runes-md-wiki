# M13 Retrieval Quality & Context Stability Layer

Status: PLANNED / STARTED
Date: 2026-06-01
Scope: Retrieval quality and context stability improvements for Hermes Runes MD Wiki under the single-owner local multi-agent model.

---

## Design Boundary

M13 improves context quality for local RAG without introducing enterprise retrieval orchestration.

M13 must remain:

```text
local-first
single-owner
multi-agent-read friendly
deterministic
citation-preserving
non-LLM-compression-first
```

M13 must avoid:

```text
enterprise retrieval planner
multi-tenant ranking policy
LLM-as-judge evaluation platform
automatic memory mutation
opaque summarization of retrieved sources
```

---

## Motivation

Current retrieval works correctly, but smoke output can show the same source path multiple times, for example:

```text
wiki/sample-project/README.md
wiki/sample-project/README.md
```

This is not a correctness failure. It means chunk-level retrieval returned multiple chunks from the same Markdown file.

M13 should improve presentation and context stability by merging or capping same-path chunks when appropriate.

---

## Initial Scope

### M13.1 Same-path dedup / source cap

Goal:
- Prevent one source file from dominating context unless explicitly needed.

Policy:
- Default maximum chunks per source path: 2.
- Same-path chunks above the cap are skipped at context-build time.
- This is applied after retrieval and lightweight rerank.

### M13.2 Sibling chunk merge

Goal:
- Preserve information when adjacent chunks from the same Markdown source are both useful.

Policy:
- Adjacent chunks from the same path can be merged into a single context source block.
- Merged source blocks retain path, chunk ids, chunk indexes, heading, and citation metadata.
- Merge happens only inside the context builder, not in the database.

### M13.3 Context budget policy

Goal:
- Keep context size bounded and predictable for 2-4 local agent personas.

Policy:
- Respect global max context chars.
- Respect per chunk char truncation.
- Respect per source path cap.
- Prefer deterministic truncation over LLM-based compression.

### M13.6 Deterministic ordering / stable tie-break

Goal:
- Similar queries should produce stable context ordering for local multi-agent readers.

Policy:
- Sort by rerank score, hybrid score, path, chunk index, chunk id.
- Avoid relying on database return order for tie cases.

---

## Deferred Scope

### M13.4 Citation-preserving compression

Deferred until after M13.1-M13.3 are validated.

Potential future scope:
- Heading-aware trimming.
- Repeated boilerplate removal.
- Citation-preserving deterministic compression.

### M13.5 Retrieval eval extension

Deferred until stable context behavior is validated.

Potential future scope:
- Expected path checks.
- Expected heading checks.
- Same-path dedup checks.
- Stable ordering checks.

---

## Implementation Location

Initial M13 implementation should live in:

```text
tools/importer/context_builder.py
```

Reason:
- Context builder is the final assembly layer.
- It can improve context without changing retrieval scoring or database schema.
- It preserves existing hybrid search behavior while improving final prompt material.

---

## Result Target

M13 initial target:

```text
M13.1 same-path source cap: PASS
M13.2 adjacent sibling merge: PASS
M13.3 context budget policy: PASS
M13.6 deterministic ordering: PASS
```

M13 should remain compatible with all existing M12 smoke baselines.
