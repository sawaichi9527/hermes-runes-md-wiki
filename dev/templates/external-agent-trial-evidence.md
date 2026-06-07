# External Agent Trial Evidence: <runtime-name> / <trial-id>

## Metadata

- Trial ID: external-agent-trial-YYYYMMDD-<short-slug>
- Date: YYYY-MM-DD
- Workspace: ~/workspace/trial/hermes-runes-md-wiki
- Project: freelancer
- Workspace slug: freelancer
- Runtime name: <OpenClaw|other non-Hermes local governed agent>
- Runtime version / commit: <version-or-commit>
- Runtime classification: <real OpenClaw runtime validation|OpenClaw-compatible shape validation with a clearly identified non-Hermes local governed agent>
- Operator: human
- Status: draft

---

## Scope Statement

This evidence record is for a future external-agent trial only.

The trial must validate whether a non-Hermes local governed agent can read and understand the compact bootstrap / governed memory boundary without using Hermes-agent-specific behavior.

The trial is read-only.

No write, import, index, apply, promote, proposal mutation, database mutation, or wiki mutation is allowed.

---

## Pre-trial Repository State

Run before the external agent starts:

```bash
cd ~/workspace/trial/hermes-runes-md-wiki

git pull
git status --short
git log --oneline -5
```

Expected working tree state:

```text
no output from git status --short
```

Observed pre-trial evidence:

```text
<paste git pull / status / log evidence here>
```

---

## Runtime Identity Evidence

Record the actual runtime used.

```text
Runtime name:
Runtime source / binary path:
Runtime version:
Runtime launch command or invocation method:
Runtime local/remote boundary:
Runtime can read local files: yes/no
Runtime can write local files: yes/no
Runtime was configured read-only: yes/no
```

Invalid evidence:

```text
Hermes-agent-only validation presented as OpenClaw-compatible validation
Unidentified third-party runtime
A web-only answer with no local repository access
A trial without pre/post git status evidence
```

---

## Exact Prompt Used

Paste the exact prompt given to the external agent.

The prompt should be copied from the current compact bootstrap prompt/checklist baseline.

```text
<paste exact prompt here>
```
