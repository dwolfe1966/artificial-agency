from __future__ import annotations

import json
import os
from pathlib import Path

from inspect_ai import Task, task

from artificial_agency.experiments.exp008.config import (
    MODEL_A_GPT,
    MODEL_B_CLAUDE,
    MODEL_C_GEMINI,
    ModelRun,
)
from artificial_agency.experiments.exp008.inspect_task import (
    evaluation_awareness_samples,
    evaluation_awareness_task,
)
from artificial_agency.runner.config import repository_root


def _missing_ids_path(run: ModelRun) -> Path:
    configured = os.environ.get("AA_RUNNER_RECOVERY_IDS_PATH")
    if configured:
        return Path(configured)
    return (
        repository_root()
        / "results"
        / "008-evaluation-awareness"
        / run.run_id
        / "RECOVERY_MISSING_IDS.json"
    )


def _recovery_task(run: ModelRun) -> Task:
    payload = json.loads(_missing_ids_path(run).read_text(encoding="utf-8"))
    missing_ids = set(str(sample_id) for sample_id in payload["missing_ids"])
    base = evaluation_awareness_task(run)
    recovery_samples = [
        sample
        for sample in evaluation_awareness_samples(run)
        if str(sample.id) in missing_ids
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
def exp008_model_a_gpt56_sol_recovery_missing() -> Task:
    return _recovery_task(MODEL_A_GPT)


@task
def exp008_model_b_claude_sonnet5_recovery_missing() -> Task:
    return _recovery_task(MODEL_B_CLAUDE)


@task
def exp008_model_c_gemini37_flash_recovery_missing() -> Task:
    return _recovery_task(MODEL_C_GEMINI)
