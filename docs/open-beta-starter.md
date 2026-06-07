# Open Beta Starter Guide

Status: STARTER / PUBLIC EVALUATION PATH
Date: 2026-06-07

## Purpose

Provide a clean public Open Beta entry path for fresh testers.

This guide intentionally avoids historical `wiki/k6-freelancer/` engineering evidence and uses the active Open Beta workspace slug.

## Clone Path

Recommended developer or dogfood checkout:

```bash
mkdir -p ~/workspace
cd ~/workspace
git clone https://github.com/sawaichi9527/hermes-runes-md-wiki.git
cd hermes-runes-md-wiki
```

Recommended clean external-user simulation checkout:

```bash
mkdir -p ~/workspace/trial
cd ~/workspace/trial
git clone https://github.com/sawaichi9527/hermes-runes-md-wiki.git
cd hermes-runes-md-wiki
```

## Default Workspace

```text
workspace_slug: freelancer
wiki_namespace: wiki/freelancer/
```

The historical `wiki/k6-freelancer/` namespace is legacy engineering evidence. It is kept for provenance and should not be treated as the default public tester workspace.

## Version

```bash
cat VERSION
```

Expected before the first tag:

```text
0.1.0-beta.1
```

The `v0.1.0-beta.1` tag is created only after public download remediation and release lock are complete.

## Environment Example

```bash
cp tools/importer/.env.example tools/importer/.env
vi tools/importer/.env
```

Recommended defaults:

```text
HERMES_MEMORY_ROOT=~/workspace/hermes-runes-md-wiki
HERMES_WORKSPACE_SLUG=freelancer
HERMES_PROJECT=freelancer
```

For clean trial checkout testing, set:

```text
HERMES_MEMORY_ROOT=~/workspace/trial/hermes-runes-md-wiki
HERMES_WORKSPACE_SLUG=freelancer
HERMES_PROJECT=freelancer
```

## Read First

```text
README.md
AGENTS.md
wiki/_system/README.md
docs/workspace-slug-policy.md
docs/versioning-policy.md
```

## Safety Boundary

```text
Do not put real local credentials into Markdown wiki memory.
Do not rely on Open Beta as a stable release.
Do not treat Open Beta as production support.
Use governed proposal/review paths for memory changes.
```

## Final Lock

```text
Open Beta Starter Guide
STARTER / public evaluation path uses freelancer workspace slug
```
