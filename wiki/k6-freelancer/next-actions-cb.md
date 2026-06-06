# Closed Beta Next Actions

Status: ACTIVE / M158 PROPOSAL-FIRST SESSION READY
Date: 2026-06-07

## Current Stage

```text
M158 Proposal-first CB Session
PASS / proposal-first session record ready / real agent run pending
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
M156 PASS / trial-root discipline verified / read-only
M156.1 PASS / registry restored / fix applied
M157 PASS / read-only technical analysis verified / proposal-first boundary preserved
```

## Prepared Remaining CB Evidence Ladder

```text
M158 PASS / proposal-first session record ready / real agent run pending
M159 PASS / reject-defer prompt ready / real agent run pending
M160 PASS / human-approved promotion prompt ready / real agent run pending
M161 PASS / post-promotion recall prompt ready / real agent run pending
M162 PASS / observation review plan ready / evidence accumulation pending
M163 PASS / CB mini baseline plan ready / early CB results pending
```

## M158 Files

```text
docs/cb-m158-proposal-first-draft-prompt.md
wiki/k6-freelancer/verification-m158.md
wiki/k6-freelancer/cb-sessions/cb-20260607-m158-proposal-first.md
```

## Current Open CB Bug Records

```text
TB-20260607-001 OPEN / M156 trial-root quote typo
TB-20260607-002 OPEN / registry restore follow-up recorded; fix commit exists: 2e8b8bd
TB-20260607-003 OPEN / M157 prompt path initially resolved outside repo before fallback
TB-20260607-004 OPEN / placeholder append path caused local append failure
```

## M158 Path Rule

Use trial-root absolute prompt path during Hermes-agent execution:

```text
/home/eye/workspace-trial/hermes-runes-md-wiki/docs/cb-m158-proposal-first-draft-prompt.md
```

This explicitly checks whether TB-20260607-003 repeats.

## Immediate Next Action

Pull the M158 session record, then run Hermes-agent with explicit consent for draft-only proposal preparation.

Developer checkout:

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status
git log --oneline -12

for f in \
  docs/cb-m158-proposal-first-draft-prompt.md \
  wiki/k6-freelancer/verification-m158.md \
  wiki/k6-freelancer/cb-sessions/cb-20260607-m158-proposal-first.md \
  wiki/k6-freelancer/next-actions-cb.md; do
  echo "== $f =="
  grep -n "Status:\|Final Lock\|M158\|PROPOSAL-FIRST\|Session Input\|Agent Path\|Actual Behavior\|Observation Evidence\|Boundary Check\|PASS /" "$f"
done
```

Trial checkout:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short

ls -l docs/cb-m158-proposal-first-draft-prompt.md
ls -l wiki/k6-freelancer/verification-m158.md
ls -l wiki/k6-freelancer/cb-sessions/cb-20260607-m158-proposal-first.md
```

## M158 Execution Input

Use a low-risk sample and explicitly allow draft-only proposal preparation.

Suggested structure:

```text
Here is a low-risk technical sample for M158 proposal-first validation:
<technical sample>

I explicitly consent to draft-only proposal preparation for this test.
Please follow /home/eye/workspace-trial/hermes-runes-md-wiki/docs/cb-m158-proposal-first-draft-prompt.md.
Do not promote memory.
Do not modify trusted wiki.
Do not run import or index refresh.
```

## Next Candidate Milestone

```text
M158 Result Lock
```

After Hermes-agent output is available, update the M158 session record and classify the result as PASS / PARTIAL / BLOCKED / FAIL.
