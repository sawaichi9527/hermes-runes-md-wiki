# M30.7 Pre-release Smoke Suite

Status: M30.7 PLAN / NO SCRIPT CHANGE
Milestone: M30.7 Pre-release Smoke Suite
Chinese: M30.7 預發佈冒煙測試套件
Runes Narrative Phrase: Runes Consistency Verified / 符文一致性驗證完成

## Purpose

M30.7 defines the pre-release smoke suite required before M30 moves from planning/policy into any actual code cleanup, wrapper addition, archive movement, or P0 trial-run start.

This milestone is a smoke-suite design document only.

It does not modify existing smoke scripts, CLI behavior, runtime behavior, or trusted wiki content beyond this document.

## Design Principle

```text
Test the governed memory contract before changing structure.
```

Chinese summary:

```text
先驗證治理記憶契約，再整理程式結構。
```

The smoke suite should stay personal-use scale:

```text
small
fast enough for local use
clear failure reason
no enterprise CI dependency required
no heavy observability stack
```

## Smoke Suite Goals

M30.7 smoke coverage should protect:

- repository baseline sanity
- Runes Seal rollback anchor awareness
- Python compile sanity
- controlled apply safety boundary
- importer refresh boundary
- strict recall verification behavior
- negative recall behavior
- retrieval consistency
- scenario regression behavior
- entrypoint availability
- narrative policy presence
- latency observation policy presence
- no secret leakage into tracked docs

## Smoke Classes

M30.7 defines these smoke classes:

```text
S0 repository/static sanity
S1 Python compile sanity
S2 core memory smoke
S3 governed apply/refresh/recall smoke
S4 scenario regression smoke
S5 entrypoint surface smoke
S6 documentation/policy presence smoke
S7 safety invariant smoke
```

## S0 Repository / Static Sanity

Purpose:

```text
Confirm repository is in expected pre-release baseline state.
```

Candidate checks:

```text
git status visibility
git log latest commit visibility
required wiki docs exist
required bin entrypoints exist
required tools directories exist
Runes Seal branch is documented
```

Expected result:

```text
PASS when required files and anchors are visible.
```

## S1 Python Compile Sanity

Purpose:

```text
Catch syntax errors before runtime smoke.
```

Candidate commands:

```text
python -m py_compile tools/importer/*.py
python -m py_compile tools/runes/*.py
```

Notes:

```text
M30.7 should not require every archived or local-only helper to compile unless it is part of active P0 flow.
```

Expected result:

```text
PASS for active P0 runtime/helper files.
```

## S2 Core Memory Smoke

Purpose:

```text
Verify existing memory smoke still passes.
```

Candidate command:

```text
./bin/hermes-memory-smoke
```

Expected result:

```text
PASS when the existing smoke runner succeeds.
```

## S3 Governed Apply / Refresh / Recall Smoke

Purpose:

```text
Protect the P0 governed memory lifecycle.
```

Required behavior:

```text
controlled apply remains explicit
refresh remains explicit
recall verification checks actual results only
operation records remain generated
rollback snapshots remain generated when apply mutates trusted wiki
```

Candidate checks:

```text
M29.1 add knowledge scenario
M29.3 correction/update scenario
M28.3 strict recall verification
M28.4 retrieval consistency smoke
```

Expected result:

```text
PASS when trusted mutation, refresh, and recall verification remain governed and verifiable.
```

## S4 Scenario Regression Smoke

Purpose:

```text
Protect P0 pre-trial scenario pack behavior.
```

Required scenarios:

```text
M29.1 Add Knowledge Scenario
M29.2 Reject / No-promotion Scenario
M29.3 Correction / Update Scenario
```

Expected result:

```text
M29.1 PASS
M29.2 PASS with rejected marker absent from trusted recall
M29.3 PASS
```

Notes:

```text
M29.2 inner recall miss may appear as an expected negative signal.
The scenario runner should interpret that as success only when the rejected marker remains absent.
```

## S5 Entrypoint Surface Smoke

Purpose:

```text
Confirm current stable entrypoints remain available before consolidation work.
```

Required entrypoints:

```text
bin/runes
bin/hermes-recall
bin/hermes-memory-smoke
```

Candidate checks:

```text
test -x bin/runes
test -x bin/hermes-recall
test -x bin/hermes-memory-smoke
```

