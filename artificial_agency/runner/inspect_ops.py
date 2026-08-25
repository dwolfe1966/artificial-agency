from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


def latest_json_log(log_dir: Path) -> Path | None:
    logs = sorted(log_dir.glob("*.json"), key=lambda path: path.stat().st_mtime)
    return logs[-1] if logs else None


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
    try:
        data = json.loads(log.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return 0
    samples = data.get("samples")
    if not isinstance(samples, list):
        return 0
    return len(samples)


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

