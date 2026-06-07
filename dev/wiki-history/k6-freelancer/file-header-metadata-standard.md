# M30.3 File Header / Version Metadata Standard

Status: M30.3 POLICY / NO BULK EDIT YET
Milestone: M30.3 File Header / Version Metadata Standard
Chinese: M30.3 檔案標頭 / 版本中繼資料標準

## Purpose

M30.3 defines the standard metadata header format for Python modules, shell entrypoints, scenario runners, smoke helpers, and verification documents before M30 applies broad code cleanup.

This milestone does not bulk-edit existing files yet.

It defines the metadata contract that later M30 phases should apply gradually.

## Core Principle

Every maintained tool should be understandable from its file header before reading the implementation.

A maintainer should be able to answer:

```text
What component owns this file?
Is it canonical or historical?
Can it mutate trusted wiki?
Can it mutate database/index state?
Does it require human confirmation?
What milestone introduced it?
What replaces it if deprecated?
```

## Metadata Classes

Files should use one of the following metadata classes:

```text
canonical_runtime
canonical_governance_tool
canonical_smoke
scenario_runner
milestone_helper
legacy_supported
archive_candidate
delete_candidate
verification_doc
policy_doc
runtime_artifact
```

These classes align with M30.2 Canonical Naming Policy.

## Required Fields for Canonical Python Tools

Canonical Python tools should include a module docstring with these fields:

```text
Project
Component
Role
File class
Stability
Introduced
Canonical since
CLI entrypoint
Writes trusted wiki
Writes database/index
Writes operation record
Requires human confirmation
Autonomous operation allowed
Rollback behavior
Replacement / deprecation
```

## Python Header Template

Preferred template:

```python
#!/usr/bin/env python3
"""
Project: Hermes Runes MD Wiki
Component: Runes Shield / <component name>
Role: <short responsibility>
File class: canonical_governance_tool
Stability: P0 pre-release
Introduced: Mxx
Canonical since: M30
CLI entrypoint: bin/runes <subcommand> or direct helper
Writes trusted wiki: yes/no
Writes database/index: yes/no
Writes operation record: yes/no
Requires human confirmation: yes/no
Autonomous operation allowed: no
Rollback behavior: none / snapshot / restore helper / manual
Replacement / deprecation: none / replaces <file> / replaced by <file>
"""
```

## Scenario Runner Header Template

Scenario runners may retain milestone names and should explicitly state their historical role.

```python
#!/usr/bin/env python3
"""
Project: Hermes Runes MD Wiki
Component: P0 Scenario Validation
Role: M29.x <scenario name>
File class: scenario_runner
Stability: P0 evidence tool
Introduced: M29.x
Canonical since: not canonical runtime
CLI entrypoint: direct helper only
Writes trusted wiki: yes/no
Writes database/index: yes/no
Writes operation record: yes/no
Requires human confirmation: yes/no
Autonomous operation allowed: no
Rollback behavior: snapshot if controlled apply is used
Replacement / deprecation: keep as historical scenario evidence
"""
```

## Shell Entrypoint Header Template

Shell entrypoints under `bin/` should include:

```bash
#!/usr/bin/env bash
# Project: Hermes Runes MD Wiki
# Component: <component name>
# Role: <short responsibility>
# File class: canonical_runtime
# Stability: P0 pre-release
# Introduced: Mxx
# Canonical since: M30
# Writes trusted wiki: yes/no
# Writes database/index: yes/no
# Writes operation record: yes/no
# Requires human confirmation: yes/no
# Autonomous operation allowed: no
# Replacement / deprecation: none
```

## Milestone Shell Script Header Template

Root milestone shell scripts are not canonical runtime entrypoints.

If retained before archive, they should include:

```bash
#!/usr/bin/env bash
# Project: Hermes Runes MD Wiki
# Component: Historical milestone helper
# Role: Mxx temporary execution helper
# File class: milestone_helper / archive_candidate
# Stability: historical evidence only
# Introduced: Mxx
# Canonical since: not canonical
# Replacement / deprecation: candidate for tools/archive/milestone-shell/
```

## Verification Document Header Standard

Verification documents should begin with:

```text
# <Milestone Title>

Status: <status>
Milestone: <milestone>
Chinese: <Chinese title if useful>
```

Recommended optional fields:

```text
Seal Name
Seal Tag Candidate
Archive Branch Candidate
Introduced
Supersedes
Depends on
```

## Policy Document Header Standard

Policy documents should begin with:

```text
# <Policy Title>

Status: <policy status>
Milestone: <milestone if applicable>
Chinese: <Chinese title if useful>
```

Policy documents should avoid runtime mutation claims unless the policy governs mutation behavior.

## Stability Values

Allowed stability values:

```text
experimental
MVP
P0 evidence tool
P0 pre-release
P0 stable baseline
legacy-supported
archived-reference
delete-candidate
```

M30 should avoid claiming `stable` for files that have not passed pre-release smoke.

## Mutation Metadata Semantics

Mutation fields must be explicit.

Allowed values:

```text
yes
no
preview-only
explicit-only
manual-only
```

Examples:

```text
Writes trusted wiki: explicit-only
Writes database/index: explicit-only
Writes operation record: yes
Requires human confirmation: yes
Autonomous operation allowed: no
```

## Deprecation Metadata

Deprecated or legacy files should identify their state clearly:

```text
File class: legacy_supported
Replacement / deprecation: replaced by tools/runes/<new_file>.py after M30.x
```

Archive candidates should state:

```text
File class: archive_candidate
Replacement / deprecation: candidate for tools/runes/_archive/ after smoke verification
```

Delete candidates should state:

```text
File class: delete_candidate
Replacement / deprecation: safe to remove only after M30 smoke passes and backup/anchor exists
```

## Required Fields by File Class

### canonical_runtime

Required:

- Project
- Component
- Role
- File class
- Stability
- Introduced
- Canonical since
- Writes trusted wiki
- Writes database/index
- Writes operation record
- Requires human confirmation
- Autonomous operation allowed
- Replacement / deprecation

### canonical_governance_tool

Required:

- Project
- Component
- Role
- File class
- Stability
- Introduced
- Canonical since
- Writes trusted wiki
- Writes database/index
- Writes operation record
- Requires human confirmation
- Autonomous operation allowed
- Rollback behavior
- Replacement / deprecation

### scenario_runner

Required:

- Project
- Component
- Role
- File class
- Stability
- Introduced
- CLI entrypoint
- Writes trusted wiki
- Writes database/index
- Writes operation record
- Requires human confirmation
- Autonomous operation allowed
- Replacement / deprecation

### milestone_helper

Required:

- Project
- Component
- Role
- File class
- Stability
- Introduced
- Replacement / deprecation

## M30.3 Does Not Authorize

M30.3 does not authorize:

- bulk header injection
- mass rename
- deletion
- archive movement
- runtime behavior changes
- schema compatibility changes

Actual application of headers should happen in later M30 phases after entrypoint and archive decisions are reviewed.

## Next Milestone

Next:

```text
M30.4 Entrypoint Consolidation Plan
```

M30.4 should map current helper scripts to future canonical entrypoints.

## Verification Status

M30.3 File Header / Version Metadata Standard:

- Python header standard defined: PASS
- shell entrypoint header standard defined: PASS
- scenario runner header standard defined: PASS
- milestone shell helper header standard defined: PASS
- verification document header standard defined: PASS
- policy document header standard defined: PASS
- stability values defined: PASS
- mutation metadata semantics defined: PASS
- deprecation metadata defined: PASS
- no-bulk-edit boundary preserved: PASS

Overall:

M30.3 File Header / Version Metadata Standard:
PASS / metadata standard defined / no bulk edit performed