Future checks after wrappers are added:

```text
bin/runes --help
bin/runes recall verify --help
bin/runes refresh importer --help
bin/runes apply controlled --help
```

M30.7 does not require future wrappers to exist yet.

## S6 Documentation / Policy Presence Smoke

Purpose:

```text
Ensure M30 policy layer remains present and searchable.
```

Required documents:

```text
wiki/k6-freelancer/pre-release-hardening.md
wiki/k6-freelancer/naming-policy.md
wiki/k6-freelancer/file-header-metadata-standard.md
wiki/k6-freelancer/multi-layer-naming-narrative-model.md
wiki/k6-freelancer/perceived-latency-observation-policy.md
wiki/k6-freelancer/entrypoint-consolidation-plan.md
wiki/k6-freelancer/code-risk-review.md
wiki/k6-freelancer/legacy-archive-deprecation-plan.md
```

Required markers:

```text
Runes Shield
Runes Aura Sense
Runes Forge Success
no code change
no runtime change
no file movement
```

Expected result:

```text
PASS when required docs and key policy markers exist.
```

## S7 Safety Invariant Smoke

Purpose:

```text
Protect non-negotiable safety/governance constraints.
```

Required invariants:

```text
no real secrets in wiki docs
no autonomous trusted memory writer claim
no hidden trusted wiki mutation policy
no recall verification weakening
no archive/deletion without classification
no enterprise observability requirement
```

Candidate grep checks:

```text
grep -R "API_KEY\|TOKEN\|PASSWORD\|SECRET" wiki/ || true
grep -R "autonomous trusted" wiki/k6-freelancer/*.md || true
grep -R "no-code-change\|no runtime change\|no file movement" wiki/k6-freelancer/*.md
```

Important:

```text
Secret grep is only a coarse smoke check.
It does not replace human review.
```

## Pre-release Smoke Runner Direction

Future M30.8/M30.9 may add a single smoke runner such as:

```text
bin/runes smoke p0-preflight
```

or:

```text
tools/runes/smoke_p0_preflight.py
```

M30.7 does not implement it.

Recommended future behavior:

```text
run S0-S7 checks
print short PASS/FAIL summary
emit JSON output optionally
avoid writing trusted wiki
avoid requiring network access
avoid requiring heavyweight services unless explicitly testing retrieval/importer
```

## Runes Narrative Mapping

If user-facing narrative is later added, smoke results may use:

```text
Runes Consistency Verified / 符文一致性驗證完成
Runes Consistency Disturbed / 符文一致性受擾
Runes Aura Stable / 符文靈氣穩定
Runes Aura Thin / 符文靈氣稀薄
```

Rules:

```text
Ritual phrase must be paired with plain PASS/FAIL evidence.
Ritual phrase must not hide failure reason.
```

## Recommended Execution Order

Suggested manual pre-release smoke order:

```text
1. git status / current branch visibility
2. Python compile active helpers
3. ./bin/hermes-memory-smoke
4. M28.3 strict recall verification smoke
5. M28.4 retrieval consistency smoke
6. M29.1 add knowledge scenario
7. M29.2 reject/no-promotion scenario
8. M29.3 correction/update scenario
9. entrypoint executable checks
10. policy document marker checks
```

## M30.7 Does Not Authorize

M30.7 does not authorize:

- new smoke runner implementation
- CLI change
- file movement
- archive movement
- deletion
- runtime replacement
- daemonization
- automatic latency logging
- enterprise CI requirement

Implementation should follow later only after this smoke design is accepted.

## Verification Status

M30.7 Pre-release Smoke Suite:

- smoke suite goals defined: PASS
- S0 repository/static sanity defined: PASS
- S1 Python compile sanity defined: PASS
- S2 core memory smoke defined: PASS
- S3 governed apply/refresh/recall smoke defined: PASS
- S4 scenario regression smoke defined: PASS
- S5 entrypoint surface smoke defined: PASS
- S6 documentation/policy presence smoke defined: PASS
- S7 safety invariant smoke defined: PASS
- future smoke runner direction defined: PASS
- no-script-change boundary preserved: PASS

Overall:

M30.7 Pre-release Smoke Suite:
PASS / smoke suite design defined / no script change performed
