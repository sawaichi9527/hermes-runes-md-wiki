# Runes Markdown Source Health

Status: M33.0 naming / concept lock

## Purpose

Runes Markdown Source Health describes the health condition of Markdown source-of-truth files.

It does not describe:

- PostgreSQL health
- agent runtime memory health
- context-window health
- the whole RAG system health

In Hermes Runes MD Wiki, Markdown files under `wiki/` are the durable governed source-of-truth.
PostgreSQL is the default local recall/index backend, not the authoritative memory layer.

## Core Concept

A Markdown source file is treated as a rune.

Knowledge solidification is treated as a governed forge operation.

Before the next forge operation, Runes Shield may perform a:

## Runes Shield Forge Readiness Check

Chinese display name:

Runes 符文鑄造前適性檢查

This check evaluates whether a target Markdown rune is suitable for the next governed knowledge forge operation.

The check uses Runes Markdown Source Health to estimate:

- file growth pressure
- estimated token pressure
- heading density
- chunk density
- source granularity risk
- append / patch / split recommendation

This check is decision support only.

It is not:

- a permission grant
- an automatic approval
- an automatic promotion
- a bypass around human review
- a replacement for proposal / review / controlled apply governance

## Refinement Level

Each Markdown rune may be described with a refinement level:

- `+0` to `+3`: Stable Rune / 穩定符文
- `+4` to `+6`: Heated Rune / 熾熱符文
- `+7` to `+9`: Overloaded Rune / 過載符文

The refinement level is an agent-facing risk model.

It should be derived from engineering signals such as:

- file size
- estimated token pressure
- heading count
- chunk count
- largest heading span
- retrieval / recall behavior
- human review burden

The refinement level should not be derived from file size alone.

## Agent-Facing Message Template

Suggested Traditional Chinese template:

`<path> 符文附魔已達 <+level> 精練狀態，屬於 <state>。繼續鑄入 / 附魔新知識可能造成 <risk>。建議：<recommended_action>。`

Example for Yellow / Heated Rune:

`services.md 符文附魔已達 +6 精練狀態，屬於熾熱符文。繼續鑄入新知識可能導致符文品質下降，影響後續召回精準度或查詢效能。建議建立獨立 topic file，或只對既有 heading 做小範圍 section patch。`

Example for Red / Overloaded Rune:

`decisions.md 符文附魔已達 +8 精練狀態，屬於過載符文。不建議繼續直接鑄入新知識，否則可能導致符文詠唱失準、召回品質劣化，或使後續知識固化難以安全審查。建議先產生 split proposal，將過大的 Markdown source 拆分為多個 topic files。`

## Recommended Write Behavior

Stable Rune / +0 to +3:

- section patch is acceptable
- small append may be acceptable
- normal proposal flow still required

Heated Rune / +4 to +6:

- avoid broad append
- prefer new topic file
- allow targeted section patch when scope is clear
- agent should warn the user before proposing placement

Overloaded Rune / +7 to +9:

- do not recommend direct append
- prefer split proposal or new topic file
- agent should warn that recall quality, query performance, or review safety may degrade
- controlled apply still requires human-governed approval

## Backend Portability Note

Runes Markdown Source Health belongs to the Markdown source-of-truth layer.

It must not make PostgreSQL part of the project identity.

Forks may replace PostgreSQL with another recall/index backend as long as they preserve:

- Markdown source-of-truth semantics
- governance policy
- proposal / review / apply boundaries
- provenance discipline
- citation discipline
- human approval semantics
