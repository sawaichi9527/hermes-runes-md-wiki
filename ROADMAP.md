# Hermes Runes MD Wiki Roadmap

This roadmap captures the current direction for Hermes Runes MD Wiki as a governed personal RAG memory substrate and Hermes Agent integration target.

The roadmap is organized by priority:

```text
P0 = must be completed before trial run
P1 = follow-up improvements after trial feedback
P2 = mature / advanced improvements
```

Hermes Runes should remain a local-first, personal, governed memory substrate. It should not grow into an enterprise CMS, a distributed SaaS memory platform, or a second autonomous decision-making agent.

---

## Current Frozen Baselines

```text
M13   Retrieval Governance + Semantic Hybrid   PASS / frozen
M14.1 Context Assembly Diagnostics             PASS / frozen / observation-enabled
```

The M13/M14 retrieval core should not be disturbed by P0 wiki governance work unless a change is explicitly required and smoke verified.

---

## Core Boundary

Hermes Runes provides governed memory evidence and safe wiki operations.

Hermes Agent remains the decision-making layer.

```text
Hermes Runes does not decide truth for Hermes Agent.
Hermes Runes provides evidence, source metadata, source status, and operational safety.
Hermes Agent compares Runes evidence with native memory, third-party RAG/notes, web search, and current user instructions.
```

This boundary prevents Hermes Runes from becoming a second agent.

---

## Command Vocabulary

Rune-themed command names are allowed, but every term must have a plain-language explanation in documentation and CLI help.

| Rune term | Plain meaning | Scope |
|---|---|---|
| `decipher` | deterministic read | Read canonical policy, wiki guide, category indexes, objective README files, freshness status. |
| `forge` | governed write | Create, update, rename, archive, or otherwise mutate Markdown wiki source-of-truth. |
| `evoke` | recall / retrieve | Query indexed RAG memory. |
| `inscribe` | index / embed | Import Markdown source-of-truth into PostgreSQL / FTS / vector indexes. |
| `probe` | diagnose / check | Check retrieval, context, links, indexes, metadata, locks, policy, and consistency. |
| `chronicle` | change history | Record structural Markdown wiki changes, normally as an internal effect of `forge`. |

---

# P0 — Before Trial Run

P0 focuses on protection rails, not feature expansion.

Goal:

```text
Hermes Agent can safely use Hermes Runes without directly mutating wiki/ or confusing Runes evidence with final truth.
```

---

## P0.1 Self-describing System Policy Baseline

Create the canonical policy layer under:

```text
wiki/_system/
```

Required files:

```text
wiki/_system/README.md
wiki/_system/memory-policy.md
wiki/_system/source-priority.md
wiki/_system/access-boundary.md
wiki/_system/wiki-operation-policy.md
wiki/_system/agent-operation-guide.md
wiki/_system/ingestion-policy.md
wiki/_system/security-policy.md
wiki/_system/observation-policy.md
wiki/_system/developer-policy.md
wiki/_system/change-history.md
wiki/_system/operations.md
```

Purpose:

- Make Hermes Runes self-describing.
- Let Hermes Agent `decipher` current operation rules instead of relying only on hardcoded assumptions.
- Separate policy, wiki operation rules, source priority, security, observation, and developer exceptions.

Success criteria:

- `_system` policy bundle exists.
- Every rune command term has plain-language meaning.
- Hermes Agent boundary is documented.
- Runes evidence vs Hermes Agent judgment boundary is documented.

---

## P0.2 Agent Operation Guide

Create:

```text
wiki/_system/agent-operation-guide.md
```

Must define:

- when Hermes Agent should use `decipher`
- when Hermes Agent should use `forge`
- when Hermes Agent should use `evoke`
- when Hermes Agent should use `inscribe`
- when Hermes Agent should use `probe`
- when `chronicle` is written
- what must be approved by the user
- what can be automated but must be reported
- how native memory skill cache is allowed
- when freshness must be checked
- how Hermes Runes relates to third-party RAG / notes / Obsidian / web

Critical rule:

