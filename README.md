# Hermes Runes MD Wiki

Markdown wiki source-of-truth for governed local RAG memory.

> **Open Beta:** Hermes Runes MD Wiki is prepared for public Open Beta evaluation. It is suitable for personal/local evaluation and feedback collection, but it is not a stable public release, not an enterprise support commitment, and not a production guarantee.

Hermes Runes MD Wiki is a local-first, agent-agnostic memory substrate that uses curated Markdown wiki content as durable long-term knowledge, with PostgreSQL / FTS / pgvector retrieval, governed context assembly, and controlled wiki operations.

Hermes Runes was originally developed for Hermes Agent, but it is intentionally designed as an agent-agnostic subsystem that can be called by Hermes Agent, OpenClaw, MCP-compatible agents, OpenAI-compatible systems, or future local agent frameworks.

---

## Open Beta Starter

Fresh Open Beta testers should start here:

```text
docs/open-beta-starter.md
```

The starter path uses the active workspace slug `freelancer` and avoids legacy engineering evidence as the default onboarding path.

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
docs/open-beta-publication-checklist.md
SECURITY.md
```

---

## Default Workspace Slug

For Open Beta, the default active workspace slug is:

```text
freelancer
```

The default user-facing wiki namespace is:

```text
wiki/freelancer/
```

Historical engineering records may still reference `wiki/k6-freelancer/`; that namespace is legacy project evidence and is not the default public user workspace.

See `docs/workspace-slug-policy.md` for the slug policy.

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
