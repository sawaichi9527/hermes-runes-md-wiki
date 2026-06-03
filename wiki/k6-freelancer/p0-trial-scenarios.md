# P0 Trial Scenarios

Status: SCENARIO TARGET / CONTROLLED MUTATION AREA
Project: k6-freelancer

## Purpose

This file is the dedicated trusted Markdown target for P0 pre-trial scenario validation.

It exists to avoid mutating core governance documents during scenario tests while still exercising the real governed pipeline:

```text
proposal
→ attunement
→ promotion preview
→ preflight
→ controlled apply
→ explicit importer refresh
→ post-refresh recall verification
```

## Scenario Evidence

Scenario evidence below this heading may be appended by controlled apply helpers only.


### M29.1 Add Knowledge Scenario

Status: PASS CANDIDATE / controlled scenario evidence
Scenario ID: m29.1-add-knowledge
Marker: M29.1_ADD_KNOWLEDGE_CANONICAL_MARKER

This scenario validates that newly provided knowledge can be appended to a trusted Markdown target through the governed P0 pipeline.

Knowledge statement:

```text
Hermes Runes MD Wiki P0 add-knowledge flow requires controlled apply, explicit importer refresh, and post-refresh recall verification before the knowledge is considered retrievable trusted memory.
```

Governance expectation:

- proposal-derived evidence is not trusted memory by itself
- controlled apply is required for trusted wiki mutation
- importer refresh is explicit and separate from apply
- recall verification is required after refresh


### M29.3 Correction Update Scenario

Status: PASS CANDIDATE / controlled correction evidence
Scenario ID: m29.3-correction-update
Marker: M29.3_CORRECTION_UPDATE_CANONICAL_MARKER
Supersedes: m29.1-add-knowledge statement refinement

Correction statement:

```text
Hermes Runes MD Wiki P0 correction/update flow treats corrections as governed trusted-memory amendments: controlled apply records the amendment, explicit importer refresh exposes it to retrieval, and post-refresh recall verification confirms the corrected marker is retrievable with provenance.
```

Governance expectation:

- correction/update is not an autonomous rewrite
- correction/update requires controlled apply
- rollback snapshot and operation record must exist
- importer refresh remains explicit after correction
- recall verification must find the corrected marker after refresh

