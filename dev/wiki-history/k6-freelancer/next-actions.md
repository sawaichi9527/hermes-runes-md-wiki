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
```

Released tag:

```text
v0.7.3 -> b60ed3c
```

Next selected work:

```text
M229 Runes Shield runtime acknowledgement protocol design
```

M229 problem:

```text
Fresh Hermes Agent / Lark bot onboarding can make the bot verbally accept the Runes Wiki boundary,
but later actions may still rely on prompt memory and direct tool edits rather than a verifiable
Runes Shield gate or evidence-backed approval state.
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
- Do not add heavy runtime enforcement, daemons, queues, telemetry, or enterprise workflow for M229.
