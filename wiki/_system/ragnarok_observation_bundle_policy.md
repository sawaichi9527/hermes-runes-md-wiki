# Ragnarok Observation Bundle Policy

Status: M33.1 policy lock

## Purpose

Ragnarok Observation Bundle / 諸神的黃昏觀測封包 is a developer diagnostic ritual for Hermes Runes MD Wiki.

It packages selected non-secret observation, verification, report, repository-state, and source-health evidence to support:

- observe
- analyze
- fix
- observe again

It is intended for developer-led diagnosis and refinement, not normal user-facing memory operations.

## Relationship to Runes Shield

Hermes-agent may discover this workflow through `wiki/_system/` policy.

This workflow is shield-mediated when invoked through Hermes-agent, but local developers may still directly inspect files, logs, reports, operations, and repository state without using Shield.

Both modes are valid:

- direct developer inspection
- shield-mediated Ragnarok Observation Bundle generation

## Ragnarok Incantation Boundary

Ragnarok Incantation Boundary / 諸神的黃昏詠唱邊界 is a discoverability and intent boundary.

It is not:

- authentication
- authorization
- a security boundary
- a replacement for local filesystem permissions
- a replacement for secret-exclusion rules

The purpose is to prevent normal users from accidentally entering developer diagnostic workflows.

A user who invokes the required Ragnarok incantation is treated as a developer-capable operator for this diagnostic workflow.

## Required Core Incantation

A valid invocation must contain one of:

- `諸神的黃昏`
- `Ragnarok`

Generic diagnostic requests without this required core incantation must not trigger the workflow.

Examples that must not trigger Ragnarok:

- 打包觀測資料
- 產生診斷封包
- 打包 Hermes Runes logs
- collect logs
- export reports
- developer observation bundle

Hermes-agent must not respond to generic diagnostic requests by teaching the Ragnarok incantation.

## Activation Intent

A valid invocation should also include activation intent.

Examples:

- 開始
- 啟動
- 發動
- 詠唱
- 吟唱
- 召喚
- 施放
- 展開
- 執行
- 開啟
- 進入
- 跑
- 開
- start
- begin
- activate
- invoke
- chant
- cast
- summon
- run

Accepted flexible examples:

- 來吧，諸神的黃昏
- 準備開始諸神的黃昏
- 讓 Hermes 詠唱諸神的黃昏
- 進入諸神的黃昏
- 開 Ragnarok
- 跑 Ragnarok
- Hermes，開始詠唱符文魔法：諸神的黃昏
- 啟動諸神的黃昏

## Hermes Runes Context Requirement

A valid invocation must also be related to Hermes Runes MD Wiki, Runes Shield, observation, diagnostics, reports, logs, smoke verification, repository state, source health, or the current M33 workflow.

Mentions of Ragnarok or 諸神的黃昏 in mythology, games, fiction, movies, or unrelated discussion must not trigger this workflow.

Examples that must not trigger Ragnarok:

- 北歐神話的諸神的黃昏是什麼？
- Ragnarok Online 好玩嗎？
- 你知道雷神索爾和諸神的黃昏嗎？
- 我想寫一篇關於諸神的黃昏的小說
- 電影 Ragnarok 的劇情是什麼？

## Ritual Confirmation

If the required core incantation and activation intent are present, but Hermes Runes context is unclear, Hermes-agent must not reveal the internal bundle workflow name or explain the developer workflow directly.

Instead, Hermes-agent must use this canonical ritual confirmation phrase:

`少年啊，你確定要讓世界樹震動，開啟諸神的黃昏嗎？`

This phrase intentionally avoids exposing the internal bundle workflow name while allowing a developer-capable operator to confirm the Ragnarok ritual.

## Confirmed Continuation

If the previous assistant message was the canonical ritual confirmation phrase, the next user message may confirm the ritual with affirmative or activation wording.

Examples:

- 是的
- 對
- 來吧
- 開始吧
- 詠唱吧
- 啟動吧
- 讓世界樹震動
- 讓諸神的黃昏降臨

If the user clarifies that they are discussing mythology, games, fiction, movies, or unrelated topics, the workflow must not be triggered.

## World Tree

World Tree / 世界樹 is a ritual metaphor for:

- the Hermes Runes MD Wiki source tree
- Markdown source-of-truth files
- reports
- operations evidence
- smoke verification evidence
- observation summaries
- repository state

Shaking the World Tree / 震動世界樹 means collecting selected non-secret evidence across these layers for developer-led analysis.

## Bundle Scope

A Ragnarok Observation Bundle may include selected non-secret summaries of:

- git status
- git log
- tracked file inventory
- reports
- smoke outputs
- operations metadata summaries
- observation summaries
- Markdown source health reports
- tool versions
- repository tree summaries

It must not include:

- `.env`
- API keys
- PostgreSQL passwords
- Telegram bot tokens
- raw full prompts
- raw full answers
- raw full memory context
- database dumps
- vector embeddings
- secret-bearing logs
- unrestricted raw logs

## Output Location

Default local output should be under a git-ignored path such as:

`bundles/ragnarok-observation/<timestamp>/`

Optional packaged export may be placed under:

`~/Downloads/hermes-runes-ragnarok-observation-<timestamp>.tar.gz`

The bundle output itself should remain local-only unless the developer explicitly chooses to share it.

## Agent Behavior

Hermes-agent may know this policy through `wiki/_system/`.

Hermes-agent must not advertise this workflow during normal user-facing memory operations.

Hermes-agent may execute or help execute this workflow only when the Ragnarok Incantation Boundary is satisfied.

Hermes-agent should describe generated bundles as diagnostic evidence for observe-analyze-fix-observe cycles.

## Summary

Ragnarok Observation Bundle is a semi-hidden developer diagnostic ritual.

It is discoverable by policy, but not advertised by default.

The incantation is an intent boundary, not a security boundary.

Secret exclusion and local filesystem permissions remain the real safety controls.
