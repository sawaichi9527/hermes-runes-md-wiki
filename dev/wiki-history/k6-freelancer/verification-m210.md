# M210 Starter Path Cleanup

Status: PASS / STARTER PATH CLEANED / FIRST TAG STILL BLOCKED
Date: 2026-06-07

## Evidence Record

```text
wiki/k6-freelancer/cb-sessions/cb-20260607-m210-starter-path-cleanup.md
README.md
docs/open-beta-starter.md
docs/open-beta-publication-checklist.md
tools/importer/.env.example
templates/external-agent-trial-evidence.md
templates/hermes-agent-governed-trial-run-dry-run-record.md
templates/trial-observation-record.md
```

## Scope

```text
public starter path cleanup
trial checkout path cleanup
workspace slug defaults in public templates
no broad historical evidence rewrite
```

## Result

```text
PASS for starter cleanup
```

## Starter Path

```text
main_checkout: ~/workspace/hermes-runes-md-wiki
clean_trial_checkout: ~/workspace/trial/hermes-runes-md-wiki
workspace_slug: freelancer
wiki_namespace: wiki/freelancer/
```

## Release Decision

```text
release_tag_ready: no
public_tester_notification_ready: no
planned_tag: v0.1.0-beta.1
tag_status: blocked
```

## Remaining Blocker

```text
Active runtime/tool legacy sweep remains required.
Some tools, smoke/eval files, and legacy command examples still reference k6-freelancer or the old trial path.
```

## Next Step

```text
M211 Runtime/Tool Legacy Sweep
```

## Final Lock

```text
M210 Starter Path Cleanup
PASS / starter path cleaned / v0.1.0-beta.1 tag blocked until runtime-tool sweep
```
