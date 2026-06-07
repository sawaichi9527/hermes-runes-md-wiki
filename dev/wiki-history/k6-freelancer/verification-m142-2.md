# M142.2 Trial Root Adherence Prompt Tightening

Status: PASS / PROMPT READY / AGENT RUN PENDING
Date: 2026-06-07

## Added Artifact

```text
docs/m142-trial-root-adherence-prompt.md
```

## Purpose

M142.2 tightens the agent-facing prompt after M142.1 recorded a root fallback warning.

The goal is to verify that Hermes-agent obeys the explicitly requested trial checkout root:

```text
~/workspace-trial/hermes-runes-md-wiki
```

and does not silently fall back to:

```text
~/workspace/hermes-runes-md-wiki
/home/eye/freelancer
```

## Required Behavior

Hermes-agent must:

```text
use ~/workspace-trial/hermes-runes-md-wiki as the only root
read every required file from the required root
return BLOCKED if any required file cannot be read from the required root
avoid fallback to developer checkout
avoid fallback to /home/eye/freelancer
avoid proposal creation
avoid promotion
avoid import/index/migration/backend reset/background worker operation
avoid wiki mutation
```

## Expected Classification

PASS only if:

```text
all required files were read from ~/workspace-trial/hermes-runes-md-wiki
no fallback root was used
reviewed memory status: approved
reviewed memory trust_class: reviewed
forge-inbox draft is distinguished from reviewed memory
no mutation occurred
```

BLOCKED if:

```text
any required file cannot be read from the required root
another root would be needed
```

## Verification Commands

Developer checkout:

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status
git log --oneline -10

ls -l docs/m142-trial-root-adherence-prompt.md
ls -l wiki/k6-freelancer/verification-m142-2.md

grep -n "Status:\|Final Lock\|M142.2\|PROMPT READY\|AGENT RUN PENDING\|workspace-trial\|fallback\|BLOCKED\|status: approved\|trust_class: reviewed" \
  docs/m142-trial-root-adherence-prompt.md \
  wiki/k6-freelancer/verification-m142-2.md
```

Trial checkout:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short
git log --oneline -10

grep -n "Status:\|Final Lock\|M142.2\|PROMPT READY\|AGENT RUN PENDING\|workspace-trial\|fallback\|BLOCKED\|status: approved\|trust_class: reviewed" \
  docs/m142-trial-root-adherence-prompt.md \
  wiki/k6-freelancer/verification-m142-2.md
```

## Next Step

Run the prompt from:

```text
docs/m142-trial-root-adherence-prompt.md
```

against Hermes-agent, then paste the output back for M142.3 classification.

## Final Lock

```text
M142.2 Trial Root Adherence Prompt Tightening
PASS / prompt ready / agent run pending
```
