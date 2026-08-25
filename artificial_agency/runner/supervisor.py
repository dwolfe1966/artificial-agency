from __future__ import annotations

import hashlib
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from .config import RUN_REGISTRY, RunSpec, known_runs, repository_root, runtime_home
from .inspect_ops import (
    count_completed_samples,
    latest_json_log,
    raw_log_bytes,
    safe_log_summary,
    samplebuffer_counts,
    token_usage,
)
from .preflight import ProbeError, full_preflight, runner_environment
from .state import (
    append_log,
    atomic_write_json,
    initial_status,
    process_alive,
    read_json,
    update_status,
    utc_now,
)


def acquire_lock(spec: RunSpec) -> tuple[bool, dict[str, Any]]:
    spec.lock_path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_json(spec.lock_path, {})
    pid = int(existing.get("supervisor_pid", 0) or 0)
    if pid and process_alive(pid):
        return False, existing
    if existing:
        existing["stale_detected_at"] = utc_now()
        existing["stale"] = True
    lock = {
        "run_id": spec.run_id,
        "state": "LOCKED",
        "supervisor_pid": os.getpid(),
        "created_at": utc_now(),
        "previous_lock": existing or None,
    }
    atomic_write_json(spec.lock_path, lock)
    return True, lock


def write_registry(spec: RunSpec, updates: dict[str, Any]) -> None:
    registry_path = repository_root() / RUN_REGISTRY
    registry = read_json(registry_path, {})
    runs = registry.setdefault("runs", {})
    current = runs.setdefault(spec.run_id, {})
    current.update(updates)
    current.update(
        {
            "run_id": spec.run_id,
            "experiment_id": spec.experiment_id,
            "frozen_commit": spec.frozen_commit,
            "status_path": str(spec.status_path),
            "raw_log_dir": str(spec.log_dir),
            "updated_at": utc_now(),
        }
    )
    atomic_write_json(registry_path, registry)


def build_inspect_command(spec: RunSpec) -> list[str]:
    return [
        sys.executable,
        "-m",
        "inspect_ai",
        "eval",
        spec.task,
        *spec.inspect_args,
        "--log-dir",
        str(spec.log_dir),
    ]


