# OPC / coordinator

**Role:** Sequential router; no deep verification; routes Runes requests

**Access boundary (runes):**
- Reads/retrieval: through runes-holder; no direct wiki mutation.
- Governed writes: only via runes-holder with secretary-mediated user approval; audit jsonl must record it (D22/D16).

**Namespace purpose:** per-role governed canonical knowledge for the OPC 8-profile set (v4.1).
