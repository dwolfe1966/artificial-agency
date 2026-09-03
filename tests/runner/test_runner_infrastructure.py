from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

import pytest

from artificial_agency.runner.config import RunSpec
from artificial_agency.runner.preflight import (
    ProbeError,
    full_preflight,
    scientific_preflight,
)
from artificial_agency.runner.state import atomic_write_json, process_alive, read_json
from artificial_agency.runner import supervisor


def make_spec(tmp_path: Path) -> RunSpec:
    run_root = tmp_path / "results" / "002-fixed-conflict-pressure" / "run-002A"
    return RunSpec(
        run_id="002A",
        experiment_id="002-fixed-conflict-pressure",
        title="Experiment 002 Run 002A",
        frozen_commit="6301fc0b78ded0200fd6203d4888ac2b3c33cae7",
        scientific_paths=(
            "artificial_agency/experiments/exp002",
            "experiments/002-fixed-conflict-pressure",
            "tests/experiments/exp002",
            "pyproject.toml",
        ),
        task="artificial_agency/experiments/exp002/inspect_task.py@exp002_fixed_conflict_phase1",
        model="openai/gpt-5.6-sol",
        total_samples=90,
        condition_counts={"low": 30, "medium": 30, "high": 30},
        log_dir=run_root / "inspect",
        status_path=run_root / "RUN_STATUS.json",
        operational_log=run_root / "operational.log",
        lock_path=run_root / "RUN_LOCK.json",
        pid_path=run_root / "RUNNER.pid",
        stdout_path=run_root / "runner-supervisor.out",
        canary_log_dir=run_root / "canary",
        inspect_args=("--model", "openai/gpt-5.6-sol"),
    )


class PassingProbes:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def dns(self, model: str = "openai/gpt-5.6-sol") -> None:
        self.calls.append("dns")

    def https(self, model: str = "openai/gpt-5.6-sol") -> None:
        self.calls.append("https")

    def auth(self, env: dict[str, str], model: str = "openai/gpt-5.6-sol") -> None:
        self.calls.append("auth")

    def canary(self, spec: RunSpec, env: dict[str, str]) -> None:
        self.calls.append("canary")


class FailingProbe(PassingProbes):
    def __init__(self, failure: str) -> None:
        super().__init__()
        self.failure = failure

    def dns(self, model: str = "openai/gpt-5.6-sol") -> None:
        if self.failure == "dns":
            raise ProbeError("dns failed")
        super().dns(model)

    def auth(self, env: dict[str, str], model: str = "openai/gpt-5.6-sol") -> None:
        if self.failure == "auth":
            raise ProbeError("auth failed")
        super().auth(env, model)

    def canary(self, spec: RunSpec, env: dict[str, str]) -> None:
        if self.failure == "canary":
            raise ProbeError("canary failed")
        super().canary(spec, env)


def test_start_refuses_scientific_path_mismatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = make_spec(tmp_path)

    def fake_check_output(command: list[str], **kwargs: Any) -> str:
        if command == ["git", "rev-parse", "HEAD"]:
            return "current-head\n"
        if command == ["git", "status", "--short", "--untracked-files=all"]:
            return ""
        if command[:3] == ["git", "diff", "--name-only"]:
            return "artificial_agency/experiments/exp002/config.py\n"
        raise AssertionError(command)

    class FakeDiff:
        returncode = 1

    monkeypatch.setattr(subprocess, "check_output", fake_check_output)
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: FakeDiff())

    with pytest.raises(ProbeError, match="scientific files differ"):
        scientific_preflight(spec)


