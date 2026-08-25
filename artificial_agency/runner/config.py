from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


RUNNER_VERSION = "v2"
RUN_REGISTRY = Path("results/run_registry.json")
PERSISTENCE_DIAGNOSTIC_TASK = "__runner_persistence_diagnostic__"
EXP002_SCIENTIFIC_FREEZE_PATHS = (
    "artificial_agency/experiments/exp002",
    "experiments/002-fixed-conflict-pressure",
    "tests/experiments/exp002",
    "pyproject.toml",
)
EXP003_SCIENTIFIC_FREEZE_PATHS = (
    "artificial_agency/experiments/exp003",
    "experiments/003-constraint-status-pressure",
    "tests/experiments/exp003",
    "pyproject.toml",
)


@dataclass(frozen=True)
class RunSpec:
    run_id: str
    experiment_id: str
    title: str
    frozen_commit: str
    scientific_paths: tuple[str, ...]
    task: str
    model: str
    total_samples: int
    condition_counts: dict[str, int]
    log_dir: Path
    status_path: Path
    operational_log: Path
    lock_path: Path
    pid_path: Path
    stdout_path: Path
    canary_log_dir: Path
    previous_attempts: list[dict[str, str]] = field(default_factory=list)
    inspect_args: tuple[str, ...] = ()


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def runtime_home(root: Path, run_id: str) -> Path:
    return root / "results" / ".runner-runtime" / run_id


def known_runs(root: Path | None = None) -> dict[str, RunSpec]:
    repo = root or repository_root()
    run002_root = repo / "results" / "002-fixed-conflict-pressure" / "run-002A"
    run003_root = repo / "results" / "003-constraint-status-pressure" / "run-003A"
    return {
        "002A": RunSpec(
            run_id="002A",
            experiment_id="002-fixed-conflict-pressure",
            title="Experiment 002 Run 002A",
            frozen_commit="6301fc0b78ded0200fd6203d4888ac2b3c33cae7",
            scientific_paths=EXP002_SCIENTIFIC_FREEZE_PATHS,
            task=(
                "artificial_agency/experiments/exp002/"
                "inspect_task.py@exp002_fixed_conflict_phase1"
            ),
            model="openai/gpt-5.6-sol",
            total_samples=90,
            condition_counts={"low": 30, "medium": 30, "high": 30},
            log_dir=run002_root / "inspect",
            status_path=run002_root / "RUN_STATUS.json",
            operational_log=run002_root / "operational.log",
            lock_path=run002_root / "RUN_LOCK.json",
            pid_path=run002_root / "RUNNER.pid",
            stdout_path=run002_root / "runner-supervisor.out",
            canary_log_dir=run002_root / "canary",
            previous_attempts=[
                {
                    "kind": "technical_pre_result_failure",
                    "completed": "0",
                    "reason": "DNS/API connectivity failure before completed samples",
                    "raw_log_sha256": (
                        "b18f043830d2d4e6ca791a119d3b6512afa6979c0bef089e22968fa0dac1dbdf"
                    ),
                }
            ],
            inspect_args=(
                "--model",
                "openai/gpt-5.6-sol",
                "--max-tokens",
                "4096",
                "--reasoning-effort",
                "medium",
                "--verbosity",
                "medium",
                "--no-parallel-tool-calls",
                "--epochs",
                "1",
                "--max-connections",
                "1",
                "--log-format",
                "json",
                "--tags",
                "exp002,phase1,run002A,fixed-conflict-pressure",
                "--metadata",
                "experiment_id=002-fixed-conflict-pressure",
                "--metadata",
                "phase=fixed_conflict_pressure",
                "--metadata",
                "run_id=run-002A",
                "--metadata",
                "git_commit=6301fc0b78ded0200fd6203d4888ac2b3c33cae7",
                "--max-retries",
                "3",
                "--timeout",
                "60",
                "--attempt-timeout",
                "45",
                "--log-buffer",
                "1",
                "--checkpoint",
                "turn:1",
                "--display",
                "plain",
            ),
        ),
        "003A": RunSpec(
            run_id="003A",
            experiment_id="003-constraint-status-pressure",
            title="Experiment 003 Run 003A Stage 1",
            frozen_commit="f8294ab172cb556f8a4c1ec4f726947672cc859a",
            scientific_paths=EXP003_SCIENTIFIC_FREEZE_PATHS,
            task=(
                "artificial_agency/experiments/exp003/"
                "inspect_task.py@exp003_constraint_status_stage1"
            ),
            model="openai/gpt-5.6-sol",
            total_samples=120,
            condition_counts={
                "categorical-ordinary": 20,
                "categorical-high": 20,
                "procedural-ordinary": 20,
                "procedural-high": 20,
                "purpose-conflict-ordinary": 20,
                "purpose-conflict-high": 20,
            },
            log_dir=run003_root / "inspect",
            status_path=run003_root / "RUN_STATUS.json",
            operational_log=run003_root / "operational.log",
            lock_path=run003_root / "RUN_LOCK.json",
            pid_path=run003_root / "RUNNER.pid",
            stdout_path=run003_root / "runner-supervisor.out",
            canary_log_dir=run003_root / "canary",
            inspect_args=(
                "--model",
                "openai/gpt-5.6-sol",
                "--max-tokens",
                "4096",
                "--reasoning-effort",
                "medium",
                "--verbosity",
                "medium",
                "--no-parallel-tool-calls",
                "--epochs",
                "1",
                "--max-connections",
                "1",
                "--log-format",
                "json",
                "--tags",
                "exp003,stage1,run003A,constraint-status-pressure",
                "--metadata",
                "experiment_id=003-constraint-status-pressure",
                "--metadata",
                "phase=constraint_status_pressure_stage1",
                "--metadata",
                "run_id=run-003A",
                "--metadata",
                "git_commit=f8294ab172cb556f8a4c1ec4f726947672cc859a",
                "--max-retries",
                "3",
                "--timeout",
                "60",
                "--attempt-timeout",
                "45",
                "--log-buffer",
                "1",
                "--checkpoint",
                "turn:1",
                "--display",
                "plain",
            ),
        ),
        "PERSISTENCE_DIAGNOSTIC": RunSpec(
            run_id="PERSISTENCE_DIAGNOSTIC",
            experiment_id="runner-persistence-diagnostic",
            title="Runner v2 Persistence Diagnostic",
            frozen_commit="6301fc0b78ded0200fd6203d4888ac2b3c33cae7",
            scientific_paths=(),
            task=PERSISTENCE_DIAGNOSTIC_TASK,
            model="none",
            total_samples=0,
            condition_counts={},
            log_dir=repo / "results" / "runner-diagnostics" / "persistence" / "logs",
            status_path=repo / "results" / "runner-diagnostics" / "persistence" / "RUN_STATUS.json",
            operational_log=repo / "results" / "runner-diagnostics" / "persistence" / "operational.log",
            lock_path=repo / "results" / "runner-diagnostics" / "persistence" / "RUN_LOCK.json",
            pid_path=repo / "results" / "runner-diagnostics" / "persistence" / "RUNNER.pid",
            stdout_path=repo / "results" / "runner-diagnostics" / "persistence" / "runner-supervisor.out",
            canary_log_dir=repo / "results" / "runner-diagnostics" / "persistence" / "canary",
        ),
    }
