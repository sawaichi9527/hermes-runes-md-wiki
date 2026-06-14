# Verification M216 - v0.7.2 Annotated Tag Lock

Status: PASS / annotated tag verified / release baseline frozen  
Scope: v0.7.2 tag evidence only; no code or wiki behavior changes

## Purpose

M216 locks the v0.7.2 release by verifying that an annotated tag exists and points at the intended release baseline.

## Preconditions

M214 and M215 completed:

- M214: release prep decision PASS
- M215: release notes / README / VERSION alignment PASS
- `VERSION`: `0.7.2`
- Core FTS smoke: PASS
- migration guard release check: PASS
- working tree clean before tag

## Local tag command

The tag was created locally and pushed to origin:

```bash
git tag -a v0.7.2 -m "Release v0.7.2"
git push origin v0.7.2
```

## Observed tag evidence

Local output confirmed:

```text
[new tag]         v0.7.2 -> v0.7.2
v0.7.2
```

The tag is visible at the local release baseline:

```text
6f68494 (HEAD -> main, tag: v0.7.2, origin/main, origin/HEAD) Update next actions for M216 tag lock
3e4632e Record M215 release alignment check
8267cec Release v0.7.2
```

## Release baseline

The v0.7.2 tag points at:

```text
6f68494 Update next actions for M216 tag lock
```

This commit includes the v0.7.2 release baseline:

- `VERSION = 0.7.2`
- `docs/releases/v0.7.2.md`
- README release alignment
- M214/M215 release-prep verification state
- M216 tag-lock next-action pointer

## Non-goals

M216 does not:

- change VERSION
- start v0.7.3 development
- modify `wiki/`
- add migration guard features
- retag or move existing release tags

## Final lock

```text
M216 v0.7.2 Annotated Tag Lock
PASS / annotated tag verified / release baseline frozen
```

---
