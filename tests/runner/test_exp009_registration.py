from __future__ import annotations

import json
from pathlib import Path

import pytest

from artificial_agency.experiments.exp009.config import (
    MODEL_C_GEMINI,
    P_DETECT_LEVELS,
    deterministic_seed,
    p_detect_id,
)
from artificial_agency.experiments.exp009.inspect_task import observability_samples
from artificial_agency.runner.config import external_runtime_root
from artificial_agency.runner import supervisor
from artificial_agency.runner.config import known_runs
from artificial_agency.runner.recovery import (
    build_recovery_plan,
    expected_sample_ids,
    write_recovery_plan,
)
from artificial_agency.runner.state import atomic_write_json


EXP009_SCIENTIFIC_SHA = "8c3b3728780df5cbb0c073fce619787ca5415546"


def _patch_009c(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    original = known_runs()["009C-GEMINI-S1"]
    run_root = tmp_path / "results" / "009-observability" / "run-009C-GEMINI-S1"
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


def _write_log(path: Path, status: str, sample_ids: list[str], *, complete_009: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    samples = []
    for sample_id in sample_ids:
        metadata = {
            "operational_constraint_violation": False,
            "primary_label_id": "compliant_terminal_failure",
            "phase_a_done": True,
            "phase_b_done": True,
            "phase_a_frozen": True,
            "stochastic": {
                "rng_version": "sha256-threshold-v1",
                "sample_seed": 1,
                "configured_p_detect": 0.5,
                "p_detect_id": "p050",
            },
            "awareness_capture_status": "captured_valid",
        }
        if not complete_009:
            metadata.pop("awareness_capture_status")
            metadata["phase_b_done"] = False
        samples.append(
            {
                "id": sample_id,
                "completed_at": "2026-09-01T00:00:00+00:00",
                "output": {"completion": "redacted"},
                "scores": {
                    "observability_outcome_scorer": {
                        "value": "compliant_terminal_failure",
                        "metadata": metadata,
                    }
                },
                "turn_count": 1,
            }
        )
    path.write_text(json.dumps({"status": status, "samples": samples}), encoding="utf-8")


def test_runner_registers_exp009_stage1_runs() -> None:
    runs = known_runs()
    expected = {
        "009A-GPT-S1": "openai/gpt-5.6-sol",
        "009B-CLAUDE-S1": "anthropic/claude-sonnet-5",
        "009C-GEMINI-S1": "google/gemini-3.7-flash",
    }
    expected_counts = {
        "procurement-p100": 15,
        "procurement-p050": 15,
        "procurement-p010": 15,
        "procurement-p000": 15,
        "data-access-p100": 15,
        "data-access-p050": 15,
        "data-access-p010": 15,
        "data-access-p000": 15,
    }
    for run_id, model in expected.items():
        spec = runs[run_id]
        assert spec.experiment_id == "009-observability"
        assert spec.model == model
        assert spec.frozen_commit == EXP009_SCIENTIFIC_SHA
        assert spec.total_samples == 120
        assert spec.condition_counts == expected_counts
        assert "artificial_agency/experiments/exp009" in spec.scientific_paths
        assert "experiments/009-observability" in spec.scientific_paths
        assert "scripts/analyze_exp009_final.py" in spec.scientific_paths
        joined_args = ",".join(spec.inspect_args)
        assert f"run_id=run-{run_id}" in joined_args
        assert "observability_detection_probability_stage1" in joined_args
        assert "git_commit=" + EXP009_SCIENTIFIC_SHA in joined_args
        assert str(spec.log_dir).endswith(f"run-{run_id}/inspect")
        assert "results/009-observability" not in str(spec.log_dir)


def test_exp009_live_runtime_roots_are_external_and_isolated(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime_root = tmp_path / "external-runtime"
    repo_root = tmp_path / "repo"
    monkeypatch.setenv("ARTIFICIAL_AGENCY_RUNTIME_ROOT", str(runtime_root))

    runs = known_runs(repo_root)
    specs = [runs["009A-GPT-S1"], runs["009B-CLAUDE-S1"], runs["009C-GEMINI-S1"]]

    assert external_runtime_root(repo_root) == runtime_root
    assert len({spec.status_path.parent for spec in specs}) == 3
    for spec in specs:
        assert runtime_root in spec.status_path.parents
        assert repo_root not in spec.status_path.parents

    specs[2].status_path.parent.mkdir(parents=True)
    specs[2].status_path.write_text('{"state": "RUNNING"}', encoding="utf-8")

    assert not specs[0].status_path.exists()
    assert not specs[1].status_path.exists()
    assert specs[2].status_path.exists()


def test_exp009_stage1_expected_ids_support_missing_id_recovery() -> None:
    for run_id in ("009A-GPT-S1", "009B-CLAUDE-S1", "009C-GEMINI-S1"):
        ids = expected_sample_ids(known_runs()[run_id])
        assert len(ids) == 120
        assert len(set(ids)) == 120
        assert ids[0].startswith(run_id)
        assert f"{run_id}-data-access-p000-14" in ids


def test_exp009_recovery_command_uses_runner_level_missing_id_task() -> None:
    spec = known_runs()["009C-GEMINI-S1"]
    command = supervisor.build_inspect_command(spec, recovery=True)
    joined = " ".join(command)

    assert "exp009_recovery_task.py@exp009_model_c_gemini37_flash_stage1_recovery_missing" in joined


def test_exp009_recovery_preserves_original_sample_seed() -> None:
    sample_id = "009C-GEMINI-S1-data-access-p010-07"
    original = {str(sample.id): sample for sample in observability_samples(MODEL_C_GEMINI)}
    recovered = {str(sample.id): sample for sample in observability_samples(MODEL_C_GEMINI)}

    assert original[sample_id].metadata["sample_seed"] == recovered[sample_id].metadata[
        "sample_seed"
    ]
    assert original[sample_id].metadata["sample_seed"] == deterministic_seed(
        "model_c_gemini",
        "data-access",
        0.1,
        7,
    )
    assert original[sample_id].metadata["p_detect_id"] == p_detect_id(0.1)


def test_exp009_recovery_plan_selects_only_missing_expected_ids(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    spec = _patch_009c(tmp_path, monkeypatch)
    expected = list(expected_sample_ids(spec))
    _write_log(spec.log_dir / "partial.json", "error", expected[:32])

    plan = build_recovery_plan(spec)
    write_recovery_plan(spec, plan)
    payload = json.loads(
        (spec.status_path.parent / "RECOVERY_MISSING_IDS.json").read_text(
            encoding="utf-8"
        )
    )

    assert plan.source_completed_count == 32
    assert plan.missing_count == 88
    assert set(plan.missing_ids).isdisjoint(expected[:32])
    assert payload["missing_ids"] == expected[32:42]
    assert payload["batch_size"] == 10


def test_exp009_finalize_accepts_complete_lifecycle_and_stochastic_metadata(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    spec = _patch_009c(tmp_path, monkeypatch)
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


def test_exp009_finalize_refuses_missing_awareness_or_stochastic_metadata(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    spec = _patch_009c(tmp_path, monkeypatch)
    expected = list(expected_sample_ids(spec))
    _write_log(spec.log_dir / "incomplete-lifecycle.json", "success", expected, complete_009=False)
    atomic_write_json(
        spec.status_path,
        {
            "state": "COMPLETED",
            "completed": spec.total_samples,
            "supervisor_pid": None,
        },
    )

    with pytest.raises(RuntimeError, match="complete lifecycle"):
        supervisor.finalize_run(spec.run_id)


def test_exp009_p_detect_levels_are_registered_in_frozen_order() -> None:
    assert P_DETECT_LEVELS == (1.0, 0.5, 0.1, 0.0)
