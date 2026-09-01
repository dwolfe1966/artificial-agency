from __future__ import annotations

import json

from inspect_ai import Task, task

from artificial_agency.experiments.exp009.config import (
    MODEL_A_GPT,
    MODEL_B_CLAUDE,
    MODEL_C_GEMINI,
    ModelRun,
)
from artificial_agency.experiments.exp009.inspect_task import (
    observability_samples,
    observability_task,
)

from .config import repository_root


RECOVERY_MISSING_IDS = "RECOVERY_MISSING_IDS.json"


def _payload() -> dict[str, object]:
    path = repository_root() / RECOVERY_MISSING_IDS
    if not path.exists():
        raise RuntimeError(f"Missing recovery manifest: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _recovery_task(run: ModelRun) -> Task:
    payload = _payload()
    missing_ids = tuple(str(sample_id) for sample_id in payload.get("missing_ids", []))
    expected = {str(sample.id): sample for sample in observability_samples(run)}
    recovery_samples = [expected[sample_id] for sample_id in missing_ids if sample_id in expected]
    if len(recovery_samples) != len(missing_ids):
        raise RuntimeError("recovery dataset did not match requested missing sample IDs")
    task_obj = observability_task(run)
    task_obj.dataset = recovery_samples
    metadata = dict(task_obj.metadata or {})
    metadata["recovery_source_log"] = payload.get("source_log")
    metadata["recovery_missing_count"] = len(missing_ids)
    metadata["recovery_mode"] = "missing_ids_only_complete_phase_a_phase_b"
    task_obj.metadata = metadata
    return task_obj


@task
def exp009_model_a_gpt56_sol_stage1_recovery_missing() -> Task:
    return _recovery_task(MODEL_A_GPT)


@task
def exp009_model_b_claude_sonnet5_stage1_recovery_missing() -> Task:
    return _recovery_task(MODEL_B_CLAUDE)


@task
def exp009_model_c_gemini37_flash_stage1_recovery_missing() -> Task:
    return _recovery_task(MODEL_C_GEMINI)

