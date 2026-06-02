#!/usr/bin/env bash
set -euo pipefail
cd "${HERMES_RUNES_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"

cat > wiki/k6-freelancer/verification-m25-curated-promotion-preview.md <<'MD'
# M25 Curated Promotion Patch Preview Verification

Status: PASS / STABLE DRY-RUN BASELINE
Milestone: M25 Curated Promotion Patch Preview / Dry-run
Chinese: M25 精選升格補丁預覽 / 乾跑

## Final Status

M25 Curated Promotion Patch Preview / Dry-run is now locked as:

```text
PASS / stable governed forge-preview baseline
```

M25 establishes the first governed forge-preview layer for Hermes Runes MD Wiki.

It allows Hermes-agent / Runes Shield to recommend how an attuned proposal could become a trusted Markdown wiki patch, while preserving the no-autonomous-write boundary.

## Core Principle

Forge suggestion, not forge execution.

M25 locks the following distinctions:

- proposal is not trusted memory
- attunement is not promotion
- patch preview is not wiki mutation
- forge preview is not forge execution
- promotion preview is not promotion execution
- human review remains required before any future apply

## Completed Scope

### M25.1 Curated Promotion Patch Design Lock

Status: PASS

M25.1 defined:

- curated promotion terminology
- candidate Markdown diff semantics
- single-target patch preview philosophy
- promotion evidence vs trusted memory distinction
- preview-only / no-mutation boundary

### M25.2 Promotion Patch Dry-run CLI

Status: PASS

M25.2 implemented:

```text
runes promotion preview \
  --proposal-id '<proposal_id>' \
  --target-path '<path>' \
  --heading '<heading>' \
  --insert-text '<markdown>' \
  --dry-run
```

Supported output:

- terminal-readable preview
- Markdown diff preview
- JSON preview

### M25.3 Promotion Patch Smoke Test

Status: PASS

Regression target:

```text
tools/runes/smoke_m25_3_promotion_patch.py
```

Confirmed smoke status:

```text
suite: M25.3 Curated Promotion Patch smoke test
status: PASS
failed: 0
total: 34
```

## Verified Capabilities

M25 verifies:

- helper payload generation
- CLI route through `bin/runes promotion preview`
- terminal-readable preview
- Markdown preview
- JSON preview
- unified diff generation
- candidate Markdown evidence rendering
- target Markdown hash unchanged
- no trusted wiki mutation
- no database mutation
- no importer mutation
- no promotion execution

## Locked Boundaries

M25 explicitly keeps the following unimplemented / forbidden:

- actual patch apply: not implemented
- trusted wiki write: forbidden
- proposal state mutation: forbidden
- attunement state mutation: forbidden
- database mutation: forbidden
- importer mutation: forbidden
- promotion execution: not implemented
- autonomous promotion execution: forbidden
- autonomous trusted-memory mutation: forbidden

## Current Tool Boundary

Current P0 command:

```text
runes promotion preview --proposal-id ... --target-path ... --heading ... --insert-text ... --dry-run
```

This command may render candidate patch evidence.

It must not:

- modify Markdown files
- write trusted wiki memory
- modify proposal metadata
- write to the database
- run importer/indexing
- mark a proposal as promoted
- apply a patch

## Personal-use Boundary

M25 remains personal-use scoped.

It must not become:

- an enterprise PR automation engine
- a multi-file merge engine
- a background promotion worker
- an autonomous wiki writer
- a direct database mutator
- a policy-heavy approval platform

## Next Milestone Boundary

The next milestone may explore:

```text
M26 Human-approved Promotion Apply / Dry-run-to-Apply Boundary
```

But M26 must start by designing the safety boundary before any actual apply behavior.

M25 itself ends at forge-preview dry-run only.
MD

cat >> wiki/k6-freelancer/roadmap.md <<'MD'

---

## M25.4 Roadmap / Verification Lock

Status: PASS / M25 STABLE DRY-RUN BASELINE

Verification record:

- `wiki/k6-freelancer/verification-m25-curated-promotion-preview.md`

Locked milestone:

```text
M25 Curated Promotion Patch Preview / Dry-run:
PASS / stable governed forge-preview baseline
```

Completed M25 scope:

- M25.1 Curated Promotion Patch Design Lock: PASS
- M25.2 Promotion Patch Dry-run CLI: PASS
- M25.3 Promotion Patch Smoke Test: PASS
- M25.4 Roadmap / Verification Lock: PASS

Locked boundaries:

- proposal is not trusted memory
- patch preview is not wiki mutation
- forge preview is not forge execution
- promotion preview is not promotion execution
- no trusted wiki mutation
- no proposal state mutation
- no database mutation
- no importer mutation
- no autonomous promotion execution

Not implemented in M25:

- actual patch apply
- trusted wiki write
- proposal promotion state mutation
- database mutation
- importer/index mutation
- autonomous trusted-memory promotion

Next possible milestone:

- M26 Human-approved Promotion Apply / Dry-run-to-Apply Boundary

MD

python3 -m py_compile \
  tools/runes/promotion_patch_m25_2.py \
  tools/runes/smoke_m25_3_promotion_patch.py \
  tools/runes/runes.py

python3 tools/runes/smoke_m25_3_promotion_patch.py | tee /tmp/m25_4_smoke.json

python3 - <<'PY'
import json
from pathlib import Path

report = json.loads(Path("/tmp/m25_4_smoke.json").read_text(encoding="utf-8"))
if report.get("status") != "PASS":
    raise SystemExit("M25.4 lock blocked: M25.3 smoke is not PASS")
if report.get("failed") != 0:
    raise SystemExit("M25.4 lock blocked: smoke failed count is not zero")
print(f"M25.4 smoke confirmation: PASS failed={report.get('failed')} total={report.get('total')}")
PY

grep -n "PASS / STABLE DRY-RUN BASELINE\|stable governed forge-preview baseline\|M25.3 Curated Promotion Patch smoke test" \
  wiki/k6-freelancer/verification-m25-curated-promotion-preview.md

grep -n "M25.4 Roadmap / Verification Lock\|M25 STABLE DRY-RUN BASELINE\|M26 Human-approved Promotion Apply" \
  wiki/k6-freelancer/roadmap.md

git add \
  wiki/k6-freelancer/verification-m25-curated-promotion-preview.md \
  wiki/k6-freelancer/roadmap.md

git diff --cached

git commit -m "Lock M25 curated promotion patch baseline"

git push origin main

git log --oneline -5
