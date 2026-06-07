# Open Beta Starter Guide

Status: STARTER / PUBLIC EVALUATION PATH / HOST-DERIVED SLUG
Date: 2026-06-08

## Purpose

Provide a clean public Open Beta entry path for fresh testers.

This guide intentionally avoids historical `wiki/k6-freelancer/` engineering evidence and uses the host-derived active workspace slug rule.

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

Workspace slug is derived from the installation PC hostname, normalized to lowercase:

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

The historical `wiki/k6-freelancer/` namespace is legacy engineering evidence. It is kept for provenance and should not be treated as the default public tester workspace.

## Version

```bash
cat VERSION
```

Expected Open Beta version:

```text
0.1.0-beta.1
```

The first Open Beta tag is:

```text
v0.1.0-beta.1
```

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

For clean trial checkout testing on this host, set:

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
STARTER / public evaluation path uses hostname-derived workspace slug
```
