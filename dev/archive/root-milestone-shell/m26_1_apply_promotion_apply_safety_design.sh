#!/usr/bin/env bash
set -euo pipefail
cd "${HERMES_RUNES_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"

cat > wiki/k6-freelancer/verification-m26-human-approved-promotion-apply.md <<'MD'
# M26 Human-approved Promotion Apply Verification

Status: DESIGN LOCK / NO APPLY IMPLEMENTATION
Milestone: M26 Human-approved Promotion Apply / Dry-run-to-Apply Boundary
Chinese: M26 人類核准升格套用 / 乾跑到套用邊界

## Purpose

M26 defines the safety boundary for a future human-approved promotion apply flow.

M26 starts from the M25 stable forge-preview baseline and asks:

```text
If a human approves a curated promotion patch preview, what must be true before the patch may ever be applied to trusted Markdown wiki memory?
```

M26.1 does not implement apply.

It only locks the safety model, preconditions, invariants, and non-goals for a future apply path.

## Core Principle

Human-approved apply must be explicit, bounded, reversible, and auditable.

A future apply operation must never be inferred from:

- proposal creation
- attunement approval
- attunement trail preview
- promotion patch preview
- smoke test success
- agent recommendation alone

## Relationship to Previous Milestones

M22 established proposal governance.

M23 established Runes Attunement dry-run.

M24 established Attunement Trail dry-run.

M25 established Curated Promotion Patch Preview dry-run.

M26 begins the boundary design for future apply.

The chain remains:

```text
proposal
→ attunement
→ attunement trail
→ curated promotion patch preview
→ human-approved apply boundary
```

But M26.1 still ends before actual trusted wiki mutation.

## Required Future Preconditions

Before any future promotion patch apply can exist, all of the following must be required:

1. A concrete proposal ID.
2. A human-approved attunement state.
3. A generated promotion patch preview.
4. A stable target path inside `wiki/`.
5. A single intended target heading or insertion point.
6. A pre-apply file hash.
7. A post-apply expected hash or generated candidate hash.
8. A visible unified diff.
9. A human confirmation token or equivalent explicit approval signal.
10. An append-only operation record / attunement trail event.
11. A rollback or restore path.
12. A post-apply smoke / verification step.

## M26.1 Design Scope

M26.1 defines:

- dry-run-to-apply terminology
- apply preconditions
- single-target apply boundary
- expected file hash checks
- operation record requirement
- rollback requirement
- post-apply verification requirement
- no-autonomous-apply invariant

## Non-goals

M26.1 explicitly does not implement:

- actual patch apply
- trusted wiki write
- database mutation
- importer mutation
- proposal state mutation
- attunement state mutation
- promotion state mutation
- automatic approval
- background apply worker
- multi-file merge engine
- enterprise approval workflow

## Locked Safety Invariants

A future apply implementation must preserve:

- proposal is not trusted memory
- attunement is not promotion
- patch preview is not wiki mutation
- human-approved apply is not autonomous apply
- apply must be single-target first
- apply must verify target path containment
- apply must verify pre-apply hash
- apply must record operation evidence
- apply must support rollback or restoration
- apply must trigger or require post-apply verification

## Forbidden Behavior

The following remain forbidden:

- agent silently applying patches
- apply without explicit human confirmation
- apply from stale preview without hash check
- writing outside `wiki/`
- modifying `.env` or secret-bearing files
- modifying database directly
- running importer as an implicit side effect
- promoting unreviewed proposal content
- treating preview smoke PASS as approval

## Future M26 Direction

Future M26 substeps may include:

- M26.2 Apply preflight dry-run CLI
- M26.3 Apply confirmation token preview
- M26.4 Rollback plan preview
- M26.5 Human-approved apply MVP, only if safety preflight is frozen first

M26.1 itself is design-only.

## Verification Status

M26.1 Human-approved Promotion Apply Safety Design Lock:

- terminology: PASS
- preconditions: PASS
- no-apply boundary: PASS
- no-autonomous-apply invariant: PASS
- single-target first policy: PASS
- rollback requirement: PASS
- post-apply verification requirement: PASS

Overall:

M26.1 Human-approved Promotion Apply Safety Design Lock:
PASS / design locked / no apply implementation
MD

cat >> wiki/k6-freelancer/roadmap.md <<'MD'

---

## M26 Human-approved Promotion Apply / Dry-run-to-Apply Boundary

Status: DESIGN LOCK / NO APPLY IMPLEMENTATION

Verification record:

- `wiki/k6-freelancer/verification-m26-human-approved-promotion-apply.md`

Goal:

Define the safety boundary for a future human-approved promotion apply flow without implementing trusted wiki writes yet.

M26.1 completed scope:

- dry-run-to-apply terminology
- apply safety preconditions
- single-target apply boundary
- pre-apply hash requirement
- operation record requirement
- rollback requirement
- post-apply verification requirement
- no-autonomous-apply invariant

Locked boundaries:

- no actual patch apply
- no trusted wiki write
- no proposal state mutation
- no attunement state mutation
- no database mutation
- no importer mutation
- no autonomous promotion execution
- no background apply worker

Future direction:

- M26.2 Apply preflight dry-run CLI
- M26.3 Apply confirmation token preview
- M26.4 Rollback plan preview
- M26.5 Human-approved apply MVP, only after safety preflight is frozen

Current milestone:

- M26.1 Human-approved Promotion Apply Safety Design Lock: PASS / design locked

MD

python3 -m py_compile \
  tools/runes/promotion_patch_m25_2.py \
  tools/runes/smoke_m25_3_promotion_patch.py \
  tools/runes/runes.py

python3 tools/runes/smoke_m25_3_promotion_patch.py | tee /tmp/m26_1_regression_smoke.json

python3 - <<'PY'
import json
from pathlib import Path

report = json.loads(Path("/tmp/m26_1_regression_smoke.json").read_text(encoding="utf-8"))
if report.get("status") != "PASS":
    raise SystemExit("M26.1 design lock blocked: M25.3 regression smoke is not PASS")
if report.get("failed") != 0:
    raise SystemExit("M26.1 design lock blocked: regression smoke failed count is not zero")
print(f"M26.1 regression confirmation: PASS failed={report.get('failed')} total={report.get('total')}")
PY

grep -n "M26 Human-approved Promotion Apply\|DESIGN LOCK / NO APPLY IMPLEMENTATION\|no-autonomous-apply" \
  wiki/k6-freelancer/verification-m26-human-approved-promotion-apply.md

grep -n "M26 Human-approved Promotion Apply\|M26.1 Human-approved Promotion Apply Safety Design Lock\|M26.2 Apply preflight dry-run CLI" \
  wiki/k6-freelancer/roadmap.md

git add \
  wiki/k6-freelancer/verification-m26-human-approved-promotion-apply.md \
  wiki/k6-freelancer/roadmap.md

git diff --cached

git commit -m "Add M26 promotion apply safety design baseline"

git push origin main

git log --oneline -5
