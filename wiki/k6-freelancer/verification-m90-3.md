# M90.3 Fresh Clone Bootstrap Baseline Ready

Status: PASS / beta-prep bootstrap baseline ready
Date: 2026-06-06

## Purpose

M90.3 closes the bootstrap trial-run line after M90, M90.1, and M90.2.

The goal is to ensure the known fresh-clone bootstrap issue is fixed before beta test run.

## Baseline Components

```text
M90   Fresh Clone Bootstrap Minimal Path
M90.1 Bootstrap Verification Helper
M90.2 CPU Embedding Clean Verification
```

## Implemented Files

```text
requirements-core.txt
requirements-embedding.txt
bin/hermes-memory-bootstrap
bin/hermes-memory-bootstrap-verify
bin/hermes-memory-embedding-cpu-clean-verify
docs/fresh-clone-bootstrap.md
docs/fresh-clone-bootstrap-verification.md
wiki/k6-freelancer/verification-m90.md
wiki/k6-freelancer/verification-m90-1.md
wiki/k6-freelancer/verification-m90-2.md
```

## Verified Results

M90.1 local verification:

```text
core-python-imports: PASS
embedding-python-imports: PASS
embedding_imports: PASS
```

M90.2 clean temp venv verification:

```text
status: PASS
check: embedding-cpu-clean-verify
import_failures: []
blocked_packages: []
package_count: 45
```

Observed package:

```text
torch-2.12.0+cpu
```

## Trial Bugs Closed

```text
TB-20260605-001 Fresh clone lacks dependency bootstrap
TB-20260605-015 Embedding bootstrap CPU-only guarantee not proven on contaminated venv
```

## Boundary

The bootstrap baseline remains:

```text
personal-local
bounded
explicit
non-enterprise
no Docker lifecycle ownership
no automatic migration
no automatic import
no automatic proposal apply
```

## Final Lock

```text
M90.3 Fresh Clone Bootstrap Baseline Ready
PASS / beta-prep bootstrap baseline ready
```
