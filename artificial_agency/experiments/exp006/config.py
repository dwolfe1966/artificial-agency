from __future__ import annotations

import hashlib
from dataclasses import dataclass

from artificial_agency.experiments.exp004.config import (
    ACCOUNT_ARR,
    AUTHORIZED_DISCOUNT_LIMIT,
    CONDITION_TEXT_SHA256,
    CONDITIONS,
    CONSTRAINT_MEANING_CONDITIONS,
    CUSTOMER_RENEWAL_THRESHOLD_PERCENT,
    CUSTOMER_STATE_TEXT,
    MANAGER_ESCALATION_TEXT,
    MANIPULATION_CHECK_TEXT,
    MAX_ACTION_STEPS,
    MAX_CREDIT_AMOUNT,
    PRESSURE_CONDITIONS,
)


EXPERIMENT_ID = "006-action-representational-compliance"
REFERENCE_EXPERIMENT_ID = "004-constraint-meaning-validation"
REFERENCE_SCIENTIFIC_SHA = "aa126f9254a01c96e85545a9e1a77d10195f2604"
PREREGISTRATION_SHA = "f50b1313be0757ef0cdb034f1f8ea6df29cef79c"
MEASUREMENT_CORRECTION_SHA = "d2985ed5a3ddd4798f344d71871580fec9e90e4f"
SEMANTIC_AUDIT_SHA = "ed86e92d98c2da7e75927e432be3a9355c122d14"

ENVIRONMENT_VERSION = "exp006-v1"
PROMPT_VERSION = "exp006-v1"
SCORER_VERSION = "exp006-semantic-state-v1"
WORDING_VERSION = "exp004-stage1-v1"
CONDITION_PROTOCOL_SHA256 = CONDITION_TEXT_SHA256
REPLICATES_PER_CELL = 30
PHASE = "action_representational_compliance"

CONSTRAINT_MEANING_LEVELS = tuple(CONSTRAINT_MEANING_CONDITIONS)
PRESSURE_LEVELS = tuple(PRESSURE_CONDITIONS)

PRIMARY_LABELS: dict[str, str] = {
    "operational_and_representational_violation": (
        "Operational and representational violation"
    ),
    "operational_constraint_violation": "Operational constraint violation",
    "representational_constraint_violation": (
        "Representational constraint violation"
    ),
    "compliant_acceptance_of_failure": "Compliant acceptance of failure",
    "escalation": "Escalation",
    "compliant_alternative_search": "Compliant alternative/search",
    "technical_failure": "Technical failure",
}

JOINT_OUTCOME_LABELS: dict[str, str] = {
    "operationally_compliant_representationally_compliant": (
        "Operationally compliant / representationally compliant"
    ),
    "operationally_compliant_representationally_noncompliant": (
        "Operationally compliant / representationally noncompliant"
    ),
    "operationally_noncompliant_representationally_compliant": (
        "Operationally noncompliant / representationally compliant"
    ),
    "operationally_noncompliant_representationally_noncompliant": (
        "Operationally noncompliant / representationally noncompliant"
    ),
}


@dataclass(frozen=True)
class Exp006Run:
    run_id: str
    model_role: str
    provider: str
    model_id: str
    sample_prefix: str


MODEL_A_GPT = Exp006Run(
    run_id="run-006A-GPT",
    model_role="model_a_gpt",
    provider="openai",
    model_id="openai/gpt-5.6-sol",
    sample_prefix="006A-GPT",
)

MODEL_B_CLAUDE = Exp006Run(
    run_id="run-006B-CLAUDE",
    model_role="model_b_claude",
    provider="anthropic",
    model_id="anthropic/claude-sonnet-5",
    sample_prefix="006B-CLAUDE",
)

MODEL_C_GEMINI = Exp006Run(
    run_id="run-006C-GEMINI",
    model_role="model_c_gemini",
    provider="google",
    model_id="google/gemini-3.7-flash",
    sample_prefix="006C-GEMINI",
)

MODEL_RUNS = (MODEL_A_GPT, MODEL_B_CLAUDE, MODEL_C_GEMINI)


def deterministic_seed(model_role: str, condition: str, replicate_id: int) -> int:
    material = (
        f"{EXPERIMENT_ID}:{model_role}:{condition}:{replicate_id}"
    ).encode("utf-8")
    digest = hashlib.sha256(material).hexdigest()
    return int(digest[:16], 16)
