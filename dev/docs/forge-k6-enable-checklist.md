# Forge K6 Real-Write Enablement Checklist

Status: M15.7d planning baseline

This checklist defines the minimum approval conditions required before enabling real-write operations for the `k6-freelancer` namespace.

## Required technical conditions

All conditions below must be satisfied before enablement:

- `create-flat` duplicate-path protection is verified.
- File lock behavior is verified under repeated execution.
- Manifest generation is stable and deterministic.
- Dry-run and real-write mode separation is verified.
- Namespace block policy is verified by smoke tests.
- Real-write still requires explicit double-confirm switches.
- Unknown namespaces remain blocked.
- Index update remains independently gated.
- Importer execution remains independently gated.
- Manifest ingestion into RAG memory remains disabled by default.

## Required operational conditions

- The repository working tree must be clean before writer execution.
- Git push workflow must be manually reviewed.
- Generated notes must be human-reviewed before importer execution.
- Real-write operations must remain single-user only during baseline phase.
- Backup and rollback procedures must be documented.

## Required scope restrictions

Even after enablement:

- Only new-note creation should be allowed initially.
- Existing-note modification should remain blocked.
- Delete operations should remain blocked.
- Automatic index update should remain blocked.
- Automatic importer execution should remain blocked.

## Required governance review

The following questions must be explicitly reviewed before enablement:

- Can malformed generated Markdown damage retrieval quality?
- Can accidental note spam pollute long-term memory?
- Can generated manifests accidentally enter memory ingestion?
- Can write operations bypass namespace restrictions?
- Can future multi-agent execution create race conditions?

## Enablement recommendation

Recommended progression:

1. sample-project verification baseline
2. namespace block verification
3. policy documentation freeze
4. limited k6-freelancer write pilot
5. manual review phase
6. optional importer/index integration phase
