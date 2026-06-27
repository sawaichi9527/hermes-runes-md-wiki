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

---

## N-20260617-v0.7.4-dev-opened

Status: READY / v0.7.4-dev opened / M229 direction recorded

Current baseline:

```text
main: single-agent / agent-agnostic active development baseline
VERSION: 0.7.4-dev
v0.7.3: released tag
v0.7.2: archived release point
archive/v0.7.2-opc: archived branch
```

Resolved in v0.7.3:

```text
M222 PASS / single-agent sanity locally verified
M223 PASS / active guidance approved and documented
M224 PASS / sync path locally verified
M225 PASS / optional embedding boundary locally verified
M226 PASS / RC locally verified / ready for final release
M227 PASS / v0.7.3 released and tagged
```

Opened after v0.7.3:

```text
M228 PASS / v0.7.4-dev opened / planning pending
M229 RECORDED / Runes Shield runtime acknowledgement gap / not implemented
```

Release artifacts:

```text
docs/releases/v0.7.3.md
dev/wiki-history/k6-freelancer/verification/verification-m227.md
dev/wiki-history/k6-freelancer/verification/verification-m228.md
```

v0.7.4-dev planning artifacts:

```text
docs/runes-shield-runtime-acknowledgement-gap.md
dev/wiki-history/k6-freelancer/verification/verification-m229.md
docs/plur-runtime-memory-bridge.md
```

Released tag:

```text
v0.7.3 -> b60ed3c
```

Next selected work:

```text
S1-S6 PLUR runtime memory bridge reintegration
```

M229 problem:

```text
Fresh Hermes Agent / Lark bot onboarding can make the bot verbally accept the Runes Wiki boundary,
but later actions may still rely on prompt memory and direct tool edits rather than a verifiable
Runes Shield gate or evidence-backed approval state.
```

M229 observation sample:

```text
O-M229-001: temporary Lark reply footer observation
- User asked the bot to append whether Runes Shield was used.
- Bot saved a footer rule and replied with `[Runes Shield: 無]`.
- This improves response visibility but is not proof that a Shield gate, guard, approval path, or git evidence check ran.
```

M229 clarification:

```text
The response footer is a short-to-mid-term observation aid only.
It may help validate whether the agent is moving toward the intended behavior.
After the real evidence path is confirmed, the footer requirement should be disabled or removed.
It must not become the formal governance mechanism.
```

M229 direction:

```text
Define a lightweight acknowledgement protocol that distinguishes:
- policy recalled from memory
- read-only action
- proposal-only action
- direct patch
- wiki write
- commit/push
- explicit user approval
- migration guard / security scan / commit evidence
- no shield used
```

Post-release guidance:

- Keep `main` single-agent / agent-agnostic.
- Keep OPC profile-agent architecture out of active mainline.
- Keep Kanban as a lightweight checkpoint layer only.
- Keep optional embedding dependencies out of the required core baseline.
- Continue using `./bin/runes-wiki-migration-guard update` for existing installs.
- Treat `Runes Shield: yes/no` as insufficient unless backed by evidence.
- Treat visible footer output as temporary observability, not a permanent feature.
- Do not add heavy runtime enforcement, daemons, queues, telemetry, or enterprise workflow for M229.
