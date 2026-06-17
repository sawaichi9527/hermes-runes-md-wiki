# Services

Status: seed

## Purpose

Reviewed notes about local services used by this workspace.

## Safety

Do not store real secrets, tokens, passwords, or private service credentials.

---

## Scheduled Tasks

### 定向情報推送 (job_id: 91d908e7d563)

- **類型**：定時情報掃描與推送（cron job）
- **頻率**：每 1 小時
- **狀態**：active
- **建立日期**：2026-06-17
- **掃描範圍**：AI Agent、Hermes Agent、MCP、CLI 工具、本地 LLM、LM Studio / llama.cpp / Vulkan 推理、自動化工具、開源專案、Lark/Feishu 工具鏈、RAG/memory、SQA/測試自動化、3D STL/FDM 列印 AI 工具、RSS 訂閱清單
- **推送規則**：每次只推一件最值得知道的事；沒有值得推的完全靜默（不發「今日無重大變化」）；不重複 seen_items 事件；深夜非緊急不吵
- **狀態追蹤**：~/.hermes/cron/output/定向情報推送-state.json（run_count / pushed_count / elapsed / tools_used / seen_items）
- **交付目標**：回傳至當前 Feishu 對話（origin）
