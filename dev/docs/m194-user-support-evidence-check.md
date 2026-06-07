# M194 User Support Evidence Bundle Check

Status: PASS / wrapper fix verified
Date: 2026-06-08
Scope: v0.3.0 support evidence / observation / Ragnarok check

## Purpose

M194 verifies that user-facing observation, diagnostic, and support evidence tooling still works after M193 root developer layout consolidation.

This milestone exists because observation and log bundle features are normal-user support tools, not developer-only fixtures.

## Boundary

User-facing support evidence tools must remain reachable from the normal runtime/support surface:

```text
bin/
tools/importer/
tools/runes/
tools/runes_shield/
```

They must not be hidden only under:

```text
dev/
```

Generated logs and bundles remain local artifacts and should not be committed by default.

## Initial Finding

Initial M194 check found one real bug:

```text
bin/hermes-observe
```

The wrapper still used the legacy fallback root:

```text
$HOME/workspace/hermes-memory
```

This caused:

```text
python3: can't open file '/home/eye/workspace/hermes-memory/tools/importer/hermes_observe.py'
```

## Fix

Commit:

```text
75b466a Fix hermes-observe root resolver
```

Fix summary:

- resolve repository root from the wrapper's own `bin/` directory
- keep `HERMES_MEMORY_ROOT` override support
- add explicit missing-script error message
- avoid legacy hardcoded `~/workspace/hermes-memory` fallback

## Verification

After pulling commit `75b466a`, the following checks passed:

```text
bash ./bin/hermes-observe --help
python tools/runes/ragnarok_observation_bundle.py --help
python tools/runes/ragnarok_incantation_boundary.py --help
python tools/runes/markdown_source_health_audit.py --help
python tools/importer/observation_summary.py --help
python -m py_compile support evidence modules
```

Observed successful `hermes-observe` output:

```text
usage: hermes_observe.py [-h] [--observe-dir OBSERVE_DIR]
                         {tail,stats,report} ...

Hermes observation JSONL viewer
```

Observed successful Ragnarok bundle output:

```text
usage: ragnarok_observation_bundle.py [-h] [--out-root OUT_ROOT]
                                      [--bundle-id BUNDLE_ID] [--json]

Generate local-only Ragnarok observation bundle MVP.
```

Observed successful observation summary output:

```text
usage: observation_summary.py [-h] [--days DAYS] [--json]

Summarize Hermes Memory observation JSONL logs.
```

Working tree after verification:

```text
main == origin/main
working tree clean
```

## Result

```text
M194: PASS / user support evidence surface preserved / hermes-observe wrapper fixed
```

## Remaining Notes

- Some `__pycache__/` files may appear in local `find` output after compile checks. They are runtime-generated Python artifacts and should remain ignored.
- M194 does not require a real support bundle upload or issue submission.
- M194 only verifies support tooling accessibility and basic CLI/module health after layout cleanup.

## Next Step

Proceed to:

```text
M195 Fresh Clone Deployment Rehearsal
```

M195 should validate a clean clone path against:

- lightweight default dependency install
- root layout sanity
- support evidence wrapper availability
- migration path presence
- no accidental dependency on developer-only root folders
