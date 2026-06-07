# Runtime / Tool Legacy Sweep

Status: PARTIAL / SWEEP CLASSIFIED / LOCAL PATCH REQUIRED
Date: 2026-06-07
Milestone: M211

## Purpose

Classify active runtime and tool references that still use legacy `k6-freelancer` or old trial checkout paths after M210 cleaned the public starter path.

## Result

```text
sweep_status: PARTIAL
release_tag_ready: no
public_tester_notification_ready: no
planned_tag: v0.1.0-beta.1
tag_status: blocked
```

## Why Partial

Direct GitHub connector replacement attempts for active Python helper files were blocked by the connector safety layer. The sweep therefore records the exact remaining local patch targets and defers executable cleanup to the next local-patch milestone.

## Already Safe From Earlier Milestones

```text
config/hermes-memory.yaml: default_project is freelancer
bin/hermes-memory-check: default fallback is freelancer
bin/hermes_memory_common.py: default fallback is freelancer
README.md: starter guide linked
docs/open-beta-starter.md: public starter path added
tools/importer/.env.example: starter path updated
templates/* starter records: updated to freelancer / ~/workspace/trial
```

## Active Runtime / Tool Targets Still Requiring Local Patch

```text
tools/importer/importer_preview.py
tools/importer/forge.py
tools/importer/forge/create_flat.py
tools/importer/memory_answer_generator.py
tools/importer/context_builder_v2.py
tools/importer/memory_adapter.py
tools/importer/eval/local_eval_set.yaml
tools/importer/eval/run_local_eval.py
tools/importer/smoke/*.py where used as public smoke entrypoints
tools/runes/runes.py
tools/runes/scenario_*.py
tools/local_tools/hermes_memory_tools.py
```

## Remediation Rules

```text
1. Public default project should be freelancer.
2. Legacy k6-freelancer may remain only when explicitly labeled legacy engineering history.
3. Smoke/eval files may keep legacy checks only when profile name says legacy.
4. Public starter commands must not require wiki/k6-freelancer.
5. Old ~/workspace-trial path should not appear in active public starter templates.
```

## Required Next Milestone

```text
M212 Runtime Tool Local Patch / Verification
```

M212 should be implemented from the local checkout with a small Python patch script, then compiled/smoked locally and pushed.

## Final Lock

```text
M211 Runtime Tool Legacy Sweep
PARTIAL / classified / local patch required / first tag remains blocked
```
