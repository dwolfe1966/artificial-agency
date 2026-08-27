from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class InspectLogMetadata:
    path: Path
    byte_size: int
    sha256: str
    status: str | None
    sample_ids: tuple[str, ...]
    error_summary: str | None = None

    @property
    def sample_count(self) -> int:
        return len(self.sample_ids)


SUCCESS_STATUSES = {"success", "completed"}


def json_logs(log_dir: Path) -> list[Path]:
    return sorted(log_dir.glob("*.json"), key=lambda path: path.stat().st_mtime)


def latest_json_log(log_dir: Path) -> Path | None:
    logs = json_logs(log_dir)
    return logs[-1] if logs else None


def _safe_error_summary(data: dict[str, Any]) -> str | None:
    error = data.get("error")
    text = json.dumps(error, sort_keys=True) if isinstance(error, dict) else str(error or "")
    if not text:
        return None
    lowered = text.lower()
    if "credit balance is too low" in lowered:
        return "provider_api_error: credit balance is too low"
    if "authentication" in lowered or "unauthorized" in lowered:
        return "provider_api_error: authentication or authorization failure"
    return "inspect_log_status_error"


def inspect_log_metadata(path: Path) -> InspectLogMetadata:
    raw = path.read_bytes()
    byte_size = len(raw)
    checksum = hashlib.sha256(raw).hexdigest()
    status: str | None = None
    sample_ids: list[str] = []
    error_summary: str | None = None
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return InspectLogMetadata(
            path=path,
            byte_size=byte_size,
            sha256=checksum,
            status=None,
            sample_ids=(),
            error_summary="unreadable inspect json",
        )
    if isinstance(data, dict):
        raw_status = data.get("status")
        status = str(raw_status) if raw_status is not None else None
        samples = data.get("samples")
        if isinstance(samples, list):
            for sample in samples:
                if isinstance(sample, dict) and sample.get("id") is not None:
                    sample_ids.append(str(sample["id"]))
        if status not in SUCCESS_STATUSES:
            error_summary = _safe_error_summary(data)
    return InspectLogMetadata(
        path=path,
        byte_size=byte_size,
        sha256=checksum,
        status=status,
        sample_ids=tuple(sample_ids),
        error_summary=error_summary,
    )


def inspect_log_status(log_dir: Path) -> str | None:
    log = latest_json_log(log_dir)
    return inspect_log_metadata(log).status if log else None


def inspect_log_success(log_dir: Path) -> bool:
    status = inspect_log_status(log_dir)
    return status in SUCCESS_STATUSES


def sample_ids_from_log(path: Path) -> tuple[str, ...]:
    return inspect_log_metadata(path).sample_ids


def raw_log_bytes(log_dir: Path) -> int:
    log = latest_json_log(log_dir)
    return log.stat().st_size if log else 0


def safe_log_summary(log_dir: Path) -> dict[str, Any]:
    log = latest_json_log(log_dir)
    if log is None:
        return {"raw_log_path": None, "raw_log_bytes": 0}
    return {
        "raw_log_path": str(log),
        "raw_log_bytes": log.stat().st_size,
    }


def count_completed_samples(log_dir: Path) -> int:
    log = latest_json_log(log_dir)
    if log is None:
        return 0
    return inspect_log_metadata(log).sample_count


def token_usage(log_dir: Path) -> int | None:
    log = latest_json_log(log_dir)
    if log is None:
        return None
    try:
        data = json.loads(log.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    stats = data.get("stats")
    if not isinstance(stats, dict):
        return None
    model_usage = stats.get("model_usage")
    if not isinstance(model_usage, dict):
        return None
    total = 0
    found = False
    for usage in model_usage.values():
        if not isinstance(usage, dict):
            continue
        for key in ("input_tokens", "output_tokens", "reasoning_tokens"):
            value = usage.get(key)
            if isinstance(value, int):
                total += value
                found = True
    return total if found else None


def samplebuffer_counts(runtime_home: Path) -> dict[str, int]:
    counts = {"buffered_samples": 0}
    base = runtime_home / "Library" / "Application Support" / "inspect_ai"
    for db_path in base.glob("samplebuffer/**/*.db"):
        try:
            with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True) as db:
                row = db.execute("select count(*) from samples").fetchone()
            counts["buffered_samples"] += int(row[0])
        except sqlite3.Error:
            continue
    return counts
