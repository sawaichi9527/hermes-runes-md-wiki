# M131 External Agent Trial Evidence Template

Status: PASS / TEMPLATE READY
Date: 2026-06-06

## Purpose

M131 prepares the reusable evidence template for future OpenClaw / non-Hermes local governed agent trials.

This milestone exists because M130 confirmed:

```text
Only Hermes-agent is available.
No OpenClaw runtime is available.
M125 remains IMPLEMENTED / PENDING.
Do not resume M125 yet.
```

M131 does not perform external runtime validation.

M131 does not mark M125 as PASS.

M131 only ensures that, when a real external runtime becomes available later, the operator has a complete evidence structure before running the trial.

## Added Artifact

M131 adds:

```text
templates/external-agent-trial-evidence.md
```

The template is intended for future trial records such as:

```text
wiki/k6-freelancer/trials/external-agent-trial-YYYYMMDD-<runtime>.md
```

## Evidence Coverage

The template requires the following evidence fields:

```text
trial metadata
runtime identity
runtime classification
pre-trial git pull / status / log evidence
exact prompt used
files read by the external agent
raw external agent output
required content checks
forbidden operation checks
post-trial git status evidence
operator assessment
final classification decision
```

This directly follows the evidence requirements recorded in M130.

## Runtime Classification Rules

Valid classifications remain:

```text
real OpenClaw runtime validation
OpenClaw-compatible shape validation with a clearly identified non-Hermes local governed agent
```

Invalid classification remains:

```text
Hermes-agent-only validation presented as OpenClaw-compatible third-party validation
```

## Read-only Boundary

The future trial must remain read-only.

Forbidden operations:

```text
file write
wiki mutation
proposal mutation
import/index
database mutation
apply/promote
runtime authority escalation
```

If any forbidden operation occurs, the future trial cannot be marked PASS.

## Required Repository Evidence

Before the external agent trial, the operator must record:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short
git log --oneline -5
```

Expected pre-trial state:

```text
no output from git status --short
```

After the external agent trial, the operator must record:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git status --short
```

Expected post-trial state:

```text
no output
```

## Required Content Checks

The future external agent output must be checked for:

```text
compact bootstrap path identification
local governed memory boundary summary
P0 durable-memory flow summary
forbidden operation summary
human-reviewed apply/promote boundary
read-only import/index/database boundary
regression checklist / smoke expectation
PASS freeze rule summary
avoidance of Hermes-agent-specific private behavior
```

## Relationship To M125

M125 remains:

```text
IMPLEMENTED / PENDING
```

M131 does not change the M125 state.

M125 can resume only when a real OpenClaw runtime or another clearly identified non-Hermes local governed agent runtime exists.

## Relationship To M130

M130 answered runtime availability.

M131 prepares evidence collection.

Together:

```text
M130: no external runtime available now
M131: future external-agent evidence template ready
```

## Verification

Static verification scope:

```text
artifact exists
evidence fields are explicit
runtime classification rules are explicit
read-only boundary is explicit
pre/post git status evidence is required
forbidden operations are enumerated
M125 remains pending
```

No runtime smoke is required because this is a documentation/template milestone.

## Final Lock

```text
M131 External Agent Trial Evidence Template
PASS / template ready / M125 remains pending
```
