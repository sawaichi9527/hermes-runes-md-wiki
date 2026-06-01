# Importer Preview Policy

Status: M16.5 read-only preview baseline

This policy defines the preview behavior before importer/index execution.

## Baseline verification

M16.1 through M16.4 status: PASS

Verified baseline:

- M16.1 importer trigger policy: PASS
- M16.2 importer preview policy: PASS
- M16.3 importer_preview.py read-only helper: PASS
- M16.4 changed-files preview smoke: PASS

## Goal

Before importer execution, the system should be able to preview which Markdown files would be processed.

The preview stage must help answer:

- Which files changed?
- Which files are eligible for import?
- Which files should be skipped?
- Is any generated forge output accidentally in scope?
- Is any manifest or temporary file accidentally in scope?

## Current baseline

`tools/importer/importer_preview.py` exists as a read-only helper.

Supported modes:

- `--changed-files`
- `--project <name>`
- `--path <markdown-path>`
- `--json`

The helper reports preview decisions only.

## Desired preview inputs

Possible preview inputs:

- Git changed files.
- Specific project namespace.
- Specific Markdown file path.
- Recently created forge note path.

## Desired preview output

Preview output includes:

- candidate file path
- project namespace
- include / exclude decision
- reason for decision
- preview-only mode
- DB write flag
- chunk creation flag
- index update flag

## Include rules

A file may be included only if:

- It is a Markdown file.
- It is under `wiki/<project>/`.
- The project namespace is allowed.
- It is not a manifest file.
- It is not under `tmp/`.
- It is not an observation log.

## Exclude rules

A file must be excluded if:

- It is outside `wiki/`.
- It is not Markdown.
- It is under `tmp/`.
- It is a generated manifest.
- It is an observation log.
- It belongs to a blocked namespace.

## Safety invariants

- Preview must not modify the database.
- Preview must not update indexes.
- Preview must not create chunks.
- Preview must not commit or push changes.
- Preview must be safe to run repeatedly.

## Helper usage

```bash
python tools/importer/importer_preview.py --changed-files --json
```

```bash
python tools/importer/importer_preview.py \
  --path wiki/sample-project/project-first-real-write-overview.md \
  --json
```

## Future integration gates

Before moving beyond preview-only behavior, separately approve:

- manual importer wrapper
- changed-file import scope
- importer dry-run mode
- index update gating
- rollback procedure
- retrieval regression smoke
