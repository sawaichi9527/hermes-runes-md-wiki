#!/usr/bin/env python3
"""Deterministic Runes offer policy for M21.3.

This module decides whether Hermes-agent should offer to create a governed
Runes proposal. It never creates proposals and never mutates memory.
"""

from __future__ import annotations

from dataclasses import dataclass

RECOMMENDED_PROMPT_ZH = "這段內容看起來像是後續會重複使用的專案知識。要不要我幫你建立一筆 Hermes Runes governed proposal，先放入待審核區，之後由你確認後再固化成 Markdown wiki？"
SHORT_PROMPT_ZH = "這看起來值得固化成長期專案記憶。要不要我透過 Runes Shield 建立一筆 governed proposal？"
RECOMMENDED_PROMPT_EN = "This looks like durable project knowledge that may be useful later. Would you like me to create a governed Hermes Runes proposal for human review before it becomes trusted Markdown memory?"

DURABLE_SIGNALS = {
    "project_decision": [
        "decision",
        "decided",
        "選定",
        "決定",
        "定案",
        "正式採用",
        "命名",
        "naming",
        "use ",
        "改成",
    ],
    "baseline": [
        "baseline",
        "frozen",
        "freeze",
        "凍結",
        "基線",
        "穩定版",
        "stable baseline",
    ],
    "verification": [
        "pass",
        "fail",
        "verified",
        "smoke",
        "regression",
        "驗證",
        "通過",
        "失敗",
        "測試",
        "已確認",
    ],
    "procedure": [
        "command",
        "procedure",
        "steps",
        "流程",
        "步驟",
        "指令",
        "操作方式",
        "run ",
        "執行",
    ],
    "architecture": [
        "architecture",
        "design",
        "service layout",
        "governance",
        "policy",
        "架構",
        "設計",
        "治理",
        "規則",
        "介面",
    ],
    "future_action": [
        "todo",
        "next action",
        "future task",
        "roadmap",
        "後續",
        "下一步",
        "待辦",
        "未來",
    ],
    "explicit_memory_request": [
        "remember",
        "solidify",
        "write into runes",
        "write into wiki",
        "long-term memory",
        "記住",
        "固化",
        "寫進 runes",
        "寫進 wiki",
        "寫進 roadmap",
        "長期記憶",
    ],
}

BLOCKING_SIGNALS = {
    "secret_or_credential": [
        "api_key",
        "apikey",
        "api key",
        "secret",
        "token",
        "password",
        "passwd",
        "pwd=",
        "pgpassword",
        "telegram_bot_token",
        "bearer ",
        "private key",
        "-----begin",
        "金鑰",
        "密碼",
        "憑證",
        "權杖",
        "token=",
    ],
    "casual": [
        "哈哈",
        "lol",
        "帥氣",
        "nice",
        "thanks",
        "謝謝",
        "了解",
        "ok",
    ],
    "unverified_speculation": [
        "maybe",
        "probably",
        "猜測",
        "可能",
        "也許",
        "未確認",
        "不確定",
        "假設",
    ],
    "raw_log_risk": [
        "-----BEGIN",
        "PRIVATE KEY",
        "Authorization:",
        "DATABASE_URL=",
        "POSTGRES_DSN=",
        "PGPASSWORD=",
        "curl -H 'Authorization",
    ],
}


@dataclass(frozen=True)
class OfferDecision:
    should_offer: bool
    action: str
    confidence: str
    reasons: list[str]
    blockers: list[str]
    matched_signals: dict[str, list[str]]
    recommended_prompt_zh: str | None
    short_prompt_zh: str | None
    recommended_prompt_en: str | None


def _matches(text_lower: str, signal_map: dict[str, list[str]]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for category, terms in signal_map.items():
        found = []
        for term in terms:
            if term.lower() in text_lower:
                found.append(term)
        if found:
            result[category] = found
    return result


def classify_offer_intent(text: str) -> OfferDecision:
    normalized = (text or "").strip()
    text_lower = normalized.lower()

    matched_durable = _matches(text_lower, DURABLE_SIGNALS)
    matched_blocking = _matches(text_lower, BLOCKING_SIGNALS)

    blockers: list[str] = []
    reasons: list[str] = []

    if not normalized:
        return OfferDecision(
            should_offer=False,
            action="do_not_offer",
            confidence="high",
            reasons=["empty input"],
            blockers=["empty input"],
            matched_signals={},
            recommended_prompt_zh=None,
            short_prompt_zh=None,
            recommended_prompt_en=None,
        )

    for category in matched_blocking:
        if category == "secret_or_credential":
            blockers.append("possible secret or credential detected")
        elif category == "raw_log_risk":
            blockers.append("raw log or secret-bearing material risk detected")
        elif category == "casual" and len(normalized) < 80 and not matched_durable:
            blockers.append("casual short acknowledgement detected")
        elif category == "unverified_speculation" and not matched_durable:
            blockers.append("unverified speculation without durable signal")

    if blockers:
        return OfferDecision(
            should_offer=False,
            action="do_not_offer",
            confidence="high",
            reasons=["blocking signal present"],
            blockers=blockers,
            matched_signals={**matched_durable, **matched_blocking},
            recommended_prompt_zh=None,
            short_prompt_zh=None,
            recommended_prompt_en=None,
        )

    durable_score = len(matched_durable)
    if durable_score >= 2:
        confidence = "high"
    elif durable_score == 1:
        confidence = "medium"
    else:
        confidence = "low"

    if durable_score > 0:
        reasons.extend(f"durable signal: {name}" for name in matched_durable)
        return OfferDecision(
            should_offer=True,
            action="ask_user_before_propose",
            confidence=confidence,
            reasons=reasons,
            blockers=[],
            matched_signals=matched_durable,
            recommended_prompt_zh=RECOMMENDED_PROMPT_ZH,
            short_prompt_zh=SHORT_PROMPT_ZH,
            recommended_prompt_en=RECOMMENDED_PROMPT_EN,
        )

    return OfferDecision(
        should_offer=False,
        action="do_not_offer",
        confidence="medium",
        reasons=["no durable memory signal detected"],
        blockers=[],
        matched_signals={},
        recommended_prompt_zh=None,
        short_prompt_zh=None,
        recommended_prompt_en=None,
    )


def decision_to_dict(decision: OfferDecision) -> dict:
    return {
        "should_offer": decision.should_offer,
        "action": decision.action,
        "confidence": decision.confidence,
        "reasons": decision.reasons,
        "blockers": decision.blockers,
        "matched_signals": decision.matched_signals,
        "recommended_prompt_zh": decision.recommended_prompt_zh,
        "short_prompt_zh": decision.short_prompt_zh,
        "recommended_prompt_en": decision.recommended_prompt_en,
        "proposal_created": False,
        "write": False,
        "requires_user_consent_before_propose": True,
    }
