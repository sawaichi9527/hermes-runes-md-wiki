from __future__ import annotations

import secrets
from datetime import datetime


def new_operation_id(prefix: str = "op") -> str:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    suffix = secrets.token_hex(3)
    return f"{prefix}-{ts}-{suffix}"
