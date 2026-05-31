## N-20260531-M8.3c Observation Report Layer

Status:
- planned

Goal:
- Add lightweight observation reporting over local JSONL observation logs.

Scope:
- `hermes-observe report`
- daily / weekly sanitizer summary
- contamination trend analysis
- structured output validity tracking
- model-profile comparison

Planned Features:
- sanitizer activation statistics
- review-status frequency
- contamination marker frequency
- structured-output success rate
- model-profile comparison
- daily/weekly markdown report export

Governance Rules:
- Observation analysis is automated.
- Heuristic modification is NOT automated.
- Human review remains required before sanitizer rule changes.

Current Observation Baseline:
- M8.3a default-on lightweight JSONL logger
- daily rotation
- retention cleanup
- no DB backend
- no RAG ingestion
- no raw/full prompt persistence

Risk Notes:
- Over-aggressive sanitizer heuristics remain possible.
- Structured-output compliance varies by model family.
- Forced-thinking models (e.g. Qwen) require stronger fallback handling.
- Observation logs must remain lightweight to avoid operational complexity.

Suggested Future Direction:
- Long-term observation-driven heuristic tuning
- Cross-model contamination comparison
- Safer language continuity heuristics
- Expanded reversible sanitizer coverage

---

## N-20260531-M8.4 Follow-up

Status: OPEN

Current baseline:
- M8.4 Multi-model Governance Baseline is PASS.
- model_profiles.yaml exists.
- answer_generator is model-profile aware.
- Qwen forced-thinking behavior is observable.
- extraction metadata is emitted.

Recommended next:
- M8.5 Extraction Quality Hardening
  - Improve fallback completeness when `finish_reason=length`.
  - Prefer complete answer blocks over partial synthesized bullet fragments.
  - Add profile-aware extraction quality checks.
  - Keep observation-first policy; do not auto-tune heuristics without evidence.

Alternative:
- M8.4.7 Add local JSONL observation logging if persistent evidence is needed before M8.5.

---

## N-20260531-M8.5 Local RAG Extraction Hardening

Status: OPEN

Recommended next milestone:
- M8.5 Local RAG Extraction Hardening

Purpose:
- Improve answer stability for local personal RAG use.
- Keep implementation lightweight and maintainable.
- Avoid turning Hermes Memory into a commercial multi-user RAG platform.

Planned scope:
1. M8.5.1 Add `tools/importer/extraction_quality.py`
   - Input:
     - answer
     - finish_reason
     - extraction_path
     - reasoning_fallback_used
   - Output:
     - ok
     - issues
     - retry_recommended

2. M8.5.2 Wire quality checker into `answer_generator.py`
   - Emit JSON metadata:
     - extraction_quality_ok
     - extraction_quality_issues
     - retry_recommended

3. M8.5.3 Optional single compact retry
   - Only when quality checker detects high-confidence incomplete output.
   - Keep disabled or conservative by default until smoke verified.

4. M8.5.4 Smoke test
   - Validate Qwen forced-thinking / `finish_reason=length` behavior.
   - Ensure answer is non-empty.
   - Ensure quality issues are observable.
   - Ensure no raw prompt / full context / secrets are logged.

Initial quality issues to detect:
- answer_empty
- finish_reason_length
- ends_mid_sentence
- dangling_citation
- dangling_markdown
- suspicious_short_answer
- reasoning_fallback_used

Out of scope for M8.5:
- Multi-model benchmark matrix.
- Dynamic model routing.
- Fallback model chain.
- OpenTelemetry / tracing backend.
- Dashboard.
- Observation database.
- Automatic heuristic tuning.
- Multi-user governance.

Local personal RAG rule:
- Use mature industry patterns as reference.
- Implement only the smallest local version that improves reliability and remains easy to maintain.

---

## N-20260531-M9 Retrieval and Citation Gap Assessment

Status: OPEN
Scope: M9 Local Personal RAG Reliability Hardening

Assessment:
- Hybrid retrieval is currently PASS / MVP.
- Citation formatting is currently Partial / usable.
- Both should be included in M9 polishing because they directly affect local RAG answer reliability.
- These are not commercial multi-user platform features; they are core local personal RAG correctness features.

