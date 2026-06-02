# M30.3b Multi-layer Naming & Narrative Model

Status: M30.3b POLICY / NARRATIVE MODEL / NO CODE CHANGE
Milestone: M30.3b Multi-layer Naming & Narrative Model
Chinese: M30.3b 多層命名與敘事模型

## Purpose

M30.3b defines how Hermes Runes MD Wiki separates engineering naming from Runes Shield semantics and user-facing narrative responses.

This policy exists because the project needs both:

- maintainable engineering names for files and implementation
- evocative Runes-style language for Hermes-agent interaction and user-visible responses

This milestone does not rename files or change runtime behavior.

## Core Principle

```text
Implementation filenames must be boring, explicit, and maintainable.
Runes Shield semantics may be evocative and mythic.
User-facing Hermes-agent responses should preserve the Runes narrative when reporting governed memory actions.
```

Chinese summary:

```text
底層工程命名要清楚無聊。
Shield 語義層可以中二。
回覆使用者時也要把符文儀式感傳出來。
```

## Three-layer Model

M30.3b defines three naming/response layers:

```text
Layer 1: Engineering Implementation Layer
Layer 2: Runes Shield Semantic Interface Layer
Layer 3: User-facing Ritual Response Layer
```

These layers must map cleanly to each other.

## Layer 1: Engineering Implementation Layer

Audience:

```text
developer / maintainer / local operator
```

Naming style:

```text
boring
explicit
grep-able
stable
maintenance-oriented
```

Examples:

```text
proposal_create.py
proposal_read.py
attunement_preview.py
promotion_preview.py
promotion_preflight.py
apply_controlled.py
refresh_importer.py
recall_verify.py
retrieval_consistency_smoke.py
seal_baseline.py
```

Layer 1 should avoid unnecessary mythic names in filenames.

## Layer 2: Runes Shield Semantic Interface Layer

Audience:

```text
Hermes-agent / future agent framework / controlled tool interface
```

Naming style:

```text
short semantic verbs
consistent Runes vocabulary
governed action concepts
```

Canonical semantic actions:

```text
forge
attune
promote
apply
refresh
recall
seal
archive
```

Examples:

```text
Runes Shield: forge proposal
Runes Shield: attune memory
Runes Shield: promote candidate
Runes Shield: controlled apply
Runes Shield: refresh runes index
Runes Shield: recall verify
Runes Shield: seal baseline
Runes Shield: archive relic
```

Layer 2 may use evocative wording, but it must map to concrete Layer 1 tools.

## Layer 3: User-facing Ritual Response Layer

Audience:

```text
user receiving Hermes-agent response
```

Purpose:

```text
Preserve the Runes Shield identity and ritual feedback when governed memory actions complete, fail, or are blocked.
```

Layer 3 is not merely internal naming.

Hermes-agent should pass the narrative state to the user when appropriate.

Examples:

```text
Runes Forge Success / 符文鑄造成功
Runes Attunement Complete / 符文調律完成
Runes Promotion Authorized / 符文晉升授權完成
Runes Apply Sealed / 符文套用封存完成
Runes Refresh Complete / 符文索引刷新完成
Runes Recall Verified / 符文追憶驗證完成
Runes Seal Established / 符文封印建立完成
Runes Archive Prepared / 符文遺物歸檔準備完成
```

## Layer Mapping Table

| Engineering Layer | Runes Shield Semantic Layer | User-facing Ritual Response |
| --- | --- | --- |
| proposal_create.py | forge proposal | Runes Forge Success / 符文鑄造成功 |
| attunement_preview.py / attunement_record.py | attune memory | Runes Attunement Complete / 符文調律完成 |
| promotion_preview.py | promote candidate | Runes Promotion Preview Ready / 符文晉升預覽完成 |
| promotion_preflight.py | preflight promotion | Runes Preflight Passed / 符文預檢通過 |
| apply_controlled.py | controlled apply | Runes Apply Sealed / 符文套用封存完成 |
| refresh_importer.py | refresh runes index | Runes Refresh Complete / 符文索引刷新完成 |
| recall_verify.py | recall verify | Runes Recall Verified / 符文追憶驗證完成 |
| retrieval_consistency_smoke.py | consistency smoke | Runes Consistency Verified / 符文一致性驗證完成 |
| seal_baseline.py / verification docs | seal baseline | Runes Seal Established / 符文封印建立完成 |
| archive helper | archive relic | Runes Archive Prepared / 符文遺物歸檔準備完成 |

