from __future__ import annotations

import json
import os
from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset

from artificial_agency.experiments.exp012.config import (
    MODEL_A_GPT,
    MODEL_B_CLAUDE,
    MODEL_C_GEMINI,
    ModelRun,
)
from artificial_agency.experiments.exp012.inspect_task import (
    capability_loss_samples,
    capability_loss_task,
)
from artificial_agency.runner.config import repository_root


RECOVERY_MISSING_IDS = "RECOVERY_MISSING_IDS.json"


def _payload() -> dict[str, object]:
    configured = os.environ.get("AA_RECOVERY_MISSING_IDS")
    path = (
        Path(configured).expanduser()
        if configured
        else repository_root() / RECOVERY_MISSING_IDS
    )
    if not path.exists():
        raise RuntimeError(f"Missing recovery manifest: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _recovery_task(run: ModelRun) -> Task:
    payload = _payload()
    missing_ids = tuple(str(sample_id) for sample_id in payload.get("missing_ids", []))
    expected = {str(sample.id): sample for sample in capability_loss_samples(run)}
    recovery_samples = [expected[sample_id] for sample_id in missing_ids if sample_id in expected]
    if len(recovery_samples) != len(missing_ids):
        raise RuntimeError("recovery dataset did not match requested missing sequence IDs")
    task_obj = capability_loss_task(run)
    task_obj.dataset = MemoryDataset(
        recovery_samples,
        name=f"{run.run_id}-sequence-atomic-recovery-missing",
        location=f"runner-v2://{run.run_id}/sequence-atomic-recovery-missing",
    )
    metadata = dict(task_obj.metadata or {})
    metadata["recovery_source_log"] = payload.get("source_log")
    metadata["recovery_missing_count"] = len(missing_ids)
    metadata["recovery_mode"] = "missing_sequences_only_sequence_atomic_phase_a_phase_b"
    metadata["sequence_atomic_recovery"] = True
    task_obj.metadata = metadata
    return task_obj


@task
def exp012_model_a_gpt56_sol_recovery_missing() -> Task:
    return _recovery_task(MODEL_A_GPT)


@task
def exp012_model_b_claude_sonnet5_recovery_missing() -> Task:
    return _recovery_task(MODEL_B_CLAUDE)


@task
def exp012_model_c_gemini37_flash_recovery_missing() -> Task:
    return _recovery_task(MODEL_C_GEMINI)
