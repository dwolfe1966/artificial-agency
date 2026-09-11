from __future__ import annotations

from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample

from artificial_agency.experiments.exp012.config import (
    MODEL_A_GPT,
    MODEL_B_CLAUDE,
    MODEL_C_GEMINI,
    ModelRun,
)
from artificial_agency.experiments.exp012.inspect_task import (
    capability_loss_samples,
    capability_loss_task,
)


BATCH_MANIFESTS: dict[int, tuple[str, tuple[int, int]]] = {
    1: ("principal", (0, 10)),
    2: ("principal", (10, 20)),
    3: ("principal", (20, 30)),
    4: ("capability", (0, 10)),
    5: ("capability", (10, 20)),
    6: ("capability", (20, 30)),
}


def batch_ids(run: ModelRun, batch_index: int) -> tuple[str, ...]:
    condition, (start, stop) = BATCH_MANIFESTS[batch_index]
    return tuple(f"{run.sample_prefix}-{condition}-{replicate:02d}" for replicate in range(start, stop))


def batch_samples(run: ModelRun, batch_index: int) -> list[Sample]:
    wanted = set(batch_ids(run, batch_index))
    selected = [
        sample for sample in capability_loss_samples(run) if str(sample.id) in wanted
    ]
    if tuple(str(sample.id) for sample in selected) != batch_ids(run, batch_index):
        raise RuntimeError(f"batch {batch_index} construction failed for {run.run_id}")
    for sample in selected:
        metadata = dict(sample.metadata or {})
        metadata.update(
            {
                "operational_batch_index": batch_index,
                "operational_batch_id": f"{run.sample_prefix}-B{batch_index}",
                "logical_confirmatory_run_id": run.run_id,
                "confirmatory_dataset_eligible": True,
                "non_confirmatory": False,
            }
        )
        sample.metadata = metadata
    return selected


def batch_task(run: ModelRun, batch_index: int) -> Task:
    task_obj = capability_loss_task(run)
    task_obj.dataset = MemoryDataset(
        batch_samples(run, batch_index),
        name=f"{run.run_id}-confirmatory-batch-{batch_index}",
        location=f"runner-v2://{run.run_id}/confirmatory-batch-{batch_index}",
    )
    condition, _ = BATCH_MANIFESTS[batch_index]
    metadata = dict(task_obj.metadata or {})
    metadata.update(
        {
            "operational_batch_index": batch_index,
            "operational_batch_condition": condition,
            "sample_count": 10,
            "confirmatory_dataset_eligible": True,
            "non_confirmatory": False,
        }
    )
    task_obj.metadata = metadata
    return task_obj


@task
def exp012_model_a_gpt56_sol_batch1() -> Task:
    return batch_task(MODEL_A_GPT, 1)


@task
def exp012_model_b_claude_sonnet5_batch1() -> Task:
    return batch_task(MODEL_B_CLAUDE, 1)


@task
def exp012_model_c_gemini37_flash_batch1() -> Task:
    return batch_task(MODEL_C_GEMINI, 1)
