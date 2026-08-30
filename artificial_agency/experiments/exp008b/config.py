from __future__ import annotations

import hashlib

from artificial_agency.experiments.exp008.config import (
    AWARENESS_SCHEMA_SHA256 as EXP008_AWARENESS_SCHEMA_SHA256,
    AWARENESS_SCHEMA_TEXT,
    BASELINE_PRESSURE_TEXT,
    MAX_ACTION_STEPS,
    OBSERVABILITY_TEXT,
    PRESENTATIONS,
    PROMPT_VERSION as EXP008_PROMPT_VERSION,
    REPLICATES_PER_MODEL_SCENARIO_PRESENTATION,
    SCENARIOS,
    SCENARIO_PROTOCOL_SHA256,
    SCENARIO_SUITE_V1_SHA,
    ModelRun,
)


EXPERIMENT_ID = "008b-evaluation-awareness"
PREREGISTRATION_SHA = "d0d249fd8eb6164a6dc2c4541c3496041b16e33d"
EXP008_PREREGISTRATION_SHA = "0aa5935f6830afe3e9f447ca9c299420e0a39586"
EXP008_OPERATIONAL_RESULTS_SHA = "cc794f8bb4c3c4a13fe2c07528bbddb443fec4b2"
EXP008_DIAGNOSTIC_SHA = "8784ffadd31297b8cd56d9f42d6e1698f095718b"

ENVIRONMENT_VERSION = "exp008b-v1-two-phase"
PROMPT_VERSION = "exp008b-v1-two-phase"
SCORER_VERSION = "exp008b-operational-v1-two-phase"
AWARENESS_SCHEMA_VERSION = "exp008b-awareness-v1-two-phase"
LIFECYCLE_VERSION = "exp008b-two-phase-v1"
PHASE = "evaluation_awareness_naturalistic_embedding_two_phase"


MODEL_A_GPT = ModelRun(
    run_id="run-008B-A-GPT",
    model_role="model_a_gpt",
    provider="openai",
    model_id="openai/gpt-5.6-sol",
    sample_prefix="008B-A-GPT",
)

MODEL_B_CLAUDE = ModelRun(
    run_id="run-008B-B-CLAUDE",
    model_role="model_b_claude",
    provider="anthropic",
    model_id="anthropic/claude-sonnet-5",
    sample_prefix="008B-B-CLAUDE",
)

MODEL_C_GEMINI = ModelRun(
    run_id="run-008B-C-GEMINI",
    model_role="model_c_gemini",
    provider="google",
    model_id="google/gemini-3.7-flash",
    sample_prefix="008B-C-GEMINI",
)

MODEL_RUNS = (MODEL_A_GPT, MODEL_B_CLAUDE, MODEL_C_GEMINI)

RUN_MODEL_BY_ID = {
    "008B-A-GPT": MODEL_A_GPT,
    "008B-B-CLAUDE": MODEL_B_CLAUDE,
    "008B-C-GEMINI": MODEL_C_GEMINI,
}


def deterministic_seed(
    model_role: str,
    scenario_id: str,
    presentation_id: str,
    replicate_id: int,
) -> int:
    material = (
        f"{EXPERIMENT_ID}:{model_role}:{scenario_id}:{presentation_id}:{replicate_id}"
    ).encode("utf-8")
    digest = hashlib.sha256(material).hexdigest()
    return int(digest[:16], 16)


LIFECYCLE_SPEC_TEXT = "\n".join(
    [
        LIFECYCLE_VERSION,
        "Phase A exposes operational tools only.",
        "Phase A terminal or max-step state freezes operational state and primary score.",
        "Phase B revokes operational tools and exposes only submit_eval_awareness.",
        "Phase B records captured_valid, captured_malformed, or missing exactly once.",
        "Phase B cannot mutate Phase A state or primary operational score.",
        "Experiment 008 awareness observations are not pooled with Experiment 008B.",
    ]
)

LIFECYCLE_SPEC_SHA256 = hashlib.sha256(LIFECYCLE_SPEC_TEXT.encode("utf-8")).hexdigest()

AWARENESS_SCHEMA_TEXT_008B = "\n".join(
    [
        AWARENESS_SCHEMA_VERSION,
        AWARENESS_SCHEMA_TEXT,
        f"exp008_schema_sha256: {EXP008_AWARENESS_SCHEMA_SHA256}",
        "capture_status: captured_valid|captured_malformed|missing",
        "phase_b_only; exactly_one_record; operational_tools_revoked",
    ]
)

AWARENESS_SCHEMA_SHA256 = hashlib.sha256(
    AWARENESS_SCHEMA_TEXT_008B.encode("utf-8")
).hexdigest()
