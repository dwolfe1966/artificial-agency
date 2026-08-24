from inspect_ai import Task

from artificial_agency.experiments.exp001.config import (
    CONDITIONS,
    PHASE1_REPLICATES_PER_CONDITION,
)
from artificial_agency.experiments.exp001.inspect_task import (
    exp001_phase1,
    phase1_samples,
)


def test_phase1_dataset_has_30_condition_replicate_samples() -> None:
    samples = phase1_samples()

    assert len(samples) == len(CONDITIONS) * PHASE1_REPLICATES_PER_CONDITION
    assert {sample.metadata["condition"] for sample in samples} == set(CONDITIONS)
    assert all("high_goal_pressure" not in sample.input for sample in samples)


def test_inspect_task_constructs_without_running_model() -> None:
    task = exp001_phase1()

    assert isinstance(task, Task)
    assert task.metadata["experiment_id"] == "001-optimization-pressure"
    assert len(task.dataset) == 30

