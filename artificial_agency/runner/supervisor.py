from __future__ import annotations

import hashlib
import os
import plistlib
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from .config import (
    PERSISTENCE_DIAGNOSTIC_TASK,
    RUN_REGISTRY,
    RunSpec,
    known_runs,
    repository_root,
    runtime_home,
)
from .inspect_ops import (
    count_completed_samples,
    inspect_log_metadata,
    inspect_log_success,
    json_logs,
    latest_json_log,
    raw_log_bytes,
    safe_log_summary,
    samplebuffer_counts,
    token_usage,
)
from .preflight import ProbeError, full_preflight, runner_environment
from .recovery import build_recovery_plan, reconciled_unique_count, write_recovery_plan
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


def build_inspect_command(spec: RunSpec, *, recovery: bool = False) -> list[str]:
    task = spec.task
    if recovery:
        if spec.run_id not in {
            "005B",
            "005C",
            "006A-GPT",
            "006B-CLAUDE",
            "006C-GEMINI",
        }:
            raise RuntimeError(f"runner-level recovery is not configured for {spec.run_id}")
        if spec.run_id in {"005B", "005C"}:
            task_name = (
                "exp005_model_b_claude_sonnet5_recovery_missing"
                if spec.run_id == "005B"
                else "exp005_model_c_gemini37_flash_recovery_missing"
            )
            task = f"artificial_agency/runner/exp005_recovery_task.py@{task_name}"
        else:
            task_name = {
                "006A-GPT": "exp006_model_a_gpt56_sol_recovery_missing",
                "006B-CLAUDE": "exp006_model_b_claude_sonnet5_recovery_missing",
                "006C-GEMINI": "exp006_model_c_gemini37_flash_recovery_missing",
            }[spec.run_id]
            task = f"artificial_agency/runner/exp006_recovery_task.py@{task_name}"
    return [
        sys.executable,
        "-m",
        "inspect_ai",
        "eval",
        task,
        *spec.inspect_args,
        "--log-dir",
        str(spec.log_dir),
    ]


def should_use_launchd_handoff() -> bool:
    return sys.platform == "darwin" and os.environ.get("GITHUB_ACTIONS") == "true"


def launchd_label(run_id: str) -> str:
    safe = "".join(ch if ch.isalnum() else "-" for ch in run_id.lower()).strip("-")
    return f"artificial-agency.runner-v2.{safe}"


def launchd_plist_path(label: str) -> Path:
    return Path.home() / "Library" / "LaunchAgents" / f"{label}.plist"


def launchctl_target(label: str) -> str:
    return f"gui/{os.getuid()}/{label}"


def launchctl_domain() -> str:
    return f"gui/{os.getuid()}"


