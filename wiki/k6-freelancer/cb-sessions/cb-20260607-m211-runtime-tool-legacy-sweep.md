# CB-20260607-M211 Runtime Tool Legacy Sweep

Status: PARTIAL / CLASSIFIED / LOCAL PATCH REQUIRED
Date: 2026-06-07
Milestone: M211
Stage: Open Beta Publication

## Purpose

Sweep active runtime and tool legacy references after M210 starter path cleanup.

## Result

```text
runtime_tool_sweep: PARTIAL
release_tag_ready: no
public_tester_notification_ready: no
planned_tag: v0.1.0-beta.1
tag_status: blocked
```

## Direct Edit Note

```text
Direct GitHub connector replacements for some active Python helper files were blocked by the connector safety layer.
Therefore M211 records classification and defers executable cleanup to local patch verification.
```

## Already Clean / Prepared

```text
config/hermes-memory.yaml
bin/hermes-memory-check
bin/hermes_memory_common.py
README.md
docs/open-beta-starter.md
tools/importer/.env.example
templates/*.md starter records
```

## Local Patch Targets

```text
tools/importer/importer_preview.py
tools/importer/forge.py
tools/importer/forge/create_flat.py
tools/importer/memory_answer_generator.py
tools/importer/context_builder_v2.py
tools/importer/memory_adapter.py
tools/importer/eval/local_eval_set.yaml
tools/importer/eval/run_local_eval.py
tools/runes/runes.py
tools/runes/scenario_*.py
tools/local_tools/hermes_memory_tools.py
```

## Decision

```text
Do not create v0.1.0-beta.1 tag yet.
Do not notify public testers yet.
Proceed to local patch / verification milestone.
```

## Final Lock

```text
M211 Runtime Tool Legacy Sweep
PARTIAL / classified / first tag blocked until local patch verification
```
