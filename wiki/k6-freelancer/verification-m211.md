# M211 Runtime Tool Legacy Sweep

Status: PARTIAL / CLASSIFIED / LOCAL PATCH REQUIRED
Date: 2026-06-07

## Evidence Record

```text
wiki/k6-freelancer/cb-sessions/cb-20260607-m211-runtime-tool-legacy-sweep.md
docs/runtime-tool-legacy-sweep.md
docs/open-beta-publication-checklist.md
M210 verification and local grep audit input
```

## Scope

```text
active runtime/tool legacy reference classification
release tag gate
public tester notification gate
no broad historical evidence rewrite
```

## Result

```text
PARTIAL
```

## Release Decision

```text
release_tag_ready: no
public_tester_notification_ready: no
planned_tag: v0.1.0-beta.1
tag_status: blocked
```

## Reason

```text
Remaining active runtime/tool defaults require local patch verification.
Direct GitHub connector replacement attempts for some active helper files were blocked by the connector safety layer.
```

## Already Clean / Prepared

```text
config/hermes-memory.yaml
bin/hermes-memory-check
bin/hermes_memory_common.py
README.md
docs/open-beta-starter.md
tools/importer/.env.example
templates/*.md starter records
```

## Next Step

```text
M212 Runtime Tool Local Patch / Verification
```

## Final Lock

```text
M211 Runtime Tool Legacy Sweep
PARTIAL / classified / v0.1.0-beta.1 tag blocked until local patch verification
```
