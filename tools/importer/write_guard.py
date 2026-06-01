#!/usr/bin/env python3
from __future__ import annotations

import os
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


class WriteGuardError(RuntimeError):
    """Raised when a governed write operation violates P0 safety rules."""


def new_operation_id(prefix: str = "op") -> str:
    ts = time.strftime("%Y%m%d-%H%M%S")
    short = uuid.uuid4().hex[:8]
    return f"{prefix}-{ts}-{short}"


def ensure_inside_root(root: Path, target: Path) -> Path:
    root = root.resolve()
    target = target.resolve()

    try:
        target.relative_to(root)
    except ValueError as exc:
        raise WriteGuardError(f"target escapes root: {target}") from exc

    return target


@contextmanager
def file_lock(lock_path: Path, timeout_sec: int = 30) -> Iterator[Path]:
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    start = time.time()
    fd: int | None = None

    while True:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, f"pid={os.getpid()} time={time.time()}\n".encode("utf-8"))
            break
        except FileExistsError:
            if time.time() - start > timeout_sec:
                raise WriteGuardError(f"lock timeout: {lock_path}")
            time.sleep(0.2)

    try:
        yield lock_path
    finally:
        if fd is not None:
            os.close(fd)
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def assert_p0_write_allowed(root: Path, target: Path, project: str) -> Path:
    root = root.resolve()
    target = ensure_inside_root(root, target)

    allowed_dir = (root / "wiki" / project / "forge-inbox").resolve()

    try:
        target.relative_to(allowed_dir)
    except ValueError as exc:
        raise WriteGuardError(
            f"P0 write denied: only forge-inbox is writable; target={target}"
        ) from exc

    if target.suffix != ".md":
        raise WriteGuardError(f"P0 write denied: only .md files allowed; target={target}")

    return target
