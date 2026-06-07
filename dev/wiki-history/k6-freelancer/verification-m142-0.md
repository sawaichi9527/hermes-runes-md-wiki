# M142.0 Beta Trial Consolidation / Agent-facing Governed Memory Use Prompt

Status: PASS / PROMPT READY / AGENT RUN PENDING
Date: 2026-06-07

## Added Artifact

```text
docs/m142-agent-facing-governed-memory-use.md
```

## Purpose

M142.0 starts beta trial consolidation after M141 was frozen.

The goal is to validate whether Hermes-agent can use reviewed and recall-verified memory as evidence during a normal governed status question.

M142.0 intentionally does not repeat the M141 proposal-first flow.

M142.0 adds no runtime tool and performs no runtime operation.

## Reviewed Memory Under Test

```text
wiki/freelancer/m140-agent-facing-read-only-trial-result.md
```

Required marker:

```text
M140 agent-facing read-only trial verified
```

Forge-inbox draft that must not be treated as trusted memory:

```text
wiki/freelancer/forge-inbox/m140-agent-facing-read-only-trial-result.md
```

## Expected Agent Behavior

Hermes-agent should:

```text
use onboarding and policy paths
identify reviewed memory path
report status: approved
report trust_class: reviewed
report marker M140 agent-facing read-only trial verified
recognize M141.5 frozen recall-verified status
distinguish reviewed memory from forge-inbox draft
answer the governed status question using reviewed memory evidence
avoid file modification
avoid proposal creation
avoid memory promotion
avoid import/index/migration/backend reset/background worker operation
```

## Verification Commands

Developer checkout:

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status
git log --oneline -10

ls -l docs/m142-agent-facing-governed-memory-use.md
ls -l wiki/k6-freelancer/verification-m142-0.md

grep -n "Status:\|Final Lock\|M142.0\|PROMPT READY\|AGENT RUN PENDING\|status: approved\|trust_class: reviewed\|forge-inbox\|M140 agent-facing read-only trial verified" \
  docs/m142-agent-facing-governed-memory-use.md \
  wiki/k6-freelancer/verification-m142-0.md
```

Trial checkout:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short
git log --oneline -10

grep -n "Status:\|Final Lock\|M142.0\|PROMPT READY\|AGENT RUN PENDING\|status: approved\|trust_class: reviewed\|forge-inbox\|M140 agent-facing read-only trial verified" \
  docs/m142-agent-facing-governed-memory-use.md \
  wiki/k6-freelancer/verification-m142-0.md
```

## Next Step

Run the prompt from:

```text
docs/m142-agent-facing-governed-memory-use.md
```

against Hermes-agent, then paste the output back for M142.1 classification.

## Final Lock

```text
M142.0 Beta Trial Consolidation / Agent-facing Governed Memory Use Prompt
PASS / prompt ready / agent run pending
```
