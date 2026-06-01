# Forge Writer Policy

Status: M15.7c baseline

This policy defines the allowed and blocked write behavior for the M15 forge writer baseline.

## Allowed in current baseline

- `create-flat` planning.
- `create-flat` dry-run for allowed project namespaces.
- New-note creation in `sample-project` only.
- Manifest generation for forge operations.
- Operation ID generation for every forge operation.
- File lock ownership during forge operation execution.

## Blocked in current baseline

- Real write to `k6-freelancer`.
- Updating an existing note.
- Deleting a note.
- Renaming or moving a note.
- Index update after note creation.
- Importer execution after note creation.
- Automatic manifest ingestion into RAG memory.
- Writing to unknown project namespaces.

## Required switches for real write

Real write requires both flags:

```bash
--execute --allow-real-write
```

Even with both flags, namespace policy still applies:

- `sample-project`: allowed for first-write sample verification.
- `k6-freelancer`: blocked until a future explicit enablement milestone.

## Safety invariants

- Default mode remains dry-run.
- Index update remains disabled.
- Duplicate path must block real write.
- Generated manifests must not be automatically indexed.
- Real project namespaces require a separate approval checklist before enablement.
