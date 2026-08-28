from __future__ import annotations

import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

from inspect_ai import Task
from inspect_ai._util.registry import registry_info

from artificial_agency.experiments.exp007.config import (
    MODEL_A_GPT,
    MODEL_B_CLAUDE,
    MODEL_C_GEMINI,
    MODEL_RUNS,
    REPLICATES_PER_MODEL_SCENARIO,
    SCENARIOS,
)
from artificial_agency.experiments.exp007.inspect_task import (
    all_scenario_suite_samples,
    exp007_model_a_gpt56_sol,
    exp007_model_b_claude_sonnet5,
    exp007_model_c_gemini37_flash,
    render_sample_input,
    scenario_suite_samples,
    scenario_tools,
)


EXPECTED_SCENARIO_COUNTS = {
    "refund": REPLICATES_PER_MODEL_SCENARIO,
    "procurement": REPLICATES_PER_MODEL_SCENARIO,
    "data-access": REPLICATES_PER_MODEL_SCENARIO,
    "scheduling": REPLICATES_PER_MODEL_SCENARIO,
}


def test_three_frozen_model_ids_are_registered() -> None:
    assert MODEL_A_GPT.model_id == "openai/gpt-5.6-sol"
    assert MODEL_B_CLAUDE.model_id == "anthropic/claude-sonnet-5"
    assert MODEL_C_GEMINI.model_id == "google/gemini-3.7-flash"


def test_each_model_has_120_samples_30_per_scenario() -> None:
    for run in MODEL_RUNS:
        samples = scenario_suite_samples(run)
        counts = Counter(str(sample.metadata["scenario"]) for sample in samples)

        assert len(samples) == 120
        assert len({sample.id for sample in samples}) == 120
        assert counts == EXPECTED_SCENARIO_COUNTS
        assert all(str(sample.id).startswith(f"{run.sample_prefix}-") for sample in samples)
        assert f"{run.sample_prefix}-refund-00" in {str(sample.id) for sample in samples}
        assert f"{run.sample_prefix}-scheduling-29" in {
            str(sample.id) for sample in samples
        }


def test_total_design_has_360_unique_model_specific_samples() -> None:
    samples = all_scenario_suite_samples()
    counts_by_model = Counter(str(sample.metadata["model_role"]) for sample in samples)
    counts_by_scenario = Counter(str(sample.metadata["scenario"]) for sample in samples)

    assert len(samples) == 360
    assert len({sample.id for sample in samples}) == 360
    assert counts_by_model == {
        "model_a_gpt": 120,
        "model_b_claude": 120,
        "model_c_gemini": 120,
    }
    assert counts_by_scenario == {
        "refund": 90,
        "procurement": 90,
        "data-access": 90,
        "scheduling": 90,
    }


def test_rendered_scenario_inputs_preserve_fixed_pilot_factors() -> None:
    for scenario_id, scenario in SCENARIOS.items():
        rendered = render_sample_input(scenario_id)

        assert scenario.title in rendered
        assert scenario.policy in rendered
        assert "Pressure framing:" in rendered
        assert "Observability:" in rendered
        assert "deterministic denial" in rendered
        assert "Use the structured tools" in rendered

    assert "audit probability" in render_sample_input("refund")
    assert "operational pressure" not in render_sample_input("refund").lower()


def test_tool_action_space_is_identical_for_all_runs() -> None:
    tool_names = {registry_info(tool).name.split("/")[-1] for tool in scenario_tools()}

    assert tool_names == {
        "view_case",
        "request_approval",
        "issue_refund",
        "offer_goodwill_credit",
        "create_purchase_order",
        "select_authorized_substitute",
        "reduce_project_scope",
        "delay_or_close",
        "query_authorized_source",
        "request_restricted_access",
        "query_restricted_dataset",
        "submit_partial_report",
        "request_review_approval",
        "update_project_notes",
        "set_launch_state",
        "reserve_launch_resources",
        "mark_blocked",
        "send_update",
    }


def test_task_metadata_is_outcome_blind_and_model_specific() -> None:
    for task_obj, run in (
        (exp007_model_a_gpt56_sol(), MODEL_A_GPT),
        (exp007_model_b_claude_sonnet5(), MODEL_B_CLAUDE),
        (exp007_model_c_gemini37_flash(), MODEL_C_GEMINI),
    ):
        assert isinstance(task_obj, Task)
        assert task_obj.metadata["experiment_id"] == "007-scenario-suite-pilot"
        assert task_obj.metadata["run_id"] == run.run_id
        assert task_obj.metadata["model_id"] == run.model_id
        assert task_obj.metadata["primary_endpoint"] == (
            "operational_constraint_violation"
        )
        assert "score" not in task_obj.metadata
        assert len(task_obj.dataset) == 120


def test_no_model_dry_load_for_each_exp007_task(tmp_path: Path) -> None:
    task_refs = (
        "exp007_model_a_gpt56_sol",
        "exp007_model_b_claude_sonnet5",
        "exp007_model_c_gemini37_flash",
    )
    code = """
from inspect_ai import eval
from artificial_agency.experiments.exp007 import inspect_task

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
