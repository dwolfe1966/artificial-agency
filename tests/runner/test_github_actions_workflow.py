from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from artificial_agency.runner.github_actions import RUNNER_LABELS, runner_command
from artificial_agency.runner.supervisor import status_report
from artificial_agency.runner.state import atomic_write_json
from tests.runner.test_runner_infrastructure import make_spec
from artificial_agency.runner import supervisor


WORKFLOW = Path(".github/workflows/experiment-runner.yml")


def load_workflow() -> dict:
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def test_production_workflow_targets_only_self_hosted_macos_label() -> None:
    workflow = load_workflow()
    runs_on = workflow["jobs"]["dispatch"]["runs-on"]

    assert runs_on == list(RUNNER_LABELS)
    assert "ubuntu-latest" not in str(workflow)
    assert "macos-latest" not in str(workflow)


def test_raw_logs_are_never_uploaded_as_artifacts() -> None:
    workflow_text = WORKFLOW.read_text(encoding="utf-8")

    assert "actions/upload-artifact" not in workflow_text
    assert "run-002A/inspect" not in workflow_text
    assert "raw Inspect logs" not in workflow_text


def test_workflow_inputs_map_to_runner_commands() -> None:
    assert runner_command("start", "002A") == [
        ".venv/bin/python",
        "-m",
        "artificial_agency.runner",
        "start",
        "002A",
    ]
    assert runner_command("preflight", "002A")[-2:] == ["preflight", "002A"]
    assert runner_command("status", "002A")[-2:] == ["status", "002A"]
    assert runner_command("health", "002A")[-2:] == ["health", "002A"]
    assert runner_command("stop", "002A")[-2:] == ["stop", "002A"]
    assert runner_command("resume", "002A")[-2:] == ["resume", "002A"]
    assert runner_command("finalize", "002A")[-2:] == ["finalize", "002A"]
    assert runner_command("start", "003A") == [
        ".venv/bin/python",
        "-m",
        "artificial_agency.runner",
        "start",
        "003A",
    ]
    assert runner_command("status", "003A")[-2:] == ["status", "003A"]
    assert runner_command("health", "003A")[-2:] == ["health", "003A"]
    assert runner_command("stop", "003A")[-2:] == ["stop", "003A"]
    assert runner_command("resume", "003A")[-2:] == ["resume", "003A"]
    assert runner_command("finalize", "003A")[-2:] == ["finalize", "003A"]
    assert runner_command("start", "003B")[-2:] == ["start", "003B"]
    assert runner_command("status", "003B")[-2:] == ["status", "003B"]
    assert runner_command("health", "003B")[-2:] == ["health", "003B"]
    assert runner_command("stop", "003B")[-2:] == ["stop", "003B"]
    assert runner_command("resume", "003B")[-2:] == ["resume", "003B"]
    assert runner_command("finalize", "003B")[-2:] == ["finalize", "003B"]
    assert runner_command("start", "004A")[-2:] == ["start", "004A"]
    assert runner_command("status", "004A")[-2:] == ["status", "004A"]
    assert runner_command("health", "004A")[-2:] == ["health", "004A"]
    assert runner_command("stop", "004A")[-2:] == ["stop", "004A"]
    assert runner_command("resume", "004A")[-2:] == ["resume", "004A"]
    assert runner_command("finalize", "004A")[-2:] == ["finalize", "004A"]
    assert runner_command("start", "004B")[-2:] == ["start", "004B"]
    assert runner_command("status", "004B")[-2:] == ["status", "004B"]
    assert runner_command("health", "004B")[-2:] == ["health", "004B"]
    assert runner_command("stop", "004B")[-2:] == ["stop", "004B"]
    assert runner_command("resume", "004B")[-2:] == ["resume", "004B"]
    assert runner_command("finalize", "004B")[-2:] == ["finalize", "004B"]
    assert runner_command("start", "005B")[-2:] == ["start", "005B"]
    assert runner_command("preflight", "005B")[-2:] == ["preflight", "005B"]
    assert runner_command("status", "005B")[-2:] == ["status", "005B"]
    assert runner_command("health", "005B")[-2:] == ["health", "005B"]
    assert runner_command("stop", "005B")[-2:] == ["stop", "005B"]
    assert runner_command("resume", "005B")[-2:] == ["resume", "005B"]
    assert runner_command("finalize", "005B")[-2:] == ["finalize", "005B"]
    assert runner_command("start", "005C")[-2:] == ["start", "005C"]
    assert runner_command("preflight", "005C")[-2:] == ["preflight", "005C"]
    assert runner_command("status", "005C")[-2:] == ["status", "005C"]
    assert runner_command("health", "005C")[-2:] == ["health", "005C"]
    assert runner_command("stop", "005C")[-2:] == ["stop", "005C"]
    assert runner_command("resume", "005C")[-2:] == ["resume", "005C"]
    assert runner_command("finalize", "005C")[-2:] == ["finalize", "005C"]
    assert runner_command("start", "006A-GPT")[-2:] == ["start", "006A-GPT"]
    assert runner_command("preflight", "006A-GPT")[-2:] == ["preflight", "006A-GPT"]
    assert runner_command("status", "006A-GPT")[-2:] == ["status", "006A-GPT"]
    assert runner_command("health", "006A-GPT")[-2:] == ["health", "006A-GPT"]
    assert runner_command("stop", "006A-GPT")[-2:] == ["stop", "006A-GPT"]
    assert runner_command("resume", "006A-GPT")[-2:] == ["resume", "006A-GPT"]
    assert runner_command("finalize", "006A-GPT")[-2:] == ["finalize", "006A-GPT"]
    assert runner_command("start", "006B-CLAUDE")[-2:] == ["start", "006B-CLAUDE"]
    assert runner_command("preflight", "006B-CLAUDE")[-2:] == [
        "preflight",
        "006B-CLAUDE",
    ]
    assert runner_command("status", "006B-CLAUDE")[-2:] == [
        "status",
        "006B-CLAUDE",
    ]
    assert runner_command("health", "006B-CLAUDE")[-2:] == [
        "health",
        "006B-CLAUDE",
    ]
    assert runner_command("stop", "006B-CLAUDE")[-2:] == [
        "stop",
        "006B-CLAUDE",
    ]
    assert runner_command("resume", "006B-CLAUDE")[-2:] == [
        "resume",
        "006B-CLAUDE",
    ]
    assert runner_command("finalize", "006B-CLAUDE")[-2:] == [
        "finalize",
        "006B-CLAUDE",
    ]
    assert runner_command("start", "006C-GEMINI")[-2:] == ["start", "006C-GEMINI"]
    assert runner_command("preflight", "006C-GEMINI")[-2:] == [
        "preflight",
        "006C-GEMINI",
    ]
    assert runner_command("status", "006C-GEMINI")[-2:] == [
        "status",
        "006C-GEMINI",
    ]
    assert runner_command("health", "006C-GEMINI")[-2:] == [
        "health",
        "006C-GEMINI",
    ]
    assert runner_command("stop", "006C-GEMINI")[-2:] == [
        "stop",
        "006C-GEMINI",
    ]
    assert runner_command("resume", "006C-GEMINI")[-2:] == [
        "resume",
        "006C-GEMINI",
    ]
    assert runner_command("finalize", "006C-GEMINI")[-2:] == [
        "finalize",
        "006C-GEMINI",
    ]


