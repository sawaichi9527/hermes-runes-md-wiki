# Hermes Runes MD Wiki

Markdown wiki source-of-truth for governed local RAG memory.

> **Open Beta:** Hermes Runes MD Wiki is prepared for public Open Beta evaluation. It is suitable for personal/local evaluation and feedback collection, but it is not a stable public release, not an enterprise support commitment, and not a production guarantee.

Hermes Runes MD Wiki is a local-first, agent-agnostic memory substrate that uses curated Markdown wiki content as durable long-term knowledge, with PostgreSQL / FTS / pgvector retrieval, governed context assembly, and controlled wiki operations.

Hermes Runes was originally developed for Hermes Agent, but it is intentionally designed as an agent-agnostic subsystem that can be called by Hermes Agent, OpenClaw, MCP-compatible agents, OpenAI-compatible systems, or future local agent frameworks.

---

## Open Beta Starter

Fresh Open Beta testers should start here:

Current released fresh install path: `v0.7.1`

```text
docs/fresh-install-manual.md
```

Current Open Beta target: `v0.7.1`
Previous released baseline: `v0.7.0`

```text
docs/open-beta-starter.md
docs/v0.7.0-tester-checklist.md
docs/releases/v0.7.1.md
```

The starter path uses a clean runtime wiki seed and a host-derived workspace slug. The fresh install manual records the current Docker / PostgreSQL / pgvector / bootstrap / migration / import / FTS smoke path for new checkouts on `main`.

---

## Existing Installation Updates

If this repository has already been used locally and `wiki/` may contain personal or project knowledge, prefer the migration guard instead of a naked `git pull`:

```bash
./bin/runes-wiki-migration-guard update
```

The guard is a small local safety helper. It backs up `wiki/`, checks incoming repository changes, applies only safe or system/index-only updates, and stops before pull if an incoming update may touch possible user-owned Markdown.

It does not automatically merge, restore, delete, or overwrite user-owned Markdown.

See:

```text
docs/runes-wiki-migration-guard.md
```

---

## Runtime Layout

```text
wiki/              Runtime Markdown memory seed.
wiki/_system/      Governed memory rules and system-facing policy.
wiki/freelancer/   Current dogfood active workspace seed.
docs/              Public tester / runtime documentation.
dev/               Developer-only history, specs, milestones, and evidence.
```

For other installations, the active workspace should be derived from the local hostname:

```text
wiki/<lowercase-hostname>/
```

`freelancer` is the current dogfood host instance, not a universal default for every tester.

Developer history is retained under `dev/` and should not be imported as runtime user memory by default.

---

## Optional OPC Workspace Overlay

Hermes Runes MD Wiki keeps the same governed access model for both single-agent and OPC usage.

When Hermes Agent OPC profile agents are used, profile memory may be organized under:

```text
wiki/<workspace-slug>/opc/
```

This overlay is optional. Forkers and users who run a single agent do not need it.

See:

```text
docs/opc-workspace-overlay.md
wiki/freelancer/opc/README.md
```

---

## Open Beta Boundary

```text
Open Beta means:
- public repository evaluation
- personal/local testing
- feedback and issue discovery are welcome
- docs and implementation may still change

Open Beta does not mean:
- stable release
- production support guarantee
- enterprise support commitment
- autonomous trusted memory writing
- automatic proposal apply
- storing secrets in Markdown wiki memory
```

See also:

```text
docs/fresh-install-manual.md
docs/open-beta-starter.md
docs/v0.7.0-tester-checklist.md
docs/releases/v0.7.1.md
docs/workspace-slug-policy.md
SECURITY.md
```

---

## License

Hermes Runes MD Wiki is licensed under the Apache License, Version 2.0.

See `LICENSE` for the full license text.

---

## Philosophy

Runtime memory is temporary.

Curated Markdown memory is durable.

Hermes Runes treats Markdown as intentional knowledge carved into durable runes rather than transient conversation state.

The database is an index and retrieval backend.

The Markdown wiki remains the human-readable source-of-truth.

Hermes Runes does not decide truth for the agent.
