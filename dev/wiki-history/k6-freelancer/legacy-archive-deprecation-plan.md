# M30.6 Legacy Archive / Deprecation Plan

Status: M30.6 PLAN / NO FILE MOVEMENT
Milestone: M30.6 Legacy Archive / Deprecation Plan
Chinese: M30.6 舊檔歸檔 / 棄用規劃
Runes Narrative Phrase: Runes Archive Prepared / 符文遺物歸檔準備完成

## Purpose

M30.6 defines how legacy helpers, milestone scripts, local artifacts, operation evidence, reports, and proposal inbox material should be classified before any archive, deprecation, or deletion action.

This milestone is a plan only.

It does not move, rename, archive, or delete files.

## Design Principle

```text
Preserve first.
Classify second.
Wrap or replace third.
Archive later.
Delete last, if ever.
```

Chinese summary:

```text
先保留，再分類；
先包裝或替代，再歸檔；
最後才考慮刪除。
```

## Baseline Anchors

Before any archive/deprecation action, the following anchors must remain available:

```text
Runes Seal branch: origin/archive/p0-runes-seal
Runes Seal commit: 3c6f860 docs: add M29 Runes Seal baseline
Pre-M30 local backup: ~/workspace/hermes-runes-md-wiki.local-backup-20260602-runes-seal-pre-m30/
```

No archive/deletion operation should proceed if these anchors are unavailable.

## Classification Labels

M30.6 uses these classification labels:

```text
keep_canonical
wrap_later
legacy_supported
scenario_runner
archive_candidate
delete_candidate
local_only
runtime_artifact
untrusted_proposal_material
trusted_wiki_content
```

## Classification Definitions

### keep_canonical

Files that should remain canonical project entrypoints or core implementation.

Examples:

```text
bin/runes
bin/hermes-recall
bin/hermes-memory-smoke
core importer/retrieval files still required by current smoke tests
```

Action:

```text
Do not archive.
Add metadata/header later if needed.
```

### wrap_later

Files whose behavior should remain but may be exposed through a future canonical wrapper.

Examples:

```text
strict recall verification helper
import refresh helper
controlled apply helper
```

Action:

```text
Keep existing helper.
Add future bin/runes wrapper after smoke coverage.
```

### legacy_supported

Files still useful but not the preferred future interface.

Action:

```text
Keep temporarily.
Document replacement path.
Do not remove before P0 trial run.
```

### scenario_runner

Historical scenario validation tools.

Examples:

```text
scenario_add_knowledge_m29_1.py
scenario_reject_m29_2.py
scenario_correction_update_m29_3.py
```

Action:

```text
Keep milestone-addressable.
Do not rename into canonical runtime modules.
```

### archive_candidate

Files likely to move into an archive after review.

Examples:

```text
root m24_*.sh / m25_*.sh / m26_*.sh milestone scripts
old milestone smoke wrappers after replacement
obsolete temporary helpers
```

Action:

```text
Do not delete.
Move only after M30.7 smoke confirms no behavior loss.
```

### delete_candidate

Files that may eventually be removed.

Strict requirements:

```text
must be classified
must have no active reference
must have replacement or archive decision
must be covered by backup/anchor
must pass smoke after removal
```

Action:

```text
Do not delete during M30.6.
```

### local_only

Files useful only for local inspection or temporary project work.

Examples:

```text
local inventory reports
local backup README
temporary manual verification notes
```

Action:

```text
Keep local unless intentionally promoted to wiki documentation.
Do not ingest into trusted memory by default.
```

### runtime_artifact

Generated outputs from operations, logs, or tool execution.

Examples:

```text
operations/
reports/
backups/
```

Action:

```text
Retain during M30.
Define retention before cleanup.
Do not ingest automatically into RAG.
```

### untrusted_proposal_material

Draft/proposal content that is not trusted memory.

Examples:

```text
forge-inbox files
proposal candidates
manual import candidates
```

Action:

```text
Do not promote without attunement/promotion/apply governance.
```

## Proposed Archive Layout

Preferred future archive locations:

```text
tools/archive/milestone-shell/
tools/runes/_archive/
docs/archive/
wiki/k6-freelancer/archive/
```

Suggested usage:

| Archive path | Intended content |
| --- | --- |
| tools/archive/milestone-shell/ | root M24/M25/M26 shell scripts |
| tools/runes/_archive/ | old Python helpers replaced by canonical tools |
| docs/archive/ | old design docs not part of trusted wiki |
| wiki/k6-freelancer/archive/ | curated historical project docs worth keeping searchable |

Archive movement must preserve original filename unless there is a strong reason not to.

## Archive Index Requirement

Each archive directory should eventually include an index file:

