# M191 BT-001 Read-only Rerun / Evidence Capture

Status: PARTIAL / READ-ONLY OUTPUT OK / TRIAL PATH ISOLATION BUG
Date: 2026-06-07

## Evidence Record

```text
wiki/k6-freelancer/cb-sessions/cb-20260607-m191-bt001-read-only-rerun.md
docs/m191-bt001-hermes-agent-run-prompt.md
docs/m190-read-only-prompt-tightening.md
docs/cb-m191-m196-execution-pack.md
wiki/k6-freelancer/cb-bugs.md
```

## Scope

```text
BT-001 read-only rerun
Hermes-agent output capture
human reviewer classification
no new runtime feature development
```

## Result

```text
PARTIAL
```

## Acceptance Review

```text
PASS aspects:
- technical answer only
- no proposal-style content
- no YAML-style memory block
- no final_trial_result
- no M191 self-assigned PASS / FAIL / PARTIAL
- candidate_result: ready_for_human_review present

PARTIAL aspect:
- Hermes-agent read evidence from /home/eye/workspace/hermes-runes-md-wiki after /home/eye/freelancer path lookup failed
- this violates the intended CB/trial checkout isolation boundary
```

## Bug Handling

```text
opened: TB-M191-BT001-FU001
status: OPEN
summary: read-only output passed, but evidence source fell back to developer checkout instead of the intended trial checkout
rerun_required: true
```

## Next Step

```text
M191.1 Trial Path Isolation Prompt / Environment Rerun Prep
```

## Final Lock

```text
M191 BT-001 Read-only Rerun / Evidence Capture
PARTIAL / read-only output OK / trial path isolation bug recorded
```