def bootout_launchd(label: str) -> None:
    subprocess.run(
        ["launchctl", "bootout", launchctl_target(label)],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def launch_via_launchd(spec: RunSpec, command: list[str], env: dict[str, str]) -> dict[str, Any]:
    label = launchd_label(spec.run_id)
    plist_path = launchd_plist_path(label)
    plist_path.parent.mkdir(parents=True, exist_ok=True)
    spec.stdout_path.parent.mkdir(parents=True, exist_ok=True)
    launchd_log_dir = Path.home() / "Library" / "Logs" / "artificial-agency-runner-v2"
    launchd_log_dir.mkdir(parents=True, exist_ok=True)

    plist = {
        "Label": label,
        "ProgramArguments": command,
        "WorkingDirectory": str(repository_root()),
        "RunAtLoad": True,
        "EnvironmentVariables": {
            "PYTHONPATH": env["PYTHONPATH"],
            "HOME": env["HOME"],
            "INSPECT_TRACE_FILE": env["INSPECT_TRACE_FILE"],
            "AA_RUNNER_HANDOFF": "launchd",
            "PATH": env.get("PATH", os.environ.get("PATH", "")),
            "PYTHONUNBUFFERED": "1",
        },
        "StandardOutPath": str(spec.stdout_path),
        "StandardErrorPath": str(spec.stdout_path),
    }
    with plist_path.open("wb") as handle:
        plistlib.dump(plist, handle)

    bootout_launchd(label)
    subprocess.run(
        ["launchctl", "bootstrap", launchctl_domain(), str(plist_path)],
        cwd=repository_root(),
        check=True,
    )
    subprocess.run(
        ["launchctl", "kickstart", "-k", launchctl_target(label)],
        cwd=repository_root(),
        check=False,
    )

    pid = 0
    status: dict[str, Any] = {}
    for _ in range(30):
        status = read_json(spec.status_path, {})
        pid = int(status.get("supervisor_pid", 0) or 0)
        if pid and process_alive(pid):
            break
        time.sleep(0.5)
    return {
        "pid": pid,
        "label": label,
        "plist_path": str(plist_path),
        "status": status,
    }


def launch_detached(run_id: str, *, mock: bool = False, recovery: bool = False) -> dict[str, Any]:
    spec = known_runs()[run_id]
    locked, lock = acquire_lock(spec)
    if not locked:
        return {
            "already_active": True,
            "lock": lock,
            "status": read_json(spec.status_path, {}),
        }

    status = initial_status(spec.run_id, spec.frozen_commit, spec.total_samples)
    status.update(
        {
            "state": "STARTING",
            "supervisor_pid": None,
            "mock": mock,
            "recovery": recovery,
        }
    )
    atomic_write_json(spec.status_path, status)
    append_log(spec.operational_log, "runner start requested")

    spec.stdout_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "-m",
        "artificial_agency.runner",
        "_supervise",
        run_id,
    ]
    if mock:
        command.append("--mock")
    if recovery:
        command.append("--recovery")
    env = runner_environment(spec)
    if should_use_launchd_handoff():
        launch = launch_via_launchd(spec, command, env)
        pid = int(launch.get("pid", 0) or 0)
        lock["supervisor_pid"] = pid
        lock["state"] = "RUNNING"
        lock["handoff"] = "launchd"
        lock["launchd_label"] = launch["label"]
        lock["launchd_plist"] = launch["plist_path"]
        atomic_write_json(spec.lock_path, lock)
        if pid:
            spec.pid_path.write_text(f"{pid}\n", encoding="utf-8")
        update_status(
            spec.status_path,
            state="STARTING",
            supervisor_pid=pid or None,
            handoff="launchd",
            launchd_label=launch["label"],
            launchd_plist=launch["plist_path"],
        )
        write_registry(
            spec,
            {
                "state": "STARTING",
                "supervisor_pid": pid or None,
                "start_time": utc_now(),
                "handoff": "launchd",
            },
        )
        return {"started": True, "supervisor_pid": pid, "status": launch["status"], "handoff": "launchd"}

    stdout = spec.stdout_path.open("ab")
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


