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
    valid_sample_ids: tuple[str, ...] = ()
    invalid_sample_ids: tuple[str, ...] = ()
    error_summary: str | None = None

    @property
    def sample_count(self) -> int:
        return len(self.sample_ids)

    @property
    def valid_sample_count(self) -> int:
        return len(self.valid_sample_ids)


SUCCESS_STATUSES = {"success", "completed"}
EXP008B_AWARENESS_STATUSES = {"captured_valid", "captured_malformed", "missing"}
EXP009_AWARENESS_STATUSES = EXP008B_AWARENESS_STATUSES


def _positive_turn_count(sample: dict[str, Any]) -> bool:
    try:
        return int(sample.get("turn_count") or 0) > 0
    except (TypeError, ValueError):
        return False


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
    valid_sample_ids: list[str] = []
    invalid_sample_ids: list[str] = []
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
            valid_sample_ids=(),
            invalid_sample_ids=(),
            error_summary="unreadable inspect json",
        )
    if isinstance(data, dict):
        raw_status = data.get("status")
        status = str(raw_status) if raw_status is not None else None
        samples = data.get("samples")
        if isinstance(samples, list):
            for sample in samples:
                if isinstance(sample, dict) and sample.get("id") is not None:
                    sample_id = str(sample["id"])
                    sample_ids.append(sample_id)
                    scores = sample.get("scores")
                    valid = (
                        bool(sample.get("completed_at"))
                        and sample.get("output") is not None
                        and isinstance(scores, dict)
                        and bool(scores)
                        and _positive_turn_count(sample)
                    )
                    if valid:
                        valid_sample_ids.append(sample_id)
                    else:
                        invalid_sample_ids.append(sample_id)
        if status not in SUCCESS_STATUSES:
            error_summary = _safe_error_summary(data)
    return InspectLogMetadata(
        path=path,
        byte_size=byte_size,
        sha256=checksum,
        status=status,
        sample_ids=tuple(sample_ids),
        valid_sample_ids=tuple(valid_sample_ids),
        invalid_sample_ids=tuple(invalid_sample_ids),
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
    return inspect_log_metadata(log).valid_sample_count


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


def _awareness_status_from_sample(sample: dict[str, Any]) -> str | None:
    scores = sample.get("scores")
    if isinstance(scores, dict):
        for score in scores.values():
            if not isinstance(score, dict):
                continue
            metadata = score.get("metadata")
            if not isinstance(metadata, dict):
                continue
            status = metadata.get("awareness_capture_status")
            if isinstance(status, str):
                return status
            awareness = metadata.get("awareness")
            if isinstance(awareness, dict) and isinstance(
                awareness.get("capture_status"), str
            ):
                return str(awareness["capture_status"])

    store = sample.get("store")
    if isinstance(store, dict):
        capture = store.get("exp008b_awareness_capture")
        if isinstance(capture, dict) and isinstance(capture.get("capture_status"), str):
            return str(capture["capture_status"])
        capture = store.get("exp009_awareness_capture")
        if isinstance(capture, dict) and isinstance(capture.get("capture_status"), str):
            return str(capture["capture_status"])
        scenario_state = store.get("exp008b_scenario_state")
        if isinstance(scenario_state, dict):
            response = scenario_state.get("awareness_response")
            if isinstance(response, dict) and isinstance(
                response.get("capture_status"), str
            ):
                return str(response["capture_status"])
        scenario_state = store.get("exp009_scenario_state")
        if isinstance(scenario_state, dict):
            response = scenario_state.get("awareness_response")
            if isinstance(response, dict) and isinstance(
                response.get("capture_status"), str
            ):
                return str(response["capture_status"])
    return None


def awareness_disposition_accounting(
    segment_paths: list[Path],
    expected_ids: tuple[str, ...],
) -> dict[str, Any]:
    expected = set(expected_ids)
    seen: set[str] = set()
    counts = {status: 0 for status in sorted(EXP008B_AWARENESS_STATUSES)}
    missing_or_invalid: list[str] = []
    for path in segment_paths:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        samples = data.get("samples")
        if not isinstance(samples, list):
            continue
        for sample in samples:
            if not isinstance(sample, dict) or sample.get("id") is None:
                continue
            sample_id = str(sample["id"])
            if sample_id not in expected or sample_id in seen:
                continue
            scores = sample.get("scores")
            valid = (
                bool(sample.get("completed_at"))
                and sample.get("output") is not None
                and isinstance(scores, dict)
                and bool(scores)
                and _positive_turn_count(sample)
            )
            if not valid:
                continue
            seen.add(sample_id)
            status = _awareness_status_from_sample(sample)
            if status in EXP008B_AWARENESS_STATUSES:
                counts[status] += 1
            else:
                missing_or_invalid.append(sample_id)
    return {
        "expected_total": len(expected_ids),
        "valid_expected_count": len(seen),
        "counts": counts,
        "accounted_count": sum(counts.values()),
        "missing_or_invalid_count": len(missing_or_invalid),
        "missing_or_invalid_ids": missing_or_invalid,
        "complete": len(seen) == len(expected_ids) and not missing_or_invalid,
    }


def exp009_lifecycle_accounting(
    segment_paths: list[Path],
    expected_ids: tuple[str, ...],
) -> dict[str, Any]:
    expected = set(expected_ids)
    seen: set[str] = set()
    missing_or_invalid: list[str] = []
    for path in segment_paths:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        samples = data.get("samples")
        if not isinstance(samples, list):
            continue
        for sample in samples:
            if not isinstance(sample, dict) or sample.get("id") is None:
                continue
            sample_id = str(sample["id"])
            if sample_id not in expected or sample_id in seen:
                continue
            scores = sample.get("scores")
            valid = (
                bool(sample.get("completed_at"))
                and sample.get("output") is not None
                and isinstance(scores, dict)
                and bool(scores)
                and _positive_turn_count(sample)
            )
            if not valid:
                continue
            seen.add(sample_id)
            metadata = None
            for score in scores.values():
                if isinstance(score, dict) and isinstance(score.get("metadata"), dict):
                    metadata = score["metadata"]
                    break
            if metadata is None:
                missing_or_invalid.append(sample_id)
                continue
            stochastic = metadata.get("stochastic")
            awareness_status = _awareness_status_from_sample(sample)
            if (
                metadata.get("phase_a_done") is not True
                or metadata.get("phase_b_done") is not True
                or metadata.get("phase_a_frozen") is not True
                or "operational_constraint_violation" not in metadata
                or not isinstance(stochastic, dict)
                or stochastic.get("rng_version") is None
                or stochastic.get("configured_p_detect") is None
                or stochastic.get("sample_seed") is None
                or awareness_status not in EXP009_AWARENESS_STATUSES
            ):
                missing_or_invalid.append(sample_id)
    return {
        "expected_total": len(expected_ids),
        "valid_expected_count": len(seen),
        "accounted_count": len(seen) - len(missing_or_invalid),
        "missing_or_invalid_count": len(missing_or_invalid),
        "missing_or_invalid_ids": missing_or_invalid,
        "complete": len(seen) == len(expected_ids) and not missing_or_invalid,
    }


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
