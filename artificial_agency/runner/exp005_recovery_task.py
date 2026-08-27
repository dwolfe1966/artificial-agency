from __future__ import annotations

import json
import os
from pathlib import Path

from inspect_ai import Task, task

from .config import repository_root
from .exp005_cross_model_task import MODEL_B, cross_model_samples, cross_model_task


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


@task
def exp005_model_b_claude_sonnet5_recovery_missing() -> Task:
    payload = json.loads(_missing_ids_path().read_text(encoding="utf-8"))
    missing_ids = set(str(sample_id) for sample_id in payload["missing_ids"])
    task_obj = cross_model_task(MODEL_B)
    task_obj.dataset = [
        sample for sample in cross_model_samples(MODEL_B) if str(sample.id) in missing_ids
    ]
    if len(task_obj.dataset) != len(missing_ids):
        raise RuntimeError("recovery dataset did not match requested missing sample IDs")
    task_obj.metadata["recovery_source_log"] = payload.get("source_log")
    task_obj.metadata["recovery_missing_count"] = len(missing_ids)
    return task_obj
