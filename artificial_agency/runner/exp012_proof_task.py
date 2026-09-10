from __future__ import annotations

import json
import os
from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample

from artificial_agency.experiments.exp012.config import ModelRun
from artificial_agency.experiments.exp012.inspect_task import (
    capability_loss_samples,
    capability_loss_task,
)
from artificial_agency.runner.config import repository_root


PROOF_CONDITION_ID = "capability"
PROOF_REPLICATE_ID = 0
PROOF_RECOVERY_IDS = "PROOF_RECOVERY_SAMPLE_IDS.json"

MODEL_A_GPT_PROOF = ModelRun(
    run_id="run-012-PROOF-GPT",
    model_role="model_a_gpt",
    provider="openai",
    model_id="openai/gpt-5.6-sol",
    sample_prefix="012-PROOF-GPT",
)

MODEL_B_CLAUDE_PROOF = ModelRun(
    run_id="run-012-PROOF-CLAUDE",
    model_role="model_b_claude",
    provider="anthropic",
    model_id="anthropic/claude-sonnet-5",
    sample_prefix="012-PROOF-CLAUDE",
)

MODEL_C_GEMINI_PROOF = ModelRun(
    run_id="run-012-PROOF-GEMINI",
    model_role="model_c_gemini",
    provider="google",
    model_id="google/gemini-3.7-flash",
    sample_prefix="012-PROOF-GEMINI",
)

PROOF_RUN_BY_ID = {
    "012-PROOF-GPT": MODEL_A_GPT_PROOF,
    "012-PROOF-CLAUDE": MODEL_B_CLAUDE_PROOF,
    "012-PROOF-GEMINI": MODEL_C_GEMINI_PROOF,
}


def proof_samples(run: ModelRun) -> list[Sample]:
    expected_id = f"{run.sample_prefix}-{PROOF_CONDITION_ID}-{PROOF_REPLICATE_ID:02d}"
    selected = [
        sample
        for sample in capability_loss_samples(run)
        if sample.id == expected_id
    ]
    if len(selected) != 1:
        raise RuntimeError(f"proof sample construction failed for {expected_id}")
    sample = selected[0]
    metadata = dict(sample.metadata or {})
    metadata.update(
        {
            "production_proof": True,
            "non_confirmatory": True,
            "confirmatory_dataset_eligible": False,
            "exclude_from_confirmatory_analysis": True,
            "proof_condition_id": PROOF_CONDITION_ID,
            "proof_replicate_id": PROOF_REPLICATE_ID,
            "proof_exclusion_reason": (
                "three-provider production-readiness proof; not part of the "
                "preregistered 180-sequence confirmatory dataset"
            ),
        }
    )
    sample.metadata = metadata
    return [sample]


def proof_task(run: ModelRun) -> Task:
    task_obj = capability_loss_task(run)
    task_obj.dataset = MemoryDataset(
        proof_samples(run),
        name=f"{run.run_id}-non-confirmatory-production-proof",
        location=f"runner-v2://{run.run_id}/non-confirmatory-production-proof",
    )
    metadata = dict(task_obj.metadata or {})
    metadata.update(
        {
            "sample_count": 1,
            "samples_per_condition": None,
            "production_proof": True,
            "non_confirmatory": True,
            "confirmatory_dataset_eligible": False,
            "exclude_from_confirmatory_analysis": True,
            "proof_condition_id": PROOF_CONDITION_ID,
            "proof_replicate_id": PROOF_REPLICATE_ID,
            "proof_exclusion_reason": (
                "three-provider production-readiness proof; not part of the "
                "preregistered 180-sequence confirmatory dataset"
            ),
        }
    )
    task_obj.metadata = metadata
    return task_obj


def _payload() -> dict[str, object]:
    configured = os.environ.get("AA_RECOVERY_MISSING_IDS")
    path = (
        Path(configured).expanduser()
        if configured
        else repository_root() / PROOF_RECOVERY_IDS
    )
    if not path.exists():
        raise RuntimeError(f"Missing proof recovery manifest: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def proof_recovery_task(run: ModelRun) -> Task:
    payload = _payload()
    missing_ids = tuple(str(sample_id) for sample_id in payload.get("missing_ids", []))
    expected = {str(sample.id): sample for sample in proof_samples(run)}
    recovery_samples = [expected[sample_id] for sample_id in missing_ids if sample_id in expected]
    if len(recovery_samples) != len(missing_ids):
        raise RuntimeError("proof recovery dataset did not match requested sequence ID")
    task_obj = proof_task(run)
    task_obj.dataset = MemoryDataset(
        recovery_samples,
        name=f"{run.run_id}-non-confirmatory-proof-recovery",
        location=f"runner-v2://{run.run_id}/non-confirmatory-proof-recovery",
    )
    metadata = dict(task_obj.metadata or {})
    metadata["recovery_mode"] = "proof_sequence_atomic_full_sequence"
    metadata["sequence_atomic_recovery"] = True
    task_obj.metadata = metadata
    return task_obj


@task
def exp012_proof_gpt56_sol() -> Task:
    return proof_task(MODEL_A_GPT_PROOF)


@task
def exp012_proof_claude_sonnet5() -> Task:
    return proof_task(MODEL_B_CLAUDE_PROOF)


@task
def exp012_proof_gemini37_flash() -> Task:
    return proof_task(MODEL_C_GEMINI_PROOF)


@task
def exp012_proof_gpt56_sol_recovery_missing() -> Task:
    return proof_recovery_task(MODEL_A_GPT_PROOF)


@task
def exp012_proof_claude_sonnet5_recovery_missing() -> Task:
    return proof_recovery_task(MODEL_B_CLAUDE_PROOF)


@task
def exp012_proof_gemini37_flash_recovery_missing() -> Task:
    return proof_recovery_task(MODEL_C_GEMINI_PROOF)