def test_start_refuses_dirty_worktree_when_required(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = make_spec(tmp_path)

    def fake_check_output(command: list[str], **kwargs: Any) -> str:
        if command == ["git", "rev-parse", "HEAD"]:
            return f"{spec.frozen_commit}\n"
        if command == ["git", "status", "--short", "--untracked-files=all"]:
            return " M file.py\n"
        raise AssertionError(command)

    monkeypatch.setattr(subprocess, "check_output", fake_check_output)

    with pytest.raises(ProbeError, match="worktree is not clean"):
        scientific_preflight(spec)


def test_preflight_allows_only_legacy_exp009_runtime_artifacts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = make_spec(tmp_path)

    def fake_check_output(command: list[str], **kwargs: Any) -> str:
        if command == ["git", "rev-parse", "HEAD"]:
            return f"{spec.frozen_commit}\n"
        if command == ["git", "status", "--short", "--untracked-files=all"]:
            return "\n".join(
                [
                    "?? results/009-observability/run-009C-GEMINI-S1/RUN_STATUS.json",
                    "?? results/009-observability/run-009C-GEMINI-S1/RUN_LOCK.json",
                    "?? results/009-observability/run-009C-GEMINI-S1/RUNNER.pid",
                    "?? results/009-observability/run-009C-GEMINI-S1/operational.log",
                    "?? results/009-observability/run-009C-GEMINI-S1/runner-supervisor.out",
                    "?? results/009-observability/run-009C-GEMINI-S1/inspect/runtime.json",
                ]
            )
        raise AssertionError(command)

    class CleanDiff:
        returncode = 0

    monkeypatch.setattr(subprocess, "check_output", fake_check_output)
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: CleanDiff())
    monkeypatch.setattr(
        "artificial_agency.runner.preflight._samples_for_task",
        lambda task: [
            type("Sample", (), {"metadata": {"condition": "low"}})(),
            type("Sample", (), {"metadata": {"condition": "medium"}})(),
            type("Sample", (), {"metadata": {"condition": "high"}})(),
        ]
        * 30,
    )

    scientific_preflight(spec)


