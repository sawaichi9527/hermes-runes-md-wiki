# Closed Beta Next Actions

Status: ACTIVE / M156-M163 CB EVIDENCE LADDER READY
Date: 2026-06-07

## Current Stage

```text
M156-M163 Closed Beta Evidence Ladder
PASS / prompts and verification plans ready / real agent runs pending
```

## Locked CB Chain

```text
M147 PASS / post-trial baseline locked / CB-prep roadmap set
M148 PASS / observation mechanism CB-ready / minimal evidence path locked
M149 PASS / model endpoint optional for CB entry
M150 PASS / CB smoke bundle defined / existing checks only
M151 PASS / CB entry criteria locked / personal-scope early test ready
M152 PASS / Closed Beta started / controlled CB mode active
M153 PASS / first CB session evidence captured
M154 PASS / first CB session prompt ready / real agent run completed
M155 PASS / first CB session result locked / read-only governance verified
```

## Prepared CB Evidence Ladder

```text
M156 PASS / trial-root check prompt ready / real agent run pending
M157 PASS / technical input read-only prompt ready / real user sample pending
M158 PASS / proposal-first prompt ready / real agent run pending
M159 PASS / reject-defer prompt ready / real agent run pending
M160 PASS / human-approved promotion prompt ready / real agent run pending
M161 PASS / post-promotion recall prompt ready / real agent run pending
M162 PASS / observation review plan ready / evidence accumulation pending
M163 PASS / CB mini baseline plan ready / early CB results pending
```

## Immediate Next Action

Pull the M156-M163 evidence ladder and start with M156.

Developer checkout:

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status
git log --oneline -20

for f in \
  docs/cb-m156-m163-evidence-ladder.md \
  docs/cb-m156-trial-root-discipline-prompt.md \
  docs/cb-m157-technical-input-readonly-prompt.md \
  docs/cb-m158-proposal-first-draft-prompt.md \
  docs/cb-m159-reject-defer-path-prompt.md \
  docs/cb-m160-human-approved-promotion-prompt.md \
  docs/cb-m161-post-promotion-recall-prompt.md \
  wiki/k6-freelancer/verification-m156.md \
  wiki/k6-freelancer/verification-m157.md \
  wiki/k6-freelancer/verification-m158.md \
  wiki/k6-freelancer/verification-m159.md \
  wiki/k6-freelancer/verification-m160.md \
  wiki/k6-freelancer/verification-m161.md \
  wiki/k6-freelancer/verification-m162.md \
  wiki/k6-freelancer/verification-m163.md \
  wiki/k6-freelancer/next-actions-cb.md; do
  echo "== $f =="
  grep -n "Status:\|Final Lock\|M156\|M157\|M158\|M159\|M160\|M161\|M162\|M163\|PASS /" "$f"
done
```

Trial checkout:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short

ls -l docs/cb-m156-m163-evidence-ladder.md
ls -l docs/cb-m156-trial-root-discipline-prompt.md
ls -l wiki/k6-freelancer/verification-m156.md
ls -l wiki/k6-freelancer/verification-m163.md
```

## Recommended Execution Order

```text
M156: close or refine CB-WATCH-20260607-001
M157: run first real technical-input read-only analysis
M158: run proposal-first draft behavior check
M159: run review reject/defer behavior check
M160: run human-approved promotion path check
M161: run post-promotion recall / answer check
M162: review accumulated observation evidence
M163: lock first CB mini baseline
```

## Boundaries

```text
personal-local
small controlled early testers
manual review expected
model endpoint optional
no autonomous trusted writer
no automatic proposal apply
no background orchestration daemon
no enterprise monitoring stack
```

## Next Candidate Milestone

```text
M156 Result Lock
```

M156 should run the trial-root prompt through Hermes-agent and classify the result as PASS / PARTIAL / BLOCKED / FAIL.
