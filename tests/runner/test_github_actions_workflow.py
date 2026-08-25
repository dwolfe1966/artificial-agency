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
    assert runner_command("status", "002A")[-2:] == ["status", "002A"]
    assert runner_command("health", "002A")[-2:] == ["health", "002A"]
    assert runner_command("stop", "002A")[-2:] == ["stop", "002A"]
    assert runner_command("resume", "002A")[-2:] == ["resume", "002A"]
    assert runner_command("finalize", "002A")[-2:] == ["finalize", "002A"]


def test_invalid_actions_and_run_ids_fail_safely() -> None:
    with pytest.raises(ValueError, match="Unsupported action"):
        runner_command("delete", "002A")
    with pytest.raises(ValueError, match="Unsupported run_id"):
        runner_command("start", "001")


def test_workflow_declares_only_supported_dispatch_inputs() -> None:
    workflow = load_workflow()
    dispatch = workflow[True]["workflow_dispatch"]["inputs"]

    assert dispatch["run_id"]["options"] == ["002A", "PERSISTENCE_DIAGNOSTIC"]
    assert dispatch["action"]["options"] == [
        "start",
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
    assert 'test -n "${OPENAI_API_KEY:-}"' in workflow_text
    assert 'if [[ "${{ inputs.run_id }}" == "002A" ]]; then' in workflow_text
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
            "artificial_agency/_registry.py",
            "pyproject.toml",
        ],
        check=False,
    )

    assert result.returncode == 0
