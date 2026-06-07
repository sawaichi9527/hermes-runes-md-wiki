# M30.9 Manual Pre-release Smoke Run

Status: M30.9 MANUAL SMOKE PLAN / NO RUNNER IMPLEMENTED
Milestone: M30.9 Manual Pre-release Smoke Run
Chinese: M30.9 手動預發佈冒煙測試
Runes Narrative Phrase: Runes Trial Circle Prepared / 符文試煉環準備完成

## Purpose

M30.9 defines a manual smoke-run procedure for validating the current pre-release baseline before implementation-level hardening begins.

This milestone provides commands and expected markers only.

It does not implement a new smoke runner.

## Scope

M30.9 covers the M30.7 S0-S7 smoke classes:

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

## Important Execution Notes

This is a manual smoke run.

Before running commands:

```text
Do not paste shell prompts.
Do not paste previous command output back into shell.
Run one command block at a time.
Review output before continuing.
```

Expected current reality:

```text
The active local workspace may still be dirty.
That is acceptable for M30.9 as long as the dirty state is already captured by M29.6 inventory and pre-M30 local backup.
```

## S0 Repository / Static Sanity

Commands:

```bash
cd ~/workspace/hermes-runes-md-wiki

printf '== HEAD ==\n'
git log --oneline -5

printf '\n== status short ==\n'
git status --short

printf '\n== required docs ==\n'
for f in \
  wiki/k6-freelancer/verification-m29-p0-pretrial-runes-seal.md \
  wiki/k6-freelancer/pre-release-hardening.md \
  wiki/k6-freelancer/naming-policy.md \
  wiki/k6-freelancer/file-header-metadata-standard.md \
  wiki/k6-freelancer/multi-layer-naming-narrative-model.md \
  wiki/k6-freelancer/perceived-latency-observation-policy.md \
  wiki/k6-freelancer/entrypoint-consolidation-plan.md \
  wiki/k6-freelancer/code-risk-review.md \
  wiki/k6-freelancer/legacy-archive-deprecation-plan.md \
  wiki/k6-freelancer/pre-release-smoke-suite.md \
  wiki/k6-freelancer/verification-m30-pre-release-hardening-status-lock.md; do
  test -f "$f" && echo "PASS $f" || echo "FAIL $f"
done
```

PASS expectation:

```text
All required docs show PASS.
Dirty git status may exist but must be understood as captured local technical debt.
```

## S1 Python Compile Sanity

Commands:

```bash
cd ~/workspace/hermes-runes-md-wiki

python -m py_compile \
  tools/runes/scenario_add_knowledge_m29_1.py \
  tools/runes/scenario_reject_m29_2.py \
  tools/runes/scenario_correction_update_m29_3.py \
  tools/runes/recall_verify_m28_3.py \
  tools/runes/retrieval_consistency_m28_4.py
```

PASS expectation:

```text
No Python syntax errors.
```

## S2 Core Memory Smoke

Command:

```bash
cd ~/workspace/hermes-runes-md-wiki

./bin/hermes-memory-smoke
```

PASS expectation:

```text
Existing core smoke runner reports PASS.
```

If this fails:

```text
Stop and inspect before continuing.
Do not start refactor until core smoke is understood.
```

## S3 Governed Apply / Refresh / Recall Smoke

Recommended low-impact verification uses existing recall/retrieval smoke rather than additional trusted wiki mutation.

Commands:

```bash
cd ~/workspace/hermes-runes-md-wiki

python tools/runes/recall_verify_m28_3.py \
  "controlled trusted wiki mutation baseline" \
  --project k6-freelancer \
  --expected-path wiki/k6-freelancer/verification-m27-human-approved-apply-mvp.md \
  --required-marker "CONTROLLED TRUSTED WIKI MUTATION BASELINE" \
  --limit 5 \
  --write-record \
  --json

python tools/runes/retrieval_consistency_m28_4.py \
  --project k6-freelancer \
  --limit 5 \
  --write-record \
  --json
```

PASS expectation:

```text
recall_verify_m28_3.py reports status PASS.
retrieval_consistency_m28_4.py reports status PASS.
```

## S4 Scenario Regression Smoke

These commands may append additional scenario evidence to the dedicated scenario target.

