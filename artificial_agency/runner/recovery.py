from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from inspect_ai.dataset import Sample

from .config import RunSpec
from .inspect_ops import InspectLogMetadata, inspect_log_metadata, json_logs
from .state import atomic_write_json, utc_now


@dataclass(frozen=True)
class RecoveryPlan:
    run_id: str
    expected_total: int
    source_log: str | None
    source_completed_count: int
    missing_count: int
    duplicate_ids: tuple[str, ...]
    unexpected_ids: tuple[str, ...]
    missing_ids: tuple[str, ...]
    segments: tuple[InspectLogMetadata, ...]

    @property
    def recoverable(self) -> bool:
        return (
            self.source_completed_count < self.expected_total
            and self.missing_count > 0
            and not self.duplicate_ids
            and not self.unexpected_ids
        )


def expected_sample_ids(spec: RunSpec) -> tuple[str, ...]:
    if spec.run_id in {"005B", "005C"}:
        from .exp005_cross_model_task import MODEL_B, MODEL_C, cross_model_samples

        run = MODEL_B if spec.run_id == "005B" else MODEL_C
        samples: list[Sample] = cross_model_samples(run)
        return tuple(str(sample.id) for sample in samples)
    raise ValueError(f"runner-level sample-id recovery is not defined for {spec.run_id}")


def build_recovery_plan(spec: RunSpec) -> RecoveryPlan:
    expected = expected_sample_ids(spec)
    expected_set = set(expected)
    segments = tuple(inspect_log_metadata(path) for path in json_logs(spec.log_dir))
    source = max(segments, key=lambda segment: segment.sample_count, default=None)
    source_ids = tuple(sample_id for segment in segments for sample_id in segment.sample_ids)
    seen: set[str] = set()
    duplicates: list[str] = []
    for segment in segments:
        segment_seen: set[str] = set()
        for sample_id in segment.sample_ids:
            if sample_id in segment_seen and sample_id not in duplicates:
                duplicates.append(sample_id)
            segment_seen.add(sample_id)
            seen.add(sample_id)
    unexpected = sorted(sample_id for sample_id in seen if sample_id not in expected_set)
    completed_expected = expected_set.intersection(seen)
    missing = tuple(sample_id for sample_id in expected if sample_id not in completed_expected)
    return RecoveryPlan(
        run_id=spec.run_id,
        expected_total=spec.total_samples,
        source_log=str(source.path) if source else None,
        source_completed_count=len(completed_expected),
        missing_count=len(missing),
        duplicate_ids=tuple(sorted(duplicates)),
        unexpected_ids=tuple(unexpected),
        missing_ids=missing,
        segments=segments,
    )


def write_recovery_plan(spec: RunSpec, plan: RecoveryPlan) -> Path:
    path = spec.status_path.parent / "RECOVERY_PLAN.json"
    payload: dict[str, Any] = asdict(plan)
    payload["created_at"] = utc_now()
    payload["scientific_implementation_sha"] = (
        "0c6dcb1b386faf6424b97cc505bd4303d697793e"
        if spec.run_id.startswith("005")
        else spec.frozen_commit
    )
    payload["segments"] = [
        {
            "path": str(segment.path),
            "byte_size": segment.byte_size,
            "sha256": segment.sha256,
            "status": segment.status,
            "sample_count": segment.sample_count,
            "error_summary": segment.error_summary,
        }
        for segment in plan.segments
    ]
    atomic_write_json(path, payload)
    ids_path = spec.status_path.parent / "RECOVERY_MISSING_IDS.json"
    atomic_write_json(
        ids_path,
        {
            "run_id": spec.run_id,
            "source_log": plan.source_log,
            "missing_count": plan.missing_count,
            "missing_ids": list(plan.missing_ids),
        },
    )
    return path


def reconciled_unique_count(spec: RunSpec, segment_paths: list[Path]) -> int:
    expected = set(expected_sample_ids(spec))
    completed: set[str] = set()
    for path in segment_paths:
        completed.update(expected.intersection(inspect_log_metadata(path).sample_ids))
    return len(completed)
