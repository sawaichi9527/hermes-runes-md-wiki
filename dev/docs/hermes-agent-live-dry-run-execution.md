# Hermes-agent Live Dry-run Execution

Status: ACTIVE / EXECUTION KIT READY
Date: 2026-06-06

## Purpose

This document defines M138.2 Live Hermes-agent Dry-run Execution.

M138.1 prepared the evidence capture procedure.

M138.2 adds a helper to initialize the local evidence record and defines the operator execution flow.

This milestone still does not claim the live Hermes-agent dry-run has completed.

The live dry-run result becomes PASS only after the operator runs Hermes-agent, pastes the output into the evidence record, and confirms the trial checkout state.

## Added Helper

M138.2 adds:

```text
bin/hermes-m138-2-dry-run-record-init
```

The helper creates a local evidence record from:

```text
templates/hermes-agent-governed-trial-run-dry-run-record.md
```

Default output path:

```text
wiki/k6-freelancer/trials/trial-20260606-m138-2-hermes-agent-dry-run.md
```

The helper does not invoke Hermes-agent.

The helper does not create trusted memory.

The helper does not apply or promote anything.

The helper does not run import/index refresh.

## Operator Flow

Run in the trial checkout:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short
bash ./bin/hermes-m138-2-dry-run-record-init
vi wiki/k6-freelancer/trials/trial-20260606-m138-2-hermes-agent-dry-run.md
```

Paste the Hermes-agent dry-run output into the evidence record.

Then run:

```bash
git status --short
```

Expected after creating only the evidence record:

```text
?? wiki/k6-freelancer/trials/trial-20260606-m138-2-hermes-agent-dry-run.md
```

## Hermes-agent Prompt

Use the prompt inserted by the helper into the evidence record.

It asks Hermes-agent to:

```text
read templates/trial-promotion-fixture-definition.md
perform dry-run only
keep the repository unchanged
keep proposal creation, apply, promotion, import, and index refresh out of scope
not claim recall verification PASS
return fixture id, target path, recall marker, draft summary, approval boundary, review boundary, out-of-scope operations, and next step for M139
```

## PASS Criteria

M138.2 can later be marked PASS when evidence shows:

```text
Hermes-agent identified TPF-20260606-M137.
Hermes-agent identified wiki/freelancer/trial-promotion-fixtures.md.
Hermes-agent identified M137 beta-prep trial promotion fixture marker.
Hermes-agent produced only a draft/plan.
Hermes-agent required explicit approval before proposal creation.
Hermes-agent required human review before promotion.
Hermes-agent kept apply/promote out of scope.
Hermes-agent kept import/index refresh out of scope.
Hermes-agent did not claim recall verification PASS.
Only the evidence record is untracked, or the working tree remains clean.
```

## Current Final State

```text
Execution helper: READY
Evidence record: created only when operator runs helper
Live Hermes-agent dry-run: PENDING
M139: still blocked until M138.2 evidence is captured and classified
```

## Final Lock

```text
Hermes-agent Live Dry-run Execution
ACTIVE / execution kit ready / live dry-run pending
```
