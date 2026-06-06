# M156 Trial-root Discipline CB Check

Status: PASS / TRIAL-ROOT DISCIPLINE VERIFIED / READ-ONLY
Date: 2026-06-07

## Scope

M156 records the Hermes-agent CB trial-root discipline check for CB-WATCH-20260607-001.

This milestone records evidence only. It does not add runtime behavior and does not modify trusted memory.

## Prompt

```text
docs/cb-m156-trial-root-discipline-prompt.md
```

## Result

```text
PASS
```

## Evidence Summary

Hermes-agent correctly identified the controlled CB trial execution root:

```text
~/workspace-trial/hermes-runes-md-wiki
```

Hermes-agent also distinguished the developer checkout:

```text
~/workspace/hermes-runes-md-wiki
```

Hermes-agent reported that both checkouts existed and had the same current HEAD:

```text
b31ac6b
```

It classified the developer checkout as acceptable for read-only document answering when content is equivalent, but not as the correct root for controlled CB trial execution validation.

## Boundary Self-check Result

```text
read-only preserved: yes
trial root identified: yes
developer root distinguished: yes
trusted wiki mutation attempted: no
proposal created: no
promotion attempted: no
```

## Non-blocking Bug

```text
TB-20260607-001
Status: OPEN
Severity: S3 minor
```

Hermes-agent cited one line as `hermes-rnes-md-wiki`, which appears to be a typo in the quoted text. This does not block M156 because the actual identified trial root and boundary self-check used the correct path:

```text
~/workspace-trial/hermes-runes-md-wiki
```

Tracking record:

```text
wiki/k6-freelancer/trial-bugs.md#tb-20260607-001-m156-trial-root-quote-typo-in-hermes-agent-output
```

## Watch Item Status

```text
CB-WATCH-20260607-001
Status: CLOSED / trial-root discipline verified for read-only CB check
```

## Boundary Confirmation

```text
no new runtime feature
no trusted memory mutation
no proposal creation
no promotion
no import/index refresh
no backend change
```

## Next Action

Proceed to:

```text
M157 First Real User Technical Input CB Session
```

M157 should run a low-risk real technical input through Hermes-agent as a read-only memory-backed analysis session.

## Final Lock

```text
M156 Trial-root Discipline CB Check
PASS / trial-root discipline verified / read-only
```
