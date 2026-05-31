PROFILE_CLEANUP_PATTERNS = {
    "qwen-forced-thinking": [
        r"\n?4\.\s+\*\*Check Against Rules:\*\*.*",
        r"\n?5\.\s+\*\*Refine Output:\*\*.*",
        r"\n?5\.\s+\*\*Final Review against Rules:\*\*.*",
        r"\n?4\.\s+\*\*Check Constraints:\*\*.*",
        r"\n?Draft:.*",
        r"\n?Checks:.*",
        r"\n?Ready\.?✅?.*",
        r"\n?Output matches.*",
        r"\n?Proceeds\..*",
    ],

    "default": [
        r"\n?Checks:.*",
    ],
}
