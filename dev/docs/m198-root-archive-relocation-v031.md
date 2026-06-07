# M198 Root Archive Relocation for v0.3.1

Status: PASS / root archive moved under dev / v0.3.0 unchanged
Date: 2026-06-08
Scope: v0.3.1 cleanup candidate after v0.3.0 tag lock

## Purpose

Move the remaining root-level `archive/` directory under `dev/` so the repository root remains focused on runtime, docs, tooling, config, migrations, reports, and wiki surfaces.

This is a post-v0.3.0 cleanup for the v0.3.1 line.

It does not modify or retag `v0.3.0`.

## Decision

Root `archive/` is developer / prototype / milestone history, not runtime user-facing content.

Therefore:

```text
archive/
→ dev/archive/
```

## Moved Content

```text
archive/prototype-history/
→ dev/archive/prototype-history/

archive/root-milestone-shell/
→ dev/archive/root-milestone-shell/
```

## Runtime Boundary

The runtime/user-facing surface should not depend on root `archive/`.

Accepted remaining wording:

```text
wiki/_system/access-boundary.md
  archive/delete state
```

This refers to governed lifecycle state, not the old root `archive/` directory.

## Version Boundary

```text
v0.3.0 tag target: 4640eb4
v0.3.0 remains unchanged
main continues toward v0.3.1 cleanup
```

## Verification

Expected after M198:

```text
root archive dir: absent
dev/archive/root-milestone-shell: present
dev/archive/prototype-history: present
runtime old archive path refs: none
v0.3.0 peeled target: 4640eb4
```

## Final Lock

```text
M198: PASS / root archive moved under dev / v0.3.0 unchanged / v0.3.1 cleanup path
```
