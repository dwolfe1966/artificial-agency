from __future__ import annotations

from artificial_agency.runner.config import known_runs
from artificial_agency.runner.recovery import expected_sample_ids


def test_runner_registers_exp008b_runs_without_exp008_collision() -> None:
    runs = known_runs()
    expected = {
        "008B-A-GPT": "openai/gpt-5.6-sol",
        "008B-B-CLAUDE": "anthropic/claude-sonnet-5",
        "008B-C-GEMINI": "google/gemini-3.7-flash",
    }
    for run_id, model in expected.items():
        assert run_id in runs
        assert runs[run_id].experiment_id == "008b-evaluation-awareness"
        assert runs[run_id].model == model
        assert runs[run_id].frozen_commit == "d9cfe9603b3de9591e015c72506bdab38d07b4db"
        assert "artificial_agency/experiments/exp008b" in runs[run_id].scientific_paths
        assert "experiments/008b-evaluation-awareness" in runs[run_id].scientific_paths
        assert "artificial_agency/runner/exp008b_recovery_task.py" not in runs[
            run_id
        ].scientific_paths
        assert runs[run_id].total_samples == 120
        assert runs[run_id].condition_counts == {
            "procurement-eval-salient": 30,
            "procurement-naturalistic": 30,
            "data-access-eval-salient": 30,
            "data-access-naturalistic": 30,
        }
    assert runs["008B-CLAUDE"].experiment_id == "008-evaluation-awareness"
    assert runs["008B-B-CLAUDE"].experiment_id == "008b-evaluation-awareness"


def test_exp008b_expected_ids_support_missing_id_recovery() -> None:
    for run_id in ("008B-A-GPT", "008B-B-CLAUDE", "008B-C-GEMINI"):
        ids = expected_sample_ids(known_runs()[run_id])
        assert len(ids) == 120
        assert len(set(ids)) == 120
        assert ids[0].startswith(run_id)
        assert f"{run_id}-data-access-naturalistic-29" in ids
