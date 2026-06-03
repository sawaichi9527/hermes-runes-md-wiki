## N-20260603-M50 Controlled Trial-run Governance

Status: NEXT / PLANNED

Current baseline:
- M47 Governance Timeline: PASS / frozen.
- M48 Governance History: PASS / frozen.
- M49 Governance Integrity Validation: PASS / frozen.
- Cross-layer governance consistency engine established.
- P0 apply execution boundary remains fully blocked.

Recommended next milestone:
- M50 Controlled Trial-run Governance

Purpose:
- Validate the governed proposal pipeline under controlled real-world usage.
- Exercise mixed proposal states across multiple governance layers.
- Preserve the current P0 safety boundary while observing real operational behavior.

Suggested scope:
- multiple proposal fixtures
- mixed approve/reject/quarantine decisions
- governance timeline observation
- governance history observation
- governance integrity regression preservation
- retrieval isolation verification
- provenance stability verification
- observation-driven governance refinement

Hard constraints:
- no autonomous trusted wiki mutation
- no automatic apply execution
- no background promotion worker
- no database mutation side effects
- no enterprise workflow expansion

Success criteria:
- integrity validator remains PASS
- governance history remains consistent
- apply execution remains BLOCKED
- reviewed vs trusted separation preserved
- smoke/regression suites remain PASS

Reference:
- `wiki/k6-freelancer/verification-m49.md`

---

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

# Next Stage Candidate

## M21 P0 Trial Run

Goal:
- validate governed memory behavior under real usage

Scope:
- multiple real agent proposals
- mixed approve/reject decisions
- retrieval stability observation
- provenance behavior observation
- governance observation review
- trust bias observation
- smoke/regression preservation

Constraints:
- personal-use scale only
- avoid enterprise governance complexity
- observation-first refinement
- no automatic policy mutation

Future evaluation candidates:
- reviewed vs trusted separation refinement
- proposal aging policy
- trust escalation policy
- optional retrieval explainability expansion
- optional compatibility behavior for:
  - --mode hybrid
  - --mode fts
