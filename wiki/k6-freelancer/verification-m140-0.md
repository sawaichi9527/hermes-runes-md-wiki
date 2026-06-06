# M140.0 Agent-facing Trial Prompt / Expected Behavior Lock

Status: PASS / PROMPT READY / AGENT RUN PENDING
Date: 2026-06-07

## Added Artifact

```text
docs/m140-agent-facing-trial-prompt.md
```

## Purpose

M140.0 returns the beta trial-run to the intended direction:

```text
validate Hermes-agent or another external agent against the existing Hermes Runes MD Wiki governance surface
```

M140.0 adds no runtime tool.

M140.0 performs no import, recall, migration, backend reset, proposal creation, or promotion.

## Trial Context

```text
workspace: freelancer
fixture id: TPF-20260606-M137
fixture path: wiki/freelancer/trial-promotion-fixtures.md
marker: M137 beta-prep trial promotion fixture marker
M139.2 status: PASS / trial verified / marker indexed
```

## Expected Agent Output

The agent should return a read-only governed status summary that identifies:

```text
onboarding path
workspace freelancer
fixture id TPF-20260606-M137
fixture path wiki/freelancer/trial-promotion-fixtures.md
recall marker M137 beta-prep trial promotion fixture marker
M139.2 PASS / trial verified / marker indexed
allowed next step
forbidden actions without explicit human approval
readiness for next agent-facing trial step
blockers, if any
```

## Verification Commands

Developer checkout:

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status
git log --oneline -8

ls -l docs/m140-agent-facing-trial-prompt.md
ls -l wiki/k6-freelancer/verification-m140-0.md

grep -n "Status:\|Final Lock\|M140.0\|PROMPT READY\|AGENT RUN PENDING\|TPF-20260606-M137\|M139.2" \
  docs/m140-agent-facing-trial-prompt.md \
  wiki/k6-freelancer/verification-m140-0.md
```

Trial checkout:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short
git log --oneline -8

grep -n "Status:\|Final Lock\|M140.0\|PROMPT READY\|AGENT RUN PENDING\|TPF-20260606-M137\|M139.2" \
  docs/m140-agent-facing-trial-prompt.md \
  wiki/k6-freelancer/verification-m140-0.md
```

## Next Step

Run the prompt from:

```text
docs/m140-agent-facing-trial-prompt.md
```

against Hermes-agent or the chosen external agent, then paste the agent output back for M140.1 classification.

## Final Lock

```text
M140.0 Agent-facing Trial Prompt / Expected Behavior Lock
PASS / prompt ready / agent run pending
```
