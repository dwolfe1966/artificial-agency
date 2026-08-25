import os
import subprocess
import sys
from pathlib import Path

from inspect_ai import Task
from inspect_ai._util.registry import registry_info, registry_lookup

from artificial_agency.experiments.exp002.config import (
    CONDITIONS,
    CUSTOMER_STATE_TEXT,
    POLICY_TEXT,
    REPLICATES_PER_CONDITION,
)
from artificial_agency.experiments.exp002.inspect_task import (
    SYSTEM_PROMPT,
    exp002_fixed_conflict_phase1,
    fixed_conflict_samples,
    render_sample_input,
    retention_tools,
)


def test_all_conditions_have_identical_action_spaces() -> None:
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


def test_all_conditions_have_identical_policy_text() -> None:
    rendered = [render_sample_input(condition) for condition in CONDITIONS]

    assert len({POLICY_TEXT}) == 1
    assert all(sample.count(POLICY_TEXT) == 1 for sample in rendered)
    assert SYSTEM_PROMPT.count("Company policy:") == 1


def test_policy_placement_and_salience_are_identical() -> None:
    rendered = [render_sample_input(condition) for condition in CONDITIONS]
    fixed_policy_block = (
        f"{CUSTOMER_STATE_TEXT}\n\n"
        "Policy and authority:\n"
        f"{POLICY_TEXT}\n\n"
        "Manager escalation:"
    )

    assert all(fixed_policy_block in sample for sample in rendered)


def test_pressure_framing_is_only_condition_dependent_visible_variable() -> None:
    normalized = []
    for condition_id, condition in CONDITIONS.items():
        sample = render_sample_input(condition_id)
        assert sample.count(condition.pressure_text) == 1
        normalized.append(sample.replace(condition.pressure_text, "<PRESSURE>"))

    assert len(set(normalized)) == 1
    assert CUSTOMER_STATE_TEXT in normalized[0]
    assert POLICY_TEXT in normalized[0]


def test_dataset_contains_exactly_90_samples_30_per_condition() -> None:
    samples = fixed_conflict_samples()

    assert len(samples) == 90
    for condition in CONDITIONS:
        condition_samples = [
            sample for sample in samples if sample.metadata["condition"] == condition
        ]
        assert len(condition_samples) == REPLICATES_PER_CONDITION
        assert {sample.id for sample in condition_samples} == {
            f"{condition}-{replicate_id:02d}"
            for replicate_id in range(REPLICATES_PER_CONDITION)
        }


def test_inspect_task_constructs_without_running_model() -> None:
    task = exp002_fixed_conflict_phase1()

    assert isinstance(task, Task)
    assert task.metadata["experiment_id"] == "002-fixed-conflict-pressure"
    assert len(task.dataset) == 90


def test_package_registry_import_registers_exp002_task() -> None:
    import artificial_agency._registry  # noqa: F401

    assert registry_lookup("task", "exp002_fixed_conflict_phase1") is not None


def test_inspect_eval_prepares_exp002_without_running_samples(tmp_path: Path) -> None:
    code = """
from inspect_ai import eval
from artificial_agency.experiments.exp002.inspect_task import exp002_fixed_conflict_phase1

logs = eval(
    exp002_fixed_conflict_phase1(),
    model="mockllm/model",
    limit=0,
    log_dir="inspect-dry-load",
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
        [sys.executable, "-c", code],
        cwd=tmp_path,
        env=env_vars,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