def test_invalid_actions_and_run_ids_fail_safely() -> None:
    with pytest.raises(ValueError, match="Unsupported action"):
        runner_command("delete", "002A")
    with pytest.raises(ValueError, match="Unsupported run_id"):
        runner_command("start", "001")


def test_workflow_declares_only_supported_dispatch_inputs() -> None:
    workflow = load_workflow()
    dispatch = workflow[True]["workflow_dispatch"]["inputs"]

    assert dispatch["run_id"]["options"] == [
        "002A",
        "003A",
        "003B",
        "004A",
        "004B",
        "005B",
        "005C",
        "006A-GPT",
        "006B-CLAUDE",
        "006C-GEMINI",
        "PERSISTENCE_DIAGNOSTIC",
    ]
    assert dispatch["action"]["options"] == [
        "start",
        "preflight",
        "status",
        "health",
        "stop",
        "resume",
        "finalize",
    ]


def test_secret_values_are_never_printed_by_generated_commands() -> None:
    workflow_text = WORKFLOW.read_text(encoding="utf-8")

    assert "echo $OPENAI_API_KEY" not in workflow_text
    assert "printenv OPENAI_API_KEY" not in workflow_text
    assert "OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}" in workflow_text
    assert "ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}" in workflow_text
    assert "GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}" in workflow_text
    assert 'test -n "${OPENAI_API_KEY:-}"' in workflow_text
    assert 'test -n "${ANTHROPIC_API_KEY:-}"' in workflow_text
    assert 'test -n "${GOOGLE_API_KEY:-}"' in workflow_text
    assert (
        'if [[ "${{ inputs.run_id }}" == "002A" || "${{ inputs.run_id }}" == "003A" || "${{ inputs.run_id }}" == "003B" || "${{ inputs.run_id }}" == "004A" || "${{ inputs.run_id }}" == "004B" || "${{ inputs.run_id }}" == "006A-GPT" ]]; then'
        in workflow_text
    )
    assert 'launchctl setenv OPENAI_API_KEY "${OPENAI_API_KEY}"' in workflow_text


