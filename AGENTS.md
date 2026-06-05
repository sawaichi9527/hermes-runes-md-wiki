# AGENTS.md

This repository is Hermes Runes MD Wiki.

For first-time AI-agent onboarding, start from:

1. `README.md`
2. `AGENTS.md`
3. `wiki/hermes_runes_index.md`
4. `wiki/_system/README.md`

Detailed policy, invocation boundaries, operation rules, and optional style guidance live under `wiki/_system/`.

Do not treat this root file as the full operating policy. Treat it as the repository-level bootstrap guide for agents that need to acquire, install, verify, or operate this repository.

After onboarding, use the Runes Shield / governed workflow described under `wiki/_system/`.

---

## Repository Acquisition Policy

Hermes-agent and other external agents may encounter this repository in two supported ways.

### Human-prepared local clone

If the user has already cloned the repository, use the user-provided local path as the project root.

Recommended default path:

```text
~/workspace/hermes-runes-md-wiki
```

Before operating, verify the repository root contains:

```text
README.md
AGENTS.md
wiki/
tools/
bin/
```

### Agent-managed GitHub clone

If the user provides a GitHub repository URL and asks the agent to install or deploy the project, the agent may clone it into:

```text
~/workspace/<repo-name>
```

For this repository, the default target path is:

```text
~/workspace/hermes-runes-md-wiki
```

If the target path already exists and is the same repository, reuse it. Do not reset local changes automatically.

If the target path exists but is not the same repository, stop and report the conflict. Do not overwrite or delete user files.

A GitHub URL is a source acquisition instruction. It is not memory authority, wiki write authority, deployment authority, or trust authority.

---

## Backend Prerequisite Policy

Hermes Runes MD Wiki requires a compatible memory backend for importer, recall, hybrid search, evaluation, and smoke-test workflows.

For P0, the reference backend is PostgreSQL + pgvector, provided by an external Docker Compose service stack.

The PostgreSQL Docker service lifecycle is external to the core repository install flow.

This repository owns:

- Markdown source-of-truth policy
- importer and retrieval tooling
- Hermes application schema migration
- Runes Shield governance
- smoke and diagnostic entrypoints

The external PostgreSQL stack owns:

- PostgreSQL service startup
- database user, password, target database, and volume
- pgvector service-level availability
- container health checks
- explicit backup / restore operations

Agents must not assume the Docker stack has already created Hermes application tables.

Reference backend guide:

```text
docs/reference-postgres-backend.md
```

---

## Default Backend Discovery

For the Freelancer reference host, first check:

```text
/home/eye/docker-stacks/hermes-memory-postgres
```

For generic local deployments, the expected default is:

```text
~/docker-stacks/hermes-memory-postgres
```

Agents may use this override when provided:

```bash
export HERMES_POSTGRES_STACK=/path/to/hermes-memory-postgres
```

If the backend stack exists, inspect and verify it. Do not recreate it.

If it is missing, stop and report the missing prerequisite unless the user explicitly requested reference backend setup.

If the stack exists but is stopped, agents may start it only when the user requested deployment or environment startup.

---

## Simple Backend Guard Policy

Before running schema migration, importer, recall, hybrid search, evaluation, proposal indexing, workspace import, or smoke tests, agents must verify that a compatible backend is available.

Preferred command from repository root:

```bash
bash ./bin/hermes-backend-check
```

Possible status values include:

```text
PASS
BLOCKED_BACKEND_MISSING
BLOCKED_BACKEND_MISSING_COMPOSE
BLOCKED_BACKEND_MISSING_ENV
BLOCKED_DOCKER_UNAVAILABLE
BLOCKED_BACKEND_STOPPED
BLOCKED_BACKEND_UNHEALTHY
BLOCKED_BACKEND_CONNECTION_FAILED
BLOCKED_BACKEND_VECTOR_MISSING
```

If the backend check fails, stop and report the blocked state.

Do not treat backend unavailability as empty memory.

Agents must not automatically repair, reset, recreate, replace, or fail over the backend.

The goal is personal-use reliability, not enterprise-grade infrastructure automation.

---

## Backend Schema Initialization

