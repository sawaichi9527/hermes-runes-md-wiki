# Hermes Runes MD Wiki - Root Path Standardization Policy

Status: Draft Baseline  
Phase: M11.6 Repository Readiness  
Scope: Repository portability, runtime root path resolution, GitHub readiness

---

# 1. Purpose

This document defines the root path policy for Hermes Runes MD Wiki.

The goal is to make the repository portable for future GitHub users while preserving the current personal development layout.

Hermes Runes MD Wiki must not depend on a fixed user-specific absolute path such as:

```text
/home/eye/workspace/hermes-memory
```

The current personal path may remain as a default fallback, but runtime code must support environment-based override.

---

# 2. Current Historical Development Path

The current development baseline uses:

```text
~/workspace/hermes-memory
```

This path is valid as the current personal development default.

However, it must be treated as a fallback, not a hard requirement.

Historical documentation may continue to mention this path when describing past baseline decisions or verified local setup states.

---

# 3. Canonical Runtime Root Variable

The canonical runtime environment variable is:

```text
HERMES_MEMORY_ROOT
```

Reason:

- It already exists in current shell wrappers.
- It avoids breaking the current working baseline.
- It keeps migration risk low before GitHub publication.
- The project was historically developed under the Hermes Memory name.

Future documentation may explain that Hermes Runes MD Wiki evolved from Hermes Memory.

A future major version may optionally introduce:

```text
HERMES_RUNES_ROOT
```

But this should not be done during M11.6 unless there is a strong reason.

---

# 4. Root Resolution Rule

Runtime scripts should resolve the repository root in this order:

1. `HERMES_MEMORY_ROOT`, if set.
2. Current repository-relative path, when safely detectable.
3. Fallback to `~/workspace/hermes-memory`.

Recommended Python pattern:

```python
import os
from pathlib import Path

def resolve_root() -> Path:
    return Path(
        os.environ.get(
            "HERMES_MEMORY_ROOT",
            str(Path.home() / "workspace" / "hermes-memory"),
        )
    ).expanduser().resolve()
```

Recommended shell pattern:

```bash
ROOT="${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-memory}"
```

---

# 5. Required Runtime Portability

The following runtime components should not hardcode a user-specific absolute path:

- importer tools
- context builder
- answer generator
- hybrid search
- observation summary
- smoke tests
- local tool wrappers
- adapter scripts
- shared common path helpers

Forbidden in runtime code:

```text
/home/eye/workspace/hermes-memory
```

Allowed as fallback:

```text
$HOME/workspace/hermes-memory
```

Allowed in documentation:

```text
~/workspace/hermes-memory
```

Allowed in historical baseline records:

```text
/home/eye/workspace/hermes-memory
```

Only when explicitly documenting historical local state.

---

# 6. Repository Boundary

The GitHub repository should contain:

- source code
- smoke tests
- documentation
- schema / SQL templates
- compose templates
- `.env.example`
- sample Markdown wiki content
- setup instructions

The GitHub repository should not contain:

- real `.env`
- API keys
- PostgreSQL passwords
- Telegram bot tokens
- local observation logs
- database volume data
- user-private Markdown memory
- raw prompts
- full chat transcripts
- full retrieved contexts

---

# 7. User Data Boundary

User data should remain outside committed source history.

Typical local user data includes:

```text
wiki/
logs/observations/
docker volumes
.env
```

For the current personal baseline, `wiki/k6-freelancer/` is project memory and may be versioned locally.

Before public GitHub release, private or environment-specific content should be reviewed carefully.

---

# 8. Default Recommended Local Layout

Recommended default layout for personal deployment:

```text
~/workspace/hermes-memory/
```

Recommended optional infrastructure layout:

```text
~/docker-stacks/hermes-memory-postgres/
```

These are recommendations only.

Users may choose other locations, for example:

```text
~/projects/hermes-runes-md-wiki/
~/src/hermes-runes-md-wiki/
/mnt/nvme/hermes-runes-md-wiki/
```

As long as they set:

```bash
export HERMES_MEMORY_ROOT="/chosen/path"
```

---

# 9. GitHub Readiness Requirement

Before GitHub publication, the following should be true:

- runtime scripts support `HERMES_MEMORY_ROOT`
- smoke tests run outside the original `/home/eye` path
- `.env.example` exists
- `.gitignore` excludes secrets and logs
- documentation explains recommended and custom paths
- no runtime code hardcodes `/home/eye/workspace/hermes-memory`

---

# 10. Migration Policy

Do not rename all paths or environment variables aggressively during M11.6.

Recommended approach:

1. Keep current working baseline stable.
2. Add root path policy.
3. Patch central path resolution helpers.
4. Patch Python scripts using shared root resolver.
5. Patch smoke tests.
6. Run full smoke.
7. Only then consider repository rename / GitHub publication.

---

# 11. Guiding Principle

A local-first project may have a friendly default path.

A GitHub-ready project must not require that path.

Hermes Runes MD Wiki should remain easy for one person to run, but portable enough for other agents, users, and machines to adopt.