### M9.6 Retrieval Profile Tuning

Status: OPEN
Priority: P1

Current state:
- Hybrid retrieval is usable.
- Recall CLI and answer_generator can retrieve relevant chunks.
- Heading-aware rerank has already shown useful behavior in earlier M5/M8 verification.

Gap:
- Retrieval is still mostly generic.
- Different query types should not always use the same retrieval behavior.
- Decision lookup, verification lookup, service lookup, operation recall, and baseline recap should have different preferences.

Planned local implementation:
- Add lightweight retrieval profile rules.
- Keep profiles local and inspectable.
- Avoid commercial routing or query-planning framework complexity.

Candidate retrieval profiles:
- decision_lookup
  - prefer `decisions.md`
  - prefer decision headings
- verification_lookup
  - prefer `verification.md`
  - prefer recent PASS markers
- service_lookup
  - prefer `services.md`
  - prefer service-specific headings
- baseline_lookup
  - prefer `baselines.md`
  - prefer frozen baseline headings
- operation_recall
  - prefer `operations.md`
  - prefer timestamped operation entries

Success criteria:
- Existing recall behavior remains PASS.
- Query-specific retrieval improves without breaking generic hybrid search.
- Smoke tests verify at least:
  - decision lookup
  - verification lookup
  - service lookup
  - baseline lookup

Out of scope:
- Commercial query router.
- Dynamic model-routing platform.
- Multi-user retrieval policy.
- Web dashboard.

---

### M9.3 Citation Integrity Checker

Status: OPEN
Priority: P0

Current state:
- Citation formatting is Partial / usable.
- Answers can cite `[Source 1]`.
- Context builder provides retrieved source chunks.

Gap:
- Citation formatting is not yet fully validated.
- The system should verify that cited source indexes are valid.
- The system should detect dangling or malformed citations.
- The system should detect answers that cite sources not present in context.

Planned local implementation:
- Add a small citation integrity checker.
- Keep it deterministic and local.
- Prefer simple checks before adding any LLM-based groundedness judge.

Initial checks:
- cited source index exists in selected context
- no dangling citation such as `[Source`, `[Source `, `[S`
- no citation to missing source such as `[Source 3]` when only Source 1 exists
- answer has citation when context-backed answer is expected
- optional: every paragraph or bullet should have at least one citation for RAG answers

Success criteria:
- Citation checker emits metadata:
  - citation_integrity_ok
  - citation_issues
  - cited_sources
  - available_sources
- answer_generator can expose citation metadata in JSON.
- Smoke test catches:
  - valid citation
  - dangling citation
  - missing source index

Out of scope:
- Full LLM-as-judge faithfulness scoring.
- External evaluation platform.
- Enterprise compliance citation framework.

Local personal RAG rule:
- Retrieval tuning and citation checking should improve correctness while staying lightweight, local, and easy to inspect.

---

## M9.8 Semantic Eval Policy
Status: Planned

Reason:
- Remaining eval failures are mostly wording / semantic-equivalence issues, not pipeline failures.
- Example: expected "dangling citation" but generated equivalent Chinese wording such as "格式錯誤的引用" or "殘留引用".

Planned:
- Add must_contain_any / semantic_alias support to local eval.
- Keep deterministic eval; do not introduce LLM-as-judge yet.

---

## M10 Observation-driven Hardening
Status: Planned

Goal:
- Stop expanding sanitizer rules blindly.
- Collect lightweight local evidence from real runs.
- Use observations to improve sanitizer, extraction cleanup, retry policy, and eval cases later.

Planned:
- Add JSONL observation logs.
- Log only metadata and short safe previews.
- Do not log raw/full prompts, full answers, full memory context, or secrets.
- Do not ingest observation logs into RAG memory.
- Keep failures non-blocking.

Initial signals:
- extraction_path
- finish_reason
- quality_issues
- risk_signals
- completeness_issues
- citation_issues
- retry_should_run
- retry_reason
- answer_chars
- answer_preview

---
