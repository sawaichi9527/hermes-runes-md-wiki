# CB-20260607-M210 Starter Path Cleanup

Status: PASS / STARTER PATH CLEANED / FIRST TAG STILL BLOCKED
Date: 2026-06-07
Milestone: M210
Stage: Open Beta Publication

## Purpose

Clean the public Open Beta starter path after M209 found remaining legacy references.

## Updated Files

```text
README.md
docs/open-beta-starter.md
docs/open-beta-publication-checklist.md
tools/importer/.env.example
templates/external-agent-trial-evidence.md
templates/hermes-agent-governed-trial-run-dry-run-record.md
templates/trial-observation-record.md
```

## Starter Path Decision

```text
main_checkout: ~/workspace/hermes-runes-md-wiki
clean_trial_checkout: ~/workspace/trial/hermes-runes-md-wiki
workspace_slug: freelancer
wiki_namespace: wiki/freelancer/
```

## Result

```text
starter_cleanup: PASS
release_tag_ready: no
public_tester_notification_ready: no
```

## Remaining Blocker

```text
Active runtime/tool legacy sweep remains required.
Some tools, smoke/eval files, and legacy command examples still reference k6-freelancer or the old trial path.
These need targeted cleanup or explicit legacy labeling before v0.1.0-beta.1 tag.
```

## Decision

```text
Do not create v0.1.0-beta.1 tag yet.
Proceed to runtime/tool legacy sweep before release lock.
```

## Final Lock

```text
M210 Starter Path Cleanup
PASS / starter path cleaned / first tag blocked until runtime-tool sweep
```
