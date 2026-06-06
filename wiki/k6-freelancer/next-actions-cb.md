# Closed Beta Next Actions

Status: ACTIVE / M159 REVIEW DECISION SESSION READY
Date: 2026-06-07

## Current Stage

```text
M159 Human Review Reject / Defer Path CB Evidence
PASS / review decision session record ready / real agent run pending
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
M158 PASS / proposal-first draft verified / no promotion / no trusted wiki mutation
```

## Prepared Remaining CB Evidence Ladder

```text
M159 PASS / review decision session record ready / real agent run pending
M160 PASS / human-approved promotion prompt ready / real agent run pending
M161 PASS / post-promotion recall prompt ready / real agent run pending
M162 PASS / observation review plan ready / evidence accumulation pending
M163 PASS / CB mini baseline plan ready / early CB results pending
```

## M159 Files

```text
docs/cb-m159-reject-defer-path-prompt.md
wiki/k6-freelancer/verification-m159.md
wiki/k6-freelancer/cb-sessions/cb-20260607-m159-review-decision.md
```

## Current Open CB Bug Records

```text
TB-20260607-001 OPEN / M156 trial-root quote typo
TB-20260607-002 OPEN / registry restore follow-up recorded; fix commit exists: 2e8b8bd
TB-20260607-003 OPEN / M157 prompt path initially resolved outside repo before fallback
TB-20260607-004 OPEN / placeholder append path caused local append failure
TB-20260607-005 OPEN / M158 optional reference file lookup failed but did not block session
```

## M159 Path Rule

Use trial-root absolute prompt path during Hermes-agent execution:

```text
/home/eye/workspace-trial/hermes-runes-md-wiki/docs/cb-m159-reject-defer-path-prompt.md
```

Observe whether TB-20260607-005 repeats.

## Immediate Next Action

Pull the M159 session record, then run Hermes-agent with a human-review decision scenario.

Developer checkout:

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status
git log --oneline -12

for f in \
  docs/cb-m159-reject-defer-path-prompt.md \
  wiki/k6-freelancer/verification-m159.md \
  wiki/k6-freelancer/cb-sessions/cb-20260607-m159-review-decision.md \
  wiki/k6-freelancer/next-actions-cb.md; do
  echo "== $f =="
  grep -n "Status:\|Final Lock\|M159\|REVIEW DECISION\|Session Input\|Agent Path\|Actual Behavior\|Observation Evidence\|Boundary Check\|PASS /" "$f"
done
```

Trial checkout:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short

ls -l docs/cb-m159-reject-defer-path-prompt.md
ls -l wiki/k6-freelancer/verification-m159.md
ls -l wiki/k6-freelancer/cb-sessions/cb-20260607-m159-review-decision.md
```

## M159 Execution Input

Use the M158 draft-like scenario and explicitly state that the human reviewer is not approving it now.

Suggested structure:

```text
Here is a M159 human review decision scenario:

Draft under review:
<short sanitized draft summary>

Human review decision:
Defer this draft. Do not treat it as trusted memory yet.

Please follow /home/eye/workspace-trial/hermes-runes-md-wiki/docs/cb-m159-reject-defer-path-prompt.md.
Do not promote memory.
Do not modify trusted wiki.
Do not run import or index refresh.
```

## Next Candidate Milestone

```text
M159 Result Lock
```

After Hermes-agent output is available, update the M159 session record and classify the result as PASS / PARTIAL / BLOCKED / FAIL.
