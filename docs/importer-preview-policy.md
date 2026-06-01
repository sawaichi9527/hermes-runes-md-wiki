# Importer Preview Policy

Status: M16.2 planning baseline

This policy defines the desired preview behavior before importer/index execution.

## Goal

Before importer execution, the system should be able to preview which Markdown files would be processed.

The preview stage must help answer:

- Which files changed?
- Which files are eligible for import?
- Which files should be skipped?
- Is any generated forge output accidentally in scope?
- Is any manifest or temporary file accidentally in scope?

## Current baseline

No automatic importer preview is implemented yet.

M16.2 is a planning baseline only.

## Desired preview inputs

Possible preview inputs:

- Git changed files.
- Specific project namespace.
- Specific Markdown file path.
- Recently created forge note path.

## Desired preview output

Preview output should include:

- candidate file path
- project namespace
- include / exclude decision
- reason for decision
- expected importer mode
- whether index update would be required later

## Include rules

A file may be included only if:

- It is a Markdown file.
- It is under `wiki/<project>/`.
- The project namespace is allowed.
- It is not a manifest file.
- It is not under `tmp/`.
- It is not an observation log.
- It has been human-reviewed.

## Exclude rules

A file must be excluded if:

- It is outside `wiki/`.
- It is not Markdown.
- It is under `tmp/`.
- It is a generated manifest.
- It is an observation log.
- It contains obvious secret placeholders or credentials.
- It belongs to a blocked namespace.

## Safety invariants

- Preview must not modify the database.
- Preview must not update indexes.
- Preview must not create chunks.
- Preview must not commit or push changes.
- Preview must be safe to run repeatedly.

## Future helper direction

A future helper may be added, for example:

```bash
python tools/importer/importer_preview.py --changed-files
```

Potential modes:

- `--changed-files`
- `--project <name>`
- `--path <markdown-path>`
- `--json`

This helper should remain read-only until separately approved.
