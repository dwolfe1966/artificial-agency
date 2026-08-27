from __future__ import annotations

from collections import Counter
from pathlib import Path

from artificial_agency.experiments.exp006.config import (
    MODEL_A_GPT,
    MODEL_B_CLAUDE,
    MODEL_C_GEMINI,
    MODEL_RUNS,
)
from artificial_agency.experiments.exp006.inspect_task import (
    action_representation_samples,
    exp006_model_a_gpt56_sol,
    exp006_model_b_claude_sonnet5,
    exp006_model_c_gemini37_flash,
)
from artificial_agency.runner.config import known_runs
from artificial_agency.runner.recovery import expected_sample_ids


EXPECTED_COUNTS = {
    "categorical-ordinary": 30,
    "categorical-high": 30,
    "procedural-ordinary": 30,
    "procedural-high": 30,
    "explicit-purpose-conflict-ordinary": 30,
    "explicit-purpose-conflict-high": 30,
}


def test_exp006_each_model_dataset_contains_180_samples_30_per_cell() -> None:
    for run in MODEL_RUNS:
        samples = action_representation_samples(run)
        counts = Counter(sample.metadata["condition"] for sample in samples)

        assert len(samples) == 180
        assert len({sample.id for sample in samples}) == 180
        assert counts == EXPECTED_COUNTS
        assert all(str(sample.id).startswith(f"{run.sample_prefix}-") for sample in samples)


def test_exp006_sample_ids_do_not_collide_across_models() -> None:
    ids_by_run = [
        {str(sample.id) for sample in action_representation_samples(run)}
        for run in MODEL_RUNS
    ]

    assert ids_by_run[0].isdisjoint(ids_by_run[1])
    assert ids_by_run[0].isdisjoint(ids_by_run[2])
    assert ids_by_run[1].isdisjoint(ids_by_run[2])
    assert "006A-GPT-categorical-ordinary-00" in ids_by_run[0]
    assert "006B-CLAUDE-explicit-purpose-conflict-high-29" in ids_by_run[1]
    assert "006C-GEMINI-procedural-high-29" in ids_by_run[2]


def test_exp006_task_metadata_is_outcome_blind_and_model_specific() -> None:
    task_run_pairs = (
        (exp006_model_a_gpt56_sol(), MODEL_A_GPT),
        (exp006_model_b_claude_sonnet5(), MODEL_B_CLAUDE),
        (exp006_model_c_gemini37_flash(), MODEL_C_GEMINI),
    )

    for task_obj, run in task_run_pairs:
        assert task_obj.metadata["experiment_id"] == (
            "006-action-representational-compliance"
        )
        assert task_obj.metadata["run_id"] == run.run_id
        assert task_obj.metadata["model_id"] == run.model_id
        assert task_obj.metadata["primary_endpoints"] == (
            "operational_constraint_violation,"
            "representational_constraint_violation"
        )
        assert "score" not in task_obj.metadata
        assert len(task_obj.dataset) == 180


def test_runner_registers_exp006_run_specs_with_provider_configs() -> None:
    runs = known_runs()
    expected = {
        "006A-GPT": ("openai/gpt-5.6-sol", "exp006_model_a_gpt56_sol"),
        "006B-CLAUDE": (
            "anthropic/claude-sonnet-5",
            "exp006_model_b_claude_sonnet5",
        ),
        "006C-GEMINI": (
            "google/gemini-3.7-flash",
            "exp006_model_c_gemini37_flash",
        ),
    }

    for run_id, (model, task_name) in expected.items():
        spec = runs[run_id]
        assert spec.model == model
        assert spec.task.endswith(f"inspect_task.py@{task_name}")
        assert spec.frozen_commit == "aeab4f447cdb57f2f1db3c5a7ca61a09266a0df8"
        assert spec.total_samples == 180
        assert spec.condition_counts == EXPECTED_COUNTS
        assert "--no-parallel-tool-calls" in spec.inspect_args
        assert "--checkpoint" in spec.inspect_args
        assert "turn:1" in spec.inspect_args


def test_exp006_openai_documents_provider_specific_reasoning_controls() -> None:
    runs = known_runs()

    assert "--reasoning-effort" in runs["006A-GPT"].inspect_args
    assert "--verbosity" in runs["006A-GPT"].inspect_args
    assert "--reasoning-effort" not in runs["006B-CLAUDE"].inspect_args
    assert "--verbosity" not in runs["006B-CLAUDE"].inspect_args
    assert "--reasoning-effort" not in runs["006C-GEMINI"].inspect_args
    assert "--verbosity" not in runs["006C-GEMINI"].inspect_args


def test_exp006_recovery_expected_ids_cover_each_registered_run() -> None:
    runs = known_runs()

    for run_id in ("006A-GPT", "006B-CLAUDE", "006C-GEMINI"):
        ids = expected_sample_ids(runs[run_id])
        assert len(ids) == 180
        assert len(set(ids)) == 180
        assert ids[0].startswith(f"{run_id}-")


def test_provider_comparability_artifacts_exist_and_document_differences() -> None:
    root = Path("experiments/006-action-representational-compliance")
    matrix = (root / "provider_comparability_matrix.md").read_text(
        encoding="utf-8"
    )
    fixture = (root / "scoring_fixture_matrix.md").read_text(encoding="utf-8")

    assert "openai/gpt-5.6-sol" in matrix
    assert "anthropic/claude-sonnet-5" in matrix
    assert "google/gemini-3.7-flash" in matrix
    assert "potentially measurement-affecting" in matrix
    assert "Phrase presence alone cannot trigger a violation" in fixture


def test_raw_logs_for_exp006_remain_ignored_by_git() -> None:
    import subprocess

    for path in (
        "results/006-action-representational-compliance/run-006A-GPT/inspect/test.json",
        "results/006-action-representational-compliance/run-006B-CLAUDE/inspect/test.json",
        "results/006-action-representational-compliance/run-006C-GEMINI/inspect/test.json",
        "results/006-action-representational-compliance/run-006A-GPT/canary/test.json",
        "results/006-action-representational-compliance/run-006B-CLAUDE/RECOVERY_PLAN.json",
        "results/006-action-representational-compliance/run-006C-GEMINI/RECOVERY_MISSING_IDS.json",
    ):
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0
