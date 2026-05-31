---
## V-20260531-M8.3a Default-on JSONL Observation Logger
Status: PASS
Phase: M8.3a
Scope: Hermes Memory / Observation Governance

Summary:
- Hermes Memory now includes a default-on lightweight local JSONL observation logger.
- Observation logging is intended to accumulate evidence for sanitizer, model-profile, and heuristic improvement.
- Observation logging is local-only and intentionally avoids production-scale observability complexity.

Verified Capabilities:
- Default-on observation logging: PASS
- Daily JSONL rotation: PASS
- Observation retention cleanup: PASS
- Observation safety size cap: PASS
- `hermes-observe tail`: PASS
- `hermes-observe stats`: PASS
- Observation logging failure does not fail answer generation: PASS

Observation Design:
- Local append-only JSONL.
- No PostgreSQL or SQLite logging backend.
- No vector ingestion.
- No RAG memory ingestion.
- No automatic heuristic modification.

Observation Path:

```text
~/workspace/hermes-memory/observations/answer-runs/YYYY-MM/YYYYMMDD.jsonl
```

Default Retention:

```text
90 days
```

Daily Safety Cap:

```text
20MB/day
```

Privacy / Redaction Policy:
- Full raw model output is NOT stored by default.
- Full final answer is NOT stored by default.
- Full prompt is NOT stored by default.
- Full memory context is NOT stored by default.
- Retrieved chunk contents are NOT stored by default.
- Observation previews are optional and redacted.

Stored Observation Metadata:
- trace_id
- timestamp
- model profile
- sanitizer strategy/confidence
- review status
- structured output validity
- token usage
- source refs
- content length/hash
- contamination markers

Known Governance Principles:
- Observe first, tune later.
- Observation is for human-reviewed heuristic improvement.
- Observation must not automatically modify sanitizer rules.

Architecture Flow:

```text
Memory QA
    ↓
Structured Extraction
    ↓
Adaptive Sanitizer
    ↓
Review Classification
    ↓
Observation JSONL Logger
    ↓
hermes-observe stats/tail
    ↓
Human Review
    ↓
Future Heuristic Improvements
```

Result:
- M8.3a observation governance baseline is considered stable for long-term sanitizer and heuristic evidence collection.

---

## V-20260531-M8.4.5b Multi-model Governance Observation Metadata

Status: PASS
Scope: M8.4 Multi-model Governance Baseline

Verified:
- `selected_model_profile` is emitted in answer_generator JSON output.
- Qwen model is matched to `qwen-forced-thinking`.
- `reasoning_fallback_used` is emitted.
- `extraction_path` is emitted.
- `finish_reason` is emitted.

Observed sample:
- selected_model_profile: qwen-forced-thinking
- extraction_path: reasoning_content.synthesize_answer
- reasoning_fallback_used: true
- finish_reason: length

Known issue:
- For qwen-forced-thinking, useful answer text may still be truncated mid-sentence when `finish_reason=length`.
- Current cleanup removes obvious dangling citation / markdown fragments, but does not guarantee semantic completeness.
- This is acceptable for M8.4.5 baseline because the purpose is observability, not final extraction perfection.

Next:
- M8.4.6 should add smoke tests for model profile selection and extraction metadata stability.
- Future tuning should use observation evidence before changing sanitizer heuristics.

---

## V-20260531-M8.4.6 Multi-model Governance Smoke

Status: PASS
Scope: M8.4 Multi-model Governance Baseline

Verified:
- Static model profile matcher PASS.
- `Qwen3.6-35B-A3B` maps to `qwen-forced-thinking`.
- answer_generator emits governance metadata.
- Required metadata fields are present:
  - selected_model_profile
  - extraction_path
  - reasoning_fallback_used
  - finish_reason
- answer_generator still returns a non-empty answer.

Observed sample:
- selected_model_profile: qwen-forced-thinking
- extraction_path: reasoning_content.synthesize_answer
- reasoning_fallback_used: true
- finish_reason: length