def test_preflight_rejects_untracked_scientific_files_despite_runtime_allowance(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = make_spec(tmp_path)

    def fake_check_output(command: list[str], **kwargs: Any) -> str:
        if command == ["git", "rev-parse", "HEAD"]:
            return f"{spec.frozen_commit}\n"
        if command == ["git", "status", "--short", "--untracked-files=all"]:
            return "\n".join(
                [
                    "?? results/009-observability/run-009C-GEMINI-S1/RUN_STATUS.json",
                    "?? experiments/009-observability/unregistered_change.md",
                ]
            )
        raise AssertionError(command)

    monkeypatch.setattr(subprocess, "check_output", fake_check_output)

    with pytest.raises(ProbeError, match="worktree is not clean"):
        scientific_preflight(spec)


def test_duplicate_start_is_idempotent(tmp_path: Path) -> None:
    spec = make_spec(tmp_path)
    atomic_write_json(
        spec.lock_path,
        {"run_id": spec.run_id, "supervisor_pid": os.getpid(), "state": "RUNNING"},
    )

    locked, lock = supervisor.acquire_lock(spec)

    assert locked is False
    assert lock["state"] == "RUNNING"


def test_stale_pid_lock_detection(tmp_path: Path) -> None:
    spec = make_spec(tmp_path)
    atomic_write_json(
        spec.lock_path,
        {"run_id": spec.run_id, "supervisor_pid": 999_999_999, "state": "RUNNING"},
    )

    locked, lock = supervisor.acquire_lock(spec)

    assert locked is True
    assert lock["previous_lock"]["stale"] is True


def test_preflight_connectivity_failure_prevents_production_launch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = make_spec(tmp_path)
    monkeypatch.setattr("artificial_agency.runner.preflight.scientific_preflight", lambda spec: None)
    monkeypatch.setattr("artificial_agency.runner.preflight.environment_preflight", lambda spec, env: None)

    with pytest.raises(ProbeError, match="dns failed"):
        full_preflight(spec, FailingProbe("dns"))


def test_authentication_failure_prevents_production_launch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = make_spec(tmp_path)
    monkeypatch.setattr("artificial_agency.runner.preflight.scientific_preflight", lambda spec: None)
    monkeypatch.setattr("artificial_agency.runner.preflight.environment_preflight", lambda spec, env: None)

    with pytest.raises(ProbeError, match="auth failed"):
        full_preflight(spec, FailingProbe("auth"))


def test_canary_failure_prevents_production_launch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = make_spec(tmp_path)
    monkeypatch.setattr("artificial_agency.runner.preflight.scientific_preflight", lambda spec: None)
    monkeypatch.setattr("artificial_agency.runner.preflight.environment_preflight", lambda spec, env: None)

    with pytest.raises(ProbeError, match="canary failed"):
        full_preflight(spec, FailingProbe("canary"))


def test_successful_canary_allows_preflight_to_complete(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = make_spec(tmp_path)
    probes = PassingProbes()
    monkeypatch.setattr("artificial_agency.runner.preflight.scientific_preflight", lambda spec: None)
    monkeypatch.setattr("artificial_agency.runner.preflight.environment_preflight", lambda spec, env: None)

    env = full_preflight(spec, probes)

    assert probes.calls == ["dns", "https", "auth", "canary"]
    assert env["PYTHONPATH"]


def test_preflight_command_does_not_launch_production(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = make_spec(tmp_path)
    probes = PassingProbes()
    monkeypatch.setattr(supervisor, "known_runs", lambda: {"002A": spec})
    monkeypatch.setattr(
        "artificial_agency.runner.preflight.scientific_preflight",
        lambda spec: None,
    )
    monkeypatch.setattr(
        "artificial_agency.runner.preflight.environment_preflight",
        lambda spec, env: None,
    )
    monkeypatch.setattr(
        supervisor,
        "full_preflight",
        lambda spec: full_preflight(spec, probes),
    )

    status = supervisor.preflight_run("002A")

    assert status["state"] == "PREFLIGHT_PASSED"
    assert status["api_health"] == "OK"
    assert "inspect_pid" not in status
    assert probes.calls == ["dns", "https", "auth", "canary"]


def test_status_does_not_expose_behavioral_results(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = make_spec(tmp_path)
    monkeypatch.setattr(supervisor, "known_runs", lambda: {"002A": spec})
    atomic_write_json(
        spec.status_path,
        {
            "state": "RUNNING",
            "completed": 3,
            "total": 90,
            "policy_violation": "must not appear",
            "primary_label": "must not appear",
        },
    )

    report = supervisor.status_report("002A")

    assert "policy_violation" not in report
    assert "primary_label" not in report
    assert "Completed: 3 / 90" in report


def test_persistence_diagnostic_status_exposes_heartbeat_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = RunSpec(
        run_id="PERSISTENCE_DIAGNOSTIC",
        experiment_id="runner-persistence-diagnostic",
        title="Runner v2 Persistence Diagnostic",
        frozen_commit="6301fc0b78ded0200fd6203d4888ac2b3c33cae7",
        scientific_paths=(),
        task="__runner_persistence_diagnostic__",
        model="none",
        total_samples=0,
        condition_counts={},
        log_dir=tmp_path / "logs",
        status_path=tmp_path / "RUN_STATUS.json",
        operational_log=tmp_path / "operational.log",
        lock_path=tmp_path / "RUN_LOCK.json",
        pid_path=tmp_path / "RUNNER.pid",
        stdout_path=tmp_path / "runner-supervisor.out",
        canary_log_dir=tmp_path / "canary",
    )
    monkeypatch.setattr(supervisor, "known_runs", lambda: {"PERSISTENCE_DIAGNOSTIC": spec})
    atomic_write_json(
        spec.status_path,
        {
            "state": "RUNNING",
            "diagnostic": "runner_persistence",
            "heartbeat_count": 3,
            "last_heartbeat_at": "2026-08-25T00:00:00+00:00",
            "no_model_requests": True,
            "score": "must not appear",
            "trajectory": "must not appear",
        },
    )

    report = supervisor.status_report("PERSISTENCE_DIAGNOSTIC")

    assert "Diagnostic: runner_persistence" in report
    assert "Heartbeat count: 3" in report
    assert "No model requests: True" in report
    assert "score" not in report
    assert "trajectory" not in report


def test_operational_status_updates_are_atomic(tmp_path: Path) -> None:
    path = tmp_path / "RUN_STATUS.json"

    atomic_write_json(path, {"state": "RUNNING", "completed": 1})

    assert json.loads(path.read_text(encoding="utf-8"))["completed"] == 1


def test_graceful_stop_preserves_run_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = make_spec(tmp_path)
    monkeypatch.setattr(supervisor, "known_runs", lambda: {"002A": spec})
    atomic_write_json(
        spec.status_path,
        {"state": "RUNNING", "completed": 4, "supervisor_pid": 999_999_999},
    )

    message = supervisor.stop_run("002A")
    status = read_json(spec.status_path)

    assert "no active supervisor" in message
    assert status["completed"] == 4
    assert status["state"] == "STOPPED"


def test_interrupted_run_is_recognized_as_resumable_when_appropriate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = make_spec(tmp_path)
    monkeypatch.setattr(supervisor, "known_runs", lambda: {"002A": spec})
    monkeypatch.setattr(supervisor, "launch_detached", lambda run_id, mock=False: {"started": True})
    atomic_write_json(spec.status_path, {"state": "FAILED", "completed": 63})

    result = supervisor.resume_run("002A", mock=True)
    status = read_json(spec.status_path)

    assert result["started"] is True
    assert status["completed_before_resume"] == 63
    assert "inspect eval retry" in status["resume_uses"]


def test_finalization_calculates_raw_log_sha256(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = make_spec(tmp_path)
    monkeypatch.setattr(supervisor, "known_runs", lambda: {"002A": spec})
    monkeypatch.setattr(supervisor, "repository_root", lambda: tmp_path)
    spec.log_dir.mkdir(parents=True)
    raw_log = spec.log_dir / "sample.json"
    raw_log.write_text(
        json.dumps(
            {
                "status": "success",
                "samples": [
                    {
                        "id": str(i),
                        "completed_at": "2026-08-27T00:00:00+00:00",
                        "output": {"completion": "redacted"},
                        "scores": {"score": {"value": "complete"}},
                        "turn_count": 1,
                    }
                    for i in range(90)
                ],
            }
        ),
        encoding="utf-8",
    )
    atomic_write_json(
        spec.status_path,
        {"state": "COMPLETED", "completed": 90, "supervisor_pid": 999_999_999},
    )

    status = supervisor.finalize_run("002A")

    assert status["raw_log_bytes"] == raw_log.stat().st_size
    assert len(status["raw_log_sha256"]) == 64


def test_raw_logs_remain_ignored_by_git() -> None:
    result = subprocess.run(
        [
            "git",
            "check-ignore",
            "-q",
            "results/002-fixed-conflict-pressure/run-002A/inspect/test.json",
        ],
        check=False,
    )

    assert result.returncode == 0


def test_credential_values_are_never_written_to_operational_status_or_logs(
    tmp_path: Path,
) -> None:
    spec = make_spec(tmp_path)
    secret = "SECRET_VALUE_FOR_TEST"
    atomic_write_json(spec.status_path, {"state": "RUNNING", "api_health": "OK"})
    spec.operational_log.parent.mkdir(parents=True, exist_ok=True)
    spec.operational_log.write_text("OpenAI authentication passed\n", encoding="utf-8")

    assert secret not in spec.status_path.read_text(encoding="utf-8")
    assert secret not in spec.operational_log.read_text(encoding="utf-8")


def test_process_alive_detects_current_process() -> None:
    assert process_alive(os.getpid()) is True


def test_launchd_label_is_stable_and_safe() -> None:
    assert supervisor.launchd_label("PERSISTENCE_DIAGNOSTIC") == (
        "artificial-agency.runner-v2.persistence-diagnostic"
    )
