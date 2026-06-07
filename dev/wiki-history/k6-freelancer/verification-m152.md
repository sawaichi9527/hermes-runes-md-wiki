# M152 Closed Beta Run Start

Status: PASS / CLOSED BETA STARTED / CONTROLLED CB MODE ACTIVE
Date: 2026-06-07

## Scope

M152 starts the Closed Beta / CB stage for Hermes Runes MD Wiki governed memory validation.

This is a controlled early-test stage for specific or limited testers. It is not a public launch and not an enterprise production rollout.

## Start Classification

```text
Closed Beta Stage
STARTED / controlled CB mode active
```

## Start Basis

```text
M147 PASS: post-trial baseline locked
M148 PASS: observation mechanism CB-ready
M149 PASS: model endpoint optional for CB entry
M150 PASS: minimal CB smoke bundle defined
M151 PASS: CB entry criteria locked
```

## CB Operating Principle

```text
Run real usage through Hermes-agent where possible.
Use Runes Shield governance as the boundary.
Use proposal-first persistence.
Require human approval for trusted memory promotion.
Keep observation lightweight and evidence-oriented.
Treat failures as tuning evidence.
Avoid new feature development unless CB evidence proves the need.
```

## First CB Session Target

The first CB session should validate the user-facing scenario rather than add new tooling:

```text
User provides technical information or asks for memory-backed analysis.
Hermes-agent reads current repo guidance and trusted memory.
Hermes-agent produces a governed answer or proposal draft.
Human reviewer decides whether anything should be promoted.
Observation evidence is recorded for later sanitizer/prompt/model-profile tuning.
Trusted wiki files are not mutated directly by the agent.
```

## Required Session Record

A CB session record should include:

```text
session id / date
input category
workspace and root used
agent behavior summary
proposal or read-only answer outcome
observation evidence location
model endpoint classification: configured / skipped / unstable
human review result if promotion is involved
boundary issues, if any
```

## Current Known Constraints

```text
model endpoint remains optional
OpenClaw real external runtime remains wait-state
CB is personal-local and small-scope
observation evidence is required for useful tuning
no enterprise telemetry or orchestration is introduced
```

## Stop / Pause Conditions

Pause CB if any of these occur:

```text
secret leakage into wiki/git/logs
trusted memory mutation without human approval
agent bypasses Runes Shield governance
trial root confusion causes wrong workspace mutation
observation path cannot capture meaningful evidence
```

## Boundary Confirmation

```text
no new feature added by this milestone
no background worker started
no automatic proposal apply enabled
no autonomous trusted memory writer enabled
no enterprise monitoring added
no model endpoint secret committed
```

## Verification Commands

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
  wiki/k6-freelancer/verification-m152.md; do
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

## Final Lock

```text
M152 Closed Beta Run Start
PASS / Closed Beta started / controlled CB mode active
```
