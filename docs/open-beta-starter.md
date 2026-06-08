# Open Beta Starter Guide

Status: STARTER / PUBLIC EVALUATION PATH / CLEAN RUNTIME SEED
Date: 2026-06-08
Recommended baseline: `v0.5.0`

## Purpose

Provide a clean public Open Beta entry path for fresh testers.

This guide uses the runtime wiki seed under `wiki/` and keeps developer history under `dev/`.

## Clone Path

Recommended checkout:

```bash
mkdir -p ~/workspace
cd ~/workspace
git clone https://github.com/sawaichi9527/hermes-runes-md-wiki.git
cd hermes-runes-md-wiki
```

## Runtime Wiki Layout

```text
wiki/
  _system/       Governed memory rules and system-facing policy.
  freelancer/   Dogfood active workspace seed for the Freelancer host.
```

For other hosts, use a hostname-derived workspace slug:

```bash
export HERMES_WORKSPACE_SLUG="$(hostname | tr '[:upper:]' '[:lower:]')"
export HERMES_PROJECT="$HERMES_WORKSPACE_SLUG"
```

The active wiki namespace is:

```text
wiki/<lowercase-hostname>/
```

Example for the current dogfood host:

```text
hostname: Freelancer
workspace_slug: freelancer
wiki_namespace: wiki/freelancer/
```

`freelancer` is only the current dogfood host instance, not a universal default for every tester.

## Forge Inbox Boundary

Each workspace may contain:

```text
wiki/<workspace-slug>/forge-inbox/
```

`forge-inbox/` is a local governed draft inbox.

Plain meaning:

```text
This is where proposed memory changes wait before human review.
```

Use it for:

- draft proposals created by an agent or helper tool
- unreviewed notes that should not yet become trusted memory
- human review, approval, rejection, or promotion through governed tooling

Do not treat files in `forge-inbox/` as trusted memory.

For public repository content, `forge-inbox/` should normally contain only README / placeholder metadata. Real local draft proposals are working artifacts and should normally remain uncommitted.

## Developer History Boundary

Historical engineering evidence, sample fixtures, milestone records, and developer-only beta evidence are retained under:

```text
dev/
```

Public testers do not need to import or edit `dev/` for normal runtime use.

Observation, support evidence, and Ragnarok-style diagnostic tooling remain user-facing support features even though generated logs and bundles should remain local and uncommitted.

## Version

```bash
cat VERSION
```

Expected Open Beta version:

```text
0.5.0
```

`v0.1.0-beta.1` is superseded and should not be used for fresh tester onboarding.

## Environment Example

```bash
cp tools/importer/.env.example tools/importer/.env
vi tools/importer/.env
```

Recommended dogfood defaults for this host:

```text
HERMES_MEMORY_ROOT=~/workspace/hermes-runes-md-wiki
HERMES_WORKSPACE_SLUG=freelancer
HERMES_PROJECT=freelancer
```

For a different tester host, replace `freelancer` with that host's lowercase hostname.

## Fresh Clone Bootstrap

Default fresh clone bootstrap is lightweight:

```bash
bash ./bin/hermes-memory-bootstrap
```

The default bootstrap installs the core profile only and does not install torch, CUDA, sentence-transformers, transformers, or Triton.

Optional hybrid/vector embedding support is explicit:

```bash
bash ./bin/hermes-memory-bootstrap --with-embedding
```

## Read First

```text
README.md
QUICKSTART.md
AGENTS.md
wiki/README.md
wiki/hermes_runes_index.md
wiki/_system/README.md
docs/workspace-slug-policy.md
docs/v0.5.0-tester-checklist.md
```

## Safety Boundary

```text
Do not put real local credentials into Markdown wiki memory.
Do not rely on Open Beta as a stable production release.
Use governed proposal/review paths for durable memory changes.
Do not import dev/ as runtime memory by default.
```

## Final Lock

```text
Open Beta Starter Guide
STARTER / v0.5.0 public evaluation path uses clean runtime wiki seed, restored hybrid recall, and cleaned runtime surface
```
