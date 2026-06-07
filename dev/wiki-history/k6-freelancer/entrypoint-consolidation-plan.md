# M30.4 Entrypoint Consolidation Plan

Status: M30.4 PLAN / NO CLI CHANGE YET
Milestone: M30.4 Entrypoint Consolidation Plan
Chinese: M30.4 入口收斂規劃

## Purpose

M30.4 defines the future entrypoint layout for Hermes Runes MD Wiki before any CLI refactor, file rename, archive move, or shell-script cleanup is performed.

This milestone is a plan only.

It does not change runtime behavior.

## Governing Inputs

M30.4 depends on the previous M30 policy layer:

```text
M30.1 Repository Inventory / Technical Debt Map
M30.2 Canonical Naming Policy
M30.3 File Header / Version Metadata Standard
M30.3b Multi-layer Naming & Narrative Model
M30.3c Personal-use & Perceived Latency Observation Policy
```

M30.4 must preserve:

- Runes Seal rollback anchor
- P0 governed proposal/apply/refresh/recall behavior
- human approval boundaries
- controlled apply hash guard
- operation record generation
- rollback evidence generation
- strict recall-result-only verification
- Python as default implementation for P0/P1
- personal-use simplicity and durability

## Current Entrypoint Surface

Current known operator-facing entrypoints include:

```text
bin/runes
bin/hermes-recall
bin/hermes-memory-smoke
```

Current helper/tool surface includes:

```text
tools/runes/*.py
tools/importer/*.py
root-level m24_*.sh / m25_*.sh / m26_*.sh milestone scripts
scenario runners
smoke helpers
```

M30.4 classifies these without moving them yet.

## Canonical Entrypoint Strategy

Long-term canonical entrypoints should be:

```text
bin/runes
bin/hermes-recall
bin/hermes-memory-smoke
```

### bin/runes

Role:

```text
Primary governed memory operator entrypoint.
Stable CLI surface for Runes Shield operations.
```

Future direction:

```text
runes proposal ...
runes attune ...
runes promote ...
runes apply ...
runes refresh ...
runes recall ...
runes smoke ...
runes archive ...
```

Layer mapping:

```text
Engineering command surface:
runes proposal create

Runes Shield semantic layer:
forge proposal

User-facing response layer:
Runes Forge Success / 符文鑄造成功
```

### bin/hermes-recall

Role:

```text
Stable recall/query entrypoint.
Can remain separate because recall is frequently used directly by humans and tools.
```

Future direction:

```text
Keep as canonical retrieval entrypoint.
Also allow bin/runes recall verify to wrap strict verification use cases.
```

### bin/hermes-memory-smoke

Role:

```text
Stable smoke-test entrypoint.
Used for quick health/regression validation.
```

Future direction:

```text
Keep as canonical smoke entrypoint.
Also allow bin/runes smoke p0 to wrap governed P0 smoke flows later.
```

## Proposed Future runes Subcommands

M30.4 proposes this future subcommand layout:

```text
runes proposal create
runes proposal read
runes proposal list
runes proposal hygiene

runes attune preview
runes attune record

runes promote preview
runes promote preflight

runes apply controlled
runes refresh importer
runes recall verify
runes smoke p0
runes archive plan
```

This is not implemented in M30.4.

M30.4 only defines the consolidation target.

## Engineering Tool Mapping

| Future command | Engineering helper candidate | Runes semantic layer | User-facing phrase |
| --- | --- | --- | --- |
| runes proposal create | proposal_create.py | forge proposal | Runes Forge Success / 符文鑄造成功 |
| runes proposal read | proposal_read.py | inspect proposal | Runes Proposal Revealed / 符文草案顯現 |
| runes proposal list | proposal_list.py | list proposals | Runes Proposals Listed / 符文草案列示完成 |
| runes proposal hygiene | proposal_cleanup.py | proposal hygiene | Runes Proposal Hygiene Complete / 符文草案淨化完成 |
| runes attune preview | attunement_preview.py | attune memory | Runes Attunement Pending / 符文調律待決 |
| runes attune record | attunement_record.py | record attunement | Runes Attunement Complete / 符文調律完成 |
| runes promote preview | promotion_preview.py | promote candidate | Runes Promotion Preview Ready / 符文晉升預覽完成 |
| runes promote preflight | promotion_preflight.py | preflight promotion | Runes Preflight Passed / 符文預檢通過 |
| runes apply controlled | apply_controlled.py | controlled apply | Runes Apply Sealed / 符文套用封存完成 |
| runes refresh importer | refresh_importer.py | refresh runes index | Runes Refresh Complete / 符文索引刷新完成 |
| runes recall verify | recall_verify.py | recall verify | Runes Recall Verified / 符文追憶驗證完成 |
| runes smoke p0 | smoke_p0.py | P0 smoke | Runes Consistency Verified / 符文一致性驗證完成 |
| runes archive plan | archive_plan.py | archive relic | Runes Archive Prepared / 符文遺物歸檔準備完成 |

## Existing Helper Classification Direction

