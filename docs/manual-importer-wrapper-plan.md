# Manual Importer Wrapper Plan

Status: M16.6 planning baseline

This document defines the intended design for a future manual importer wrapper.

The wrapper is not implemented in M16.6.

## Goal

Provide a safer manual path from reviewed Markdown changes to importer execution.

Target flow:

```text
importer_preview.py
  ↓
human review
  ↓
manual scoped importer wrapper
  ↓
manual recall smoke
  ↓
optional git commit / push
```

## Non-goals

M16.6 does not introduce:

- automatic importer execution
- automatic index update
- automatic commit or push
- automatic manifest ingestion
- automatic write approval

## Future wrapper requirements

A future wrapper should:

- require a clean repository or explicit override
- accept an explicit path or project scope
- show importer preview before execution
- require manual confirmation before importer execution
- emit clear JSON output
- never run from generated manifest paths
- never import `tmp/`, `logs/`, or observation paths
- never run git commit or git push

## Proposed future command

```bash
python tools/importer/manual_import.py \
  --path wiki/sample-project/example.md \
  --preview-first \
  --confirm
```

Possible options:

- `--path <markdown-path>`
- `--project <name>`
- `--changed-files`
- `--preview-first`
- `--confirm`
- `--json`

## Required guard checks

Before importer execution, the wrapper should verify:

- target file is Markdown
- target file is under `wiki/<project>/`
- project namespace is allowed
- preview decision is include=true
- no manifest or runtime path is selected
- user confirmation flag is present
- importer command is available

## Post-import requirements

After importer execution, the user should manually run recall smoke checks.

Recommended smoke:

```bash
./bin/hermes-recall "<query related to new note>" \
  --project <project> \
  --mode hybrid \
  --limit 5 \
  --json
```

## Freeze rule

Until this plan is separately implemented and smoke verified, importer execution remains manual and direct.