```text
README.md
```

The index should explain:

```text
why archived
when archived
what replaced it
whether it is safe to delete later
which milestone performed the archive
```

## Root Milestone Shell Scripts Plan

Known category:

```text
root m24_*.sh / m25_*.sh / m26_*.sh milestone scripts
```

Risk:

```text
medium
```

M30.6 plan:

```text
1. classify as archive_candidate by default
2. inspect for unique commands not captured elsewhere
3. preserve in tools/archive/milestone-shell/ later
4. add archive README later
5. delete only if confirmed obsolete after P0 trial run
```

No root milestone shell script should become a canonical operator entrypoint.

## tools/runes Helper Plan

Existing `tools/runes/*.py` should be classified individually.

Likely treatment:

| Helper type | Default classification | Future direction |
| --- | --- | --- |
| proposal helpers | legacy_supported / wrap_later | map to proposal_create/read/list/hygiene |
| attunement helpers | wrap_later | map to attune preview/record |
| promotion helpers | wrap_later | map to promote preview/preflight |
| controlled apply helper | keep_canonical / wrap_later | preserve safety behavior |
| import refresh helper | wrap_later | map to refresh importer |
| recall verifier | keep_canonical / wrap_later | preserve strict result-only behavior |
| scenario runners | scenario_runner | keep milestone-addressable |
| old smoke helpers | archive_candidate / legacy_supported | retain until M30.7 smoke suite exists |

No helper should be deleted before classification.

## Scenario Runner Plan

Scenario runners remain important historical evidence.

M29 scenario runners should stay as:

```text
scenario_runner
```

M30.6 does not recommend archiving them before P0 trial run because they are useful as regression references.

## Operation Evidence Plan

Operation evidence should be classified as:

```text
runtime_artifact
```

M30.6 plan:

```text
keep during M30
avoid importing into RAG by default
consider local retention cleanup later
preserve key verification records by summarizing into wiki docs, not by indexing raw operations
```

## Reports Plan

Reports are classified as:

```text
local_only
runtime_artifact
```

M30.6 plan:

```text
keep local reports while M30 is active
promote only durable summaries into wiki
avoid committing large or noisy reports unless intentionally curated
```

## Forge Inbox Plan

Forge inbox files are classified as:

```text
untrusted_proposal_material
```

M30.6 plan:

```text
preserve until reviewed
never treat as trusted memory directly
only promote through governed proposal/attunement/promotion/apply flow
```

## Backups Plan

Backups are classified as:

```text
local_only
runtime_artifact
```

Current backup:

```text
~/workspace/hermes-runes-md-wiki.local-backup-20260602-runes-seal-pre-m30/
```

Old delete candidate:

```text
~/workspace/_delete_candidate_hermes-memory.local-backup-20260601-003128
```

Deletion of old backup should wait until:

```text
P0 trial run starts
M30 cleanup is stable
Runes Seal anchor remains available
```

## Deprecation Metadata

Any deprecated file should eventually have a header or archive index entry stating:

```text
File class: legacy_supported / archive_candidate / delete_candidate
Replacement / deprecation: <replacement path or reason>
Safe to remove: yes/no/later
```

This should follow M30.3 metadata/header standard.

## Deletion Gate

No deletion should occur unless all are true:

```text
classified as delete_candidate
not referenced by current scripts/docs
replacement or archive path exists
local backup exists
Runes Seal rollback anchor exists
M30.7 smoke suite passes after removal
user explicitly approves deletion
```

## Recommended Execution Order After M30.6

Recommended order:

```text
1. M30.7 Pre-release Smoke Suite
2. classify root milestone shell scripts
3. classify tools/runes helpers
4. add archive README skeletons
5. move archive candidates only after smoke pass
6. mark deprecated files
7. delay deletion until after P0 trial-run stability
```

## No-change Boundary

M30.6 does not perform:

- file movement
- archive movement
- deletion
- rename
- CLI change
- runtime change
- trusted wiki mutation beyond this policy document
- operation evidence cleanup
- backup deletion

It only defines archive/deprecation policy.

## Verification Status

M30.6 Legacy Archive / Deprecation Plan:

- classification labels defined: PASS
- archive layout proposed: PASS
- archive index requirement defined: PASS
- root milestone shell script plan defined: PASS
- tools/runes helper plan defined: PASS
- scenario runner plan defined: PASS
- operation evidence plan defined: PASS
- reports plan defined: PASS
- forge inbox plan defined: PASS
- backup plan defined: PASS
- deletion gate defined: PASS
- no-file-movement boundary preserved: PASS

Overall:

M30.6 Legacy Archive / Deprecation Plan:
PASS / archive-deprecation policy defined / no file movement performed
