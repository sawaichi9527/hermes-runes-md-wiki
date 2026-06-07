# Importer Trigger Policy

Status: M16.1 planning baseline

This policy defines how notes created by the forge writer may enter the importer and index workflow.

## Current baseline

The M15 forge writer baseline can create controlled sample notes, but it must not automatically trigger importer or index updates.

Current flow:

```text
forge writer
  ↓
created or planned Markdown note
  ↓
human review
  ↓
manual importer command
  ↓
manual smoke verification
  ↓
optional git commit / push
```

## Allowed actions

- Human-reviewed manual importer execution.
- Manual smoke verification after importer execution.
- Manual git review before commit.
- Manual commit and push after verification.

## Blocked actions

- Automatic importer execution immediately after writer operation.
- Automatic index update immediately after writer operation.
- Automatic manifest ingestion into RAG memory.
- Automatic commit or push after writer operation.
- Automatic write-to-index for unreviewed generated notes.

## Review requirements before importer execution

Before running importer manually, verify:

- The generated Markdown note is intended to persist.
- The note belongs to an allowed namespace.
- The note does not contain secrets or credentials.
- The note does not contain accidental prompt/debug/log noise.
- The note has useful title, metadata, and body content.
- The note should improve retrieval quality rather than add noise.

## Manual importer trigger model

Importer execution should remain explicit:

```bash
python tools/importer/importer.py
```

Project-specific wrappers may be added later, but they must remain manually triggered until a future governance milestone.

## Post-import verification

After manual importer execution, run at least one retrieval smoke query that targets the new note.

Expected verification:

- The new note is retrievable.
- Existing high-value retrieval results are not degraded.
- No generated manifest file is retrieved as memory.
- No temporary forge output is indexed.

## Future integration gates

Importer/index integration may only become more automated after separate approval for:

- importer dry-run preview
- importer changed-file scope
- index update scope control
- rollback procedure
- retrieval quality regression smoke
- generated note quality checklist
