# M144 Model Endpoint Configuration Check

Status: ACTIVE / CHECK READY
Date: 2026-06-07

## Purpose

M144 classifies model endpoint readiness for trial run closure without storing private configuration values in wiki or git.

This check is bounded. It does not benchmark answer quality and does not require enterprise service-level validation.

## Allowed Classifications

```text
configured / usable
configured / optional
not configured / intentionally deferred
```

The trial run stage may close with model endpoint marked as intentionally deferred if the memory governance path remains verified and the deferral is explicitly documented.

## Privacy Rule

Do not paste or write private configuration values into Markdown memory or git.

Record only safe summaries such as:

```text
configuration file present: yes/no
model endpoint configured: yes/no/unknown
endpoint probe result: PASS/WARN/SKIP
classification: configured usable / configured optional / intentionally deferred
private values printed: no
```

## Manual Check Procedure

Run from the trial checkout:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

printf '== root ==\n'
pwd

printf '\n== config presence ==\n'
if [ -f tools/importer/.env ]; then
  echo 'config_file_present: yes'
else
  echo 'config_file_present: no'
fi

printf '\n== model config safe summary ==\n'
python3 - <<'PY'
from pathlib import Path

p = Path('tools/importer/.env')
if not p.exists():
    print('model_endpoint_configured: unknown')
    print('private_values_printed: no')
    raise SystemExit(0)

model_related = []
for line in p.read_text(encoding='utf-8', errors='replace').splitlines():
    line = line.strip()
    if not line or line.startswith('#') or '=' not in line:
        continue
    key = line.split('=', 1)[0].strip()
    upper = key.upper()
    if any(token in upper for token in ('MODEL', 'LLM', 'BASE_URL', 'ENDPOINT', 'OPENAI', 'LMSTUDIO')):
        model_related.append(key)

print('model_related_key_count:', len(model_related))
for key in sorted(model_related):
    print(f'{key}=<redacted>')
print('private_values_printed: no')
PY
```

Optional endpoint reachability may be checked manually by the operator without pasting private values into the repo.

## Classification Rules

```text
configured / usable:
  model-related configuration exists and the operator confirms the endpoint is usable.

configured / optional:
  model-related configuration exists, but model-dependent checks are optional for trial closure.

not configured / intentionally deferred:
  model-related configuration is absent or intentionally not used, and trial closure explicitly excludes model-dependent answer-quality validation.
```

## Expected Verification Record

M144 verification should record:

```text
config_file_present: yes/no
model_related_key_count: number
endpoint_reachability: PASS/WARN/SKIP/operator-confirmed
classification: configured usable / configured optional / intentionally deferred
private_values_printed: no
```

## Final Lock Target

```text
M144 Model Endpoint Configuration Check
PASS / classified / private values not written
```
