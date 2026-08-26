from __future__ import annotations

from collections import Counter
from pathlib import Path

from artificial_agency.experiments.exp004.config import (
    AUTHORIZED_DISCOUNT_LIMIT,
    CONDITION_TEXT_SHA256,
    CUSTOMER_RENEWAL_THRESHOLD_PERCENT,
    MANIPULATION_CHECK_TEXT,
    MAX_CREDIT_AMOUNT,
)
from artificial_agency.experiments.exp004.inspect_task import render_sample_input
from artificial_agency.runner.config import known_runs
from artificial_agency.runner.exp005_cross_model_task import (
    MODEL_B,
    MODEL_C,
    cross_model_samples,
    exp005_model_b_claude_sonnet5,
    exp005_model_c_gemini37_flash,
)


EXPECTED_COUNTS = {
    "categorical-ordinary": 50,
    "categorical-high": 50,
    "procedural-ordinary": 50,
    "procedural-high": 50,
    "explicit-purpose-conflict-ordinary": 50,
    "explicit-purpose-conflict-high": 50,
}


def test_exp005_model_b_dataset_contains_300_samples_50_per_cell() -> None:
    samples = cross_model_samples(MODEL_B)
    counts = Counter(sample.metadata["condition"] for sample in samples)

    assert len(samples) == 300
    assert len({sample.id for sample in samples}) == 300
    assert counts == EXPECTED_COUNTS
    assert all(sample.id.startswith("005B-") for sample in samples)


def test_exp005_model_c_dataset_contains_300_samples_50_per_cell() -> None:
    samples = cross_model_samples(MODEL_C)
    counts = Counter(sample.metadata["condition"] for sample in samples)

    assert len(samples) == 300
    assert len({sample.id for sample in samples}) == 300
    assert counts == EXPECTED_COUNTS
    assert all(sample.id.startswith("005C-") for sample in samples)


def test_exp005_sample_ids_do_not_collide_across_models() -> None:
    model_b_ids = {sample.id for sample in cross_model_samples(MODEL_B)}
    model_c_ids = {sample.id for sample in cross_model_samples(MODEL_C)}

    assert model_b_ids.isdisjoint(model_c_ids)
    assert "005B-categorical-ordinary-00" in model_b_ids
    assert "005B-explicit-purpose-conflict-high-49" in model_b_ids
    assert "005C-categorical-ordinary-00" in model_c_ids
    assert "005C-explicit-purpose-conflict-high-49" in model_c_ids


def test_exp005_reuses_frozen_exp004_scientific_wording() -> None:
    for run in (MODEL_B, MODEL_C):
        for sample in cross_model_samples(run):
            condition = str(sample.metadata["condition"])
            assert sample.input == render_sample_input(condition)
            assert sample.metadata["condition_protocol_sha256"] == (
                CONDITION_TEXT_SHA256
            )
            assert sample.metadata["environment_version"] == "stage1-v1"
            assert sample.metadata["prompt_version"] == "stage1-v1"
            assert sample.metadata["wording_version"] == "stage1-v1"
            assert sample.metadata["annual_recurring_revenue"] == 100_000
            assert sample.metadata["customer_renewal_threshold_percent"] == (
                CUSTOMER_RENEWAL_THRESHOLD_PERCENT
            )
            assert sample.metadata["authorized_discount_limit_percent"] == (
                AUTHORIZED_DISCOUNT_LIMIT
            )
            assert sample.metadata["max_credit_amount"] == MAX_CREDIT_AMOUNT
            assert sample.metadata["reference_scientific_sha"] == (
                "aa126f9254a01c96e85545a9e1a77d10195f2604"
            )


def test_exp005_task_metadata_preserves_manipulation_check_schema() -> None:
    for task_obj, run in (
        (exp005_model_b_claude_sonnet5(), MODEL_B),
        (exp005_model_c_gemini37_flash(), MODEL_C),
    ):
        assert task_obj.metadata["experiment_id"] == "005-cross-model-replication"
        assert task_obj.metadata["reference_experiment_id"] == (
            "004-constraint-meaning-validation"
        )
        assert task_obj.metadata["run_id"] == run.run_id
        assert task_obj.metadata["model_id"] == run.model_id
        assert task_obj.metadata["manipulation_check_protocol"] == (
            "pre_action_structured_tool"
        )
        assert task_obj.metadata["manipulation_check_text"] == MANIPULATION_CHECK_TEXT
        assert len(task_obj.dataset) == 300


def test_runner_registers_005b_and_005c_with_frozen_ids() -> None:
    runs = known_runs()
    model_b = runs["005B"]
    model_c = runs["005C"]

    assert model_b.model == "anthropic/claude-sonnet-5"
    assert model_c.model == "google/gemini-3.7-flash"
    assert model_b.frozen_commit == "aa126f9254a01c96e85545a9e1a77d10195f2604"
    assert model_c.frozen_commit == "aa126f9254a01c96e85545a9e1a77d10195f2604"
    assert model_b.total_samples == 300
    assert model_c.total_samples == 300
    assert model_b.condition_counts == EXPECTED_COUNTS
    assert model_c.condition_counts == EXPECTED_COUNTS
    assert model_b.task.endswith(
        "exp005_cross_model_task.py@exp005_model_b_claude_sonnet5"
    )
    assert model_c.task.endswith(
        "exp005_cross_model_task.py@exp005_model_c_gemini37_flash"
    )


def test_exp005_inspect_args_document_provider_specific_unsupported_settings() -> None:
    runs = known_runs()
    for run_id in ("005B", "005C"):
        spec = runs[run_id]
        assert "--reasoning-effort" not in spec.inspect_args
        assert "--verbosity" not in spec.inspect_args
        assert "--no-parallel-tool-calls" in spec.inspect_args
        assert "--checkpoint" in spec.inspect_args
        assert "turn:1" in spec.inspect_args


def test_provider_comparability_artifacts_document_expected_differences() -> None:
    root = Path("experiments/005-cross-model-replication")
    matrix = (root / "provider_comparability_matrix.md").read_text(
        encoding="utf-8"
    )
    config_b = (root / "run_config_005B.md").read_text(encoding="utf-8")
    config_c = (root / "run_config_005C.md").read_text(encoding="utf-8")

    assert "anthropic/claude-sonnet-5" in matrix
    assert "google/gemini-3.7-flash" in matrix
    assert "unsupported / not sent" in config_b
    assert "unsupported / not sent" in config_c
    assert "Material scientific difference?" in matrix


def test_raw_logs_for_exp005_remain_ignored_by_git() -> None:
    import subprocess

    for path in (
        "results/005-cross-model-replication/run-005B/inspect/test.json",
        "results/005-cross-model-replication/run-005C/inspect/test.json",
        "results/005-cross-model-replication/run-005B/canary/test.json",
        "results/005-cross-model-replication/run-005C/canary/test.json",
    ):
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0
