from __future__ import annotations

from artificial_agency.runner.config import known_runs
from artificial_agency.runner.recovery import expected_sample_ids


EXPECTED_COUNTS = {
    "refund": 30,
    "procurement": 30,
    "data-access": 30,
    "scheduling": 30,
}


def test_runner_registers_exp007_scenario_suite_runs() -> None:
    runs = known_runs()
    expected = {
        "007A-GPT": ("openai/gpt-5.6-sol", "exp007_model_a_gpt56_sol"),
        "007B-CLAUDE": (
            "anthropic/claude-sonnet-5",
            "exp007_model_b_claude_sonnet5",
        ),
        "007C-GEMINI": (
            "google/gemini-3.7-flash",
            "exp007_model_c_gemini37_flash",
        ),
    }

    for run_id, (model, task_name) in expected.items():
        spec = runs[run_id]
        assert spec.experiment_id == "007-scenario-suite-pilot"
        assert spec.model == model
        assert spec.task.endswith(f"inspect_task.py@{task_name}")
        assert spec.frozen_commit == "a59995e7317b2d3bd86f91f0b07d3046c056e3b6"
        assert spec.total_samples == 120
        assert spec.condition_counts == EXPECTED_COUNTS
        assert "--max-connections" in spec.inspect_args
        assert "1" in spec.inspect_args
        assert "--max-retries" in spec.inspect_args
        assert "3" in spec.inspect_args
        assert "--checkpoint" in spec.inspect_args
        assert "turn:1" in spec.inspect_args


def test_exp007_openai_only_documents_openai_reasoning_controls() -> None:
    runs = known_runs()

    assert "--reasoning-effort" in runs["007A-GPT"].inspect_args
    assert "--verbosity" in runs["007A-GPT"].inspect_args
    assert "--reasoning-effort" not in runs["007B-CLAUDE"].inspect_args
    assert "--verbosity" not in runs["007B-CLAUDE"].inspect_args
    assert "--reasoning-effort" not in runs["007C-GEMINI"].inspect_args
    assert "--verbosity" not in runs["007C-GEMINI"].inspect_args


def test_exp007_recovery_expected_ids_cover_each_registered_run() -> None:
    runs = known_runs()

    for run_id in ("007A-GPT", "007B-CLAUDE", "007C-GEMINI"):
        ids = expected_sample_ids(runs[run_id])
        assert len(ids) == 120
        assert len(set(ids)) == 120
        assert ids[0] == f"{run_id}-refund-00"
        assert ids[-1] == f"{run_id}-scheduling-29"


def test_raw_logs_for_exp007_remain_ignored_by_git() -> None:
    import subprocess

    for path in (
        "results/007-scenario-suite-pilot/run-007A-GPT/inspect/test.json",
        "results/007-scenario-suite-pilot/run-007A-GPT/canary/test.json",
        "results/007-scenario-suite-pilot/run-007B-CLAUDE/inspect/test.json",
        "results/007-scenario-suite-pilot/run-007B-CLAUDE/canary/test.json",
        "results/007-scenario-suite-pilot/run-007C-GEMINI/inspect/test.json",
        "results/007-scenario-suite-pilot/run-007C-GEMINI/canary/test.json",
        "results/007-scenario-suite-pilot/run-007B-CLAUDE/RECOVERY_PLAN.json",
        "results/007-scenario-suite-pilot/run-007C-GEMINI/RECOVERY_MISSING_IDS.json",
    ):
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0
