# M30.5 Code Risk Review

Status: M30.5 REVIEW / NO CODE CHANGE
Milestone: M30.5 Code Risk Review
Chinese: M30.5 程式風險盤點
Runes Narrative Phrase: Runes Risk Sight / 符文風險視界

## Purpose

M30.5 reviews current code and workspace risk before any refactor, archive, deletion, or entrypoint consolidation is implemented.

This milestone is a review document only.

It does not change code, CLI behavior, runtime behavior, file locations, or trusted wiki content.

## Review Context

M30.5 follows:

```text
M30.1 Repository Inventory / Technical Debt Map
M30.2 Canonical Naming Policy
M30.3 File Header / Version Metadata Standard
M30.3b Multi-layer Naming & Narrative Model
M30.3c Personal-use & Perceived Latency Observation Policy
M30.4 Entrypoint Consolidation Plan
```

Current baseline anchors:

```text
Runes Seal: origin/archive/p0-runes-seal
Pre-M30 local backup: ~/workspace/hermes-runes-md-wiki.local-backup-20260602-runes-seal-pre-m30/
```

## Risk Scale

M30.5 uses a simple personal-project risk scale:

```text
low
medium
high
critical
```

This is not enterprise risk management.

It is a lightweight map to decide what must be preserved, reviewed, wrapped, archived, or avoided before P0 trial run.

## Risk Category Summary

| Area | Risk | Reason | M30 direction |
| --- | --- | --- | --- |
| Controlled apply boundary | high | trusted wiki mutation path must remain safe | preserve first, refactor later |
| Recall verification semantics | high | false positive recall caused earlier issue | keep strict result-only checks |
| Importer refresh boundary | medium-high | refresh changes retrieval/index state | wrap carefully, preserve direct tool use |
| Helper sprawl | medium | many Mxx helpers overlap in purpose | classify before rename/archive |
| Root milestone shell scripts | medium | root clutter and stale wrappers | archive later, no immediate deletion |
| Dirty workspace drift | medium | local changes may contain useful history | preserve backup and inventory |
| Operation evidence | medium | useful governance evidence but can clutter repo | retention/archive policy needed |
| Narrative response layer | low-medium | can confuse if it hides engineering state | keep ritual phrase + plain evidence |
| Python runtime latency | low-medium | not proven bottleneck | observe perceived latency only |
| Secrets handling | critical | real secrets must never enter wiki/git | preserve strict exclusion policy |

## Critical Invariant: No Secrets in Wiki/Git

Risk:

```text
critical
```

Rule:

```text
Real secrets must not be stored in Markdown memory or git.
```

Includes:

```text
PostgreSQL passwords
LM Studio/OpenAI-compatible API keys
Telegram bot tokens
Tavily keys
future service credentials
```

M30 refactor must not import `.env`, local secret files, or operation logs containing secrets into trusted wiki content.

## Controlled Apply Risk

Risk:

```text
high
```

Reason:

```text
Controlled apply is the path that can write trusted Markdown wiki content.
It must preserve human approval, expected-hash guard, rollback snapshot, and operation record semantics.
```

Must preserve:

- explicit human confirmation token
- expected pre-apply hash check
- single target path discipline
- rollback snapshot generation
- operation record generation
- no autonomous trusted writer behavior

M30 direction:

```text
Do not refactor controlled apply until smoke coverage and wrapper compatibility are confirmed.
Prefer wrapping first, then internal cleanup later.
```

## Recall Verification Risk

Risk:

```text
high
```

Reason:

```text
Earlier M29.1 exposed a false-positive risk when verifier payload fields were checked instead of actual retrieval results.
```

Must preserve:

- strict retrieval-result-only verification
- expected path validation inside results
- expected marker validation inside results
- result_count_positive when required
- negative recall semantics for rejected knowledge

M30 direction:

```text
Do not loosen recall verifier behavior.
Any consolidation into runes recall verify must preserve strict M28.3 v2 behavior.
```

## Importer Refresh Risk

Risk:

```text
medium-high
```

Reason:

```text
Importer refresh updates database/index state and affects retrieval behavior.
It is not trusted wiki mutation, but it can change what future recall returns.
```

Must preserve:

- explicit refresh boundary
- operation record when refresh helper runs
- direct importer usability
- no hidden refresh after unrelated actions unless explicitly designed later

M30 direction:

```text
Future runes refresh importer may wrap importer refresh, but should not hide the refresh boundary.
```

## Helper Sprawl Risk

Risk:

```text
medium
```

Reason:

```text
Many milestone-numbered helpers exist and may overlap in role.
Renaming them blindly may lose historical traceability.
```

Examples:

```text
proposal_writer_m22_1.py
proposal_reader_m22_2.py
proposal_hygiene_m22_3.py
promotion_apply_m27_2.py
import_refresh_m28_2.py
scenario_add_knowledge_m29_1.py
scenario_reject_m29_2.py
scenario_correction_update_m29_3.py
```

M30 direction:

