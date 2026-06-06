# Closed Beta Next Actions

Status: ACTIVE / M147-M152 CB LINE STARTED
Date: 2026-06-07

## Current Stage

```text
M152 Closed Beta Run Start
PASS / Closed Beta started / controlled CB mode active
```

## Locked CB-prep Chain

```text
M147 PASS / post-trial baseline locked / CB-prep roadmap set
M148 PASS / observation mechanism CB-ready / minimal evidence path locked
M149 PASS / model endpoint optional for CB entry
M150 PASS / CB smoke bundle defined / existing checks only
M151 PASS / CB entry criteria locked / personal-scope early test ready
M152 PASS / Closed Beta started / controlled CB mode active
```

## Immediate Next Action

Run local pull and smoke verification in both developer and trial checkouts.

Developer checkout:

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status
git log --oneline -12

for f in \
  wiki/k6-freelancer/verification-m147.md \
  wiki/k6-freelancer/verification-m148.md \
  wiki/k6-freelancer/verification-m149.md \
  wiki/k6-freelancer/verification-m150.md \
  wiki/k6-freelancer/verification-m151.md \
  wiki/k6-freelancer/verification-m152.md \
  wiki/k6-freelancer/next-actions-cb.md; do
  echo "== $f =="
  grep -n "Status:\|Final Lock\|M147\|M148\|M149\|M150\|M151\|M152\|Closed Beta\|CB" "$f"
done
```

Trial checkout:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short

export HERMES_WORKSPACE_SLUG=freelancer
export HERMES_PROJECT=freelancer

./bin/hermes-memory-check
./bin/hermes-memory-smoke
```

## First CB Session Goal

The first CB session should run through the real user scenario with Hermes-agent:

```text
user gives technical information or asks for memory-backed analysis
Hermes-agent reads repo guidance and trusted memory
Hermes-agent stays inside Runes Shield governance
Hermes-agent produces a governed answer or proposal draft
human reviewer decides whether promotion is appropriate
observation evidence is recorded
trusted wiki memory is not mutated directly by the agent
```

## Highest-priority Evidence Gap

Observation is the highest-priority CB evidence path.

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
M153 First Controlled CB Session Evidence Record
```

M153 should capture the first real CB session result rather than add new functionality.
