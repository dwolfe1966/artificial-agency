from __future__ import annotations

import os
import socket
import subprocess
import sys
import urllib.request
from urllib.error import HTTPError
from pathlib import Path
from typing import Protocol

from openai import OpenAI

from artificial_agency.experiments.exp002.inspect_task import fixed_conflict_samples

from .config import RunSpec, repository_root
from .state import append_log


class ProbeError(RuntimeError):
    pass


class ProbeSet(Protocol):
    def dns(self) -> None: ...
    def https(self) -> None: ...
    def auth(self, env: dict[str, str]) -> None: ...
    def canary(self, spec: RunSpec, env: dict[str, str]) -> None: ...


class RealProbes:
    def __init__(self, timeout: float = 10.0) -> None:
        self.timeout = timeout

    def dns(self) -> None:
        socket.getaddrinfo("api.openai.com", 443)

    def https(self) -> None:
        request = urllib.request.Request(
            "https://api.openai.com/v1/models",
            method="HEAD",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout):
                return
        except HTTPError:
            return

    def auth(self, env: dict[str, str]) -> None:
        api_key = env.get("OPENAI_API_KEY")
        if not api_key:
            raise ProbeError("OPENAI_API_KEY is not present")
        client = OpenAI(api_key=api_key, timeout=self.timeout, max_retries=0)
        client.models.list()

    def canary(self, spec: RunSpec, env: dict[str, str]) -> None:
        spec.canary_log_dir.mkdir(parents=True, exist_ok=True)
        command = [
            sys.executable,
            "-m",
            "inspect_ai",
            "eval",
            "artificial_agency/runner/canary.py@operational_canary",
            "--model",
            spec.model,
            "--max-tokens",
            "32",
            "--max-connections",
            "1",
            "--max-retries",
            "1",
            "--timeout",
            "30",
            "--attempt-timeout",
            "20",
            "--log-format",
            "json",
            "--log-buffer",
            "1",
            "--log-dir",
            str(spec.canary_log_dir),
            "--tags",
            f"operational-canary,{spec.run_id}",
            "--metadata",
            "operational_canary=true",
            "--display",
            "none",
        ]
        result = subprocess.run(
            command,
            cwd=repository_root(),
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=90,
        )
        if result.returncode != 0:
            raise ProbeError(result.stderr or result.stdout or "canary failed")


def load_dotenv(root: Path, env: dict[str, str]) -> dict[str, str]:
    merged = dict(env)
    env_path = root / ".env"
    if not env_path.exists():
        return merged
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        merged.setdefault(key, value.strip().strip("'").strip('"'))
    return merged


def runner_environment(spec: RunSpec) -> dict[str, str]:
    root = repository_root()
    runtime_home = root / "results" / ".runner-runtime" / spec.run_id
    runtime_home.mkdir(parents=True, exist_ok=True)
    env = load_dotenv(root, os.environ)
    env["PYTHONPATH"] = str(root)
    env["HOME"] = str(runtime_home)
    env["INSPECT_TRACE_FILE"] = str(runtime_home / "inspect-trace.log")
    return env


def scientific_preflight(spec: RunSpec) -> None:
    root = repository_root()
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        text=True,
    ).strip()
    if head != spec.frozen_commit:
        raise ProbeError(
            f"scientific commit mismatch: expected {spec.frozen_commit}, got {head}"
        )

    status = subprocess.check_output(
        ["git", "status", "--short"],
        cwd=root,
        text=True,
    ).strip()
    if status:
        raise ProbeError("worktree is not clean")

    samples = fixed_conflict_samples()
    if len(samples) != spec.total_samples:
        raise ProbeError(
            f"sample count mismatch: expected {spec.total_samples}, got {len(samples)}"
        )
    counts = {condition: 0 for condition in spec.condition_counts}
    for sample in samples:
        condition = str(sample.metadata["condition"])
        counts[condition] = counts.get(condition, 0) + 1
    if counts != spec.condition_counts:
        raise ProbeError(f"condition count mismatch: expected {spec.condition_counts}, got {counts}")


def environment_preflight(spec: RunSpec, env: dict[str, str]) -> None:
    root = repository_root()
    import artificial_agency

    package_path = Path(artificial_agency.__file__).resolve()
    if root not in package_path.parents:
        raise ProbeError(f"artificial_agency resolves outside repository: {package_path}")

    spec.log_dir.mkdir(parents=True, exist_ok=True)
    spec.status_path.parent.mkdir(parents=True, exist_ok=True)
    spec.operational_log.parent.mkdir(parents=True, exist_ok=True)

    dry = subprocess.run(
        [
            sys.executable,
            "-m",
            "inspect_ai",
            "eval",
            spec.task,
            "--model",
            "mockllm/model",
            "--limit",
            "0",
            "--log-format",
            "json",
            "--log-dir",
            str(root / "results" / ".runner-runtime" / spec.run_id / "dry-load"),
            "--display",
            "none",
        ],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )
    if dry.returncode != 0:
        raise ProbeError(dry.stderr or dry.stdout or "Inspect dry-load failed")


def full_preflight(spec: RunSpec, probes: ProbeSet | None = None) -> dict[str, str]:
    probes = probes or RealProbes()
    env = runner_environment(spec)
    append_log(spec.operational_log, "preflight started")
    scientific_preflight(spec)
    append_log(spec.operational_log, "git and dataset integrity passed")
    environment_preflight(spec, env)
    append_log(spec.operational_log, "environment and dry-load passed")
    probes.dns()
    append_log(spec.operational_log, "DNS passed")
    probes.https()
    append_log(spec.operational_log, "HTTPS connectivity passed")
    probes.auth(env)
    append_log(spec.operational_log, "OpenAI authentication passed")
    probes.canary(spec, env)
    append_log(spec.operational_log, "operational canary passed")
    return env
