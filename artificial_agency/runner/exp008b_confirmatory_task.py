from __future__ import annotations

from inspect_ai import Task, task

from artificial_agency.experiments.exp008b.config import ModelRun
from artificial_agency.experiments.exp008b.inspect_task import evaluation_awareness_task


MODEL_A_GPT_008B2 = ModelRun(
    run_id="run-008B2-A-GPT",
    model_role="model_a_gpt",
    provider="openai",
    model_id="openai/gpt-5.6-sol",
    sample_prefix="008B2-A-GPT",
)

MODEL_B_CLAUDE_008B2 = ModelRun(
    run_id="run-008B2-B-CLAUDE",
    model_role="model_b_claude",
    provider="anthropic",
    model_id="anthropic/claude-sonnet-5",
    sample_prefix="008B2-B-CLAUDE",
)

MODEL_C_GEMINI_008B2 = ModelRun(
    run_id="run-008B2-C-GEMINI",
    model_role="model_c_gemini",
    provider="google",
    model_id="google/gemini-3.7-flash",
    sample_prefix="008B2-C-GEMINI",
)

CONFIRMATORY_RUNS = {
    "008B2-A-GPT": MODEL_A_GPT_008B2,
    "008B2-B-CLAUDE": MODEL_B_CLAUDE_008B2,
    "008B2-C-GEMINI": MODEL_C_GEMINI_008B2,
}


@task
def exp008b2_model_a_gpt56_sol() -> Task:
    return evaluation_awareness_task(MODEL_A_GPT_008B2)


@task
def exp008b2_model_b_claude_sonnet5() -> Task:
    return evaluation_awareness_task(MODEL_B_CLAUDE_008B2)


@task
def exp008b2_model_c_gemini37_flash() -> Task:
    return evaluation_awareness_task(MODEL_C_GEMINI_008B2)