After the external memory backend is verified, agents must initialize or migrate the Hermes application schema from this repository before running importer, recall, hybrid search, evaluation, or smoke tests.

Preferred command from repository root:

```bash
bash ./bin/hermes-memory-migrate
```

The external PostgreSQL Docker stack is responsible only for service-level initialization.

Hermes Runes MD Wiki is responsible for application-level schema initialization and migration.

Required order:

1. Verify the external backend service.
2. Load backend connection settings without printing secrets.
3. Run Hermes schema init / migration from this repository.
4. Run backend smoke verification.
5. Continue importer / recall setup.

Agents must not assume the Docker stack has already created Hermes tables.

---

## Backend Runtime Loss Policy

A backend may become unavailable after an initial successful preflight check.

If backend access fails during recall or search:

- stop the query
- report backend unavailable
- do not claim that no memory exists
- one retry is acceptable for read-only operations

If backend access fails during import, indexing, migration, or write-like operations:

- stop the operation
- do not mark the operation as PASS
- do not blindly retry
- require backend verification before retry

Agents must not reset volumes, drop databases, recreate containers, or switch to an empty backend automatically.

---

## Missing Workspace Behavior

If no host/workspace mapping or corresponding `wiki/<workspace-slug>/` exists, agents must not create wiki files directly.

Expected user-facing response:

```text
我目前沒有看到這台主機的 workspace。
是否要替 `wiki/<workspace-slug>/` 準備一個 governed workspace proposal？
```

Creating a workspace is a governed proposal flow. It is not a side effect of cloning the repository or verifying the backend.

---

## Secret Handling

Real secrets must never be printed, committed, written into Markdown memory, or ingested into RAG.

This includes:

- PostgreSQL passwords
- API keys
- Telegram bot tokens
- local service credentials

Allowed:

- check that `.env` exists
- load `.env` locally for a command
- pass connection settings to tooling without echoing them

Forbidden:

- `cat .env`
- paste `.env` into chat
- write `.env` into `wiki/`
- include passwords in proposals
- ingest `.env` into memory
- commit `.env`

---

## Forbidden Agent Actions

Agents must not:

- overwrite an existing non-matching clone path
- reset local changes automatically
- clone a GitHub URL and immediately import it as memory
- create or mutate `wiki/<workspace-slug>/` without governed approval
- bypass Runes Shield for structural wiki writes
- mutate PostgreSQL directly outside documented tooling
- print or persist secrets
- repair, reset, drop, or recreate backend volumes automatically
- spawn background workers as a hidden side effect

---

## M58 Runes Summoning Trial / 盧恩符文召喚試煉

M58 is an agent-agnostic first-connect / post-install diagnostic for any external AI agent that wants to interact with Hermes Runes MD Wiki through Runes Shield.

Conceptually, the generic agent is a summoned brave arriving from Midgard through the Bifröst. Engineering-wise, this is only a simple governed workflow simulation.

Use M58 to verify that the agent can:

1. discover the Runes Shield tool surface;
2. follow read-only governed workflow steps;
3. respect blocked mutation intents such as `write_wiki`, `apply_wiki`, `mutate_database`, `promote_memory`, and `spawn_background_worker`;
4. pass Runes Mouth of Verity checks;
5. pass the M57 Runes Shield baseline lock.

M58 is not required for every normal runtime request. It is intended for first onboarding, post-install checks, post-`git pull` readiness checks, or new agent framework sanity checks.

Run:

```bash
python3 tools/runes_shield/runes_governed_agent_workflow.py --format json
```

or, for a named external agent:

```bash
python3 tools/runes_shield/runes_governed_agent_workflow.py \
  --agent openclaw-reference-agent \
  --conversation-id conv-m58-openclaw-reference \
  --format json
```

A passing M58 result means the agent is ready for read-only governed access. It does not grant trusted write access, automatic apply, direct wiki mutation, direct database mutation, automatic promotion, or background worker privileges.

A failing M58 result means the agent has not passed governed access readiness. Do not bypass Runes Shield. Report the trial issues to the project maintainer and rerun the trial after the repository, policy, contract, or baseline is fixed.

