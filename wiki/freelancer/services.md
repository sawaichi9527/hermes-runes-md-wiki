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
- **掃描範圍**：AI Agent、MCP、CLI 工具、自動化、本地 LLM、開源專案、Hermes Agent、Lark/Feishu 工具鏈、RAG / memory、SQA 自動化、RSS 訂閱清單
- **推送規則**：每次只推一件最值得知道的事；沒有值得推的完全靜默；不重複已討論內容；深夜非緊急不吵
- **交付目標**：回傳至當前 Feishu 對話（origin）
