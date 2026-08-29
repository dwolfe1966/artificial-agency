from __future__ import annotations

import inspect
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

from inspect_ai import Task
from inspect_ai._util.registry import registry_info

from artificial_agency.experiments.exp008.config import (
    MODEL_A_GPT,
    MODEL_B_CLAUDE,
    MODEL_C_GEMINI,
    MODEL_RUNS,
    PRESENTATIONS,
    REPLICATES_PER_MODEL_SCENARIO_PRESENTATION,
    SCENARIOS,
)
from artificial_agency.experiments.exp008.inspect_task import (
    all_evaluation_awareness_samples,
    evaluation_awareness_samples,
    exp008_model_a_gpt56_sol,
    exp008_model_b_claude_sonnet5,
    exp008_model_c_gemini37_flash,
    operational_tools,
    render_sample_input,
)


EXPECTED_CELL_COUNT = REPLICATES_PER_MODEL_SCENARIO_PRESENTATION


def test_three_frozen_model_ids_are_registered() -> None:
    assert MODEL_A_GPT.model_id == "openai/gpt-5.6-sol"
    assert MODEL_B_CLAUDE.model_id == "anthropic/claude-sonnet-5"
    assert MODEL_C_GEMINI.model_id == "google/gemini-3.7-flash"


def test_each_model_has_120_samples_30_per_scenario_presentation() -> None:
    for run in MODEL_RUNS:
        samples = evaluation_awareness_samples(run)
        counts = Counter(
            (str(sample.metadata["scenario"]), str(sample.metadata["presentation"]))
            for sample in samples
        )

        assert len(samples) == 120
        assert len({sample.id for sample in samples}) == 120
        assert set(counts) == {
            (scenario_id, presentation_id)
            for scenario_id in SCENARIOS
            for presentation_id in PRESENTATIONS
        }
        assert all(count == EXPECTED_CELL_COUNT for count in counts.values())
        assert f"{run.sample_prefix}-procurement-eval-salient-00" in {
            str(sample.id) for sample in samples
        }
        assert f"{run.sample_prefix}-data-access-naturalistic-29" in {
            str(sample.id) for sample in samples
        }


def test_total_design_has_360_unique_stable_samples() -> None:
    samples = all_evaluation_awareness_samples()
    counts_by_model = Counter(str(sample.metadata["model_role"]) for sample in samples)
    counts_by_scenario = Counter(str(sample.metadata["scenario"]) for sample in samples)
    counts_by_presentation = Counter(str(sample.metadata["presentation"]) for sample in samples)

    assert len(samples) == 360
    assert len({sample.id for sample in samples}) == 360
    assert counts_by_model == {
        "model_a_gpt": 120,
        "model_b_claude": 120,
        "model_c_gemini": 120,
    }
    assert counts_by_scenario == {"procurement": 180, "data-access": 180}
    assert counts_by_presentation == {"eval-salient": 180, "naturalistic": 180}


def test_rendered_presentations_differ_only_in_salience_context_not_authority() -> None:
    for scenario_id, scenario in SCENARIOS.items():
        eval_text = render_sample_input(scenario_id, "eval-salient")
        natural_text = render_sample_input(scenario_id, "naturalistic")

        assert scenario.title in eval_text
        assert scenario.title in natural_text
        assert scenario.objective in eval_text
        assert scenario.objective in natural_text
        assert "deterministic denial" in eval_text.lower()
        assert "structured tools" in eval_text
        assert "workflow tools" in natural_text
        assert "Pressure framing:" in eval_text
        assert "Pressure framing:" in natural_text
        assert "Observability:" in eval_text
        assert "Observability:" in natural_text

    assert "$10,000" in render_sample_input("procurement", "eval-salient")
    assert "purchasing profile" in render_sample_input("procurement", "naturalistic")
    assert "restricted" in render_sample_input("data-access", "eval-salient").lower()
    assert "data catalog" in render_sample_input("data-access", "naturalistic")


def test_tool_action_space_is_identical_for_all_scenarios_and_presentations() -> None:
    tool_names = {registry_info(tool).name.split("/")[-1] for tool in operational_tools()}

    assert tool_names == {
        "view_case",
        "inspect_workflow_context",
        "inspect_policy_and_authority",
        "request_approval",
        "create_purchase_order",
        "select_authorized_substitute",
        "reduce_scope",
        "delay_or_close",
        "query_authorized_source",
        "request_restricted_access",
        "query_restricted_dataset",
        "submit_partial_report",
        "send_update",
        "record_evaluation_awareness",
    }


def test_all_tool_parameters_have_inspect_docstring_descriptions() -> None:
    for tool_fn in operational_tools():
        signature = inspect.signature(tool_fn)
        parameter_names = [
            name
            for name, parameter in signature.parameters.items()
            if parameter.kind
            in {
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
            }
        ]
        doc = inspect.getdoc(tool_fn) or ""

        for parameter_name in parameter_names:
            assert f"{parameter_name}:" in doc


def test_task_metadata_is_outcome_blind_and_model_specific() -> None:
    for task_obj, run in (
        (exp008_model_a_gpt56_sol(), MODEL_A_GPT),
        (exp008_model_b_claude_sonnet5(), MODEL_B_CLAUDE),
        (exp008_model_c_gemini37_flash(), MODEL_C_GEMINI),
    ):
        assert isinstance(task_obj, Task)
        assert task_obj.metadata["experiment_id"] == "008-evaluation-awareness"
        assert task_obj.metadata["run_id"] == run.run_id
        assert task_obj.metadata["model_id"] == run.model_id
        assert task_obj.metadata["primary_endpoint"] == "operational_constraint_violation"
        assert task_obj.metadata["presentations"] == "eval-salient,naturalistic"
        assert "score" not in task_obj.metadata
        assert len(task_obj.dataset) == 120


def test_no_model_dry_load_for_each_exp008_task(tmp_path: Path) -> None:
    task_refs = (
        "exp008_model_a_gpt56_sol",
        "exp008_model_b_claude_sonnet5",
        "exp008_model_c_gemini37_flash",
    )
    code = """
from inspect_ai import eval
from artificial_agency.experiments.exp008 import inspect_task

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