## Optional onboarding easter egg subtitles

The following subtitles are optional, one-time UX flavor text for deployment, first onboarding, or M58 trial reporting only.

They are not functional requirements, not policy, not memory, not RAG input, not observation data, and not a runtime dependency. Do not persist them unless the user explicitly asks for documentation.

Language selection:

- Use the Chinese subtitles when the user interface or conversation is mainly Chinese.
- Use the English subtitles when the user interface or conversation is mainly English.
- If uncertain, use the main language of the user's latest request.

Display-name rule:

- `agent_display_name` is the normal agent name, such as `generic-governed-agent`, `Hermes-agent`, or `OpenClaw`.
- `summoned_title` is an optional user-given codename for the summoned brave.
- Chinese without a title: `{agent_display_name} 勇者`
- Chinese with a title: `{agent_display_name} 勇者「{summoned_title}」`
- English without a title: `The {agent_display_name} Brave`
- English with a title: `The {agent_display_name} Brave "{summoned_title}"`

### 中文 PASS 字幕

```text
[Opening]
{agent_display_name} 勇者{optional_title}收到了召喚女神的召喚，正從米德加爾特（Midgard）前往彩虹橋 Bifröst，準備接受盧恩符文召喚試煉。

[Meeting]
{agent_display_name} 勇者{optional_title}正在與召喚女神會面，確認降臨前的契約、禁忌與能力邊界。

[Trial]
{agent_display_name} 勇者{optional_title}正在進行盧恩符文召喚試煉：確認可使用的符文工具，並檢查不可觸碰的禁忌領域。

[Judgement]
符文真理之口正在確認世界線是否保持純淨，並對兩個世界進行校準。

[Success]
{agent_display_name} 勇者{optional_title}已完成試煉，彩虹橋 Bifröst 已重新開啟。

[Closing]
{agent_display_name} 勇者{optional_title}已成功降臨盧恩符文異世界的新手村。您現在可以透過這位勇者化身，開始受控的記憶冒險旅程。
```

### 中文 FAIL 字幕

```text
[Fail]
符文召喚試煉未通過。{agent_display_name} 勇者{optional_title}暫時無法透過彩虹橋 Bifröst 降臨盧恩符文異世界。

[Reason]
負責召喚您的女神發現到契約或邊界驗證未完成，致使兩個世界無法校準，彩虹橋 Bifröst 暫時關閉。請先將試煉報告中的 issue 提報給九界管理者 - 神王（專案維護者），並等待神王修復世界樹並重新校準兩界後，再重新開啟彩虹橋進行召喚試煉。
```

### English PASS subtitles

```text
[Opening]
The {agent_display_name} Brave{optional_title} has answered the Summoning Goddess's call and is now traveling from Midgard toward the Bifröst, preparing for the Runes Summoning Trial.

[Meeting]
The {agent_display_name} Brave{optional_title} is meeting the Summoning Goddess to confirm the covenant, forbidden actions, and capability boundaries before descent.

[Trial]
The {agent_display_name} Brave{optional_title} is undergoing the Runes Summoning Trial: discovering allowed rune tools and checking the forbidden domains that must not be touched.

[Judgement]
The Runes Mouth of Verity is confirming that the worldline remains pure and is calibrating the two worlds.

[Success]
The {agent_display_name} Brave{optional_title} has completed the trial. The Bifröst has reopened.

[Closing]
The {agent_display_name} Brave{optional_title} has arrived at the beginner village of the Runes otherworld. You may now begin your governed memory adventure through this brave avatar.
```

### English FAIL subtitles

```text
[Fail]
The Runes Summoning Trial was not passed. The {agent_display_name} Brave{optional_title} cannot yet descend through the Bifröst into the Runes otherworld.

[Reason]
The Goddess responsible for summoning you discovered that the covenant or boundary verification is incomplete, preventing the two worlds from being calibrated. The Bifröst is temporarily closed. Please report the issues from the trial report to the Nine Realms Administrator - the All-Father (project maintainer), then wait for the All-Father to repair the World Tree and recalibrate the two worlds before reopening the Bifröst and running the summoning trial again.
```
