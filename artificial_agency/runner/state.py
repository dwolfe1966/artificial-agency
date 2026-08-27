from __future__ import annotations

import json
import os
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


TERMINAL_STATES = {"COMPLETED", "FAILED", "STOPPED", "INTERRUPTED", "INCOMPLETE"}


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def read_json(path: Path, default: dict[str, Any] | None = None) -> dict[str, Any]:
    if not path.exists():
        return default or {}
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        delete=False,
    ) as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
        tmp_name = handle.name
    os.replace(tmp_name, path)


def append_log(path: Path, message: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"{utc_now()} {message}\n")


def update_status(path: Path, **updates: Any) -> dict[str, Any]:
    current = read_json(path, {})
    current.update(updates)
    current["updated_at"] = utc_now()
    atomic_write_json(path, current)
    return current


def initial_status(run_id: str, frozen_commit: str, total: int) -> dict[str, Any]:
    now = utc_now()
    return {
        "run_id": run_id,
        "runner_version": "v2",
        "state": "INITIALIZED",
        "frozen_commit": frozen_commit,
        "completed": 0,
        "total": total,
        "technical_failures": 0,
        "elapsed_seconds": 0,
        "api_health": "UNKNOWN",
        "created_at": now,
        "updated_at": now,
    }


def process_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True