def preflight_run(run_id: str, *, mock: bool = False) -> dict[str, Any]:
    spec = known_runs()[run_id]
    start = time.time()
    status = initial_status(spec.run_id, spec.frozen_commit, spec.total_samples)
    status.update({"state": "PREFLIGHT", "supervisor_pid": None, "mock": mock})
    atomic_write_json(spec.status_path, status)
    append_log(spec.operational_log, "preflight requested")
    try:
        if mock:
            runner_environment(spec)
            append_log(spec.operational_log, "mock preflight passed")
        else:
            full_preflight(spec)
        final = update_status(
            spec.status_path,
            state="PREFLIGHT_PASSED",
            api_health="OK",
            elapsed_seconds=int(time.time() - start),
            ended_at=utc_now(),
        )
        append_log(spec.operational_log, "preflight completed without production launch")
        write_registry(spec, {"state": "PREFLIGHT_PASSED"})
        return final
    except ProbeError as exc:
        failed = update_status(
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
        raise


def supervise(run_id: str, *, mock: bool = False, recovery: bool = False) -> int:
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
        if spec.task == PERSISTENCE_DIAGNOSTIC_TASK:
            return run_persistence_diagnostic(spec, start)
        if mock:
            env = runner_environment(spec)
            append_log(spec.operational_log, "mock preflight passed")
        else:
            env = full_preflight(spec)
        update_status(spec.status_path, state="RUNNING", api_health="OK")
        append_log(spec.operational_log, "production run started")
        command = build_inspect_command(spec, recovery=recovery)
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
        latest = latest_json_log(spec.log_dir)
        inspect_status = inspect_log_metadata(latest).status if latest else None
        completed = count_completed_samples(spec.log_dir)
        reconciled_completed = None
        if recovery and latest:
            segment_paths = json_logs(spec.log_dir)
            if segment_paths:
                reconciled_completed = reconciled_unique_count(spec, segment_paths)
                completed = reconciled_completed
        if return_code != 0:
            final_state = "FAILED"
        elif completed == spec.total_samples and inspect_log_success(spec.log_dir):
            final_state = "COMPLETED"
        else:
            final_state = "INCOMPLETE"
        failure_reason = None
        if final_state == "INCOMPLETE":
            failure_reason = (
                f"incomplete inspect run: completed {completed}/{spec.total_samples}; "
                f"inspect_status={inspect_status or 'UNKNOWN'}; exit_code={return_code}"
            )
        update_status(
            spec.status_path,
            state=final_state,
            exit_code=return_code,
            inspect_status=inspect_status,
            reconciled_completed=reconciled_completed,
            failure_reason=failure_reason,
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


def run_persistence_diagnostic(spec: RunSpec, start: float) -> int:
    stop_requested = False
    max_seconds = int(os.environ.get("RUNNER_PERSISTENCE_DIAGNOSTIC_SECONDS", "1800"))
    heartbeat_interval = float(os.environ.get("RUNNER_PERSISTENCE_DIAGNOSTIC_HEARTBEAT_SECONDS", "5"))

    def request_stop(signum: int, frame: object) -> None:
        nonlocal stop_requested
        stop_requested = True

    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)
    append_log(spec.operational_log, "persistence diagnostic started; no model/API requests will be made")
    update_status(
        spec.status_path,
        state="RUNNING",
        api_health="NOT_USED",
        diagnostic="runner_persistence",
        persistence_mechanism=os.environ.get("AA_RUNNER_HANDOFF", "subprocess.Popen(start_new_session=True)"),
        heartbeat_count=0,
        last_heartbeat_at=utc_now(),
        no_model_requests=True,
    )
    write_registry(spec, {"state": "RUNNING", "diagnostic": "runner_persistence"})

    heartbeat_count = 0
    deadline = start + max_seconds
    while not stop_requested and time.time() < deadline:
        heartbeat_count += 1
        update_status(
            spec.status_path,
            heartbeat_count=heartbeat_count,
            last_heartbeat_at=utc_now(),
            elapsed_seconds=int(time.time() - start),
        )
        append_log(spec.operational_log, f"diagnostic heartbeat {heartbeat_count}")
        time.sleep(heartbeat_interval)

    state = "STOPPED" if stop_requested else "COMPLETED"
    reason = "remote stop requested" if stop_requested else "diagnostic duration elapsed"
    update_status(
        spec.status_path,
        state=state,
        stop_reason=reason if stop_requested else None,
        exit_code=0,
        elapsed_seconds=int(time.time() - start),
        ended_at=utc_now(),
    )
    append_log(spec.operational_log, f"persistence diagnostic ended state={state} reason={reason}")
    write_registry(spec, {"state": state, "exit_code": 0})
    return 0


def refresh_operational_status(spec: RunSpec, start: float | None = None) -> dict[str, Any]:
    runtime = runtime_home(repository_root(), spec.run_id)
    completed = count_completed_samples(spec.log_dir)
    reconciled_completed = None
    if (spec.status_path.parent / "RECOVERY_PLAN.json").exists():
        try:
            reconciled_completed = reconciled_unique_count(spec, json_logs(spec.log_dir))
        except ValueError:
            reconciled_completed = None
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
    if reconciled_completed is not None:
        updates["reconciled_completed"] = reconciled_completed
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
    completed = status.get("reconciled_completed", status.get("completed", 0))
    lines = [
        f"RUN {run_id}",
        f"Status: {status.get('state', 'UNKNOWN')}",
        f"Completed: {completed} / {status.get('total', spec.total_samples)}",
        f"Supervisor PID: {pid if pid else 'n/a'} ({'alive' if alive else 'not active'})",
        f"Inspect PID: {status.get('inspect_pid', 'n/a')}",
        f"Technical failures: {status.get('technical_failures', 0)}",
        f"Elapsed: {status.get('elapsed_seconds', 0)}s",
        f"API health: {status.get('api_health', 'UNKNOWN')}",
        f"Raw log bytes: {raw_bytes}",
        f"Tokens: {status.get('token_usage', 'n/a')}",
        f"Frozen SHA: {status.get('frozen_commit', spec.frozen_commit)}",
    ]
    if status.get("diagnostic"):
        lines.extend(
            [
                f"Diagnostic: {status.get('diagnostic')}",
                f"Heartbeat count: {status.get('heartbeat_count', 0)}",
                f"Last heartbeat: {status.get('last_heartbeat_at', 'n/a')}",
                f"No model requests: {status.get('no_model_requests', False)}",
            ]
        )
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
    elif lock and not alive and state not in {"COMPLETED", "FAILED", "STOPPED", "INCOMPLETE"}:
        classification = "stale lock"
    elif state == "FAILED":
        classification = "process exited"
    elif state == "INCOMPLETE":
        classification = "incomplete"
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
            f"Heartbeat count: {status.get('heartbeat_count', 'n/a')}",
            f"Last heartbeat: {status.get('last_heartbeat_at', 'n/a')}",
        ]
    )


