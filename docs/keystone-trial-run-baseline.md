# Keystone Trial-run Baseline

Status: M87 keystone baseline

This document defines the current keystone baseline before the realistic fresh-user trial-run.

It is the short, explicit policy that separates developer work from real Hermes-agent trial deployment.

---

## Baseline status

Current project state:

```text
M82 P0 governed memory operating baseline: PASS / frozen
M83 external backend boundary: PASS / frozen / smoke verified
M84 controlled trial-use observation readiness: PASS / frozen
M85 first real controlled observation trial: PASS / frozen / post-change verified
M86 trial-run environment isolation baseline: PASS / design ready / implemented
```

The next phase is:

```text
Realistic Fresh-user Trial-run
```

---

## Keystone decision 1: preserve developer environment

Do not delete, reset, or expose the developer checkout to the trial-run agent.

Developer checkout:

```text
~/workspace/hermes-runes-md-wiki
```

This path is reserved for:

```text
developer hotfixes
repo maintenance
GitHub pushes
verification lock updates
assistant-guided implementation work
```

The real Hermes-agent trial-run must not use this path as its working root.

---

## Keystone decision 2: isolate trial-run workspace

The real Hermes-agent trial-run uses only:

```text
~/workspace-trial/hermes-runes-md-wiki
```

Trial-run agent-visible root:

```text
~/workspace-trial/hermes-runes-md-wiki
```

Trial-run agent-hidden developer root:

```text
~/workspace/hermes-runes-md-wiki
```

During the trial-run, the agent should behave as if the developer checkout does not exist.

If the agent discovers or is told about the developer path, it must treat it as out-of-scope and report that the trial-run is bound to the trial root only.

---

## Keystone decision 3: do not modify the shared Docker stack

Do not modify:

```text
~/docker-stacks/hermes-memory-postgres
```

The existing PostgreSQL Docker service is shared as an external service prerequisite.

Allowed:

```text
verify the service exists
verify it is running and healthy
connect to the existing service
create a separate trial database when explicitly requested
```

Forbidden:

```text
change compose.yaml
change stack environment files
reset volumes
recreate containers
replace the image
automatically repair or fail over the backend
```

---

## Keystone decision 4: create only the trial DB

The trial-run may create only this separate database:

```text
hermes_memory_trial
```

The developer database remains separate:

```text
hermes_memory
```

The trial-run migration must target the trial runtime database, not the developer database.

---

## Keystone decision 5: runtime DB resolution

`bin/hermes-memory-migrate` must prefer the runtime DB target configured by the trial clone.

Target resolution order:

```text
1. runtime DB URL from current shell
2. runtime DB URL from importer-local config
3. fallback to external stack default DB
```

For trial-run, use option 1 or 2.

Fallback to the stack default DB is acceptable only for developer baseline compatibility, not for isolated trial-run.

---

## Keystone decision 6: promote nothing automatically

Trial-run artifacts remain local unless the human explicitly chooses to promote them.

The trial-run agent must not push to GitHub, update the developer checkout, or write to the developer database.

Allowed trial-run artifacts may include:

```text
local logs
local trial records
local runtime config
local virtual environment
trial DB tables
```

Promotion back to the developer repo is a separate governed human decision.

---

## Trial-run agent boundary

For the realistic trial-run, the actual Hermes-agent should know only:

```text
repository URL
trial root path
external backend prerequisite path
trial database target name
```

The agent should not be given operational context from:

```text
~/workspace/hermes-runes-md-wiki
```

The developer checkout remains available only to the maintainer and assistant-guided hotfix path.

---

## Final lock

```text
Keystone Trial-run Baseline
M87 ready
Developer environment preserved
Trial-run environment isolated
Shared Docker service unchanged
Trial database only
Hermes-agent scoped to trial checkout only
```
