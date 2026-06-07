#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HEALTH_TOOL = ROOT / "tools/runes/markdown_source_health.py"


def readiness_for_path(path: str) -> dict[str, Any]:
    proc = subprocess.run(
        [sys.executable, str(HEALTH_TOOL), "--path", path, "--json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or f"readiness check failed for {path}")
    return json.loads(proc.stdout)


def synthetic_signal(zone: str, path: str) -> dict[str, Any]:
    if zone == "green":
        return {
            "schema": "m33_runes_shield_forge_readiness_v1",
            "check": "Runes Shield Forge Readiness Check",
            "display_name_zh": "Runes 符文鑄造前適性檢查",
            "health_subject": "markdown_source",
            "path": path,
            "growth_zone": "green",
            "refinement_level": "+2",
            "rune_state": "stable",
            "rune_state_label_zh": "穩定符文",
            "risk_level": "low",
            "recommended_write_behavior": "section_patch_ok_small_append_ok",
            "agent_guidance_zh": f"{path} 符文附魔已達 +2 精練狀態，屬於穩定符文。可進行小型 section patch。",
            "source_health": {},
            "governance_boundary": {
                "decision_support_only": True,
                "permission_grant": False,
                "automatic_approval": False,
                "automatic_promotion": False,
                "human_review_required": True,
            },
        }
    if zone == "yellow":
        return {
            "schema": "m33_runes_shield_forge_readiness_v1",
            "check": "Runes Shield Forge Readiness Check",
            "display_name_zh": "Runes 符文鑄造前適性檢查",
            "health_subject": "markdown_source",
            "path": path,
            "growth_zone": "yellow",
            "refinement_level": "+6",
            "rune_state": "heated",
            "rune_state_label_zh": "熾熱符文",
            "risk_level": "medium",
            "recommended_write_behavior": "avoid_broad_append_prefer_new_topic_file_or_targeted_section_patch",
            "agent_guidance_zh": f"{path} 符文附魔已達 +6 精練狀態，屬於熾熱符文。避免 broad append。",
            "source_health": {},
            "governance_boundary": {
                "decision_support_only": True,
                "permission_grant": False,
                "automatic_approval": False,
                "automatic_promotion": False,
                "human_review_required": True,
            },
        }
    if zone == "red":
        return {
            "schema": "m33_runes_shield_forge_readiness_v1",
            "check": "Runes Shield Forge Readiness Check",
            "display_name_zh": "Runes 符文鑄造前適性檢查",
            "health_subject": "markdown_source",
            "path": path,
            "growth_zone": "red",
            "refinement_level": "+8",
            "rune_state": "overloaded",
            "rune_state_label_zh": "過載符文",
            "risk_level": "high",
            "recommended_write_behavior": "do_not_direct_append_prefer_split_proposal_or_new_topic_file",
            "agent_guidance_zh": f"{path} 符文附魔已達 +8 精練狀態，屬於過載符文。不建議繼續直接鑄入新知識。",
            "source_health": {},
            "governance_boundary": {
                "decision_support_only": True,
                "permission_grant": False,
                "automatic_approval": False,
                "automatic_promotion": False,
                "human_review_required": True,
            },
        }
    raise SystemExit(f"unsupported synthetic zone: {zone}")


def proposal_recommendation(signal: dict[str, Any], incoming_summary: str) -> dict[str, Any]:
    zone = signal["growth_zone"]
    path = signal["path"]

    if zone == "green":
        proposal_strategy = "targeted_section_patch"
        placement = "existing_markdown_source"
        should_warn_user = False
        direct_append_allowed = True
        split_required = False
        recommendation_zh = (
            f"{path} 目前屬於穩定符文，可提出明確 heading 下的 section patch。"
            "小型 append 可接受，但仍必須經過 proposal / review / controlled apply。"
        )
    elif zone == "yellow":
        proposal_strategy = "new_topic_file_or_targeted_section_patch"
        placement = "prefer_new_topic_file"
        should_warn_user = True
        direct_append_allowed = False
        split_required = False
        recommendation_zh = (
            f"{path} 已進入熾熱符文區間，不建議 broad append。"
            "建議建立獨立 topic file，或只對既有 heading 做小範圍 section patch。"
        )
    elif zone == "red":
        proposal_strategy = "split_proposal_or_new_topic_file"
        placement = "avoid_existing_markdown_source"
        should_warn_user = True
        direct_append_allowed = False
        split_required = True
        recommendation_zh = (
            f"{path} 已進入過載符文區間，不建議繼續直接鑄入新知識。"
            "建議先產生 split proposal，或建立新的 topic file 後再固化。"
        )
    else:
        raise SystemExit(f"unsupported growth zone: {zone}")

    return {
        "schema": "m33_growth_aware_forge_proposal_trial_v1",
        "incoming_summary": incoming_summary,
        "target_path": path,
        "readiness": {
            "growth_zone": signal["growth_zone"],
            "refinement_level": signal["refinement_level"],
            "rune_state": signal["rune_state"],
            "rune_state_label_zh": signal["rune_state_label_zh"],
            "risk_level": signal["risk_level"],
        },
        "proposal_strategy": proposal_strategy,
        "placement": placement,
        "direct_append_allowed": direct_append_allowed,
        "split_required": split_required,
        "should_warn_user": should_warn_user,
        "recommendation_zh": recommendation_zh,
        "agent_guidance_zh": signal["agent_guidance_zh"] + " " + recommendation_zh,
        "governance_boundary": {
            "decision_support_only": True,
            "permission_grant": False,
            "automatic_approval": False,
            "automatic_promotion": False,
            "human_review_required": True,
            "controlled_apply_required": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Trial growth-aware forge proposal placement recommendation.")
    parser.add_argument("--path", default=None, help="Target Markdown source path.")
    parser.add_argument("--incoming-summary", default="new knowledge to solidify")
    parser.add_argument("--synthetic-zone", choices=["green", "yellow", "red"], default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.synthetic_zone:
        signal = synthetic_signal(args.synthetic_zone, args.path or f"synthetic/{args.synthetic_zone}.md")
    else:
        if not args.path:
            raise SystemExit("--path is required unless --synthetic-zone is used")
        signal = readiness_for_path(args.path)

    result = proposal_recommendation(signal, args.incoming_summary)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["agent_guidance_zh"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