```text
Hermes Agent may learn Hermes Runes usage as a native-memory skill, but native memory is not the authority for Hermes Runes policy.
Before Runes operations, Hermes Agent must check policy freshness or decipher relevant guidance.
```

---

## P0.3 Source Priority and External Source Relationship

Create/update:

```text
wiki/_system/source-priority.md
```

Baseline source relationship:

```text
1. Current user instruction / current conversation
2. Hermes Agent native memory
   - runtime state / preferences / skill cache / recent working context
   - not canonical long-term truth
3. Hermes Runes MD Wiki
   - governed personal/project long-term memory evidence
4. Third-party RAG / third-party notes / Obsidian
   - auxiliary source, explicit-use source, comparison source, or import candidate
5. Web / external public sources
   - current/public/version-sensitive facts
```

Critical rule:

```text
Hermes Runes provides evidence and reliability metadata.
Hermes Agent performs source comparison and final answer judgment.
```

Hermes Runes should not silently override Obsidian / third-party RAG / web.

Third-party systems should not silently override Hermes Runes canonical memory.

The agent compares sources and explains conflicts when needed.

---

## P0.4 Wiki Operation Policy

Create:

```text
wiki/_system/wiki-operation-policy.md
```

Must define:

- structural change vs content update
- allowed and reserved `forge` operations
- path safety rules
- index consistency rules
- objective README contract
- category index contract
- change-history / chronicle contract
- approval boundary
- failure and recovery behavior

Structural changes include:

```text
create file
create objective namespace
create objective file
rename file
move file
archive file
delete file
promote flat file to objective namespace
split file
merge files
repair index relationship
```

Normal RAG reads do not update indexes or chronicle.

---

## P0.5 Wiki Layout and Knowledge Placement Guide

Create/update:

```text
wiki/README.md
wiki/long-term-objectives-index.md
wiki/specs-index.md
wiki/engineering-index.md
wiki/products-index.md
wiki/operations-index.md
wiki/references-index.md
wiki/personal-index.md
```

Purpose:

- Tell Hermes Agent how to place new knowledge.
- Decide between existing objective, new objective, flat-first file, or no Runes write.
- Define category index behavior.
- Define flat-first naming.
- Define objective promotion rules.

Baseline flat-first naming:

```text
wiki/<category>-<topic>-<note_type>.md
```

Baseline categories:

```text
specs
engineering
products
operations
references
personal
```

Hermes Agent should ask the user before creating:

- new objective namespace
- new flat-first memory file
- new objective file
- promoted objective structure

---

## P0.6 Markdown-native Metadata Format

P0 uses Markdown-native metadata sections, not YAML frontmatter.

Reason:

- lower RAG pollution risk
- no new parser required before trial
- compatible with current chunking / smoke tests
- human-readable in `vi` and grep
- can be migrated later if needed

Baseline file template:

```markdown
# <Title>

## Metadata

- Category: <specs|engineering|products|operations|references|personal>
- Topic: <topic-slug>
- Note type: <spec|requirements|design|decision|baseline|profile|runbook|troubleshooting|reference|preference|note>
- Status: <draft|active|superseded|archived>
- Memory quality: <verified|user-approved|agent-drafted|inferred|needs-review>
- Related objective: <none|objective-slug>
- Parent index: wiki/<category>-index.md
- Source type: <user-curated|hermes-agent-curated|external-summary|manual-note>
- Last reviewed: <YYYY-MM-DD>

## Summary

## Canonical Memory

## Evidence / Source Notes

## Open Questions

## Change Log
```

Rules:

- `Metadata` classifies the file.
- `Summary` helps relevance.
- `Canonical Memory` stores solidified long-term memory.
- `Evidence / Source Notes` records source context.
- `Open Questions` must not be treated as confirmed truth.
- `Change Log` records local file changes.

---

## P0.7 Objective README Contract

Every objective namespace must have:

```text
wiki/<objective-slug>/README.md
```

Required sections:

```markdown
# <Objective Name>

## Metadata

- Objective slug:
- Objective type:
- Status:
- Owner:
- Created:
- Last reviewed:

## Purpose

## Scope

## Files

## File Creation Rules

## Related Flat Files

## Change Log
```

Rules:

