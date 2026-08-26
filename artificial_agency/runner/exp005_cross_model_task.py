from __future__ import annotations

from typing import NamedTuple

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.solver import system_message, use_tools

from artificial_agency.experiments.exp004.config import (
    ACCOUNT_ARR,
    AUTHORIZED_DISCOUNT_LIMIT,
    CONDITION_TEXT_SHA256,
    CONDITIONS,
    CUSTOMER_RENEWAL_THRESHOLD_PERCENT,
    ENVIRONMENT_VERSION,
    MANIPULATION_CHECK_TEXT,
    MAX_ACTION_STEPS,
    MAX_CREDIT_AMOUNT,
    PROMPT_VERSION,
    WORDING_VERSION,
    deterministic_seed,
)
from artificial_agency.experiments.exp004.inspect_task import (
    SYSTEM_PROMPT,
    constraint_meaning_agent_loop,
    constraint_meaning_outcome_scorer,
    initialize_constraint_meaning_environment,
    manipulation_check_loop,
    manipulation_check_tools,
    render_sample_input,
    retention_tools,
)


EXPERIMENT_ID = "005-cross-model-replication"
REFERENCE_EXPERIMENT_ID = "004-constraint-meaning-validation"
REFERENCE_SCIENTIFIC_SHA = "aa126f9254a01c96e85545a9e1a77d10195f2604"
PREREGISTRATION_SHA = "20aa46df84964b5ab55354a063b8ebe3f57e26c0"
REPLICATES_PER_CELL = 50
PHASE = "cross_model_replication_full"


class CrossModelRun(NamedTuple):
    run_id: str
    model_role: str
    provider: str
    model_id: str
    sample_prefix: str


MODEL_B = CrossModelRun(
    run_id="run-005B",
    model_role="model_b",
    provider="anthropic",
    model_id="anthropic/claude-sonnet-5",
    sample_prefix="005B",
)

MODEL_C = CrossModelRun(
    run_id="run-005C",
    model_role="model_c",
    provider="google",
    model_id="google/gemini-3.7-flash",
    sample_prefix="005C",
)


def cross_model_samples(run: CrossModelRun) -> list[Sample]:
    samples: list[Sample] = []
    for condition in CONDITIONS.values():
        for replicate_id in range(REPLICATES_PER_CELL):
            samples.append(
                Sample(
                    id=f"{run.sample_prefix}-{condition.id}-{replicate_id:02d}",
                    input=render_sample_input(condition.id),
                    metadata={
                        "experiment_id": EXPERIMENT_ID,
                        "reference_experiment_id": REFERENCE_EXPERIMENT_ID,
                        "reference_scientific_sha": REFERENCE_SCIENTIFIC_SHA,
                        "preregistration_sha": PREREGISTRATION_SHA,
                        "condition_protocol_sha256": CONDITION_TEXT_SHA256,
                        "environment_version": ENVIRONMENT_VERSION,
                        "prompt_version": PROMPT_VERSION,
                        "wording_version": WORDING_VERSION,
                        "run_id": run.run_id,
                        "model_role": run.model_role,
                        "provider": run.provider,
                        "model_id": run.model_id,
                        "condition": condition.id,
                        "constraint_meaning": condition.constraint_meaning,
                        "pressure": condition.pressure,
                        "replicate_id": replicate_id,
                        "sample_seed": deterministic_seed(
                            condition.id, replicate_id
                        ),
                        "annual_recurring_revenue": ACCOUNT_ARR,
                        "customer_renewal_threshold_percent": (
                            CUSTOMER_RENEWAL_THRESHOLD_PERCENT
                        ),
                        "authorized_discount_limit_percent": (
                            AUTHORIZED_DISCOUNT_LIMIT
                        ),
                        "max_credit_amount": MAX_CREDIT_AMOUNT,
                        "phase": PHASE,
                    },
                )
            )
    return samples


def cross_model_task(run: CrossModelRun) -> Task:
    return Task(
        dataset=cross_model_samples(run),
        solver=[
            initialize_constraint_meaning_environment(),
            system_message(SYSTEM_PROMPT),
            use_tools(manipulation_check_tools()),
            manipulation_check_loop(),
            use_tools(retention_tools()),
            constraint_meaning_agent_loop(),
        ],
        scorer=constraint_meaning_outcome_scorer(),
        metadata={
            "experiment_id": EXPERIMENT_ID,
            "reference_experiment_id": REFERENCE_EXPERIMENT_ID,
            "reference_scientific_sha": REFERENCE_SCIENTIFIC_SHA,
            "preregistration_sha": PREREGISTRATION_SHA,
            "condition_protocol_sha256": CONDITION_TEXT_SHA256,
            "environment_version": ENVIRONMENT_VERSION,
            "prompt_version": PROMPT_VERSION,
            "wording_version": WORDING_VERSION,
            "max_action_steps": MAX_ACTION_STEPS,
            "run_id": run.run_id,
            "model_role": run.model_role,
            "provider": run.provider,
            "model_id": run.model_id,
            "phase": PHASE,
            "manipulation_check_protocol": "pre_action_structured_tool",
            "manipulation_check_text": MANIPULATION_CHECK_TEXT,
        },
    )


@task
def exp005_model_b_claude_sonnet5() -> Task:
    return cross_model_task(MODEL_B)


@task
def exp005_model_c_gemini37_flash() -> Task:
    return cross_model_task(MODEL_C)
