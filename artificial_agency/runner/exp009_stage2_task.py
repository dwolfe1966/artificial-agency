from __future__ import annotations

from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset

from artificial_agency.experiments.exp009.config import (
    MODEL_A_GPT_STAGE2,
    MODEL_B_CLAUDE_STAGE2,
    MODEL_C_GEMINI_STAGE2,
    ModelRun,
)
from artificial_agency.experiments.exp009.inspect_task import (
    observability_samples,
    observability_task,
)


def stage2_observability_task(run: ModelRun) -> Task:
    task_obj = observability_task(run)
    samples = observability_samples(run, stage="stage2")
    task_obj.dataset = MemoryDataset(
        samples,
        name=f"{run.run_id}-stage2",
        location=f"runner-v2://{run.run_id}/stage2",
    )
    metadata = dict(task_obj.metadata or {})
    metadata["stage"] = "stage2"
    metadata["phase"] = "observability_detection_probability_stage2"
    metadata["replicates_per_cell"] = 15
    metadata["sample_count"] = len(samples)
    task_obj.metadata = metadata
    return task_obj


@task
def exp009_model_a_gpt56_sol_stage2() -> Task:
    return stage2_observability_task(MODEL_A_GPT_STAGE2)


@task
def exp009_model_b_claude_sonnet5_stage2() -> Task:
    return stage2_observability_task(MODEL_B_CLAUDE_STAGE2)


@task
def exp009_model_c_gemini37_flash_stage2() -> Task:
    return stage2_observability_task(MODEL_C_GEMINI_STAGE2)
