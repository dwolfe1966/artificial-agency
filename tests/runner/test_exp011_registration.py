from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from artificial_agency.experiments.exp011.config import (
    MODEL_A_GPT,
    deterministic_sample_seed,
)
from artificial_agency.experiments.exp011.inspect_task import delegation_samples
from artificial_agency.runner.exp011_proof_task import MODEL_A_GPT_PROOF, proof_samples
from artificial_agency.runner import supervisor
from artificial_agency.runner.config import external_runtime_root, known_runs
from artificial_agency.runner.recovery import expected_sample_ids


def test_runner_registers_exp011_confirmatory_runs() -> None:
    runs = known_runs()
    expected = {
        "011A-GPT": "openai/gpt-5.6-sol",
        "011B-CLAUDE": "anthropic/claude-sonnet-5",
        "011C-GEMINI": "google/gemini-3.7-flash",
    }
    expected_counts = {"direct": 30, "delegation": 30}
    for run_id, model in expected.items():
        spec = runs[run_id]
        assert spec.experiment_id == "011-multi-agent-delegation"
        assert spec.model == model
        assert spec.total_samples == 60
        assert spec.condition_counts == expected_counts
        assert spec.recovery_batch_size == 10
        assert "artificial_agency/experiments/exp011" in spec.scientific_paths
        assert "experiments/011-multi-agent-delegation" in spec.scientific_paths
        assert "scripts/analyze_exp011_final.py" in spec.scientific_paths
        joined_args = ",".join(spec.inspect_args)
        assert f"run_id=run-{run_id}" in joined_args
        assert "preregistration_sha=07f3c0bdcb7dee96fe7b350363905ffdd585edaf" in joined_args
        assert str(spec.log_dir).endswith(f"run-{run_id}/inspect")
        assert "results/011-multi-agent-delegation" not in str(spec.log_dir)


def test_exp011_expected_ids_support_sample_atomic_recovery() -> None:
    for run_id in ("011A-GPT", "011B-CLAUDE", "011C-GEMINI"):
        ids = expected_sample_ids(known_runs()[run_id])
        assert len(ids) == 60
        assert len(set(ids)) == 60
        assert ids[0] == f"{run_id}-direct-00"
        assert ids[-1] == f"{run_id}-delegation-29"


def test_exp011_proof_runs_are_non_confirmatory_one_sample_runs() -> None:
    runs = known_runs()
    expected = {
        "011-PROOF-GPT": "openai/gpt-5.6-sol",
        "011-PROOF-CLAUDE": "anthropic/claude-sonnet-5",
        "011-PROOF-GEMINI": "google/gemini-3.7-flash",
    }
    confirmatory_ids = {str(sample.id) for sample in delegation_samples(MODEL_A_GPT)}
    for run_id, model in expected.items():
        spec = runs[run_id]
        ids = expected_sample_ids(spec)
        assert spec.experiment_id == "011-multi-agent-delegation"
        assert spec.model == model
        assert spec.total_samples == 1
        assert spec.condition_counts == {"delegation": 1}
        assert "production_proof=true" in ",".join(spec.inspect_args)
        assert "confirmatory_dataset_eligible=false" in ",".join(spec.inspect_args)
        assert ids == (f"{run_id}-delegation-00",)
        assert set(ids).isdisjoint(confirmatory_ids)


def test_exp011_proof_sample_marks_future_analysis_exclusion() -> None:
    sample = proof_samples(MODEL_A_GPT_PROOF)[0]

    assert sample.id == "011-PROOF-GPT-delegation-00"
    assert sample.metadata["actor_condition"] == "delegation"
    assert sample.metadata["production_proof"] is True
    assert sample.metadata["non_confirmatory"] is True
    assert sample.metadata["confirmatory_dataset_eligible"] is False
    assert sample.metadata["exclude_from_confirmatory_analysis"] is True


def test_exp011_live_runtime_roots_are_external_and_isolated(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime_root = tmp_path / "external-runtime"
    repo_root = tmp_path / "repo"
    monkeypatch.setenv("ARTIFICIAL_AGENCY_RUNTIME_ROOT", str(runtime_root))

    runs = known_runs(repo_root)
    specs = [runs["011A-GPT"], runs["011B-CLAUDE"], runs["011C-GEMINI"]]

    assert external_runtime_root(repo_root) == runtime_root
    assert len({spec.status_path.parent for spec in specs}) == 3
    for spec in specs:
        assert runtime_root in spec.status_path.parents
        assert repo_root not in spec.status_path.parents


def test_exp011_recovery_command_uses_sample_atomic_task() -> None:
    spec = known_runs()["011C-GEMINI"]
    command = supervisor.build_inspect_command(spec, recovery=True)
    joined = " ".join(command)

    assert "exp011_recovery_task.py@exp011_model_c_gemini37_flash_recovery_missing" in joined


def test_exp011_proof_recovery_command_uses_proof_task() -> None:
    spec = known_runs()["011-PROOF-GEMINI"]
    command = supervisor.build_inspect_command(spec, recovery=True)
    joined = " ".join(command)

    assert "exp011_proof_task.py@exp011_proof_gemini37_flash_recovery_missing" in joined


def test_exp011_recovery_task_imports_under_inspect_file_loader(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    recovery_ids = tmp_path / "runtime" / "RECOVERY_MISSING_IDS.json"
    recovery_ids.parent.mkdir()
    recovery_ids.write_text(
        json.dumps(
            {
                "run_id": "011C-GEMINI",
                "missing_ids": ["011C-GEMINI-delegation-07"],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("AA_RECOVERY_MISSING_IDS", str(recovery_ids))

    task_path = Path("artificial_agency/runner/exp011_recovery_task.py").resolve()
    spec = importlib.util.spec_from_file_location("inspect_loaded_exp011_recovery", task_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    task = module.exp011_model_c_gemini37_flash_recovery_missing()
    assert task.dataset.name == "run-011C-GEMINI-sample-atomic-recovery-missing"
    assert [sample.id for sample in task.dataset] == ["011C-GEMINI-delegation-07"]
    assert list(task.dataset)[0].metadata["sample_seed"] == deterministic_sample_seed(
        "model_c_gemini",
        "delegation",
        7,
    )
