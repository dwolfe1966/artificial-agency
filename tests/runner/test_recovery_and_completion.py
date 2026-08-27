from __future__ import annotations

import json
from pathlib import Path

import pytest

from artificial_agency.runner import supervisor
from artificial_agency.runner.config import known_runs
from artificial_agency.runner.inspect_ops import inspect_log_metadata
from artificial_agency.runner.recovery import (
    build_recovery_plan,
    expected_sample_ids,
    reconciled_unique_count,
    write_recovery_plan,
)
from artificial_agency.runner.state import atomic_write_json, read_json


def write_log(path: Path, status: str, sample_ids: list[str], error: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, object] = {
        "status": status,
        "samples": [{"id": sample_id} for sample_id in sample_ids],
    }
    if error:
        payload["error"] = {"message": error}
    path.write_text(json.dumps(payload), encoding="utf-8")


def patch_005b(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    original = known_runs()["005B"]
    run_root = tmp_path / "results" / "005-cross-model-replication" / "run-005B"
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
    monkeypatch.setattr(supervisor, "known_runs", lambda: {"005B": spec})
    monkeypatch.setattr(supervisor, "repository_root", lambda: tmp_path)
    return spec


def test_inspect_error_log_metadata_is_operational_only(tmp_path: Path) -> None:
    log = tmp_path / "error.json"
    write_log(log, "error", ["005B-categorical-ordinary-00"], "credit balance is too low")

    metadata = inspect_log_metadata(log)

    assert metadata.status == "error"
    assert metadata.sample_count == 1
    assert metadata.error_summary == "provider_api_error: credit balance is too low"


def test_partial_successful_process_exit_cannot_be_completed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    spec = patch_005b(tmp_path, monkeypatch)
    ids = list(expected_sample_ids(spec))[:259]
    write_log(spec.log_dir / "partial.json", "error", ids, "credit balance is too low")
    monkeypatch.setattr(supervisor, "full_preflight", lambda spec: {})

    class FakeChild:
        pid = 12345
        returncode = 0

        def __init__(self, *args, **kwargs) -> None:
            pass

        def poll(self):
            return 0

    monkeypatch.setattr(supervisor.subprocess, "Popen", FakeChild)

    supervisor.supervise("005B")
    status = read_json(spec.status_path)

    assert status["state"] == "INCOMPLETE"
    assert status["completed"] == 259
    assert "completed 259/300" in status["failure_reason"]


def test_finalize_refuses_incomplete_logical_run(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    spec = patch_005b(tmp_path, monkeypatch)
    write_log(spec.log_dir / "partial.json", "error", list(expected_sample_ids(spec))[:259])
    atomic_write_json(spec.status_path, {"state": "COMPLETED", "completed": 259})

    with pytest.raises(RuntimeError, match="cannot finalize incomplete run"):
        supervisor.finalize_run("005B")


def test_recovery_plan_uses_largest_original_segment_not_latest_resume(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    spec = patch_005b(tmp_path, monkeypatch)
    expected = list(expected_sample_ids(spec))
    write_log(spec.log_dir / "original.json", "error", expected[:259])
    write_log(spec.log_dir / "invalid-resume.json", "error", expected[10:12])

    plan = build_recovery_plan(spec)

    assert plan.source_log and plan.source_log.endswith("original.json")
    assert plan.source_completed_count == 259
    assert plan.missing_count == 41
    assert plan.missing_ids == tuple(expected[259:])
    assert plan.recoverable is True


def test_recovery_plan_accumulates_completed_ids_across_partial_segments(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = patch_005b(tmp_path, monkeypatch)
    expected = list(expected_sample_ids(spec))
    write_log(spec.log_dir / "original.json", "error", expected[:20])
    write_log(spec.log_dir / "recovery-1.json", "error", expected[20:100])

    plan = build_recovery_plan(spec)

    assert plan.source_completed_count == 100
    assert plan.missing_count == 200
    assert plan.missing_ids == tuple(expected[100:])


def test_duplicate_ids_in_source_segment_block_recovery(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    spec = patch_005b(tmp_path, monkeypatch)
    expected = list(expected_sample_ids(spec))
    write_log(spec.log_dir / "original.json", "error", expected[:258] + [expected[0]])

    plan = build_recovery_plan(spec)

    assert plan.recoverable is False
    assert plan.duplicate_ids == (expected[0],)


def test_recovery_never_selects_completed_ids_for_missing_dataset(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    spec = patch_005b(tmp_path, monkeypatch)
    expected = list(expected_sample_ids(spec))
    write_log(spec.log_dir / "original.json", "error", expected[:259])

    plan = build_recovery_plan(spec)

    assert set(plan.missing_ids).isdisjoint(expected[:259])
    assert len(plan.missing_ids) == 41


def test_reconciled_count_requires_expected_unique_ids(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    spec = patch_005b(tmp_path, monkeypatch)
    expected = list(expected_sample_ids(spec))
    original = spec.log_dir / "original.json"
    recovery = spec.log_dir / "recovery.json"
    write_log(original, "error", expected[:259])
    write_log(recovery, "success", expected[259:])

    assert reconciled_unique_count(spec, [original, recovery]) == 300


def test_resume_writes_recovery_plan_without_resetting_completed_count(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = patch_005b(tmp_path, monkeypatch)
    expected = list(expected_sample_ids(spec))
    write_log(spec.log_dir / "original.json", "error", expected[:259])
    atomic_write_json(spec.status_path, {"state": "INCOMPLETE", "completed": 259})
    monkeypatch.setattr(supervisor, "launch_detached", lambda run_id, mock=False, recovery=False: {"started": True, "recovery": recovery})

    result = supervisor.resume_run("005B")
    status = read_json(spec.status_path)

    assert result == {"started": True, "recovery": True}
    assert status["completed_before_resume"] == 259
    assert status["recovery_source_completed"] == 259
    assert status["recovery_missing"] == 41
    assert read_json(spec.status_path.parent / "RECOVERY_MISSING_IDS.json")["missing_count"] == 41


def test_status_reports_reconciled_count_after_recovery_completion(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    spec = patch_005b(tmp_path, monkeypatch)
    expected = list(expected_sample_ids(spec))
    original = spec.log_dir / "original.json"
    recovery = spec.log_dir / "recovery.json"
    write_log(original, "error", expected[:259])
    write_log(recovery, "success", expected[259:])
    plan = build_recovery_plan(spec)
    write_recovery_plan(spec, plan)
    atomic_write_json(
        spec.status_path,
        {"state": "COMPLETED", "completed": 41, "reconciled_completed": 300},
    )

    report = supervisor.status_report("005B")

    assert "Status: COMPLETED" in report
    assert "Completed: 300 / 300" in report
