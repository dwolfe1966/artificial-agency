from __future__ import annotations

import subprocess

from artificial_agency.runner.config import known_runs
from artificial_agency.runner import supervisor
from artificial_agency.runner.exp008_recovery_task import (
    exp008_model_c_gemini37_flash_recovery_missing,
)
from artificial_agency.runner.recovery import expected_sample_ids
from artificial_agency.runner.state import atomic_write_json


EXPECTED_COUNTS = {
    "procurement-eval-salient": 30,
    "procurement-naturalistic": 30,
    "data-access-eval-salient": 30,
    "data-access-naturalistic": 30,
}


def test_runner_registers_exp008_evaluation_awareness_runs() -> None:
    runs = known_runs()
    expected = {
        "008A-GPT": ("openai/gpt-5.6-sol", "exp008_model_a_gpt56_sol"),
        "008B-CLAUDE": (
            "anthropic/claude-sonnet-5",
            "exp008_model_b_claude_sonnet5",
        ),
        "008C-GEMINI": (
            "google/gemini-3.7-flash",
            "exp008_model_c_gemini37_flash",
        ),
    }

    for run_id, (model, task_name) in expected.items():
        spec = runs[run_id]
        assert spec.experiment_id == "008-evaluation-awareness"
        assert spec.model == model
        assert spec.task.endswith(f"inspect_task.py@{task_name}")
        assert spec.frozen_commit == "02f7098dea80156ae48faee5ee091659f538beee"
        assert spec.total_samples == 120
        assert spec.condition_counts == EXPECTED_COUNTS
        assert "--max-connections" in spec.inspect_args
        assert "1" in spec.inspect_args
        assert "--max-retries" in spec.inspect_args
        assert "3" in spec.inspect_args
        assert "--checkpoint" in spec.inspect_args
        assert "turn:1" in spec.inspect_args


def test_exp008_openai_only_documents_openai_reasoning_controls() -> None:
    runs = known_runs()

    assert "--reasoning-effort" in runs["008A-GPT"].inspect_args
    assert "--verbosity" in runs["008A-GPT"].inspect_args
    assert "--reasoning-effort" not in runs["008B-CLAUDE"].inspect_args
    assert "--verbosity" not in runs["008B-CLAUDE"].inspect_args
    assert "--reasoning-effort" not in runs["008C-GEMINI"].inspect_args
    assert "--verbosity" not in runs["008C-GEMINI"].inspect_args


def test_exp008_recovery_expected_ids_cover_each_registered_run() -> None:
    runs = known_runs()

    for run_id in ("008A-GPT", "008B-CLAUDE", "008C-GEMINI"):
        ids = expected_sample_ids(runs[run_id])
        assert len(ids) == 120
        assert len(set(ids)) == 120
        assert ids[0] == f"{run_id}-procurement-eval-salient-00"
        assert ids[-1] == f"{run_id}-data-access-naturalistic-29"


def test_exp008_recovery_dispatch_uses_exp008_recovery_task() -> None:
    spec = known_runs()["008C-GEMINI"]

    command = supervisor.build_inspect_command(spec, recovery=True)

    joined = " ".join(command)
    assert "artificial_agency/runner/exp008_recovery_task.py" in joined
    assert "exp008_model_c_gemini37_flash_recovery_missing" in joined


def test_exp008_recovery_task_filters_to_missing_ids(tmp_path, monkeypatch) -> None:
    missing_ids = [
        "008C-GEMINI-procurement-eval-salient-02",
        "008C-GEMINI-procurement-naturalistic-00",
        "008C-GEMINI-data-access-naturalistic-29",
    ]
    ids_path = tmp_path / "RECOVERY_MISSING_IDS.json"
    atomic_write_json(
        ids_path,
        {
            "run_id": "008C-GEMINI",
            "source_log": "original.json",
            "missing_count": len(missing_ids),
            "missing_ids": missing_ids,
        },
    )
    monkeypatch.setenv("AA_RUNNER_RECOVERY_IDS_PATH", str(ids_path))

    task_obj = exp008_model_c_gemini37_flash_recovery_missing()

    assert [str(sample.id) for sample in task_obj.dataset] == missing_ids
    assert task_obj.metadata["recovery_missing_count"] == len(missing_ids)
    assert task_obj.metadata["model_id"] == "google/gemini-3.7-flash"


def test_raw_logs_for_exp008_remain_ignored_by_git() -> None:
    for path in (
        "results/008-evaluation-awareness/run-008A-GPT/inspect/test.json",
        "results/008-evaluation-awareness/run-008A-GPT/canary/test.json",
        "results/008-evaluation-awareness/run-008B-CLAUDE/inspect/test.json",
        "results/008-evaluation-awareness/run-008B-CLAUDE/canary/test.json",
        "results/008-evaluation-awareness/run-008C-GEMINI/inspect/test.json",
        "results/008-evaluation-awareness/run-008C-GEMINI/canary/test.json",
        "results/008-evaluation-awareness/run-008B-CLAUDE/RECOVERY_PLAN.json",
        "results/008-evaluation-awareness/run-008C-GEMINI/RECOVERY_MISSING_IDS.json",
    ):
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0
