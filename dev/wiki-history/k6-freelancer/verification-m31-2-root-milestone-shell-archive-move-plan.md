# M31.2 Root Milestone Shell Archive Move Plan

Status: M31.2 PLAN / NO FILE MOVEMENT / NO DELETION
Milestone: M31.2 Root Milestone Shell Archive Move Plan
Chinese: M31.2 根目錄里程碑 Shell Script 歸檔搬移規劃
Runes Narrative Phrase: Runes Relic Path Prepared / 符文遺物路徑準備完成

## Purpose

M31.2 plans how to move root-level M24/M25/M26 milestone shell scripts into an archive directory without changing runtime behavior or deleting historical evidence.

This milestone is a move plan only.

It does not move files.

## Baseline Dependencies

M31.2 depends on:

```text
M30.11 Manual Pre-release Smoke Result Lock
M31.1 Root Milestone Shell Script Classification
Pre-M30 local backup
Runes Seal rollback anchor
```

M31.1 classified all known root-level milestone shell scripts as:

```text
archive_candidate / preserve_reference
```

## Target Archive Layout

Recommended archive directory:

```text
tools/archive/milestone-shell/
```

Required archive index:

```text
tools/archive/milestone-shell/README.md
```

Purpose:

```text
Preserve historical milestone execution recipes while removing root-level clutter.
```

## Files Planned for Archive Move

Planned move set:

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

No file in this list is classified as immediate delete.

## Planned Move Commands

M31.2 proposes the following future move commands for M31.3 or later:

```bash
cd ~/workspace/hermes-runes-md-wiki

mkdir -p tools/archive/milestone-shell

mv m24_2_apply_attunement_trail_cli.sh tools/archive/milestone-shell/
mv m24_3_apply_trail_markdown_preview.sh tools/archive/milestone-shell/
mv m24_3_fix_newline_literal.sh tools/archive/milestone-shell/
mv m24_4_apply_attunement_trail_smoke.sh tools/archive/milestone-shell/
mv m24_5_lock_attunement_trail_baseline.sh tools/archive/milestone-shell/
mv m25_1_2_apply_curated_promotion_patch_preview.sh tools/archive/milestone-shell/
mv m25_3_apply_promotion_patch_smoke.sh tools/archive/milestone-shell/
mv m25_4_lock_curated_promotion_patch_baseline.sh tools/archive/milestone-shell/
mv m26_1_apply_promotion_apply_safety_design.sh tools/archive/milestone-shell/
mv m26_2_apply_preflight_dry_run_cli.sh tools/archive/milestone-shell/
mv m26_3_apply_preflight_confirmation_smoke.sh tools/archive/milestone-shell/
mv m26_3_fix_preflight_blocking.sh tools/archive/milestone-shell/
mv m26_4_apply_rollback_plan_preview.sh tools/archive/milestone-shell/
```

M31.2 does not execute these commands.

## Archive README Plan

The future archive README should include:

```text
# Milestone Shell Archive

Purpose:
- Preserve historical one-off M24/M25/M26 execution helpers.
- These scripts are not canonical operator entrypoints.
- Canonical entrypoints remain bin/runes, bin/hermes-recall, and bin/hermes-memory-smoke.

Policy:
- Do not execute archived scripts blindly.
- Treat archived scripts as historical recipes.
- Prefer current canonical tools and verification docs.
- Do not delete without explicit approval and post-move smoke.
```

Recommended index table columns:

```text
file
milestone
classification
reason archived
replacement/current reference
safe to delete
```

## Proposed README Table

