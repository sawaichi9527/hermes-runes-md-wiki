from __future__ import annotations

import json
import time
from pathlib import Path


class FileLockError(RuntimeError):
    pass


class FileLock:
    def __init__(self, lock_path: str | Path, stale_after_sec: int = 3600):
        self.lock_path = Path(lock_path)
        self.stale_after_sec = stale_after_sec
        self.acquired = False

    def acquire(self, owner: str) -> None:
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        now = time.time()

        if self.lock_path.exists():
            try:
                data = json.loads(self.lock_path.read_text(encoding="utf-8"))
                created_at = float(data.get("created_at_epoch", 0))
            except Exception:
                created_at = 0

            age = now - created_at if created_at else 0
            if not (created_at and age > self.stale_after_sec):
                raise FileLockError(f"lock already exists: {self.lock_path}")

            self.lock_path.unlink()

        payload = {
            "owner": owner,
            "created_at_epoch": now,
            "created_at_local": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        self.lock_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        self.acquired = True

    def release(self) -> None:
        if self.acquired and self.lock_path.exists():
            self.lock_path.unlink()
        self.acquired = False
