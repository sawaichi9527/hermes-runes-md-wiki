# M203 GitHub Release Publication Verification

Status: PASS / GitHub Release published / v0.5.0 latest  
Version line: 0.5.0  
Date: 2026-06-08

## Scope

M203 publishes the GitHub Release entry for the already-created `v0.5.0` annotated tag.

This milestone does not move, recreate, or retag `v0.5.0`.

## Release anchor

GitHub Release:

- `https://github.com/sawaichi9527/hermes-runes-md-wiki/releases/tag/v0.5.0`

Release title:

- `Hermes Runes MD Wiki v0.5.0`

Release tag:

- `v0.5.0`

Tag target:

- `3fa580b Promote v0.5.0 final version line`

Post-release verification state before publication:

- `24839f8 Lock M202 post-release docs verification`

## Publication method

Published using GitHub CLI:

- `gh version 2.45.0`
- authenticated account: `sawaichi9527`
- command: `gh release create v0.5.0 --title "Hermes Runes MD Wiki v0.5.0" --notes-file docs/github-release-note-v0.5.0.md --latest`

## Release note source

Release note source file:

- `docs/github-release-note-v0.5.0.md`

Release note documents:

- v0.5.0 as recommended Open Beta baseline
- CPU-only embedding writer enablement
- PostgreSQL / pgvector backend verification
- hybrid/vector recall restoration
- fresh runtime smoke fixture alignment
- runtime CLI/tools surface cleanup
- accepted SKIP gates
- personal/local Open Beta boundary

## Final lock

M203 is locked as:

PASS / GitHub Release published / v0.5.0 latest / tag preserved