Run only if acceptable:

```bash
cd ~/workspace/hermes-runes-md-wiki

python tools/runes/scenario_add_knowledge_m29_1.py \
  --apply \
  --refresh \
  --verify-recall \
  --write-records \
  --json

python tools/runes/scenario_reject_m29_2.py \
  --verify-recall \
  --write-records \
  --json

python tools/runes/scenario_correction_update_m29_3.py \
  --apply \
  --refresh \
  --verify-recall \
  --write-records \
  --json
```

PASS expectation:

```text
M29.1 scenario reports status PASS.
M29.2 scenario reports status PASS with rejected marker absent from trusted recall.
M29.3 scenario reports status PASS.
```

Note:

```text
M29.2 inner recall miss is expected.
The outer scenario result should still be PASS.
```

## S5 Entrypoint Surface Smoke

Commands:

```bash
cd ~/workspace/hermes-runes-md-wiki

for f in bin/runes bin/hermes-recall bin/hermes-memory-smoke; do
  test -x "$f" && echo "PASS executable $f" || echo "FAIL executable $f"
done
```

PASS expectation:

```text
All current stable entrypoints are executable.
```

## S6 Documentation / Policy Presence Smoke

Commands:

```bash
cd ~/workspace/hermes-runes-md-wiki

grep -n "Runes Shield" wiki/k6-freelancer/*.md | head -20
grep -n "Runes Aura Sense" wiki/k6-freelancer/*.md
grep -n "Runes Forge Success" wiki/k6-freelancer/*.md
grep -n "no code change\|no runtime change\|no file movement\|no CLI change" wiki/k6-freelancer/*.md | head -40
```

PASS expectation:

```text
Required policy/narrative markers are present.
```

## S7 Safety Invariant Smoke

Commands:

```bash
cd ~/workspace/hermes-runes-md-wiki

printf '== possible secret markers in wiki ==\n'
grep -RIn "API_KEY\|TOKEN\|PASSWORD\|SECRET" wiki/ || true

printf '\n== autonomous trusted wording check ==\n'
grep -RIn "autonomous trusted" wiki/k6-freelancer/*.md || true

printf '\n== strict recall wording check ==\n'
grep -RIn "strict retrieval-result-only\|strict recall-result-only\|retrieval-result-only" wiki/k6-freelancer/*.md || true
```

PASS expectation:

```text
No real secrets should appear.
Any SECRET/TOKEN hits must be policy examples, not actual values.
No document should authorize autonomous trusted memory writing.
Strict recall verification wording should remain present.
```

## Manual Smoke Result Template

After running the smoke commands, record a short summary in the conversation or a local note:

```text
M30.9 Manual Pre-release Smoke Run

S0 repository/static sanity: PASS/FAIL
S1 Python compile sanity: PASS/FAIL
S2 core memory smoke: PASS/FAIL
S3 governed apply/refresh/recall smoke: PASS/FAIL
S4 scenario regression smoke: PASS/FAIL/SKIPPED
S5 entrypoint surface smoke: PASS/FAIL
S6 documentation/policy presence smoke: PASS/FAIL
S7 safety invariant smoke: PASS/FAIL

Notes:
- <important observations>
```

## Mutation Awareness

S0, S1, S2, S3, S5, S6, and S7 are intended to be low or non-mutating, except operation records may be written when `--write-record` is used.

S4 may mutate the dedicated scenario target:

```text
wiki/k6-freelancer/p0-trial-scenarios.md
```

This is acceptable only because it is the dedicated scenario target created for P0 pre-trial validation.

## M30.9 Does Not Authorize

M30.9 does not authorize:

- new smoke runner implementation
- CLI change
- code refactor
- file movement
- archive movement
- deletion
- daemonization
- runtime replacement
- automatic latency logging

## Verification Status

M30.9 Manual Pre-release Smoke Run:

- manual S0-S7 command list defined: PASS
- PASS expectations defined: PASS
- mutation awareness documented: PASS
- scenario regression caveat documented: PASS
- result template defined: PASS
- no-runner boundary preserved: PASS

Overall:

M30.9 Manual Pre-release Smoke Run:
PASS / manual smoke procedure defined / no runner implemented
