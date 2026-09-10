from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from artificial_agency.experiments.exp012.config import (
    MODEL_A_GPT,
    deterministic_sequence_seed,
)
from artificial_agency.experiments.exp012.inspect_task import capability_loss_samples
from artificial_agency.runner import supervisor
from artificial_agency.runner.config import external_runtime_root, known_runs
from artificial_agency.runner.exp012_proof_task import MODEL_A_GPT_PROOF, proof_samples
from artificial_agency.runner.recovery import expected_sample_ids


def test_runner_registers_exp012_confirmatory_runs() -> None:
    runs = known_runs()
    expected = {
        "012A-GPT": "openai/gpt-5.6-sol",
        "012B-CLAUDE": "anthropic/claude-sonnet-5",
        "012C-GEMINI": "google/gemini-3.7-flash",
    }
    expected_counts = {"principal": 30, "capability": 30}
    for run_id, model in expected.items():
        spec = runs[run_id]
        assert spec.experiment_id == "012-agent-relative-capability-loss"
        assert spec.model == model
        assert spec.total_samples == 60
        assert spec.condition_counts == expected_counts
        assert spec.recovery_batch_size == 10
        assert spec.frozen_commit == "41c937ad40e275a019ac26c526c343f40bdbad4d"
        assert "artificial_agency/experiments/exp012" in spec.scientific_paths
        assert "experiments/012-agent-relative-capability-loss" in spec.scientific_paths
        assert "scripts/analyze_exp012_final.py" in spec.scientific_paths
        joined_args = ",".join(spec.inspect_args)
        assert f"run_id=run-{run_id}" in joined_args
        assert "preregistration_sha=93a89945ae98166d89939bcf28f8e0bba45db947" in joined_args
        assert "capability_amendment_sha=f6cf9a49119671888176e8d6b79fbab7b567e2b6" in joined_args
        assert "results/012-agent-relative-capability-loss" not in str(spec.log_dir)


def test_exp012_expected_ids_support_sequence_atomic_recovery() -> None:
    for run_id in ("012A-GPT", "012B-CLAUDE", "012C-GEMINI"):
        ids = expected_sample_ids(known_runs()[run_id])
        assert len(ids) == 60
        assert len(set(ids)) == 60
        assert ids[0] == f"{run_id}-principal-00"
        assert ids[-1] == f"{run_id}-capability-29"


def test_exp012_proof_runs_are_non_confirmatory_one_sequence_runs() -> None:
    runs = known_runs()
    expected = {
        "012-PROOF-GPT": "openai/gpt-5.6-sol",
        "012-PROOF-CLAUDE": "anthropic/claude-sonnet-5",
        "012-PROOF-GEMINI": "google/gemini-3.7-flash",
    }
    confirmatory_ids = {str(sample.id) for sample in capability_loss_samples(MODEL_A_GPT)}
    for run_id, model in expected.items():
        spec = runs[run_id]
        ids = expected_sample_ids(spec)
        assert spec.experiment_id == "012-agent-relative-capability-loss"
        assert spec.model == model
        assert spec.total_samples == 1
        assert spec.condition_counts == {"capability": 1}
        assert "production_proof=true" in ",".join(spec.inspect_args)
        assert "confirmatory_dataset_eligible=false" in ",".join(spec.inspect_args)
        assert ids == (f"{run_id}-capability-00",)
        assert set(ids).isdisjoint(confirmatory_ids)


def test_exp012_proof_sample_marks_future_analysis_exclusion() -> None:
    sample = proof_samples(MODEL_A_GPT_PROOF)[0]

    assert sample.id == "012-PROOF-GPT-capability-00"
    assert sample.metadata["consequence_condition"] == "capability"
    assert sample.metadata["production_proof"] is True
    assert sample.metadata["non_confirmatory"] is True
    assert sample.metadata["confirmatory_dataset_eligible"] is False
    assert sample.metadata["exclude_from_confirmatory_analysis"] is True


def test_exp012_live_runtime_roots_are_external_and_isolated(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime_root = tmp_path / "external-runtime"
    repo_root = tmp_path / "repo"
    monkeypatch.setenv("ARTIFICIAL_AGENCY_RUNTIME_ROOT", str(runtime_root))

    runs = known_runs(repo_root)
    specs = [runs["012A-GPT"], runs["012B-CLAUDE"], runs["012C-GEMINI"]]

    assert external_runtime_root(repo_root) == runtime_root
    assert len({spec.status_path.parent for spec in specs}) == 3
    for spec in specs:
        assert runtime_root in spec.status_path.parents
        assert repo_root not in spec.status_path.parents


def test_exp012_recovery_command_uses_sequence_atomic_task() -> None:
    spec = known_runs()["012C-GEMINI"]
    command = supervisor.build_inspect_command(spec, recovery=True)
    joined = " ".join(command)

    assert "exp012_recovery_task.py@exp012_model_c_gemini37_flash_recovery_missing" in joined


def test_exp012_proof_recovery_command_uses_proof_task() -> None:
    spec = known_runs()["012-PROOF-GEMINI"]
    command = supervisor.build_inspect_command(spec, recovery=True)
    joined = " ".join(command)

    assert "exp012_proof_task.py@exp012_proof_gemini37_flash_recovery_missing" in joined


def test_exp012_recovery_task_imports_under_inspect_file_loader(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    recovery_ids = tmp_path / "runtime" / "RECOVERY_MISSING_IDS.json"
    recovery_ids.parent.mkdir()
    recovery_ids.write_text(
        json.dumps(
            {
                "run_id": "012C-GEMINI",
                "missing_ids": ["012C-GEMINI-capability-07"],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("AA_RECOVERY_MISSING_IDS", str(recovery_ids))

    task_path = Path("artificial_agency/runner/exp012_recovery_task.py").resolve()
    spec = importlib.util.spec_from_file_location("inspect_loaded_exp012_recovery", task_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    task = module.exp012_model_c_gemini37_flash_recovery_missing()
    assert task.dataset.name == "run-012C-GEMINI-sequence-atomic-recovery-missing"
    assert [sample.id for sample in task.dataset] == ["012C-GEMINI-capability-07"]
    assert list(task.dataset)[0].metadata["sequence_seed"] == deterministic_sequence_seed(
        "model_c_gemini",
        "capability",
        7,
    )
