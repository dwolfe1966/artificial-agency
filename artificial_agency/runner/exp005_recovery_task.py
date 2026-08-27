from __future__ import annotations

import json
import os
from pathlib import Path

from inspect_ai import Task, task

from artificial_agency.runner.config import repository_root
from artificial_agency.runner.exp005_cross_model_task import (
    MODEL_B,
    MODEL_C,
    CrossModelRun,
    cross_model_samples,
    cross_model_task,
)


def _missing_ids_path() -> Path:
    configured = os.environ.get("AA_RUNNER_RECOVERY_IDS_PATH")
    if configured:
        return Path(configured)
    return (
        repository_root()
        / "results"
        / "005-cross-model-replication"
        / "run-005B"
        / "RECOVERY_MISSING_IDS.json"
    )


def _recovery_task(run: CrossModelRun) -> Task:
    payload = json.loads(_missing_ids_path().read_text(encoding="utf-8"))
    missing_ids = set(str(sample_id) for sample_id in payload["missing_ids"])
    base = cross_model_task(run)
    recovery_samples = [
        sample for sample in cross_model_samples(run) if str(sample.id) in missing_ids
    ]
    if len(recovery_samples) != len(missing_ids):
        raise RuntimeError("recovery dataset did not match requested missing sample IDs")
    metadata = dict(base.metadata)
    metadata["recovery_source_log"] = payload.get("source_log")
    metadata["recovery_missing_count"] = len(missing_ids)
    return Task(
        dataset=recovery_samples,
        solver=base.solver,
        scorer=base.scorer,
        metadata=metadata,
    )


@task
def exp005_model_b_claude_sonnet5_recovery_missing() -> Task:
    return _recovery_task(MODEL_B)


@task
def exp005_model_c_gemini37_flash_recovery_missing() -> Task:
    return _recovery_task(MODEL_C)
