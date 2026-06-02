# M30.2 Canonical Naming Policy

Status: M30.2 POLICY / NO RENAME YET
Milestone: M30.2 Canonical Naming Policy
Chinese: M30.2 正式命名政策

## Purpose

M30.2 defines canonical naming rules before any pre-release refactor, rename, archive, or deletion work begins.

This policy intentionally does not rename files yet.

Its purpose is to prevent M30 cleanup from becoming subjective or destructive.

## Core Principle

Program names should describe stable product/component responsibilities.

Milestone numbers should describe historical verification context.

Therefore:

```text
Mxx belongs primarily in documentation, verification files, scenario runners, and archive references.
Canonical runtime module names should avoid long-term Mxx naming.
```

## Naming Classes

Every file should eventually be classified into one of these classes:

```text
canonical_runtime
canonical_governance_tool
canonical_smoke
canonical_verification_doc
scenario_runner
milestone_helper
legacy_supported
archive_candidate
delete_candidate
runtime_artifact
local_report
```

No file should be renamed or deleted before classification.

## Canonical Runtime Entrypoints

Long-term operator-facing entrypoints should be concentrated under:

```text
bin/runes
bin/hermes-recall
bin/hermes-memory-smoke
```

Preferred future operator UX:

```text
runes proposal ...
runes attune ...
runes promote ...
runes apply ...
runes refresh ...
runes verify-recall ...
runes smoke ...
```

M30 must avoid introducing many new top-level operator scripts.

## Canonical Python Module Naming

Future canonical Python modules should use stable responsibility names, for example:

```text
tools/runes/proposal.py
tools/runes/attunement.py
tools/runes/promotion.py
tools/runes/controlled_apply.py
tools/runes/refresh_importer.py
tools/runes/verify_recall.py
tools/runes/smoke_retrieval_consistency.py
```

These names describe component role, not historical milestone.

## Milestone Helper Naming

Existing milestone-numbered helpers may remain during M30 review, for example:

```text
tools/runes/proposal_writer_m22_1.py
tools/runes/promotion_apply_m27_2.py
tools/runes/import_refresh_m28_2.py
tools/runes/scenario_add_knowledge_m29_1.py
```

These should be classified as one of:

```text
scenario_runner
milestone_helper
legacy_supported
archive_candidate
```

They should not be treated as long-term canonical module names unless explicitly promoted.

## Scenario Runner Naming

Scenario runners may keep milestone numbers because their purpose is historical reproducibility.

Allowed style:

```text
scenario_add_knowledge_m29_1.py
scenario_reject_m29_2.py
scenario_correction_update_m29_3.py
```

Reason:

```text
Scenario runners are evidence-producing historical validation tools, not long-term runtime APIs.
```

## Smoke Naming

Canonical smoke tests should eventually use stable behavior names:

```text
smoke_controlled_apply.py
smoke_refresh_importer.py
smoke_recall_verification.py
smoke_retrieval_consistency.py
```

Milestone smoke files may remain as archived evidence:

```text
smoke_m22_1_propose.py
smoke_m22_3b_hygiene_cli.py
```

## Verification Document Naming

Verification documents should keep milestone identifiers.

Allowed style:

```text
verification-m27-human-approved-apply-mvp.md
verification-m28-importer-retrieval-refresh-boundary.md
verification-m29-p0-pretrial-runes-seal.md
```

Reason:

```text
Verification documents are timeline evidence and should remain milestone-addressable.
```

## Wiki Policy Document Naming

Long-term policy documents should avoid Mxx numbers unless they are milestone-specific.

Preferred style:

```text
pre-release-hardening.md
naming-policy.md
repo-boundary-policy.md
taxonomy-layout-policy.md
```

## Root-level Shell Script Policy

Root-level milestone shell scripts such as:

```text
m24_*.sh
m25_*.sh
m26_*.sh
```

should not remain in the project root long-term.

M30 should classify each as:

```text
archive_candidate
convert_to_canonical_tool
delete_candidate
```

Preferred future locations:

```text
tools/archive/milestone-shell/
tools/runes/_archive/
docs/archive/
```

No root milestone shell script should be promoted to canonical runtime entrypoint.

## Schema Version Policy

Schema versions may keep milestone references when they describe evidence payload compatibility.

Allowed:

```text
m27.2.p0.v1
m28.3.p0.v2
m29.1.p0.v2
```

Reason:

```text
Schema versions are compatibility identifiers, not file names.
```

However, future schema versions should follow a consistent pattern:

```text
<milestone>.<stage>.<major>
```

Examples:

```text
m30.naming_policy.v1
p0.controlled_apply.v1
p0.recall_verification.v2
```

M30.3 should refine this into a formal metadata/header standard.

## Archive Naming Policy

Archived files should preserve original filename and include a relocation note when possible.

Preferred archive layout:

```text
tools/runes/_archive/<original_filename>
tools/archive/milestone-shell/<original_filename>
docs/archive/<topic>/<original_filename>
```

Archive index files should explain:

```text
why archived
when archived
replacement entrypoint
whether safe to delete later
```

## Deletion Policy

Deletion requires prior classification as:

```text
delete_candidate
```

Deletion should be delayed until:

```text
1. Runes Seal rollback anchor exists
2. Pre-M30 local backup exists
3. replacement or archive decision is documented
4. relevant smoke tests pass after removal
```

## Naming Decisions Locked in M30.2

Locked decisions:

- Mxx may remain in verification documents.
- Mxx may remain in scenario runners.
- Mxx should not be long-term canonical runtime module naming.
- Root milestone shell scripts should not remain in the root long-term.
- bin/ should hold only stable operator entrypoints.
- Canonical tools should use responsibility-based names.
- Archive should preserve original filenames.
- Schema versions may keep milestone references for compatibility.

## M30.2 Does Not Authorize

M30.2 does not authorize:

- immediate rename
- immediate deletion
- moving files into archive
- changing runtime behavior
- changing CLI behavior
- weakening verification semantics

Actual rename/archive/delete work must happen in later M30 phases after review.

## Next Milestone

Next:

```text
M30.3 File Header / Version Metadata Standard
```

M30.3 should define standard headers for canonical Python entrypoints and helpers.

## Verification Status

M30.2 Canonical Naming Policy:

- canonical naming classes defined: PASS
- runtime entrypoint policy defined: PASS
- Python module naming policy defined: PASS
- milestone helper policy defined: PASS
- scenario runner policy defined: PASS
- verification document naming policy defined: PASS
- root shell script policy defined: PASS
- schema version policy defined: PASS
- archive/deletion policy defined: PASS
- no-rename-yet boundary preserved: PASS

Overall:

M30.2 Canonical Naming Policy:
PASS / policy defined / no rename performed
