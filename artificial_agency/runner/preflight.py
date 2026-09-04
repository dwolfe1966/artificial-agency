from __future__ import annotations

import importlib
import os
import re
import socket
import subprocess
import sys
import urllib.request
from urllib.error import HTTPError
from pathlib import Path
from typing import Protocol

from openai import OpenAI

from .config import RunSpec, repository_root
from .state import append_log


class ProbeError(RuntimeError):
    pass


class ProbeSet(Protocol):
    def dns(self, model: str = "openai/gpt-5.6-sol") -> None: ...
    def https(self, model: str = "openai/gpt-5.6-sol") -> None: ...
    def auth(
        self, env: dict[str, str], model: str = "openai/gpt-5.6-sol"
    ) -> None: ...
    def canary(self, spec: RunSpec, env: dict[str, str]) -> None: ...


class RealProbes:
    def __init__(self, timeout: float = 10.0) -> None:
        self.timeout = timeout

    def _provider_host(self, model: str) -> str:
        if model.startswith("anthropic/"):
            return "api.anthropic.com"
        if model.startswith("google/"):
            return "generativelanguage.googleapis.com"
        return "api.openai.com"

    def _provider_url(self, model: str) -> str:
        if model.startswith("anthropic/"):
            return "https://api.anthropic.com/v1/models"
        if model.startswith("google/"):
            return "https://generativelanguage.googleapis.com"
        return "https://api.openai.com/v1/models"

    def _provider_key_name(self, model: str) -> str:
        if model.startswith("anthropic/"):
            return "ANTHROPIC_API_KEY"
        if model.startswith("google/"):
            return "GOOGLE_API_KEY"
        return "OPENAI_API_KEY"

    def dns(self, model: str = "openai/gpt-5.6-sol") -> None:
        socket.getaddrinfo(self._provider_host(model), 443)

    def https(self, model: str = "openai/gpt-5.6-sol") -> None:
        request = urllib.request.Request(
            self._provider_url(model),
            method="HEAD",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout):
                return
        except HTTPError:
            return

    def auth(self, env: dict[str, str], model: str = "openai/gpt-5.6-sol") -> None:
        key_name = self._provider_key_name(model)
        api_key = env.get(key_name)
        if not api_key:
            raise ProbeError(f"{key_name} is not present")
        if model.startswith("openai/"):
            client = OpenAI(api_key=api_key, timeout=self.timeout, max_retries=0)
            client.models.list()
            return
        # Anthropic and Google authenticated connectivity is exercised by the
        # provider-specific Inspect canary. Avoid duplicating provider SDK logic
        # here so secrets are not printed or committed in diagnostic code.
        return

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
    runtime_home = spec.status_path.parent / ".runner-home"
    runtime_home.mkdir(parents=True, exist_ok=True)
    env = load_dotenv(root, os.environ)
    env["PYTHONPATH"] = str(root)
    env["HOME"] = str(runtime_home)
    env["INSPECT_TRACE_FILE"] = str(runtime_home / "inspect-trace.log")
    recovery_ids = spec.status_path.parent / "RECOVERY_MISSING_IDS.json"
    if recovery_ids.exists():
        env["AA_RECOVERY_MISSING_IDS"] = str(recovery_ids)
    return env


def scientific_preflight(spec: RunSpec) -> None:
    root = repository_root()
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        text=True,
    ).strip()

    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=root,
        text=True,
    ).strip()
    dirty = _scientifically_dirty_status_lines(status)
    if dirty:
        raise ProbeError("worktree is not clean")

    diff = subprocess.run(
        [
            "git",
            "diff",
            "--quiet",
            f"{spec.frozen_commit}..{head}",
            "--",
            *spec.scientific_paths,
        ],
        cwd=root,
        check=False,
    )
    if diff.returncode == 1:
        changed = subprocess.check_output(
            [
                "git",
                "diff",
                "--name-only",
                f"{spec.frozen_commit}..{head}",
                "--",
                *spec.scientific_paths,
            ],
            cwd=root,
            text=True,
        ).strip()
        raise ProbeError(
            "scientific files differ from frozen commit "
            f"{spec.frozen_commit}: {changed}"
        )
    if diff.returncode not in (0, 1):
        raise ProbeError("unable to compare scientific freeze paths")

    samples = _samples_for_task(spec.task)
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


def _samples_for_task(task_ref: str) -> list[object]:
    module_ref, _, task_name = task_ref.partition("@")
    if not module_ref or not task_name:
        raise ProbeError(f"invalid task reference: {task_ref}")
    module_name = module_ref.removesuffix(".py").replace("/", ".")
    task_func = getattr(importlib.import_module(module_name), task_name)
    task_obj = task_func()
    return list(task_obj.dataset)


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
            str(Path(env["HOME"]) / "dry-load"),
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
    probes.dns(spec.model)
    append_log(spec.operational_log, "DNS passed")
    probes.https(spec.model)
    append_log(spec.operational_log, "HTTPS connectivity passed")
    probes.auth(env, spec.model)
    append_log(spec.operational_log, "provider authentication precheck passed")
    probes.canary(spec, env)
    append_log(spec.operational_log, "operational canary passed")
    return env


LEGACY_RUNTIME_RE = re.compile(
    r"^results/009-observability/run-009[A-Z]-[A-Z]+-S1/"
    r"("
    r"RUN_STATUS\.json|RUN_LOCK\.json|RUNNER\.pid|operational\.log|"
    r"runner-supervisor\.out|RECOVERY_MISSING_IDS\.json|RECOVERY_PLAN\.json|"
    r"inspect/.*|canary/.*|\.runner-home/.*"
    r")$"
)


def _scientifically_dirty_status_lines(status: str) -> list[str]:
    dirty: list[str] = []
    for line in status.splitlines():
        if not line:
            continue
        path = line[3:] if len(line) > 3 else ""
        if line.startswith("?? ") and LEGACY_RUNTIME_RE.match(path):
            continue
        dirty.append(line)
    return dirty
