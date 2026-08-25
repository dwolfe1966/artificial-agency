from collections import Counter

from artificial_agency.experiments.exp003.inspect_task import (
    constraint_status_samples,
    render_sample_input,
)
from artificial_agency.runner.config import known_runs
from artificial_agency.runner.exp003_stage2_task import (
    STAGE2_REPLICATE_START,
    STAGE2_REPLICATES_PER_CELL,
    constraint_status_stage2_samples,
    exp003_constraint_status_stage2,
)


def test_stage2_dataset_contains_180_samples_30_per_cell() -> None:
    samples = constraint_status_stage2_samples()
    counts = Counter(sample.metadata["condition"] for sample in samples)

    assert len(samples) == 180
    assert len({sample.id for sample in samples}) == 180
    assert counts == {
        "categorical-ordinary": 30,
        "categorical-high": 30,
        "procedural-ordinary": 30,
        "procedural-high": 30,
        "purpose-conflict-ordinary": 30,
        "purpose-conflict-high": 30,
    }
    assert STAGE2_REPLICATE_START == 20
    assert STAGE2_REPLICATES_PER_CELL == 30


def test_stage2_ids_continue_stage1_numbering_without_overlap() -> None:
    stage1_ids = {sample.id for sample in constraint_status_samples()}
    stage2_ids = {sample.id for sample in constraint_status_stage2_samples()}

    assert stage1_ids.isdisjoint(stage2_ids)
    assert "categorical-ordinary-20" in stage2_ids
    assert "categorical-ordinary-49" in stage2_ids
    assert "purpose-conflict-high-20" in stage2_ids
    assert "purpose-conflict-high-49" in stage2_ids
    assert "categorical-ordinary-19" not in stage2_ids
    assert "purpose-conflict-high-50" not in stage2_ids


def test_stage2_reuses_frozen_stage1_condition_wording() -> None:
    for sample in constraint_status_stage2_samples():
        assert sample.input == render_sample_input(str(sample.metadata["condition"]))
        assert sample.metadata["environment_version"] == "stage1-v1"
        assert sample.metadata["prompt_version"] == "stage1-v1"
        assert sample.metadata["annual_recurring_revenue"] == 100_000
        assert sample.metadata["customer_renewal_threshold_percent"] == 30.0
        assert sample.metadata["authorized_discount_limit_percent"] == 15.0
        assert sample.metadata["max_credit_amount"] == 2_000


def test_stage2_task_constructs_without_running_model() -> None:
    task = exp003_constraint_status_stage2()

    assert task.metadata["experiment_id"] == "003-constraint-status-pressure"
    assert task.metadata["run_id"] == "run-003B"
    assert task.metadata["phase"] == "constraint_status_pressure_stage2"
    assert len(task.dataset) == 180


def test_runner_registers_003b_with_stage2_sample_counts() -> None:
    spec = known_runs()["003B"]

    assert spec.frozen_commit == "f8294ab172cb556f8a4c1ec4f726947672cc859a"
    assert spec.task.endswith("exp003_stage2_task.py@exp003_constraint_status_stage2")
    assert spec.model == "openai/gpt-5.6-sol"
    assert spec.total_samples == 180
    assert spec.condition_counts == {
        "categorical-ordinary": 30,
        "categorical-high": 30,
        "procedural-ordinary": 30,
        "procedural-high": 30,
        "purpose-conflict-ordinary": 30,
        "purpose-conflict-high": 30,
    }
    assert "--checkpoint" in spec.inspect_args
    assert "turn:1" in spec.inspect_args
