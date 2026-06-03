# AGENTS.md

This repository is Hermes Runes MD Wiki.

For first-time AI-agent onboarding, start from:

1. `wiki/hermes_runes_index.md`
2. `wiki/_system/README.md`

Detailed policy, invocation boundaries, operation rules, and optional style guidance live under `wiki/_system/`.

Do not treat this root file as the full operating policy.

After onboarding, use the Runes Shield / governed workflow described under `wiki/_system/`.

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