Existing `tools/runes/*.py` files should be classified before any rename.

Likely categories:

```text
canonical_governance_tool
scenario_runner
milestone_helper
legacy_supported
archive_candidate
```

### Scenario Runners

Files such as:

```text
scenario_add_knowledge_m29_1.py
scenario_reject_m29_2.py
scenario_correction_update_m29_3.py
```

should remain milestone-addressable as historical validation tools.

Classification:

```text
scenario_runner
```

They should not be renamed into canonical runtime modules unless duplicated or wrapped by a stable smoke command.

### M22-M29 Milestone Helpers

Files such as:

```text
proposal_writer_m22_1.py
proposal_reader_m22_2.py
proposal_hygiene_m22_3.py
promotion_apply_m27_2.py
import_refresh_m28_2.py
```

should be reviewed individually.

Possible outcomes:

```text
legacy_supported
archive_candidate
converted_to_canonical_tool
```

No automatic conversion should happen.

### Importer and Recall Runtime

Files under `tools/importer/` remain core retrieval/importer implementation.

M30.4 does not move them.

Future `runes refresh importer` and `runes recall verify` may wrap importer/recall behavior, but should not make the importer less usable as direct engineering tooling.

## Root Milestone Shell Script Direction

Root-level scripts such as:

```text
m24_*.sh
m25_*.sh
m26_*.sh
```

should not remain canonical root entrypoints long-term.

M30.4 direction:

```text
1. classify each script
2. preserve historical evidence until reviewed
3. move to archive only after smoke coverage is confirmed
4. delete only after backup, anchor, and replacement decision exist
```

Preferred future archive location:

```text
tools/archive/milestone-shell/
```

No root milestone shell script should be promoted as the main operator entrypoint.

## Hermes-agent Interface Stability

Hermes-agent should depend on stable Runes Shield operations, not internal helper filenames.

Preferred long-term agent-facing verbs:

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

However, implementation files should remain engineering-clear.

Example mapping:

```text
Hermes-agent semantic action:
Runes Shield: forge proposal

Engineering implementation:
proposal_create.py

User-visible response:
Runes Forge Success / 符文鑄造成功
```

## Narrative Boundary

M30.4 must not force mythic names into implementation filenames.

Rule:

```text
Engineering layer stays boring and explicit.
Runes Shield semantic layer may be evocative.
User-facing response may preserve ritual phrasing.
```

Example:

```text
Good engineering filename:
apply_controlled.py

Good user-facing response:
Runes Apply Sealed / 符文套用封存完成。
```

## Latency / Runtime Boundary

M30.4 keeps Python as the default P0/P1 implementation.

Entrypoints should remain implementation-neutral, but this does not mean adding runtime complexity now.

M30.4 does not introduce:

- Go rewrite
- Rust rewrite
- daemon
- metrics DB
- observe index
- tracing framework

Future P2/P3 optimization must be based on Personal-use & Perceived Latency Observation Policy.

Narrative concept:

```text
Runes Aura Sense / 符文靈氣感知
```

Meaning:

```text
Observe user-perceived waiting points lightly, without turning a personal memory project into enterprise observability.
```

## Compatibility Policy

During M30 and P0 trial-run preparation:

```text
Existing working commands should not be broken without replacement.
Legacy helpers may continue to exist.
Canonical wrappers may be added later.
Deprecation should be documented before removal.
```

M30.4 does not require a single grand migration.

Preferred approach:

```text
wrap first
verify
mark legacy
archive later
remove last
```

## Proposed Migration Sequence

Suggested future sequence after M30.4:

```text
M30.5 Code Risk Review
M30.6 Legacy Archive / Deprecation Plan
M30.7 Pre-release Smoke Suite
M30.8 Optional first canonical wrapper additions
```

Potential wrapper addition order:

```text
1. runes recall verify
2. runes refresh importer
3. runes apply controlled
4. runes proposal create/list/read
5. runes smoke p0
```

Rationale:

```text
recall/refresh/apply are closest to P0 trial-run critical path.
proposal and smoke wrappers can follow once safety behavior remains verified.
```

## No-change Boundary

M30.4 does not perform:

- CLI rewrite
- helper rename
- file movement
- archive move
- deletion
- daemonization
- runtime implementation replacement
- response-template implementation

It only defines the consolidation target.

## Verification Status

M30.4 Entrypoint Consolidation Plan:

- current entrypoint surface identified: PASS
- canonical entrypoint strategy defined: PASS
- future runes subcommands proposed: PASS
- engineering tool mapping defined: PASS
- scenario runner classification direction defined: PASS
- milestone helper classification direction defined: PASS
- root milestone shell script direction defined: PASS
- Hermes-agent interface stability defined: PASS
- narrative boundary preserved: PASS
- Python/P0 latency boundary preserved: PASS
- compatibility policy defined: PASS
- no-CLI-change boundary preserved: PASS

Overall:

M30.4 Entrypoint Consolidation Plan:
PASS / consolidation target defined / no CLI change performed