def test_workflow_preserves_runner_runtime_files_between_dispatches() -> None:
    workflow = load_workflow()
    checkout = workflow["jobs"]["dispatch"]["steps"][0]

    assert checkout["with"]["clean"] is False


def test_workflow_status_health_remain_outcome_blind(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = make_spec(tmp_path)
    monkeypatch.setattr(supervisor, "known_runs", lambda: {"002A": spec})
    atomic_write_json(
        spec.status_path,
        {
            "state": "RUNNING",
            "completed": 12,
            "total": 90,
            "score": "must not appear",
            "policy_violation": "must not appear",
            "tool_calls": "must not appear",
            "trajectory": "must not appear",
        },
    )

    report = status_report("002A")

    assert "Completed: 12 / 90" in report
    assert "score" not in report
    assert "policy_violation" not in report
    assert "tool_calls" not in report
    assert "trajectory" not in report


def test_scientific_experiment_002_files_remain_unchanged() -> None:
    import subprocess

    result = subprocess.run(
        [
            "git",
            "diff",
            "--quiet",
            "6301fc0b78ded0200fd6203d4888ac2b3c33cae7..HEAD",
            "--",
            "artificial_agency/experiments/exp002",
            "experiments/002-fixed-conflict-pressure",
            "tests/experiments/exp002",
            "pyproject.toml",
        ],
        check=False,
    )

    assert result.returncode == 0


def test_runner_registers_003a_with_frozen_stage1_sample_counts() -> None:
    from artificial_agency.runner.config import known_runs

    spec = known_runs()["003A"]

    assert spec.frozen_commit == "f8294ab172cb556f8a4c1ec4f726947672cc859a"
    assert spec.task.endswith("inspect_task.py@exp003_constraint_status_stage1")
    assert spec.model == "openai/gpt-5.6-sol"
    assert spec.total_samples == 120
    assert spec.condition_counts == {
        "categorical-ordinary": 20,
        "categorical-high": 20,
        "procedural-ordinary": 20,
        "procedural-high": 20,
        "purpose-conflict-ordinary": 20,
        "purpose-conflict-high": 20,
    }
    assert "--checkpoint" in spec.inspect_args
    assert "turn:1" in spec.inspect_args


def test_runner_registers_004a_with_frozen_stage1_sample_counts() -> None:
    from artificial_agency.runner.config import known_runs

    spec = known_runs()["004A"]

    assert spec.frozen_commit == "aa126f9254a01c96e85545a9e1a77d10195f2604"
    assert spec.task.endswith("inspect_task.py@exp004_constraint_meaning_stage1")
    assert spec.model == "openai/gpt-5.6-sol"
    assert spec.total_samples == 120
    assert spec.condition_counts == {
        "categorical-ordinary": 20,
        "categorical-high": 20,
        "procedural-ordinary": 20,
        "procedural-high": 20,
        "explicit-purpose-conflict-ordinary": 20,
        "explicit-purpose-conflict-high": 20,
    }
    assert "--checkpoint" in spec.inspect_args
    assert "turn:1" in spec.inspect_args


def test_runner_registers_004b_with_frozen_stage2_sample_counts() -> None:
    from artificial_agency.runner.config import known_runs

    spec = known_runs()["004B"]

    assert spec.frozen_commit == "aa126f9254a01c96e85545a9e1a77d10195f2604"
    assert spec.task.endswith("exp004_stage2_task.py@exp004_constraint_meaning_stage2")
    assert spec.model == "openai/gpt-5.6-sol"
    assert spec.total_samples == 180
    assert spec.condition_counts == {
        "categorical-ordinary": 30,
        "categorical-high": 30,
        "procedural-ordinary": 30,
        "procedural-high": 30,
        "explicit-purpose-conflict-ordinary": 30,
        "explicit-purpose-conflict-high": 30,
    }
    assert "--checkpoint" in spec.inspect_args
    assert "turn:1" in spec.inspect_args


def test_workflow_allows_registered_exp005_and_exp006_cross_model_runs() -> None:
    workflow_text = WORKFLOW.read_text(encoding="utf-8")

    assert '- "005B"' in workflow_text
    assert '- "005C"' in workflow_text
    assert '- "006A-GPT"' in workflow_text
    assert '- "006B-CLAUDE"' in workflow_text
    assert '- "006C-GEMINI"' in workflow_text
    assert (
        "002A|003A|003B|004A|004B|005B|005C|006A-GPT|006B-CLAUDE|006C-GEMINI|PERSISTENCE_DIAGNOSTIC"
        in workflow_text
    )
    assert "ANTHROPIC_API_KEY" in workflow_text
    assert "GOOGLE_API_KEY" in workflow_text
    assert 'inputs.run_id }}" == "006B-CLAUDE"' in workflow_text
    assert 'inputs.run_id }}" == "006C-GEMINI"' in workflow_text


def test_runner_registers_005_cross_model_runs() -> None:
    from artificial_agency.runner.config import known_runs

    runs = known_runs()
    assert runs["005B"].model == "anthropic/claude-sonnet-5"
    assert runs["005C"].model == "google/gemini-3.7-flash"
    assert runs["005B"].total_samples == 300
    assert runs["005C"].total_samples == 300


def test_runner_registers_006_action_representation_runs() -> None:
    from artificial_agency.runner.config import known_runs

    runs = known_runs()
    expected_counts = {
        "categorical-ordinary": 30,
        "categorical-high": 30,
        "procedural-ordinary": 30,
        "procedural-high": 30,
        "explicit-purpose-conflict-ordinary": 30,
        "explicit-purpose-conflict-high": 30,
    }

    assert runs["006A-GPT"].model == "openai/gpt-5.6-sol"
    assert runs["006B-CLAUDE"].model == "anthropic/claude-sonnet-5"
    assert runs["006C-GEMINI"].model == "google/gemini-3.7-flash"
    for run_id in ("006A-GPT", "006B-CLAUDE", "006C-GEMINI"):
        spec = runs[run_id]
        assert spec.frozen_commit == "dac39e4d898c652f5b31c9dc80218ab4c9d9fccb"
        assert spec.experiment_id == "006-action-representational-compliance"
        assert spec.total_samples == 180
        assert spec.condition_counts == expected_counts
        assert "--checkpoint" in spec.inspect_args
        assert "turn:1" in spec.inspect_args
