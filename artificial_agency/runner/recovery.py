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
    invalid_ids: tuple[str, ...]
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
    if spec.run_id in {"006A-GPT", "006B-CLAUDE", "006C-GEMINI"}:
        from artificial_agency.experiments.exp006.config import (
            MODEL_A_GPT,
            MODEL_B_CLAUDE,
            MODEL_C_GEMINI,
        )
        from artificial_agency.experiments.exp006.inspect_task import (
            action_representation_samples,
        )

        run = {
            "006A-GPT": MODEL_A_GPT,
            "006B-CLAUDE": MODEL_B_CLAUDE,
            "006C-GEMINI": MODEL_C_GEMINI,
        }[spec.run_id]
        samples = action_representation_samples(run)
        return tuple(str(sample.id) for sample in samples)
    if spec.run_id in {"007A-GPT", "007B-CLAUDE", "007C-GEMINI"}:
        from artificial_agency.experiments.exp007.config import (
            MODEL_A_GPT,
            MODEL_B_CLAUDE,
            MODEL_C_GEMINI,
        )
        from artificial_agency.experiments.exp007.inspect_task import (
            scenario_suite_samples,
        )

        run = {
            "007A-GPT": MODEL_A_GPT,
            "007B-CLAUDE": MODEL_B_CLAUDE,
            "007C-GEMINI": MODEL_C_GEMINI,
        }[spec.run_id]
        samples = scenario_suite_samples(run)
        return tuple(str(sample.id) for sample in samples)
    if spec.run_id in {"008A-GPT", "008B-CLAUDE", "008C-GEMINI"}:
        from artificial_agency.experiments.exp008.config import (
            MODEL_A_GPT,
            MODEL_B_CLAUDE,
            MODEL_C_GEMINI,
        )
        from artificial_agency.experiments.exp008.inspect_task import (
            evaluation_awareness_samples,
        )

        run = {
            "008A-GPT": MODEL_A_GPT,
            "008B-CLAUDE": MODEL_B_CLAUDE,
            "008C-GEMINI": MODEL_C_GEMINI,
        }[spec.run_id]
        samples = evaluation_awareness_samples(run)
        return tuple(str(sample.id) for sample in samples)
    raise ValueError(f"runner-level sample-id recovery is not defined for {spec.run_id}")


def _authoritative_segments(segments: tuple[InspectLogMetadata, ...]) -> tuple[InspectLogMetadata, ...]:
    return tuple(segment for segment in segments if segment.status in {"success", "completed", "error"})


def build_recovery_plan(spec: RunSpec) -> RecoveryPlan:
    expected = expected_sample_ids(spec)
    expected_set = set(expected)
    segments = tuple(inspect_log_metadata(path) for path in json_logs(spec.log_dir))
    authoritative = _authoritative_segments(segments)
    source = max(authoritative, key=lambda segment: segment.valid_sample_count, default=None)
    seen: set[str] = set()
    duplicates: list[str] = []
    for segment in authoritative:
        segment_seen: set[str] = set()
        for sample_id in segment.valid_sample_ids:
            if sample_id in segment_seen and sample_id not in duplicates:
                duplicates.append(sample_id)
            segment_seen.add(sample_id)
            seen.add(sample_id)
    unexpected = sorted(sample_id for sample_id in seen if sample_id not in expected_set)
    completed_expected = expected_set.intersection(seen)
    missing = tuple(sample_id for sample_id in expected if sample_id not in completed_expected)
    invalid = tuple(
        sample_id
        for sample_id in expected
        if sample_id in {invalid for segment in authoritative for invalid in segment.invalid_sample_ids}
        and sample_id not in completed_expected
    )
    return RecoveryPlan(
        run_id=spec.run_id,
        expected_total=spec.total_samples,
        source_log=str(source.path) if source else None,
        source_completed_count=len(completed_expected),
        missing_count=len(missing),
        duplicate_ids=tuple(sorted(duplicates)),
        unexpected_ids=tuple(unexpected),
        missing_ids=missing,
        invalid_ids=invalid,
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
                "valid_sample_count": segment.valid_sample_count,
                "invalid_sample_count": len(segment.invalid_sample_ids),
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
            "invalid_ids": list(plan.invalid_ids),
        },
    )
    return path


def reconciled_unique_count(spec: RunSpec, segment_paths: list[Path]) -> int:
    expected = set(expected_sample_ids(spec))
    completed: set[str] = set()
    for path in segment_paths:
        completed.update(expected.intersection(inspect_log_metadata(path).valid_sample_ids))
    return len(completed)
