from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from artificial_agency.experiments.exp010.config import (
    MODEL_C_GEMINI,
    deterministic_sequence_seed,
)
from artificial_agency.experiments.exp010.inspect_task import repeated_pressure_samples
from artificial_agency.runner import supervisor
from artificial_agency.runner.config import external_runtime_root, known_runs
from artificial_agency.runner.recovery import (
    build_recovery_plan,
    expected_sample_ids,
    write_recovery_plan,
)
from artificial_agency.runner.state import atomic_write_json


def _patch_010c(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    original = known_runs()["010C-GEMINI"]
    run_root = tmp_path / "runtime" / "010-repeated-operational-pressure" / "run-010C-GEMINI"
    spec = type(original)(
        **{
            **original.__dict__,
            "log_dir": run_root / "inspect",
            "status_path": run_root / "RUN_STATUS.json",
            "operational_log": run_root / "operational.log",
            "lock_path": run_root / "RUN_LOCK.json",
            "pid_path": run_root / "RUNNER.pid",
            "stdout_path": run_root / "runner-supervisor.out",
            "canary_log_dir": run_root / "canary",
        }
    )
    monkeypatch.setattr(supervisor, "known_runs", lambda: {spec.run_id: spec})
    monkeypatch.setattr(supervisor, "repository_root", lambda: tmp_path)
    return spec


def _write_log(path: Path, status: str, sample_ids: list[str], *, complete_010: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    samples = []
    for sample_id in sample_ids:
        metadata = {
            "sequence_any_operational_constraint_violation": False,
            "primary_label_id": "sequence_constraint_bounded_no_violation",
            "phase_a_done": True,
            "phase_b_done": True,
            "phase_a_frozen": True,
            "episode_records": [
                {"episode": episode, "resource_after": 100}
                for episode in range(1, 11)
            ],
            "stochastic": {
                "rng_version": "exp010-sequence-seed-v1-no-stochastic-events",
                "sequence_seed": 1,
            },
            "awareness_capture_status": "captured_valid",
        }
        if not complete_010:
            metadata["phase_b_done"] = False
            metadata.pop("awareness_capture_status")
        samples.append(
            {
                "id": sample_id,
                "completed_at": "2026-09-06T00:00:00+00:00",
                "output": {"completion": "redacted"},
                "scores": {
                    "repeated_pressure_outcome_scorer": {
                        "value": "sequence_constraint_bounded_no_violation",
                        "metadata": metadata,
                    }
                },
                "turn_count": 1,
            }
        )
    path.write_text(json.dumps({"status": status, "samples": samples}), encoding="utf-8")


def test_runner_registers_exp010_runs() -> None:
    runs = known_runs()
    expected = {
        "010A-GPT": "openai/gpt-5.6-sol",
        "010B-CLAUDE": "anthropic/claude-sonnet-5",
        "010C-GEMINI": "google/gemini-3.7-flash",
    }
    expected_counts = {"low": 20, "medium": 20, "high": 20}
    for run_id, model in expected.items():
        spec = runs[run_id]
        assert spec.experiment_id == "010-repeated-operational-pressure"
        assert spec.model == model
        assert spec.total_samples == 60
        assert spec.condition_counts == expected_counts
        assert spec.recovery_batch_size == 5
        assert "artificial_agency/experiments/exp010" in spec.scientific_paths
        assert "experiments/010-repeated-operational-pressure" in spec.scientific_paths
        assert "scripts/analyze_exp010_final.py" in spec.scientific_paths
        joined_args = ",".join(spec.inspect_args)
        assert f"run_id=run-{run_id}" in joined_args
        assert "preregistration_sha=accfa2ef5a89a465083306ccee0fe0bec66f46dc" in joined_args
        assert "pressure_amendment_sha=49c683d179f86fa16d587bfc4ae0767f8e5d16cf" in joined_args
        assert str(spec.log_dir).endswith(f"run-{run_id}/inspect")
        assert "results/010-repeated-operational-pressure" not in str(spec.log_dir)


def test_exp010_expected_ids_support_sequence_atomic_recovery() -> None:
    for run_id in ("010A-GPT", "010B-CLAUDE", "010C-GEMINI"):
        ids = expected_sample_ids(known_runs()[run_id])
        assert len(ids) == 60
        assert len(set(ids)) == 60
        assert ids[0] == f"{run_id}-low-00"
        assert ids[-1] == f"{run_id}-high-19"


def test_exp010_live_runtime_roots_are_external_and_isolated(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime_root = tmp_path / "external-runtime"
    repo_root = tmp_path / "repo"
    monkeypatch.setenv("ARTIFICIAL_AGENCY_RUNTIME_ROOT", str(runtime_root))

    runs = known_runs(repo_root)
    specs = [runs["010A-GPT"], runs["010B-CLAUDE"], runs["010C-GEMINI"]]

    assert external_runtime_root(repo_root) == runtime_root
    assert len({spec.status_path.parent for spec in specs}) == 3
    for spec in specs:
        assert runtime_root in spec.status_path.parents
        assert repo_root not in spec.status_path.parents


def test_exp010_recovery_command_uses_sequence_atomic_task() -> None:
    spec = known_runs()["010C-GEMINI"]
    command = supervisor.build_inspect_command(spec, recovery=True)
    joined = " ".join(command)

    assert "exp010_recovery_task.py@exp010_model_c_gemini37_flash_recovery_missing" in joined


def test_exp010_recovery_task_imports_under_inspect_file_loader(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    recovery_ids = tmp_path / "runtime" / "RECOVERY_MISSING_IDS.json"
    recovery_ids.parent.mkdir()
    recovery_ids.write_text(
        json.dumps(
            {
                "run_id": "010C-GEMINI",
                "missing_ids": ["010C-GEMINI-high-07"],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("AA_RECOVERY_MISSING_IDS", str(recovery_ids))

    task_path = Path("artificial_agency/runner/exp010_recovery_task.py").resolve()
    spec = importlib.util.spec_from_file_location("inspect_loaded_exp010_recovery", task_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    task = module.exp010_model_c_gemini37_flash_recovery_missing()
    assert task.dataset.name == "run-010C-GEMINI-sequence-atomic-recovery-missing"
    assert [sample.id for sample in task.dataset] == ["010C-GEMINI-high-07"]
    assert list(task.dataset)[0].metadata["sequence_seed"] == deterministic_sequence_seed(
        "model_c_gemini",
        "high",
        7,
    )


def test_exp010_recovery_plan_selects_only_missing_sequences(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    spec = _patch_010c(tmp_path, monkeypatch)
    expected = list(expected_sample_ids(spec))
    _write_log(spec.log_dir / "partial.json", "error", expected[:12])

    plan = build_recovery_plan(spec)
    write_recovery_plan(spec, plan)
    payload = json.loads(
        (spec.status_path.parent / "RECOVERY_MISSING_IDS.json").read_text(
            encoding="utf-8"
        )
    )

    assert plan.source_completed_count == 12
    assert plan.missing_count == 48
    assert set(plan.missing_ids).isdisjoint(expected[:12])
    assert payload["missing_ids"] == expected[12:17]
    assert payload["batch_size"] == 5


def test_exp010_finalize_accepts_complete_sequence_lifecycle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    spec = _patch_010c(tmp_path, monkeypatch)
    expected = list(expected_sample_ids(spec))
    _write_log(spec.log_dir / "complete.json", "success", expected)
    atomic_write_json(
        spec.status_path,
        {
            "state": "COMPLETED",
            "completed": spec.total_samples,
            "supervisor_pid": None,
        },
    )

    status = supervisor.finalize_run(spec.run_id)

    assert status["raw_log_path"].endswith("complete.json")
    assert status["raw_log_sha256"]


def test_exp010_finalize_refuses_incomplete_sequence_lifecycle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    spec = _patch_010c(tmp_path, monkeypatch)
    expected = list(expected_sample_ids(spec))
    _write_log(spec.log_dir / "incomplete.json", "success", expected, complete_010=False)
    atomic_write_json(
        spec.status_path,
        {
            "state": "COMPLETED",
            "completed": spec.total_samples,
            "supervisor_pid": None,
        },
    )

    with pytest.raises(RuntimeError, match="Experiment 010"):
        supervisor.finalize_run(spec.run_id)


def test_workflow_allows_registered_exp010_runs() -> None:
    workflow_text = Path(".github/workflows/experiment-runner.yml").read_text(
        encoding="utf-8"
    )

    assert '- "010A-GPT"' in workflow_text
    assert '- "010B-CLAUDE"' in workflow_text
    assert '- "010C-GEMINI"' in workflow_text
    assert "010A-GPT|010B-CLAUDE|010C-GEMINI" in workflow_text


def test_exp010_recovery_preserves_original_sequence_seed() -> None:
    sample_id = "010C-GEMINI-medium-13"
    original = {str(sample.id): sample for sample in repeated_pressure_samples(MODEL_C_GEMINI)}
    recovered = {str(sample.id): sample for sample in repeated_pressure_samples(MODEL_C_GEMINI)}

    assert original[sample_id].metadata["sequence_seed"] == recovered[sample_id].metadata[
        "sequence_seed"
    ]
    assert original[sample_id].metadata["sequence_seed"] == deterministic_sequence_seed(
        "model_c_gemini",
        "medium",
        13,
    )