- Objective folders may contain additional purpose-specific Markdown files beyond the default lifecycle files.
- Adding a new objective file requires updating objective `README.md`.
- The new file must link back with `Related objective` and `Parent index` metadata.

---

## P0.8 Index Consistency Rule

Structural Markdown changes must update all affected indexes.

Affected files may include:

```text
wiki/long-term-objectives-index.md
wiki/<category>-index.md
wiki/<objective-slug>/README.md
wiki/_system/change-history.md
```

Examples:

| Operation | Required index updates |
|---|---|
| create flat file | category index |
| create objective | long-term objectives index |
| create objective file | objective README |
| rename file | all affected indexes and README references |
| archive/delete file | affected indexes, objective README, change-history |
| promote flat file to objective | category index, objective README, long-term objectives index |

---

## P0.9 Change History / Chronicle

Create:

```text
wiki/_system/change-history.md
```

Scope:

Records structural Markdown wiki changes only.

Record:

```text
CREATE_FILE
CREATE_OBJECTIVE
CREATE_OBJECTIVE_FILE
UPDATE_CONTENT
RENAME_FILE
MOVE_FILE
ARCHIVE_FILE
DELETE_FILE
PROMOTE_FILE
SPLIT_FILE
MERGE_FILE
RESTORE_FILE
PURGE_FILE
RESOLVE_CONFLICT
INDEX_REPAIR
POLICY_UPDATE
```

Do not record:

- normal RAG recall
- context build
- answer generation
- full prompt
- full context
- secrets

The latest chronicle entries are part of freshness checking.

---

## P0.10 Freshness Rule

Hermes Agent may cache operational skill in native memory.

Before Runes operations, it must verify freshness.

Conceptual commands:

```bash
hermes-runes decipher freshness
hermes-runes decipher chronicle-head
```

Freshness should expose:

```text
policy_bundle_version
policy_bundle_hash
latest_change_history_entry
needs_reload
```

P0 may document this before full implementation.

---

## P0.11 Forge P0 Boundary

P0 forge operations:

```text
create-flat
create-objective
create-objective-file
update-content
rename
archive
```

Every forge operation should eventually:

```text
ask user approval when required
acquire single-writer lock
validate path safety
stage changes
atomically replace files
update index / README relationships
append change-history
run inscribe as needed
run probe subset
report partial success / failure clearly
```

P1/P2 reserved operations:

```text
move
promote
restore
purge
resolve-conflict
split
merge
```

---

## P0.12 Probe P0 Boundary

P0 probe concepts:

```text
probe policy
probe indexes
probe links
probe objectives
probe metadata
probe lock
```

Minimum checks:

- required `_system` files exist
- category index paths exist
- objective README listed files exist
- `Related objective` exists
- `Parent index` exists
- `change-history.md` is readable
- no path escape / illegal path
- no obvious broken index relationship

---

## P0.13 Approval Boundary

Must ask user before:

- creating objective namespace
- creating new flat-first memory file
- creating new objective file
- changing draft to active
- renaming file
- archiving / deleting file
- promoting / moving / splitting / merging memory
- solidifying third-party RAG / Obsidian / web content into Hermes Runes
- resolving conflicting memory

May automate but must report:

- inscribe import
- embed-missing
- probe diagnostics
- append change-history
- repair obvious broken index entry, if policy allows

---

## P0.14 Evidence Output Boundary

