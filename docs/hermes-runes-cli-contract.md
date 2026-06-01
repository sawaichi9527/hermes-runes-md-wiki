# Hermes Runes CLI Contract

Status: M15.2 draft contract  
Scope: planned command vocabulary and operation boundaries

## Purpose

This document defines the planned Hermes Runes command interface before implementation.

The goal is to keep Hermes Agent integration clean:

```text
Hermes Agent reads policy and asks the user.
Hermes Runes tools perform controlled wiki/RAG/index operations.
```

This file is a contract, not a complete implementation.

## Command Families

| Command family | Plain meaning | Primary layer |
|---|---|---|
| `decipher` | deterministic read | wiki policy / guide / index read layer |
| `forge` | governed write | wiki Markdown source-of-truth mutation layer |
| `evoke` | recall / retrieve | RAG recall layer |
| `inscribe` | import / embed / index | index lifecycle layer |
| `probe` | diagnose / check | diagnostics / consistency layer |
| `chronicle` | change history | structural history, usually internal to `forge` |

## Non-goal

The CLI should not turn Hermes Runes into a second autonomous agent.

Hermes Runes provides evidence and safe operations.

Hermes Agent performs final judgment.

---

# `decipher`

## Purpose

Read canonical wiki policy, guide, index, objective README, and freshness information deterministically.

This is not semantic RAG search.

## Planned commands

```bash
hermes-runes decipher policy
hermes-runes decipher guide
hermes-runes decipher indexes
hermes-runes decipher objective <objective-slug>
hermes-runes decipher freshness
hermes-runes decipher chronicle-head
```

## Output expectations

Should support human output and JSON output.

JSON should include:

```text
status
files
policy_bundle_version
policy_bundle_hash
latest_change_history_entry
needs_reload
content or summary
```

## Boundary

`decipher` is read-only.

It does not update Markdown, indexes, embeddings, or change-history.

---

# `forge`

## Purpose

Perform governed Markdown source-of-truth mutations.

## P0 planned operations

```bash
hermes-runes forge create-flat
hermes-runes forge create-objective
hermes-runes forge create-objective-file
hermes-runes forge update-content
hermes-runes forge rename
hermes-runes forge archive
```

## Reserved operations

```bash
hermes-runes forge move
hermes-runes forge promote
hermes-runes forge restore
hermes-runes forge purge
hermes-runes forge resolve-conflict
hermes-runes forge split
hermes-runes forge merge
```

## P0 operation expectations

Every structural `forge` should eventually:

```text
validate path
acquire single-writer lock
stage writes
atomically replace files where practical
update affected category index / objective README
append change-history
run inscribe as needed
run probe subset
report partial success/failure
```

## Output expectations

JSON should include:

```text
status
operation
paths_changed
indexes_updated
change_history_entry
inscribe_status
probe_status
warnings
recovery_hint
```

## Boundary

`forge` is the only planned structural wiki write interface.

Hermes Agent should not freely edit wiki structure outside `forge`.

---

# `evoke`

## Purpose

Recall indexed personal RAG memory.

`evoke` is the rune-themed alias for recall.

## Planned commands

```bash
hermes-runes evoke "query"
hermes-runes evoke "query" --project <project>
hermes-runes evoke "query" --mode hybrid --json
```

`hermes-recall` may remain as an engineering alias or compatibility wrapper.

## Output expectations

`evoke` should provide evidence, not final judgment.

Target evidence fields:

```text
path
heading
status
memory_quality
source_type
last_reviewed
related_objective
retrieval_score
rerank_score
warning_flags
content_preview
```

## Boundary

`evoke` does not mutate Markdown.

`evoke` does not decide final answer truth.

Hermes Agent compares Runes evidence with other sources.

---

# `inscribe`

## Purpose

Import and embed Markdown source-of-truth into derived search indexes.

## Planned commands

```bash
hermes-runes inscribe import
hermes-runes inscribe embed-missing
hermes-runes inscribe refresh
hermes-runes inscribe status
```

## Boundary

`inscribe` updates derived index state.

It should not be treated as canonical memory writing.

Markdown remains source-of-truth.

`forge` may call `inscribe` after structural or content writes.

Developers may also call `inscribe` directly for verification.

---

# `probe`

## Purpose

Diagnose retrieval, context, wiki consistency, metadata, links, locks, and policy health.

## P0 planned probes

```bash
hermes-runes probe policy
hermes-runes probe indexes
hermes-runes probe links
hermes-runes probe objectives
hermes-runes probe metadata
hermes-runes probe lock
hermes-runes probe retrieval
hermes-runes probe context
```

## Output expectations

JSON should include:

```text
status
issues
warnings
checked_files
broken_links
missing_indexes
missing_objectives
recovery_hint
```

## Boundary

`probe` is normally read-only.

If future auto-repair is added, it should be separate from normal probe and require policy approval.

---

# `chronicle`

## Purpose

Record structural Markdown wiki changes.

P0 direction:

```text
chronicle is normally internal to forge
```

Direct manual chronicle commands are not required for P0.

Change records live in:

```text
wiki/_system/change-history.md
```

## Boundary

Normal RAG recall, context build, and answer generation do not write chronicle entries.

---

# Implementation Notes

P0 should prefer simple local tooling:

- Python CLI
- file-based lock
- staged writes
- atomic replace where practical
- human-readable JSON outputs
- no daemon required
- no enterprise workflow engine

## Change Log

- 2026-06-01: Initial M15.2 CLI contract draft.