Status:
- M8.4 baseline is usable as a governance and observation baseline.
- Extraction quality is not considered fully solved yet; it is now measurable by profile.

---

## V-20260531-M8.5.1 Local Extraction Quality Checker

Status: PASS
Scope: M8.5 Local RAG Extraction Hardening

Verified:
- `tools/importer/extraction_quality.py` exists.
- `evaluate_extraction_quality()` returns:
  - ok
  - issues
  - retry_recommended
  - finish_reason
  - extraction_path
  - reasoning_fallback_used
  - answer_chars
- Smoke test PASS:
  - `smoke/extraction_quality_smoke.py`

Notes:
- This is a local personal RAG quality checker.
- It does not perform retry.
- It does not log raw prompt, full context, full answer, or secrets.

---

## V-20260531-M8.5.2 Extraction Quality Metadata

Status: PASS
Scope: M8.5 Local RAG Extraction Hardening

Verified:
- `answer_generator.py` emits extraction quality metadata.
- Required fields are present:
  - extraction_quality_ok
  - extraction_quality_issues
  - retry_recommended
  - answer_chars
- Smoke test PASS:
  - `smoke/extraction_quality_metadata_smoke.py`

Observed sample:
- selected_model_profile: qwen-forced-thinking
- extraction_path: message.content
- reasoning_fallback_used: false
- finish_reason: length
- extraction_quality_ok: true
- extraction_quality_issues:
  - finish_reason_length
- retry_recommended: true
- answer_chars: 331

Interpretation:
- `finish_reason=length` is treated as an observable risk signal.
- A length finish does not automatically mean the answer is unusable.
- The answer can still be quality-ok if it ends cleanly and passes local checks.

Next:
- Consider M8.5.3 optional single compact retry.
- Keep retry conservative and disabled or profile-gated until smoke verified.

---

## V-20260531-M8.5.2c Quality Signals and Retry Policy Split

Status: PASS
Scope: M8.5 Local RAG Extraction Hardening

Verified:
- `extraction_quality.py` now separates:
  - quality_issues
  - risk_signals
- `retry_policy.py` exists.
- Retry decision is made by programmatic local policy, not by manual human inspection.
- `answer_generator.py` emits:
  - quality_issues
  - risk_signals
  - retry_should_run
  - retry_reason
  - retry_mode
- Smoke test PASS:
  - `smoke/retry_policy_smoke.py`

Observed sample:
- selected_model_profile: qwen-forced-thinking
- extraction_quality_ok: true
- quality_issues: []
- risk_signals:
  - finish_reason_length
  - reasoning_fallback_used
- retry_should_run: false
- retry_reason: quality_ok_with_risk_signals
- retry_mode: none

Decision semantics:
- `finish_reason_length` is a risk signal, not an automatic retry trigger.
- `reasoning_fallback_used` is a risk signal, not an automatic retry trigger.
- Retry should run only for hard quality issues such as:
  - answer_empty
  - ends_mid_sentence
  - dangling_citation
  - dangling_markdown
- Retry is bounded by retry count and must not loop.

Local RAG boundary:
- This remains a local personal RAG policy module.
- No tracing backend, dashboard, queue, multi-user role system, or automatic heuristic tuning is introduced.

---

## V-20260531-M9.1a Local Eval Set Stabilization

Status: PASS
Scope: M9 Local Personal RAG Reliability Hardening

Verified:
- `eval/local_eval_set.yaml` exists.
- `eval/run_local_eval.py` exists.
- Eval runner can distinguish normal PASS from generation failure.
- Overly brittle lexical assertion in `eval-m8-governance-001` was relaxed.
- Eval set now exposes stable Qwen generation-length failures.

Observed result:
- eval-telegram-001: PASS
- eval-m8-governance-001: PASS
- eval-m85-quality-001: FAIL / generation_length_failure
- eval-m9-citation-001: FAIL / generation_length_failure

