# M31.1 Root Milestone Shell Script Classification

Status: M31.1 CLASSIFICATION / NO FILE MOVEMENT / NO DELETION
Milestone: M31.1 Root Milestone Shell Script Classification
Chinese: M31.1 根目錄里程碑 Shell Script 分類
Runes Narrative Phrase: Runes Relic Sight / 符文遺物視界

## Purpose

M31.1 begins the first implementation-hardening cleanup track after the M30 pre-implementation baseline lock.

This milestone classifies root-level milestone shell scripts before any archive movement, deletion, rename, or wrapper replacement.

M31.1 does not move or delete files.

## Baseline Dependencies

M31.1 depends on:

```text
M29 Runes Seal baseline
M30.11 Manual Pre-release Smoke Result Lock
Pre-M30 local backup
```

Current locked baseline:

```text
M30.11 Manual Pre-release Smoke Result Lock:
PASS / manual smoke verified / pre-implementation baseline locked
```

## Scope

M31.1 covers root-level milestone shell scripts currently visible in the local workspace inventory:

```text
m24_2_apply_attunement_trail_cli.sh
m24_3_apply_trail_markdown_preview.sh
m24_3_fix_newline_literal.sh
m24_4_apply_attunement_trail_smoke.sh
m24_5_lock_attunement_trail_baseline.sh
m25_1_2_apply_curated_promotion_patch_preview.sh
m25_3_apply_promotion_patch_smoke.sh
m25_4_lock_curated_promotion_patch_baseline.sh
m26_1_apply_promotion_apply_safety_design.sh
m26_2_apply_preflight_dry_run_cli.sh
m26_3_apply_preflight_confirmation_smoke.sh
m26_3_fix_preflight_blocking.sh
m26_4_apply_rollback_plan_preview.sh
```

## Classification Labels

M31.1 uses these labels:

```text
archive_candidate
legacy_supported
preserve_reference
delete_candidate
```

Definitions:

- `archive_candidate`: should likely move to an archive path later.
- `legacy_supported`: still potentially useful for local execution or reproduction.
- `preserve_reference`: valuable historical recipe/reference; keep visible until archive index exists.
- `delete_candidate`: may be deleted only after archive/replacement/smoke/user approval.

M31.1 does not assign immediate deletion.

## Default Classification

All root-level milestone shell scripts are classified as:

```text
archive_candidate + preserve_reference
```

Reason:

```text
They are historical milestone execution recipes.
They should not remain root-level long-term.
They may still contain useful command history for M24-M26 governance evolution.
```

## Per-file Classification

| File | Classification | Rationale |
| --- | --- | --- |
| m24_2_apply_attunement_trail_cli.sh | archive_candidate / preserve_reference | M24 attunement trail CLI execution history; useful historical recipe, not canonical entrypoint. |
| m24_3_apply_trail_markdown_preview.sh | archive_candidate / preserve_reference | M24 markdown preview helper; historical preview recipe. |
| m24_3_fix_newline_literal.sh | archive_candidate / preserve_reference | Fix helper for newline literal issue; useful as debugging history only. |
| m24_4_apply_attunement_trail_smoke.sh | archive_candidate / preserve_reference | M24 smoke execution helper; historical smoke recipe. |
| m24_5_lock_attunement_trail_baseline.sh | archive_candidate / preserve_reference | M24 baseline lock helper; historical lock evidence. |
| m25_1_2_apply_curated_promotion_patch_preview.sh | archive_candidate / preserve_reference | M25 curated promotion patch preview recipe; useful historical governance path. |
| m25_3_apply_promotion_patch_smoke.sh | archive_candidate / preserve_reference | M25 promotion patch smoke helper; historical smoke recipe. |
| m25_4_lock_curated_promotion_patch_baseline.sh | archive_candidate / preserve_reference | M25 baseline lock helper; historical lock evidence. |
| m26_1_apply_promotion_apply_safety_design.sh | archive_candidate / preserve_reference | M26 promotion apply safety design helper; historical safety-design recipe. |
| m26_2_apply_preflight_dry_run_cli.sh | archive_candidate / preserve_reference | M26 preflight dry-run CLI recipe; relevant to controlled apply safety history. |
| m26_3_apply_preflight_confirmation_smoke.sh | archive_candidate / preserve_reference | M26 confirmation smoke recipe; relevant to confirmation-token safety history. |
| m26_3_fix_preflight_blocking.sh | archive_candidate / preserve_reference | M26 fix helper for preflight blocking; debugging history. |
| m26_4_apply_rollback_plan_preview.sh | archive_candidate / preserve_reference | M26 rollback plan preview recipe; relevant to rollback governance history. |

## Not Canonical Entrypoints

M31.1 confirms that these scripts should not become canonical operator entrypoints.

Canonical entrypoints remain:

```text
bin/runes
bin/hermes-recall
bin/hermes-memory-smoke
```

Future root milestone scripts should not be added as primary operator interfaces.

## Recommended Future Archive Path

Recommended archive destination for M31.2 or later:

```text
tools/archive/milestone-shell/
```

Recommended archive index:

```text
tools/archive/milestone-shell/README.md
```

The archive index should include:

```text
original filename
milestone
reason archived
replacement/canonical path if any
safe-to-delete status
```

## Deletion Position

M31.1 explicitly does not classify any root milestone shell script as immediately deletable.

Deletion may only be considered later if all are true:

```text
script is archived or fully superseded
archive README exists
M30.11 smoke baseline remains available
post-move smoke passes
user explicitly approves deletion
```

## Suggested M31.2 Direction

M31.2 should be:

```text
M31.2 Root Milestone Shell Archive Move Plan
```

Recommended M31.2 behavior:

```text
plan archive directory
plan README content
plan mv commands
plan post-move smoke checks
still avoid deletion
```

Actual move can be M31.3 only after review.

## No-change Boundary

M31.1 does not perform:

- file movement
- archive movement
- deletion
- rename
- CLI change
- runtime change
- smoke runner change
- trusted wiki behavior change

It only classifies root milestone shell scripts.

## Verification Status

M31.1 Root Milestone Shell Script Classification:

- root milestone shell script scope defined: PASS
- classification labels defined: PASS
- all known root M24/M25/M26 shell scripts classified: PASS
- canonical entrypoint boundary preserved: PASS
- archive path recommendation defined: PASS
- no immediate deletion decision: PASS
- no-file-movement boundary preserved: PASS

Overall:

M31.1 Root Milestone Shell Script Classification:
PASS / root milestone shell scripts classified / no file movement performed
