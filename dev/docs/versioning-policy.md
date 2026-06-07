# Versioning Policy

Status: ACTIVE / OPEN BETA VERSIONING BASELINE
Date: 2026-06-07

## Purpose

Define how Hermes Runes MD Wiki versions are named and published during Open Beta.

## Current Version

```text
0.1.0-beta.1
```

The matching Git tag should be:

```text
v0.1.0-beta.1
```

The tag is intentionally not created by M207. It should be created only after workspace slug realignment and public download audit are complete.

## Version Scheme

Hermes Runes MD Wiki uses SemVer-style versioning with beta prerelease labels during Open Beta.

```text
MAJOR.MINOR.PATCH-beta.N
```

## Meaning

```text
0.x.x        Open Beta / not stable API or workflow
0.1.0        first public Open Beta baseline
beta.1       first beta baseline candidate
```

## Update Rules

```text
PATCH bump:
- documentation fixes
- small smoke or workflow corrections
- non-breaking bug fixes

MINOR bump:
- visible workflow changes
- new governed tool behavior
- new public-facing setup path
- changed workspace or memory policy

MAJOR bump:
- stable release boundary
- incompatible public API/workflow break after v1.0.0
```

## Tagging Rules

```text
Use annotated tags.
Do not tag before public download readiness checks pass.
Do not tag while known public-facing path or slug blockers remain unresolved.
```

Recommended first tag command after readiness is complete:

```bash
git tag -a v0.1.0-beta.1 -m "Open Beta v0.1.0-beta.1"
git push origin v0.1.0-beta.1
```

## Release Boundary

```text
Open Beta version does not mean stable release.
Open Beta version does not mean production support.
Open Beta version does not mean enterprise support.
Open Beta version does not relax governed memory safety boundaries.
```

## Final Lock

```text
Versioning Policy
ACTIVE / Open Beta versioning baseline established
```
