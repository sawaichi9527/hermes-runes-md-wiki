# Closed Beta Next Actions

Status: ACTIVE / M153 EVIDENCE CAPTURE READY
Date: 2026-06-07

## Current Stage

```text
M153 First Controlled CB Session Evidence Record
PASS / first CB session evidence capture ready / no new feature
```

## Locked CB-prep Chain

```text
M147 PASS / post-trial baseline locked / CB-prep roadmap set
M148 PASS / observation mechanism CB-ready / minimal evidence path locked
M149 PASS / model endpoint optional for CB entry
M150 PASS / CB smoke bundle defined / existing checks only
M151 PASS / CB entry criteria locked / personal-scope early test ready
M152 PASS / Closed Beta started / controlled CB mode active
M153 PASS / first CB session evidence capture ready / no new feature
```

## Immediate Next Action

Run local pull verification, then run the first real Hermes-agent CB session and fill the evidence record.

Developer checkout:

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status
git log --oneline -10

for f in \
  wiki/k6-freelancer/verification-m153.md \
  wiki/k6-freelancer/cb-sessions/cb-20260607-m153-first-session.md \
  wiki/k6-freelancer/next-actions-cb.md; do
  echo "== $f =="
  grep -n "Status:\|Final Lock\|M153\|FIRST CB SESSION\|Session Input\|Agent Path\|Actual Behavior\|Observation Evidence\|Boundary Check\|Next Action" "$f"
done
```

Trial checkout:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short

ls -l wiki/k6-freelancer/verification-m153.md
ls -l wiki/k6-freelancer/cb-sessions/cb-20260607-m153-first-session.md
```

## First CB Session Goal

The first CB session should run through the real user scenario with Hermes-agent:

```text
user gives technical information or asks for memory-backed analysis
Hermes-agent reads repo guidance and trusted memory
Hermes-agent stays inside Runes Shield governance
Hermes-agent produces a governed answer or proposal draft
human reviewer decides whether promotion is appropriate
observation evidence is recorded or explicitly classified as skipped
trusted wiki memory is not mutated directly by the agent
```

## Evidence Record To Fill

```text
wiki/k6-freelancer/cb-sessions/cb-20260607-m153-first-session.md
```

Required areas:

```text
Session Input
Agent Path
Actual Behavior
Observation Evidence
Human Review
Boundary Check
Session Result
```

## Highest-priority Evidence Gap

Observation remains the highest-priority CB evidence path.

```text
Collect enough real behavior evidence to tune sanitizer, prompt shape, model profile choice, and hardcoded heuristics later.
Do not build enterprise telemetry.
Do not ingest observation logs into trusted memory automatically.
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
M154 First CB Session Result Lock
```

M154 should update the M153 evidence record after the real Hermes-agent CB session and classify the result as PASS / PARTIAL / BLOCKED / FAIL.