## Response Tone Rules

User-facing ritual responses should be:

- short
- consistent
- paired with plain engineering evidence
- never obscure failure reason
- never imply autonomous approval
- never hide safety boundaries

Good style:

```text
Runes Recall Verified / 符文追憶驗證完成。
Evidence: expected path and marker were found in retrieval results.
```

Bad style:

```text
The sacred archive has accepted the soul of memory.
```

Reason:

```text
Ritual flavor is allowed, but operational clarity must dominate.
```

## Success Response Pattern

Recommended pattern:

```text
<Runes phrase> / <Chinese phrase>。
Plain engineering summary.
Evidence pointers.
Next safe action.
```

Example:

```text
Runes Forge Success / 符文鑄造成功。
Proposal evidence has been created. It is not trusted memory yet.
Next: run attunement before promotion.
```

## Blocked Response Pattern

Recommended pattern:

```text
<Runes blocked phrase> / <Chinese phrase>。
Blocked reason.
No mutation occurred.
Next safe action.
```

Examples:

```text
Runes Apply Blocked / 符文套用受阻。
Expected pre-apply hash did not match the current target file.
No trusted wiki mutation occurred.
```

```text
Runes Recall Miss / 符文追憶未命中。
The expected marker was not found in trusted retrieval results.
No memory mutation occurred.
```

## Failure / Error Response Pattern

Recommended pattern:

```text
<Runes failure phrase> / <Chinese phrase>。
Technical failure summary.
Mutation status.
Suggested diagnostic command.
```

Example:

```text
Runes Refresh Failed / 符文索引刷新失敗。
Importer returned a non-zero exit code.
Trusted wiki content was not modified by this refresh step.
```

## Canonical Ritual Phrases

### Proposal / Forge

```text
Runes Forge Success / 符文鑄造成功
Runes Forge Drafted / 符文草案鑄成
Runes Forge Blocked / 符文鑄造受阻
```

### Attunement

```text
Runes Attunement Complete / 符文調律完成
Runes Attunement Pending / 符文調律待決
Runes Attunement Rejected / 符文調律駁回
```

### Promotion

```text
Runes Promotion Preview Ready / 符文晉升預覽完成
Runes Promotion Authorized / 符文晉升授權完成
Runes Promotion Blocked / 符文晉升受阻
```

### Apply

```text
Runes Apply Sealed / 符文套用封存完成
Runes Apply Blocked / 符文套用受阻
Runes Apply Rolled Back / 符文套用回復完成
```

### Refresh

```text
Runes Refresh Complete / 符文索引刷新完成
Runes Refresh Required / 符文索引需要刷新
Runes Refresh Failed / 符文索引刷新失敗
```

### Recall

```text
Runes Recall Verified / 符文追憶驗證完成
Runes Recall Miss / 符文追憶未命中
Runes Recall Ambiguous / 符文追憶結果不明
```

### Seal / Archive

```text
Runes Seal Established / 符文封印建立完成
Runes Seal Candidate / 符文封印候選
Runes Archive Prepared / 符文遺物歸檔準備完成
```

## Safety Language Requirements

Ritual language must never claim:

- autonomous approval
- hidden memory mutation
- guaranteed truth
- deletion without confirmation
- trusted memory status before controlled apply

Required safety phrases when applicable:

```text
not trusted memory yet
no trusted wiki mutation occurred
refresh is still required
recall verification is still required
human confirmation is required
```

## Relationship to M30.2 and M30.3

M30.2 defines naming policy.

M30.3 defines metadata/header standards.

M30.3b adds narrative mapping:

```text
engineering name
→ Runes Shield semantic action
→ user-visible ritual response
```

M30.4 should use this model when planning entrypoint consolidation.

## M30.3b Does Not Authorize

M30.3b does not authorize:

- renaming files
- changing CLI behavior
- changing Hermes-agent prompts
- changing runtime output
- adding automatic narrative generation
- weakening engineering clarity

Actual response template implementation should be a later M30/M31 task.

## Verification Status

M30.3b Multi-layer Naming & Narrative Model:

- engineering layer defined: PASS
- Runes Shield semantic layer defined: PASS
- user-facing ritual response layer defined: PASS
- layer mapping table defined: PASS
- success/block/failure response patterns defined: PASS
- canonical ritual phrases defined: PASS
- safety language requirements defined: PASS
- no-code-change boundary preserved: PASS

Overall:

M30.3b Multi-layer Naming & Narrative Model:
PASS / narrative policy defined / no code change performed
