# M151 Closed Beta Entry Criteria Lock

Status: PASS / CB ENTRY CRITERIA LOCKED / PERSONAL-SCOPE EARLY TEST READY
Date: 2026-06-07

## Scope

M151 locks the entry criteria for the first Closed Beta / CB run.

The CB target is a small, controlled, early-play / early-test stage for specific or limited testers. It is not a public beta, enterprise rollout, or production service launch.

## Entry Criteria

CB may start when the following are true:

```text
M147 post-trial baseline is locked
M148 observation evidence path is available
M149 model endpoint policy is decided
M150 minimal smoke bundle is defined
trial workspace can be pulled and checked locally
trusted memory mutation remains human-reviewed
Hermes-agent interaction remains agent-facing, not agent-owned
```

## Required Operating Mode

```text
Hermes-agent may read guidance and evidence.
Hermes-agent may draft proposals or status summaries.
Hermes-agent may support governed recall and answer generation.
Hermes-agent must not directly mutate trusted wiki memory.
Hermes-agent must not promote memory without human approval.
Hermes-agent must not bypass Runes Shield governance.
```

## Tester Boundary

CB testers should be treated as limited trusted early testers, not general public users.

```text
small number of testers
manual review expected
local/private endpoint variation allowed
observation notes expected
failures treated as evidence, not production incidents
simple recovery over automated orchestration
```

## Required Evidence Per CB Session

Each meaningful CB session should record at least:

```text
session purpose
workspace / trial root
agent path used
whether proposal-first behavior was followed
whether trusted mutation boundary was preserved
whether observation record/log was produced
whether model endpoint was configured, skipped, or unstable
human reviewer decision if any memory promotion is proposed
```

## Blockers

CB should not start or should be paused if any of these occur:

```text
trusted wiki mutation without human approval
secret value written into wiki/git/logs
agent claims background work or hidden mutation
trial workspace points to wrong root
core import/recall path fails without explanation
observation path is unavailable for meaningful sessions
Runes Shield boundary is bypassed
```

## Non-blockers

The following do not block CB entry:

```text
model endpoint not configured
model-dependent smoke SKIP
OpenClaw runtime unavailable
enterprise telemetry unavailable
multi-user concurrency not implemented
public documentation polish incomplete
large-scale answer-quality benchmark absent
```

## Final Entry Decision

```text
Closed Beta Entry
READY / allowed to start controlled CB run after local pull and smoke verification
```

## Verification Commands

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status

grep -n "Status:\|M151\|CB ENTRY\|Entry Criteria\|Blockers\|Non-blockers\|READY" \
  wiki/k6-freelancer/verification-m151.md
```

## Final Lock

```text
M151 Closed Beta Entry Criteria Lock
PASS / CB entry criteria locked / personal-scope early test ready
```
