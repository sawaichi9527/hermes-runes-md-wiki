## B-20260531-M8 Local Agentic RAG Governance Baseline

Status: FROZEN
Scope: M8.3 ~ M8.5.2c

### Summary

* Hermes Memory has evolved from local RAG retrieval into local agentic RAG governance.
* The system now includes:

  * model-aware behavior profiles
  * extraction quality checks
  * deterministic retry policy decisions
* Retry execution is not yet enabled.
* Current baseline stops at deterministic retry decision metadata.

### Frozen baseline includes

* M8.3 JSONL observation governance baseline
* M8.4 Multi-model Governance Baseline
* M8.5.1 Local Extraction Quality Checker
* M8.5.2 Extraction Quality Metadata
* M8.5.2c Quality Signals and Retry Policy Split

---

## Architecture

```text
LLM output
  ↓
model profile selection
  ↓
profile-aware extraction
  ↓
extraction_quality.py
  ↓
retry_policy.py
  ↓
answer_generator metadata
  ↓
future: bounded compact retry executor
```

---

## Current Governance Metadata

* selected_model_profile
* extraction_path
* reasoning_fallback_used
* finish_reason
* extraction_quality_ok
* quality_issues
* risk_signals
* retry_should_run
* retry_reason
* retry_mode
* answer_chars

---

## Important Decisions

### Risk signal semantics

The following are treated as risk signals, not automatic retry triggers:

* `finish_reason_length`
* `reasoning_fallback_used`

The following are treated as hard quality issues:

* `answer_empty`
* `ends_mid_sentence`
* `dangling_citation`
* `dangling_markdown`

Retry decisions should be determined programmatically by local retry policy logic.

---

## Local Personal RAG Boundary

Hermes Memory remains a local personal RAG system.

The implementation intentionally avoids commercial multi-user platform complexity.

### Accepted design principles

1. Keep implementation local, inspectable, and lightweight.
2. Prefer understandable Python modules over framework-heavy abstraction.
3. Prefer profile-aware rules over global hardcoded heuristics.
4. Prefer smoke tests over large evaluation platforms.
5. Prefer observation-first tuning instead of automatic heuristic modification.
6. Do not ingest observation logs into RAG memory.
7. Do not store:

   * raw prompts
   * full retrieved context
   * full answers
   * real secrets
     inside observation logs.

### Explicitly out of scope

* Multi-user role/policy systems
* Distributed queue architecture
* Commercial routing platform
* OpenTelemetry / tracing backend
* Dashboard UI
* Database-backed event warehouse
* Automatic heuristic tuning
* Full fallback model chain
* SaaS / multi-tenant governance platform

---

## Current Status

### PASS

* model_profiles.yaml
* profile-aware extraction
* extraction_quality.py
* retry_policy.py
* answer_generator governance metadata
* smoke tests
* verification recall

### NOT YET IMPLEMENTED

* bounded compact retry executor

---

## Next Step

### M8.5.3 bounded compact retry executor

Future retry execution must satisfy:

* profile-aware behavior
* bounded retry count
* max-once retry by default
* smoke verification before freeze
* no retry loops
* maintain local personal RAG simplicity

---

## B-20260531-M8.4.7 Thinking-model Stabilization Freeze

Status: FROZEN

Summary:
- Hermes Memory now includes profile-aware extraction templates.
- Qwen forced-thinking behavior is stabilized through:
  - profile-aware extraction markers
  - last-match extraction
  - deterministic reasoning slicing
- Governance pipeline order is now:
  1. extraction
  2. quality evaluation
  3. completeness heuristic
  4. retry policy
  5. bounded retry
  6. retry validation

Key result:
- Extraction correctness is now treated as a first-class governance layer.
- Retry execution is no longer misused to compensate for extraction drift.

Known remaining tuning area:
- completeness heuristic false-positive reduction
- citation integrity polish
- retrieval profile tuning

Next stage:
- M9 Local Personal RAG Reliability Hardening

---