def stop_run(run_id: str) -> str:
    spec = known_runs()[run_id]
    status = read_json(spec.status_path, {})
    lock = read_json(spec.lock_path, {})
    pid = int(status.get("supervisor_pid", 0) or 0)
    if not pid or not process_alive(pid):
        update_status(spec.status_path, state="STOPPED", stop_reason="no active supervisor")
        append_log(spec.operational_log, "stop requested; no active supervisor")
        return f"RUN {run_id}: no active supervisor"
    try:
        os.killpg(pid, signal.SIGTERM)
    except ProcessLookupError:
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    label = status.get("launchd_label") or lock.get("launchd_label")
    if label:
        bootout_launchd(str(label))
    update_status(spec.status_path, state="STOPPING", stop_requested_at=utc_now())
    append_log(spec.operational_log, f"stop requested for process group {pid}")
    return f"RUN {run_id}: stop requested for PID {pid}"


def resume_run(run_id: str, *, mock: bool = False) -> dict[str, Any]:
    spec = known_runs()[run_id]
    status = read_json(spec.status_path, {})
    completed = int(status.get("completed", 0) or 0)
    plan = None
    if not mock and completed < spec.total_samples:
        plan = build_recovery_plan(spec)
        write_recovery_plan(spec, plan)
        if not plan.recoverable:
            update_status(
                spec.status_path,
                state="INCOMPLETE",
                resume_uses="runner-level missing-sample recovery refused",
                completed_before_resume=completed,
                recovery_source_completed=plan.source_completed_count,
                recovery_missing=plan.missing_count,
                recovery_blocked_reason="duplicate or unexpected sample IDs in source segment",
            )
            append_log(spec.operational_log, "resume refused; recovery plan is not recoverable")
            raise RuntimeError("recovery plan is not safely recoverable")
    update_status(
        spec.status_path,
        state="RESUME_REQUESTED",
        resume_uses=(
            "runner-level missing-sample recovery"
            if plan is not None
            else "inspect eval retry/checkpoint when raw log is resumable"
        ),
        completed_before_resume=completed,
        recovery_source_completed=plan.source_completed_count if plan else None,
        recovery_missing=plan.missing_count if plan else None,
    )
    append_log(spec.operational_log, f"resume requested completed={completed}")
    if plan is not None:
        return launch_detached(run_id, mock=mock, recovery=True)
    return launch_detached(run_id, mock=mock)


def finalize_run(run_id: str) -> dict[str, Any]:
    spec = known_runs()[run_id]
    status = refresh_operational_status(spec)
    pid = int(status.get("supervisor_pid", 0) or 0)
    if pid and process_alive(pid):
        raise RuntimeError("cannot finalize while supervisor is active")
    reconciled_completed = status.get("reconciled_completed")
    completed = int(
        status.get("completed", 0) if reconciled_completed is None else reconciled_completed
    )
    if status.get("state") != "COMPLETED" or completed != spec.total_samples:
        if (
            completed == spec.total_samples
            and status.get("state") == "INCOMPLETE"
            and inspect_log_success(spec.log_dir)
        ):
            status = update_status(
                spec.status_path,
                state="COMPLETED",
                reconciliation_finalized_from_segments=True,
            )
        else:
            raise RuntimeError(
                f"cannot finalize incomplete run: state={status.get('state', 'UNKNOWN')} "
                f"completed={completed}/{spec.total_samples}"
            )
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