`evoke` output should support evidence fields, not final judgment.

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
```

Runes should not output:

```text
recommended final answer
you should trust this source
```

Hermes Agent performs source comparison and final answer judgment.

---

# P1 — After Trial Feedback

P1 should improve correctness and safety based on real trial observations.

---

## P1.1 Policy Bundle Hash / Freshness Implementation

Implement:

```text
policy_bundle_version
policy_bundle_hash
latest_change_history_entry
needs_reload
```

Commands:

```bash
hermes-runes decipher freshness
hermes-runes decipher chronicle-head
```

Purpose:

- allow Hermes Agent native memory skill cache
- prevent stale operation policy use
- detect structural wiki changes before operation

---

## P1.2 Metadata Extraction

Parse Markdown-native metadata into retrievable document metadata.

Candidate fields:

```text
status
memory_quality
related_objective
source_type
last_reviewed
category
note_type
```

Storage may use PostgreSQL JSONB or dedicated fields.

Do not introduce YAML frontmatter unless justified later.

---

## P1.3 Source-status-aware Retrieval

Use metadata to support:

```text
active boost
verified / user-approved boost
draft warning
agent-drafted warning
superseded downrank
archived downrank
stale-risk warning
```

This remains evidence ranking, not final truth judgment.

---

## P1.4 Conflict Handling

Add policy and tool support for:

```text
probe conflicts
forge mark-superseded
forge resolve-conflict
```

Rules:

- if two active memories conflict, Runes should surface the conflict
- Hermes Agent must not silently merge conflicting memory into one answer
- conflict resolution requires user approval

---

## P1.5 Archive / Delete / Purge Separation

Define and optionally implement:

```text
archive = keep Markdown, lower priority
delete  = remove Markdown, retain change-history
purge   = remove Markdown + index + embeddings + sensitive references
```

Purge requires explicit confirmation and security policy handling.

---

## P1.6 Objective Promotion

Support:

```text
flat-first file → objective namespace
```

Promotion must update:

- category index
- long-term objectives index
- objective README
- source file status or movement
- change-history
- index lifecycle

---

## P1.7 Observation Summary Governance

Add observation review tooling that summarizes:

- common metadata hits
- missed retrievals
- repeated category confusion
- objective split candidates
- extraction quality issues
- Qwen forced-thinking contamination patterns

Observation remains:

```text
observe first, tune later
```

No automatic policy or heuristic mutation.

---

# P2 — Mature Improvements

P2 should be added only after P0/P1 have proven useful.

---

## P2.1 Split / Merge Automation

Support:

```text
large Markdown split
duplicate memory merge
section move
canonical memory extraction
```

Requires strong safeguards and user approval.

---

## P2.2 Redirects / Tombstones

Optional:

```text
wiki/_system/redirects.md
```

Purpose:

- old path → new path mapping
- rename history
- retrieval/reference repair

P0 uses `change-history.md` only.

---

## P2.3 Strong Metadata Schema / YAML Frontmatter

YAML frontmatter is deferred.

Only consider after:

- importer supports parsing
- chunker can exclude/downweight metadata
- smoke tests cover metadata behavior
- context builder handles metadata safely
- migration tooling exists

Until then, Markdown-native metadata remains preferred.

---

## P2.4 Advanced Source Reconciliation Support

Future Hermes Agent capability:

- compare Runes evidence
- compare Obsidian / third-party RAG
- compare web search
- compare current user instruction
- surface conflicts clearly

This remains Hermes Agent responsibility.

Runes should only provide standardized evidence fields.

---

## P2.5 Sensitive Data Classifier

Possible future tools:

```text
probe sensitivity
forge reject secret
forge warn confidential
```

P0 security policy already forbids real secrets in Markdown/git.

---

# Deferred / Not Recommended

Do not add before trial run:

- enterprise multi-user governance
- distributed cloud memory backend
- dashboard-first architecture
- OpenTelemetry / tracing stack
- automatic heuristic tuning
- automatic policy rewriting
- full LLM-as-judge faithfulness scoring
- YAML frontmatter migration
- autonomous split/merge without approval

---

# Trial Run Entry Criteria

Trial run can start when P0 documentation baseline is in place and the next implementation step is clear.

Minimum P0 documentation entry criteria:

```text
README.md updated with governance model
ROADMAP.md created
wiki/_system policy file list planned
wiki operation vocabulary documented
source priority and external RAG relationship documented
P0/P1/P2 scope documented
```

Minimum P0 tool entry criteria before letting Hermes Agent perform real structural writes:

```text
decipher policy/guide/freshness plan
forge P0 boundary
single-writer lock plan
index consistency plan
change-history plan
probe P0 consistency plan
```

---

# Guiding Rule

```text
Keep Hermes Runes simple enough for local personal RAG,
but governed enough that Hermes Agent cannot accidentally corrupt wiki source-of-truth.
```