| File | Milestone | Classification | Reason archived | Replacement/current reference | Safe to delete |
| --- | --- | --- | --- | --- | --- |
| m24_2_apply_attunement_trail_cli.sh | M24.2 | archive_candidate / preserve_reference | Historical attunement trail CLI recipe | verification-m24-attunement-trail.md | no |
| m24_3_apply_trail_markdown_preview.sh | M24.3 | archive_candidate / preserve_reference | Historical markdown preview helper | verification-m24-attunement-trail.md | no |
| m24_3_fix_newline_literal.sh | M24.3 fix | archive_candidate / preserve_reference | Historical newline literal fix | verification-m24-attunement-trail.md | no |
| m24_4_apply_attunement_trail_smoke.sh | M24.4 | archive_candidate / preserve_reference | Historical attunement trail smoke | verification-m24-attunement-trail.md | no |
| m24_5_lock_attunement_trail_baseline.sh | M24.5 | archive_candidate / preserve_reference | Historical baseline lock helper | verification-m24-attunement-trail.md | no |
| m25_1_2_apply_curated_promotion_patch_preview.sh | M25.1/M25.2 | archive_candidate / preserve_reference | Historical curated promotion preview recipe | verification-m25-curated-promotion-preview.md | no |
| m25_3_apply_promotion_patch_smoke.sh | M25.3 | archive_candidate / preserve_reference | Historical promotion patch smoke | verification-m25-curated-promotion-preview.md | no |
| m25_4_lock_curated_promotion_patch_baseline.sh | M25.4 | archive_candidate / preserve_reference | Historical baseline lock helper | verification-m25-curated-promotion-preview.md | no |
| m26_1_apply_promotion_apply_safety_design.sh | M26.1 | archive_candidate / preserve_reference | Historical safety design helper | verification-m26-human-approved-promotion-apply.md | no |
| m26_2_apply_preflight_dry_run_cli.sh | M26.2 | archive_candidate / preserve_reference | Historical preflight dry-run recipe | verification-m26-human-approved-promotion-apply.md | no |
| m26_3_apply_preflight_confirmation_smoke.sh | M26.3 | archive_candidate / preserve_reference | Historical confirmation smoke recipe | verification-m26-human-approved-promotion-apply.md | no |
| m26_3_fix_preflight_blocking.sh | M26.3 fix | archive_candidate / preserve_reference | Historical preflight blocking fix | verification-m26-human-approved-promotion-apply.md | no |
| m26_4_apply_rollback_plan_preview.sh | M26.4 | archive_candidate / preserve_reference | Historical rollback preview recipe | verification-m26-human-approved-promotion-apply.md | no |

## Post-move Smoke Plan

After future archive movement, run at minimum:

```bash
cd ~/workspace/hermes-runes-md-wiki

python -m py_compile \
  tools/runes/recall_verify_m28_3.py \
  tools/runes/retrieval_consistency_m28_4.py

./bin/hermes-memory-smoke

for f in bin/runes bin/hermes-recall bin/hermes-memory-smoke; do
  test -x "$f" && echo "PASS executable $f" || echo "FAIL executable $f"
done
```

Recommended additional check:

```bash
git status --short
find tools/archive/milestone-shell -maxdepth 1 -type f | sort
```

Expected result:

```text
core smoke remains PASS
canonical entrypoints remain executable
root milestone scripts no longer appear at repository root
archived scripts are visible under tools/archive/milestone-shell/
```

## Rollback Plan

If post-move smoke fails, restore scripts from archive:

```bash
cd ~/workspace/hermes-runes-md-wiki

mv tools/archive/milestone-shell/m24_*.sh . 2>/dev/null || true
mv tools/archive/milestone-shell/m25_*.sh . 2>/dev/null || true
mv tools/archive/milestone-shell/m26_*.sh . 2>/dev/null || true
```

If needed, restore from pre-M30 local backup:

```text
~/workspace/hermes-runes-md-wiki.local-backup-20260602-runes-seal-pre-m30/
```

or from git if the move is committed later.

## Deletion Boundary

M31.2 does not authorize deletion.

Even after archive move, deletion requires:

```text
archive README exists
post-move smoke passes
no active references remain
M30.11 lock remains available
user explicitly approves deletion
```

## Risks

Primary risk:

```text
A historical script may contain a useful command not yet documented elsewhere.
```

Mitigation:

```text
Archive instead of delete.
Preserve original filenames.
Add README index.
Run smoke after move.
```

Secondary risk:

```text
Some documentation or user workflow may still mention root-level script paths.
```

Mitigation:

```text
Search references before M31.3 move.
Optionally update references to archived path.
```

## Pre-move Reference Search Plan

Before M31.3, run:

```bash
cd ~/workspace/hermes-runes-md-wiki

grep -RIn "m24_\|m25_\|m26_" . \
  --exclude-dir=.git \
  --exclude-dir=.venv \
  --exclude-dir=operations \
  --exclude-dir=backups \
  --exclude-dir=logs \
  | head -120
```

Use this to decide whether any docs need path updates after archive movement.

## No-change Boundary

M31.2 does not perform:

- file movement
- archive movement
- deletion
- rename
- CLI change
- runtime change
- smoke runner change
- trusted wiki behavior change

It only plans the future archive move.

## Verification Status

M31.2 Root Milestone Shell Archive Move Plan:

- target archive layout defined: PASS
- planned move set defined: PASS
- archive README plan defined: PASS
- post-move smoke plan defined: PASS
- rollback plan defined: PASS
- deletion boundary preserved: PASS
- pre-move reference search plan defined: PASS
- no-file-movement boundary preserved: PASS

Overall:

M31.2 Root Milestone Shell Archive Move Plan:
PASS / archive move plan defined / no file movement performed
