# M29 P0 Pre-trial Scenario Pack / Runes Seal Baseline

Status: PASS / RUNES SEAL BASELINE CANDIDATE
Milestone: M29 P0 Pre-trial Scenario Pack
Chinese: M29 P0 預試行情境包 / 符文封印基準
Seal Name: Runes Seal / 符文封印
Seal Tag Candidate: v0.1.0-runes-seal
Archive Branch Candidate: archive/p0-runes-seal

## Purpose

M29 validates the P0 governed memory pipeline through three pre-trial scenarios before M30 pre-release hardening and refactor work begins.

M29.5 seals the current working baseline as a rollback anchor before M30.

The seal exists because the project has accumulated early local-development and GitHub-era technical debt, including:

- milestone-numbered helper scripts
- MVP-era naming
- duplicate or workaround flows
- incomplete file header / metadata conventions
- helper scripts that should later be consolidated into canonical entrypoints
- scenario target append duplication from repeated validation runs

M29.5 therefore records a known-good P0 scenario baseline before structural cleanup.

## Governed Pipeline Covered

M29 confirms the following governed pipeline is operational:

```text
user-provided knowledge
→ proposal / scenario evidence
→ human decision
→ controlled apply or reject
→ explicit importer refresh when applicable
→ strict recall verification
→ provenance-visible trusted retrieval
```

## Scenario Target

M29 scenarios use a dedicated trusted Markdown target:

```text
wiki/k6-freelancer/p0-trial-scenarios.md
```

This avoids mutating core governance documents while still exercising real controlled trusted wiki mutation.

## M29.1 Add Knowledge Scenario

Helper:

```text
tools/runes/scenario_add_knowledge_m29_1.py
```

Marker:

```text
M29.1_ADD_KNOWLEDGE_CANONICAL_MARKER
```

M29.1 verifies that newly provided knowledge can be governed into trusted memory.

Verified result:

- status: PASS
- controlled apply: PASS
- target file written: PASS
- explicit importer refresh: PASS
- strict recall verification: PASS
- retrieval result count positive: PASS
- expected path verified: PASS
- marker verified: PASS
- retrieval provenance checked: PASS

Important fix discovered during M29.1:

The first version of recall verification produced a false positive because it searched the whole verifier payload instead of only retrieval results.

M28.3 verifier was corrected to check only `results[]` path/citation/content evidence.

## M29.2 Reject / No-promotion Scenario

Helper:

```text
tools/runes/scenario_reject_m29_2.py
```

Rejected marker:

```text
M29.2_REJECTED_KNOWLEDGE_SHOULD_NOT_APPEAR_IN_TRUSTED_RECALL
```

M29.2 verifies that rejected knowledge is not promoted into trusted memory.

Verified result:

- status: PASS
- decision: REJECT
- target hash unchanged: PASS
- controlled apply not executed: PASS
- importer refresh not executed: PASS
- trusted wiki not mutated: PASS
- rejected marker not found in trusted recall: PASS
- trusted recall result count zero: PASS
- rejection operation record written: PASS

Expected detail:

The inner recall verifier returns FAIL for the rejected marker, and M29.2 interprets that as PASS because negative recall is the expected outcome.

## M29.3 Correction / Update Scenario

Helper:

```text
tools/runes/scenario_correction_update_m29_3.py
```

Marker:

```text
M29.3_CORRECTION_UPDATE_CANONICAL_MARKER
```

M29.3 verifies that trusted memory can be corrected or updated through a governed amendment flow.

P0 correction/update mode:

```text
append amendment
```

M29.3 intentionally does not perform destructive rewrite. It appends correction evidence to preserve auditability and rollback safety before M30 hardening.

Verified result:

- status: PASS
- controlled apply: PASS
- target file written: PASS
- pre-hash changed after apply: PASS
- rollback snapshot written: PASS
- apply operation record written: PASS
- explicit importer refresh: PASS
- strict recall verification: PASS
- retrieval result count positive: PASS
- expected path verified: PASS
- marker verified: PASS
- retrieval provenance checked: PASS

## Runes Seal Baseline

M29.5 defines the sealed pre-refactor baseline:

```text
Runes Seal / 符文封印
```

Meaning:

```text
A known-good P0 governed memory baseline sealed before M30 pre-release hardening.
```

The Runes Seal baseline includes:

- M27 controlled trusted wiki mutation baseline
- M28 governed retrieval refresh baseline
- M29.1 add-knowledge scenario PASS
- M29.2 reject/no-promotion scenario PASS
- M29.3 correction/update scenario PASS
- strict recall verifier fixed to avoid false positives
- dedicated P0 scenario target available
- operation evidence generated for apply / reject / refresh / recall verification

## Known Gaps Preserved for M30

M29.5 intentionally does not resolve technical debt.

M30 should review and harden:

- Python helper naming conventions
- milestone-numbered script names
- MVP / v1 / v2 schema and file naming policy
- file headers and component metadata
- canonical entrypoint consolidation
- idempotency guard for scenario runners
- duplicate scenario target appends from repeated validation
- rollback execution helper
- path / hash / confirmation-token risk review
- subprocess and JSON parsing robustness
- recall verifier regression tests
- importer target-specific refresh design
- negative recall semantics and reporting clarity

## M30 Boundary

M30 must not begin until this Runes Seal baseline is locally pulled, verified, and optionally anchored through an archive branch or tag.

M30 may refactor implementation details, but it must preserve the behavioral guarantees proven by M29.

## Verification Status

M29.1 Add Knowledge Scenario:

PASS / controlled apply verified / explicit refresh verified / strict recall verified

M29.2 Reject / No-promotion Scenario:

PASS / rejected content not trusted / negative recall verified

M29.3 Correction / Update Scenario:

PASS / controlled correction amendment verified / refresh verified / strict recall verified

M29.5 Runes Seal Baseline:

PASS / seal document created / rollback anchor candidate declared

Overall:

M29 P0 Pre-trial Scenario Pack:
PASS / Runes Seal baseline candidate
