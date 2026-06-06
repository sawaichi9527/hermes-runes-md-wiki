# M139.2 Local Import / Recall Check

Status: ACTIVE / LOCAL CHECK READY
Date: 2026-06-07

## Purpose

M139.2 verifies that the M139.1 fixture target can be loaded into the local index and found by its recall marker.

## Added Checker

```text
tools/importer/m139_2_local_recall_check.py
```

The checker:

```text
uses HERMES_MEMORY_ROOT
runs importer.py with workspace freelancer
checks public.documents and public.chunks
looks for the marker in wiki/freelancer/trial-promotion-fixtures.md
prints JSON
```

## Fixture

```text
Fixture ID: TPF-20260606-M137
Project: freelancer
Path: wiki/freelancer/trial-promotion-fixtures.md
Marker: M137 beta-prep trial promotion fixture marker
```

## Local Command

Run in the trial checkout:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short

HERMES_MEMORY_ROOT=$PWD \
HERMES_WORKSPACE_SLUG=freelancer \
HERMES_PROJECT=freelancer \
python3 tools/importer/m139_2_local_recall_check.py
```

Expected JSON fields:

```text
status: PASS
project: freelancer
target_path: wiki/freelancer/trial-promotion-fixtures.md
marker: M137 beta-prep trial promotion fixture marker
marker_result.row_count: at least 1
```

## Final Lock

```text
M139.2 Local Import / Recall Check
ACTIVE / local check ready / pending trial run
```
