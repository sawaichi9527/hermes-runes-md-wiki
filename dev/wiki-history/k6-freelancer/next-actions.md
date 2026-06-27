## N-20260627-v0.7.4-final-release

Status: FINAL RELEASE RECORDED / tag pending

Current decision:

```text
v0.7.4 is the formal release for the conservative PLUR runtime memory bridge documentation/governance-boundary line.
After v0.7.4 release marking, main advances to v0.7.5-dev.
```

Final v0.7.4 state:

```text
S1-S6  PLUR bridge scope / policy / hygiene recorded
S7-S9  design-only
S10    paused
S11    candidate dry-run design-only
S12    verification/docs sync design-only
```

Release artifacts:

```text
docs/releases/v0.7.4.md
dev/wiki-history/k6-freelancer/verification/verification-v0.7.4-final.md
docs/plur-runtime-memory-bridge.md
CHANGELOG.md
```

Final local verification evidence before release marking:

```text
Repo head: e84972c
git status: clean
migration guard: SAFE
Core FTS smoke: PASS
PLUR helper: not added
PLUR smoke: not added
embedding profile: SKIP as expected
```

Release boundary:

- No new PLUR runtime helper.
- No new PLUR smoke.
- No Hermes Agent core patch.
- No Hermes Agent native configuration change.
- No PLUR memory read/write/migration/deletion.
- No automatic PLUR-to-Runes Wiki promotion.

Tagging note:

```text
Create git tag v0.7.4 on the release commit where VERSION is 0.7.4.
```

Next selected work:

```text
Advance main to v0.7.5-dev after v0.7.4 release marking.
Keep PLUR runtime implementation paused unless a concrete need appears.
```

---

## N-20260627-v0.7.4-dev-plur-s10-s12-design-only

Status: DESIGN-ONLY / no runtime implementation

Decision:

```text
S10 is paused because PLUR read-only context summary value is unclear.
S11-S12 are design-only and add no runtime helper, smoke, PLUR read/write, or Hermes Agent tool surface.
```

Design scope:

```text
S10  Read-only PLUR context summary pause
S11  Candidate dry-run flow design
S12  Smoke / verification / docs sync design
```

S10 pause:

- Do not implement a PLUR context summary helper.
- Do not inject PLUR context by default.
- Do not add every-turn PLUR scanning.
- Revisit only if a concrete user-visible failure shows native Hermes Agent runtime memory is insufficient.

S11 candidate dry-run:

- Proposal-only.
- No wiki write.
- No PLUR write.
- No PLUR read requirement.
- No automatic promotion.
- User approval is required before any future forge path.
- User approval is not the same as forge completion.

Candidate card fields:

```text
Candidate:
- Type: decision | preference | project-state | warning | procedure | open-question
- Scope: <project/workspace/user scope>
- Source: current-conversation | user-instruction | PLUR-checkpoint | Runes-Wiki-reference | other
- Proposed target: wiki/<workspace>/... or undecided
- Proposal: <short memory statement>
- Why preserve: <why this should survive the current session>
- Risk: low | medium | high
- Approval state: pending
- Writes performed: none
```

S12 verification/docs sync:

```bash
cd ~/workspace/hermes-runes-md-wiki
git pull
git status
./bin/runes-wiki-migration-guard plan --no-fetch
./bin/hermes-memory-smoke
```

Expected result:

```text
git status clean
migration guard SAFE
Core FTS smoke PASS
no PLUR helper required
no PLUR smoke required
embedding profile skip remains acceptable when embedding profile is not installed
```

Next selected work:

```text
Local pull verification for S10-S12 design-only docs.
After that, pause PLUR runtime implementation unless a concrete need appears.
```

---

## N-20260627-v0.7.4-dev-plur-s7-s9-design-only

Status: DESIGN-ONLY / no runtime tool added

Decision:

```text
S7-S9 remain design-only for now.
Do not add a new PLUR runtime helper, smoke test, or Hermes Agent tool surface until explicitly approved.
```

Design scope:

```text
S7  PLUR read-only discovery / status check design
S8  Runtime memory provider abstraction / Noop provider design
S9  PLUR memory schema mapping design
```

Reason:

- v0.7.4-dev should stay simple and personal-use oriented.
- The project should avoid adding unnecessary runtime surface.
- Hermes Agent should not carry extra tool burden for a bridge that is not yet needed at runtime.
- Existing deployed PLUR memory must remain untouched.

Explicitly removed from this line:

```text
tools/importer/plur_runtime_bridge.py
tools/importer/smoke/eval_smoke_plur_bridge.py
S7-S9 implemented verification note
PLUR bridge invocation from ./bin/hermes-memory-smoke
```

Local verification requested:

```bash
cd ~/workspace/hermes-runes-md-wiki
git pull
git status
./bin/runes-wiki-migration-guard plan --no-fetch
./bin/hermes-memory-smoke
```

Expected result:

```text
git status clean
migration guard SAFE
Core FTS smoke PASS
no PLUR bridge smoke runs
embedding profile skip remains acceptable when embedding profile is not installed
```

Next selected work:

```text
S10 design discussion only: when and whether a read-only PLUR context summary is worth implementing.
No runtime implementation until explicitly approved.
```

---

## N-20260627-v0.7.4-dev-plur-runtime-memory-bridge

Status: READY / v0.7.4-dev scope recalibrated to PLUR reintegration

Current decision:

```text
v0.7.4-dev focuses on optional PLUR runtime memory bridge reintegration.
This is a deployed correction line for the current single-agent / agent-agnostic mainline.
It is not a long-range roadmap expansion and does not restore OPC profile-agent architecture.
```

Scope:

```text
S1  Detachable PLUR integration
S2  Minimal Hermes Agent native customization
S3  PLUR runtime memory role and source priority
S4  Engram / episode / checkpoint / candidate policy
S5  Human-in-the-loop forge candidate flow
S6  Minimal PLUR memory hygiene and deployed-memory caution
```

Implementation boundary:

```text
PLUR = optional runtime persistent working memory
Runes Wiki = governed canonical long-term memory source
Runes Shield = protected forge gate / operation protection layer
Hermes Agent / Lark bot = candidate proposer and task reasoner
User = human-in-the-loop approval authority
```

Key rules:

- PLUR must be detachable and non-required.
- Hermes Agent core must not be patched for this integration.
- Hermes Agent native settings should remain minimally customized.
- Existing deployed PLUR memory must be treated carefully as non-authoritative runtime state.
- Existing PLUR records must not be bulk migrated, bulk deleted, or promoted into Runes Wiki automatically.
- Candidate forge requires explicit user approval and Runes Shield protected operation.
- Do not add daemon, queue, telemetry, enterprise approval workflow, heavy LLM judge, or multi-profile mesh.

Primary planning artifact:

```text
docs/plur-runtime-memory-bridge.md
```

Next selected work:

```text
S7-S9 PLUR read-only discovery, Noop provider, and schema mapping design only.
```