def launch_detached(run_id: str, *, mock: bool = False) -> dict[str, Any]:
    spec = known_runs()[run_id]
    locked, lock = acquire_lock(spec)
    if not locked:
        return {
            "already_active": True,
            "lock": lock,
            "status": read_json(spec.status_path, {}),
        }

    status = initial_status(spec.run_id, spec.frozen_commit, spec.total_samples)
    status.update({"state": "STARTING", "supervisor_pid": None, "mock": mock})
    atomic_write_json(spec.status_path, status)
    append_log(spec.operational_log, "runner start requested")

    spec.stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stdout = spec.stdout_path.open("ab")
    command = [
        sys.executable,
        "-m",
        "artificial_agency.runner",
        "_supervise",
        run_id,
    ]
    if mock:
        command.append("--mock")
    env = runner_environment(spec)
    process = subprocess.Popen(
        command,
        cwd=repository_root(),
        env=env,
        stdout=stdout,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    lock["supervisor_pid"] = process.pid
    lock["state"] = "RUNNING"
    atomic_write_json(spec.lock_path, lock)
    spec.pid_path.write_text(f"{process.pid}\n", encoding="utf-8")
    update_status(spec.status_path, state="STARTING", supervisor_pid=process.pid)
    write_registry(
        spec,
        {
            "state": "STARTING",
            "supervisor_pid": process.pid,
            "start_time": utc_now(),
        },
    )
    return {"started": True, "supervisor_pid": process.pid, "status": status}


def supervise(run_id: str, *, mock: bool = False) -> int:
    spec = known_runs()[run_id]
    start = time.time()
    update_status(
        spec.status_path,
        state="PREFLIGHT",
        supervisor_pid=os.getpid(),
        previous_attempts=spec.previous_attempts,
    )
    append_log(spec.operational_log, "supervisor process started")

    try:
        if mock:
            env = runner_environment(spec)
            append_log(spec.operational_log, "mock preflight passed")
        else:
            env = full_preflight(spec)
        update_status(spec.status_path, state="RUNNING", api_health="OK")
        append_log(spec.operational_log, "production run started")
        command = build_inspect_command(spec)
        with spec.stdout_path.open("ab") as output:
            child = subprocess.Popen(
                command if not mock else [sys.executable, "-c", "import time; time.sleep(0.2)"],
                cwd=repository_root(),
                env=env,
                stdout=output,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
            update_status(spec.status_path, inspect_pid=child.pid)
            write_registry(spec, {"state": "RUNNING", "inspect_pid": child.pid})
            while child.poll() is None:
                refresh_operational_status(spec, start)
                time.sleep(10 if not mock else 0.05)
            return_code = child.returncode

        refresh_operational_status(spec, start)
        final_state = "COMPLETED" if return_code == 0 else "FAILED"
        update_status(
            spec.status_path,
            state=final_state,
            exit_code=return_code,
            elapsed_seconds=int(time.time() - start),
            ended_at=utc_now(),
        )
        append_log(spec.operational_log, f"production run ended state={final_state} exit_code={return_code}")
        write_registry(spec, {"state": final_state, "exit_code": return_code})
        return return_code
    except ProbeError as exc:
        update_status(
            spec.status_path,
            state="FAILED",
            api_health="FAILED",
            failure_class=exc.__class__.__name__,
            failure_reason=str(exc),
            elapsed_seconds=int(time.time() - start),
            ended_at=utc_now(),
        )
        append_log(spec.operational_log, f"preflight failed: {exc}")
        write_registry(spec, {"state": "FAILED", "failure_reason": str(exc)})
        return 2
    finally:
        lock = read_json(spec.lock_path, {})
        lock["released_at"] = utc_now()
        lock["state"] = read_json(spec.status_path, {}).get("state", "UNKNOWN")
        atomic_write_json(spec.lock_path, lock)


def refresh_operational_status(spec: RunSpec, start: float | None = None) -> dict[str, Any]:
    runtime = runtime_home(repository_root(), spec.run_id)
    completed = count_completed_samples(spec.log_dir)
    buffered = samplebuffer_counts(runtime)
    raw = safe_log_summary(spec.log_dir)
    usage = token_usage(spec.log_dir)
    updates: dict[str, Any] = {
        "completed": completed,
        "total": spec.total_samples,
        "elapsed_seconds": int(time.time() - start) if start else None,
        "last_progress_at": utc_now() if completed else read_json(spec.status_path, {}).get("last_progress_at"),
        **raw,
        **buffered,
    }
    if usage is not None:
        updates["token_usage"] = usage
    return update_status(spec.status_path, **{k: v for k, v in updates.items() if v is not None})


def status_report(run_id: str) -> str:
    spec = known_runs()[run_id]
    status = read_json(spec.status_path, {})
    if not status:
        return f"RUN {run_id}\nStatus: NOT_STARTED"
    pid = int(status.get("supervisor_pid", 0) or 0)
    alive = process_alive(pid) if pid else False
    raw_bytes = status.get("raw_log_bytes", raw_log_bytes(spec.log_dir))
    lines = [
        f"RUN {run_id}",
        f"Status: {status.get('state', 'UNKNOWN')}",
        f"Completed: {status.get('completed', 0)} / {status.get('total', spec.total_samples)}",
        f"Supervisor PID: {pid if pid else 'n/a'} ({'alive' if alive else 'not active'})",
        f"Inspect PID: {status.get('inspect_pid', 'n/a')}",
        f"Technical failures: {status.get('technical_failures', 0)}",
        f"Elapsed: {status.get('elapsed_seconds', 0)}s",
        f"API health: {status.get('api_health', 'UNKNOWN')}",
        f"Raw log bytes: {raw_bytes}",
        f"Tokens: {status.get('token_usage', 'n/a')}",
        f"Frozen SHA: {status.get('frozen_commit', spec.frozen_commit)}",
    ]
    return "\n".join(lines)


def health_report(run_id: str) -> str:
    spec = known_runs()[run_id]
    status = read_json(spec.status_path, {})
    lock = read_json(spec.lock_path, {})
    pid = int(status.get("supervisor_pid", lock.get("supervisor_pid", 0)) or 0)
    alive = process_alive(pid) if pid else False
    state = status.get("state", "NOT_STARTED")
    if state == "COMPLETED":
        classification = "completed"
    elif alive and state in {"RUNNING", "PREFLIGHT", "STARTING"}:
        classification = "healthy"
    elif lock and not alive and state not in {"COMPLETED", "FAILED", "STOPPED"}:
        classification = "stale lock"
    elif state == "FAILED":
        classification = "process exited"
    else:
        classification = "not started"
    raw = safe_log_summary(spec.log_dir)
    return "\n".join(
        [
            f"RUN {run_id} health: {classification}",
            f"State: {state}",
            f"Supervisor alive: {alive}",
            f"Raw log bytes: {raw['raw_log_bytes']}",
            f"Status path: {spec.status_path}",
        ]
    )


def stop_run(run_id: str) -> str:
    spec = known_runs()[run_id]
    status = read_json(spec.status_path, {})
    pid = int(status.get("supervisor_pid", 0) or 0)
    if not pid or not process_alive(pid):
        update_status(spec.status_path, state="STOPPED", stop_reason="no active supervisor")
        append_log(spec.operational_log, "stop requested; no active supervisor")
        return f"RUN {run_id}: no active supervisor"
    try:
        os.killpg(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    update_status(spec.status_path, state="STOPPING", stop_requested_at=utc_now())
    append_log(spec.operational_log, f"stop requested for process group {pid}")
    return f"RUN {run_id}: stop requested for PID {pid}"


def resume_run(run_id: str, *, mock: bool = False) -> dict[str, Any]:
    spec = known_runs()[run_id]
    status = read_json(spec.status_path, {})
    completed = int(status.get("completed", 0) or 0)
    update_status(
        spec.status_path,
        state="RESUME_REQUESTED",
        resume_uses="inspect eval retry/checkpoint when raw log is resumable",
        completed_before_resume=completed,
    )
    append_log(spec.operational_log, f"resume requested completed={completed}")
    return launch_detached(run_id, mock=mock)


def finalize_run(run_id: str) -> dict[str, Any]:
    spec = known_runs()[run_id]
    status = refresh_operational_status(spec)
    pid = int(status.get("supervisor_pid", 0) or 0)
    if pid and process_alive(pid):
        raise RuntimeError("cannot finalize while supervisor is active")
    log = latest_json_log(spec.log_dir)
    checksum = None
    size = 0
    if log is not None:
        size = log.stat().st_size
        checksum = hashlib.sha256(log.read_bytes()).hexdigest()
    finalized = update_status(
        spec.status_path,
        finalized_at=utc_now(),
        raw_log_path=str(log) if log else None,
        raw_log_bytes=size,
        raw_log_sha256=checksum,
    )
    append_log(spec.operational_log, "finalization completed")
    write_registry(
        spec,
        {
            "state": finalized.get("state", "UNKNOWN"),
            "raw_log_path": finalized.get("raw_log_path"),
            "raw_log_sha256": checksum,
        },
    )
    return finalized

