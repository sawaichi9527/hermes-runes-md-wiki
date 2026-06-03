#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
AUDIT_TOOL = ROOT / "tools/runes/markdown_source_health_audit.py"


STATE_LABELS_ZH = {
    "stable": "穩定符文",
    "heated": "熾熱符文",
    "overloaded": "過載符文",
}

RISK_LEVELS = {
    "green": "low",
    "yellow": "medium",
    "red": "high",
}

RISK_TEXT_ZH = {
    "green": "目前符文狀態穩定，適合小型知識鑄入或明確 heading 下的 section patch。",
    "yellow": "繼續廣域附魔可能導致符文品質下降，增加後續召回精準度、查詢效能或人工審查負擔。",
    "red": "不建議繼續直接鑄入新知識，否則可能導致符文詠唱失準、召回品質劣化，或使後續知識固化難以安全審查。",
}

ACTION_TEXT_ZH = {
    "section_patch_ok_small_append_ok": "可進行小型 section patch；小型 append 可接受，但仍須走 proposal / review / controlled apply。",
    "avoid_broad_append_prefer_new_topic_file_or_targeted_section_patch": "避免 broad append；建議建立獨立 topic file，或只對既有 heading 做小範圍 section patch。",
    "do_not_direct_append_prefer_split_proposal_or_new_topic_file": "不建議直接追加；建議產生 split proposal，或建立新的 topic file 後再固化新知識。",
}


def run_audit_for_path(path: str) -> dict[str, Any]:
    if not AUDIT_TOOL.is_file():
        raise SystemExit(f"missing audit tool: {AUDIT_TOOL.relative_to(ROOT)}")

    proc = subprocess.run(
        [sys.executable, str(AUDIT_TOOL), "--path", path, "--json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or f"audit failed for {path}")

    return json.loads(proc.stdout)


def build_signal(item: dict[str, Any]) -> dict[str, Any]:
    path = item["path"]
    growth_zone = item["growth_zone"]
    rune_state = item["rune_state"]
    state_zh = STATE_LABELS_ZH.get(rune_state, rune_state)
    recommended_action = item["recommended_action"]

    agent_guidance_zh = (
        f"{path} 符文附魔已達 {item['refinement_level']} 精練狀態，屬於{state_zh}。"
        f"{RISK_TEXT_ZH[growth_zone]}"
        f"建議：{ACTION_TEXT_ZH[recommended_action]}"
    )

    return {
        "schema": "m33_runes_shield_forge_readiness_v1",
        "check": "Runes Shield Forge Readiness Check",
        "display_name_zh": "Runes 符文鑄造前適性檢查",
        "health_subject": "markdown_source",
        "path": path,
        "growth_zone": growth_zone,
        "refinement_level": item["refinement_level"],
        "rune_state": rune_state,
        "rune_state_label_zh": state_zh,
        "risk_level": RISK_LEVELS[growth_zone],
        "recommended_write_behavior": recommended_action,
        "recommended_write_behavior_zh": ACTION_TEXT_ZH[recommended_action],
        "risk_text_zh": RISK_TEXT_ZH[growth_zone],
        "agent_guidance_zh": agent_guidance_zh,
        "source_health": {
            "size_kb": item["size_kb"],
            "estimated_tokens_pressure": item["estimated_tokens_pressure"],
            "heading_count": item["heading_count"],
            "chunk_estimate": item["chunk_estimate"],
            "largest_heading_span_lines": item["largest_heading_span_lines"],
            "largest_heading_span_est_tokens": item["largest_heading_span_est_tokens"],
            "level_components": item["level_components"],
        },
        "governance_boundary": {
            "decision_support_only": True,
            "permission_grant": False,
            "automatic_approval": False,
            "automatic_promotion": False,
            "human_review_required": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Return agent-facing Runes Shield forge readiness signal.")
    parser.add_argument("--path", required=True, help="Markdown source path under repository root.")
    parser.add_argument("--json", action="store_true", help="Print compact JSON signal.")
    args = parser.parse_args()

    item = run_audit_for_path(args.path)
    signal = build_signal(item)

    if args.json:
        print(json.dumps(signal, ensure_ascii=False, indent=2))
    else:
        print(signal["agent_guidance_zh"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
