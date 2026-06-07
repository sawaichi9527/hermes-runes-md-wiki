# Developer Area

Status: developer-only

This directory contains development history, milestone evidence, trial records, beta observations, and developer-facing design notes.

## Layout

```text
dev/docs/          Developer-only specs, trial plans, beta evidence, regression notes, and historical docs.
dev/wiki-history/  Historical wiki namespaces moved out of runtime wiki memory seed.
```

## Runtime Boundary

Public testers and normal runtime import should use:

```text
wiki/
docs/
```

Do not import `dev/` as runtime user memory by default.

## Purpose

`dev/` preserves project provenance without polluting the runtime Markdown memory seed.
