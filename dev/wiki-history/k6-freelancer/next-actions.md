## N-20260617-Post-M221 Baseline Frozen

Status: FROZEN / no immediate required action

Current baseline:

```text
main: single-agent / agent-agnostic active baseline
VERSION: 0.7.3-dev
v0.7.2: archived release tag
archive/v0.7.2-opc: archived OPC-capable branch
```

M221 result:

```text
M221 De-OPC Mainline Rebaseline
PASS / single-agent mainline restored / RSS local commit preserved
```

Decisions:

- Hermes Agent profile-based OPC/A2A deployment is abandoned for this project.
- Active OPC overlay docs and workspace seed are removed from `main`.
- `v0.7.2` and `archive/v0.7.2-opc` preserve the old OPC-capable release baseline.
- Migration guard remains active.
- Existing-installation guarded update flow remains active.
- Local RSS active feeds commit is preserved on top of the de-OPC baseline.
- Abandoned OPC/PLUR operations log was not merged into active main.

No immediate required action.

Next work starts only when a concrete `0.7.3-dev` feature, bug fix, or documentation task is selected.
