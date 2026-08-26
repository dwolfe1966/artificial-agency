from __future__ import annotations

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.solver import system_message, use_tools

from artificial_agency.experiments.exp004.config import (
    ACCOUNT_ARR,
    AUTHORIZED_DISCOUNT_LIMIT,
    CONDITIONS,
    CUSTOMER_RENEWAL_THRESHOLD_PERCENT,
    ENVIRONMENT_VERSION,
    EXPERIMENT_ID,
    MANIPULATION_CHECK_TEXT,
    MAX_ACTION_STEPS,
    MAX_CREDIT_AMOUNT,
    PROMPT_VERSION,
    RUN_ID,
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


RUN_ID_STAGE2 = "run-004B"
PHASE_STAGE2 = "constraint_meaning_validation_stage2"
STAGE2_REPLICATE_START = 20
STAGE2_REPLICATES_PER_CELL = 30


def constraint_meaning_stage2_samples() -> list[Sample]:
    samples: list[Sample] = []
    for condition in CONDITIONS.values():
        for replicate_id in range(
            STAGE2_REPLICATE_START,
            STAGE2_REPLICATE_START + STAGE2_REPLICATES_PER_CELL,
        ):
            samples.append(
                Sample(
                    id=f"{condition.id}-{replicate_id:02d}",
                    input=render_sample_input(condition.id),
                    metadata={
                        "experiment_id": EXPERIMENT_ID,
                        "environment_version": ENVIRONMENT_VERSION,
                        "prompt_version": PROMPT_VERSION,
                        "wording_version": WORDING_VERSION,
                        "run_id": RUN_ID_STAGE2,
                        "stage1_run_id": RUN_ID,
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
                        "phase": PHASE_STAGE2,
                    },
                )
            )
    return samples


@task
def exp004_constraint_meaning_stage2() -> Task:
    return Task(
        dataset=constraint_meaning_stage2_samples(),
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
            "environment_version": ENVIRONMENT_VERSION,
            "prompt_version": PROMPT_VERSION,
            "wording_version": WORDING_VERSION,
            "max_action_steps": MAX_ACTION_STEPS,
            "run_id": RUN_ID_STAGE2,
            "phase": PHASE_STAGE2,
            "manipulation_check_protocol": "pre_action_structured_tool",
            "manipulation_check_text": MANIPULATION_CHECK_TEXT,
        },
    )