Interpretation:
- Retrieval is not the primary failure in these failing cases.
- Context is available, but Qwen forced-thinking behavior can spend the token budget in reasoning.
- This confirms the need for M8.5.3 bounded compact retry executor.

Local RAG boundary:
- This eval layer remains local and lightweight.
- It does not introduce external evaluation platforms or LLM-as-judge infrastructure.

---

## V-20260531-M8.4.7 Profile-aware Extraction Templates

Status: PASS
Scope: M8.4 Multi-model Governance Baseline

Verified:
- `extraction_templates.py` exists.
- Profile-aware extraction markers are implemented.
- Qwen reasoning_content extraction is now profile-aware.
- Extraction uses:
  - marker priority
  - last-match extraction
  - deterministic slicing
- `answer_generator.py` can now recover usable answers directly from Qwen reasoning output without bounded retry execution.

Observed behavior:
- `initial_answer_empty=false`
- `final_answer_empty=false`
- `retry_should_run=false`
- `retry_executed=false`

Observed improvement:
- Previous failures were caused by extraction drift.
- Root cause was not retrieval failure.
- Root cause was not retry orchestration.
- Root cause was model-specific reasoning extraction mismatch.

Architecture outcome:
- Hermes Memory now supports profile-aware thinking-model extraction stabilization.
- Retry executor is no longer incorrectly used as a substitute for extraction correctness.

Known limitation:
- Completeness heuristic still produces some false positives for concise answers.
- Current false positives are treated as soft governance signals only.
- This is acceptable for current baseline freeze.

Boundary:
- No external orchestration framework added.
- No tracing backend added.
- No multi-user governance complexity added.
- Remains local personal RAG scoped.

---

## V-20260531-M9.6a Retrieval Profile Registry

Status: PASS
Scope: M9 Retrieval Reliability Hardening

Verified:
- `retrieval_profiles.yaml` exists.
- Retrieval query types are now explicitly defined.
- `retrieval_profiles.py` can:
  - load profile registry
  - select retrieval profile
  - fallback to default profile
- Smoke test PASS:
  - `smoke/retrieval_profile_smoke.py`

Architecture outcome:
- Retrieval intent semantics are now registry-based.
- Future retrieval tuning can remain local, inspectable, and deterministic.
- Avoids hardcoded retrieval heuristics inside hybrid retrieval logic.

Boundary:
- No LLM retrieval router added.
- No orchestration framework added.
- No enterprise retrieval planner added.
- Remains local personal RAG scoped.

---

## V-010: Verify Phase3 M9.7 Response Sanitization Layer
Status: PASS
Scope: final answer deterministic cleanup

Verified:
- Citation normalization PASS.
- Artifact line stripping PASS.
- Meta section cutoff PASS.
- Final review cutoff PASS.
- Duplicated regenerated answer cleanup PASS.

Result:
- M9.7 Response Sanitization Layer is implemented as a deterministic final-output cleanup layer.
- Architecture remains stable: retrieval → generation → sanitization → validation.

---

## V-012: Verify Phase3 M9.7~M9.8 Governed Output Baseline
Status: PASS / FROZEN
Scope: sanitizer, structured extraction cleanup, semantic eval policy

Verified:
- M9.7 Response Sanitization Layer is operational.
- M9.7a Structured Reasoning Extraction smoke test PASS.
- M9.8 Semantic Eval Policy reduced brittle exact-wording failures.
- Local eval improved to 3/4 PASS.
- Remaining 1 FAIL is known limitation: aggressive slicing / suspicious_short_answer in forced-thinking output, not pipeline crash.

Known limitation:
- Qwen forced-thinking may emit partial tail answers through reasoning_content.synthesize_answer.
- This should be handled by observation-driven hardening rather than more regex expansion.

Result:
- Governed output baseline is usable and frozen for next-stage observation.

---