```text
Classify first.
Wrap canonical paths second.
Mark legacy third.
Archive later.
Delete last, if ever.
```

## Scenario Runner Risk

Risk:

```text
low-medium
```

Reason:

```text
Scenario runners are historical evidence tools. They are useful but should not become canonical runtime APIs.
```

Must preserve:

- M29.1 add knowledge scenario
- M29.2 reject/no-promotion scenario
- M29.3 correction/update scenario
- historical reproducibility

M30 direction:

```text
Keep scenario runner names milestone-addressable.
Do not fold them into canonical modules unless a separate wrapper is created.
```

## Root Milestone Shell Script Risk

Risk:

```text
medium
```

Reason:

```text
Root-level M24/M25/M26 shell scripts clutter the repo and may duplicate current tool behavior.
However, they may still hold useful historical execution recipes.
```

M30 direction:

```text
Do not delete directly.
Classify each script.
Archive to tools/archive/milestone-shell/ only after review.
```

## Dirty Workspace Drift Risk

Risk:

```text
medium
```

Known inventory:

```text
modified files: 21
untracked files: 41
operations records: 20
root milestone shell files: 13
forge-inbox files: 5
inventory lines: 141
```

Risk:

```text
Some local files may contain important evolution history, but others may be stale runtime artifacts.
```

M30 direction:

```text
Use inventory + backup as preservation layer.
Do not bulk restore or bulk clean until classification is done.
```

## Operation Evidence Risk

Risk:

```text
medium
```

Reason:

```text
operations/ records are useful governance evidence but can grow and clutter the repo.
```

M30 direction:

```text
Keep for now.
Define retention/archive policy before moving or deleting.
Do not ingest operation evidence into RAG by default.
```

## Reports Risk

Risk:

```text
low-medium
```

Reason:

```text
reports/ contains inventory and review evidence useful during M30, but may not be long-term trusted wiki content.
```

M30 direction:

```text
Keep local reports unless explicitly promoted to wiki docs.
Archive or ignore later based on usefulness.
```

## Forge Inbox Risk

Risk:

```text
medium
```

Reason:

```text
forge-inbox may contain proposal candidates that are not trusted memory.
Mixing inbox content into trusted wiki would violate governance boundaries.
```

M30 direction:

```text
Treat forge-inbox as untrusted proposal material.
Do not promote without attunement/promotion/apply governance.
```

## Narrative Layer Risk

Risk:

```text
low-medium
```

Reason:

```text
Runes ritual phrases improve UX, but could confuse users if they hide operational truth.
```

Must preserve:

```text
ritual phrase + plain engineering evidence
```

Example:

```text
Runes Recall Verified / 符文追憶驗證完成。
Evidence: expected path and marker were found in retrieval results.
```

M30 direction:

```text
Narrative response layer should never replace plain status, evidence, or safety boundary.
```

## Python Runtime / Perceived Latency Risk

Risk:

```text
low-medium
```

Reason:

```text
Python may not be the main latency bottleneck. P0/P1 should not add complexity based on theoretical runtime concerns.
```

M30 direction:

```text
Keep Python.
Observe only personal-use perceived latency later if needed.
Do not add daemon, Go/Rust rewrite, metrics DB, or observe index in M30.
```

Narrative concept:

```text
Runes Aura Sense / 符文靈氣感知
```

## Importer / Retrieval Hot Path Risk

Risk:

```text
medium
```

Reason:

```text
Importer, hybrid search, and answer/retrieval helpers are likely closer to user-perceived delay than simple Python control logic.
```

M30 direction:

```text
Do not optimize before observing.
Preserve existing retrieval behavior and smoke coverage.
```

## Recommended M30.6 Inputs

M30.5 recommends M30.6 Legacy Archive / Deprecation Plan should classify files into:

```text
keep_canonical
wrap_later
legacy_supported
archive_candidate
delete_candidate
local_only
```

Priority review order:

```text
1. root milestone shell scripts
2. tools/runes M22-M29 helpers
3. scenario runners
4. operation evidence
5. reports
6. forge-inbox
```

## No-change Boundary

M30.5 does not perform:

- code refactor
- file rename
- file movement
- archive movement
- deletion
- CLI change
- runtime behavior change
- observation implementation
- response-template implementation

It only reviews risk.

## Verification Status

M30.5 Code Risk Review:

- risk scale defined: PASS
- controlled apply risk reviewed: PASS
- recall verification risk reviewed: PASS
- importer refresh risk reviewed: PASS
- helper sprawl risk reviewed: PASS
- scenario runner risk reviewed: PASS
- root milestone shell script risk reviewed: PASS
- dirty workspace drift risk reviewed: PASS
- operation evidence risk reviewed: PASS
- forge inbox risk reviewed: PASS
- narrative layer risk reviewed: PASS
- Python/perceived latency risk reviewed: PASS
- secrets invariant preserved: PASS
- no-code-change boundary preserved: PASS

Overall:

M30.5 Code Risk Review:
PASS / risk review defined / no code change performed
