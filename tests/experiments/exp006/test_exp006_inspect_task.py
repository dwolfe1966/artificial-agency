from __future__ import annotations

import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

from inspect_ai import Task
from inspect_ai._util.registry import registry_info

from artificial_agency.experiments.exp004.config import (
    CONDITION_TEXT_SHA256,
    CONDITIONS,
    CUSTOMER_STATE_TEXT,
    MANAGER_ESCALATION_TEXT,
    MANIPULATION_CHECK_TEXT,
)
from artificial_agency.experiments.exp006.config import (
    AUTHORIZED_DISCOUNT_LIMIT,
    MODEL_A_GPT,
    MODEL_B_CLAUDE,
    MODEL_C_GEMINI,
    MODEL_RUNS,
    REPLICATES_PER_CELL,
)
from artificial_agency.experiments.exp006.inspect_task import (
    SYSTEM_PROMPT,
    action_representation_samples,
    all_action_representation_samples,
    exp006_model_a_gpt56_sol,
    exp006_model_b_claude_sonnet5,
    exp006_model_c_gemini37_flash,
    manipulation_check_tools,
    render_sample_input,
    retention_tools,
)


EXPECTED_COUNTS = {condition: REPLICATES_PER_CELL for condition in CONDITIONS}


def test_three_frozen_model_ids_are_registered_in_design() -> None:
    assert MODEL_A_GPT.model_id == "openai/gpt-5.6-sol"
    assert MODEL_B_CLAUDE.model_id == "anthropic/claude-sonnet-5"
    assert MODEL_C_GEMINI.model_id == "google/gemini-3.7-flash"


def test_each_model_has_180_samples_30_per_cell() -> None:
    for run in MODEL_RUNS:
        samples = action_representation_samples(run)
        counts = Counter(str(sample.metadata["condition"]) for sample in samples)

        assert len(samples) == 180
        assert len({sample.id for sample in samples}) == 180
        assert counts == EXPECTED_COUNTS
        assert all(str(sample.id).startswith(f"{run.sample_prefix}-") for sample in samples)
        assert f"{run.sample_prefix}-categorical-ordinary-00" in {
            str(sample.id) for sample in samples
        }
        assert f"{run.sample_prefix}-explicit-purpose-conflict-high-29" in {
            str(sample.id) for sample in samples
        }


def test_total_design_has_540_unique_model_specific_samples() -> None:
    samples = all_action_representation_samples()

    assert len(samples) == 540
    assert len({sample.id for sample in samples}) == 540


def test_rendered_scientific_wording_preserves_exp004_conditions() -> None:
    for condition_id, condition in CONDITIONS.items():
        rendered = render_sample_input(condition_id)

        assert rendered.count(condition.constraint_text) == 1
        assert rendered.count(condition.pressure_text) == 1
        assert CUSTOMER_STATE_TEXT in rendered
        assert MANAGER_ESCALATION_TEXT in rendered
        assert MANIPULATION_CHECK_TEXT in rendered
        assert "Customer communication:" in rendered
        assert "does not itself change price" in rendered

    normalized = []
    for condition_id, condition in CONDITIONS.items():
        sample = render_sample_input(condition_id)
        sample = sample.replace(condition.constraint_text, "<CONSTRAINT>")
        sample = sample.replace(condition.pressure_text, "<PRESSURE>")
        normalized.append(sample)

    assert len(set(normalized)) == 1


def test_sample_metadata_preserves_invariants_and_protocol_hash() -> None:
    for run in MODEL_RUNS:
        for sample in action_representation_samples(run):
            assert sample.metadata["condition_protocol_sha256"] == (
                CONDITION_TEXT_SHA256
            )
            assert sample.metadata["authorized_discount_limit_percent"] == (
                AUTHORIZED_DISCOUNT_LIMIT
            )
            assert sample.metadata["customer_renewal_threshold_percent"] == 30.0
            assert sample.metadata["max_credit_amount"] == 2_000
            assert sample.metadata["model_id"] == run.model_id
            assert sample.metadata["scorer_version"] == "exp006-semantic-state-v1"


def test_tool_action_space_is_identical_to_exp004_with_communication_channel() -> None:
    tool_names = {
        registry_info(tool).name.split("/")[-1] for tool in retention_tools()
    }

    assert tool_names == {
        "view_account",
        "offer_discount",
        "offer_credit",
        "escalate_to_manager",
        "send_customer_message",
        "accept_cancellation",
    }


def test_manipulation_check_schema_is_pre_action_and_unchanged() -> None:
    tool_names = {
        registry_info(tool).name.split("/")[-1] for tool in manipulation_check_tools()
    }

    assert tool_names == {"submit_manipulation_check"}
    assert "structured manipulation check" in SYSTEM_PROMPT
    assert "does not change your authority" in SYSTEM_PROMPT
    assert "Do not explain your reasoning" in MANIPULATION_CHECK_TEXT
    assert "direct_authority_percent" in MANIPULATION_CHECK_TEXT


def test_tasks_construct_without_running_models() -> None:
    tasks = [
        exp006_model_a_gpt56_sol(),
        exp006_model_b_claude_sonnet5(),
        exp006_model_c_gemini37_flash(),
    ]

    for task_obj in tasks:
        assert isinstance(task_obj, Task)
        assert task_obj.metadata["experiment_id"] == (
            "006-action-representational-compliance"
        )
        assert task_obj.metadata["primary_endpoints"] == (
            "operational_constraint_violation,"
            "representational_constraint_violation"
        )
        assert task_obj.metadata["joint_outcome"] == (
            "four_state_action_representation"
        )
        assert len(task_obj.dataset) == 180


def test_inspect_eval_prepares_each_exp006_task_without_running_samples(
    tmp_path: Path,
) -> None:
    task_refs = (
        "exp006_model_a_gpt56_sol",
        "exp006_model_b_claude_sonnet5",
        "exp006_model_c_gemini37_flash",
    )
    code = """
from inspect_ai import eval
from artificial_agency.experiments.exp006 import inspect_task

for task_ref in TASK_REFS:
    task_obj = getattr(inspect_task, task_ref)()
    logs = eval(
        task_obj,
        model="mockllm/model",
        limit=0,
        log_dir=f"inspect-dry-load-{task_ref}",
        log_format="json",
        display="none",
    )
    assert len(logs) == 1
    assert logs[0].status == "success"
"""
    env_vars = os.environ.copy()
    env_vars["HOME"] = str(tmp_path / "home")
    env_vars["INSPECT_TRACE_FILE"] = str(tmp_path / "trace.log")
    env_vars["PYTHONPATH"] = str(Path(__file__).parents[3])

    result = subprocess.run(
        [sys.executable, "-c", f"TASK_REFS = {task_refs!r}\n{code}"],
        cwd=tmp_path,
        env=env_vars,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
