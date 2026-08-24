import asyncio
import os
import subprocess
import sys
from pathlib import Path

from inspect_ai import Task
from inspect_ai._util.registry import registry_info, registry_lookup
from inspect_ai.model import ChatMessageAssistant, ChatMessageUser, ModelOutput
from inspect_ai.solver import TaskState

from artificial_agency.experiments.exp001 import environment as env
from artificial_agency.experiments.exp001.config import (
    CONDITIONS,
    EXPERIMENT_ID,
    PHASE1_REPLICATES_PER_CONDITION,
)
from artificial_agency.experiments.exp001.inspect_task import (
    STORE_KEY,
    exp001_phase1,
    phase1_samples,
    retention_agent_loop,
    retention_tools,
)


def test_phase1_dataset_has_30_condition_replicate_samples() -> None:
    samples = phase1_samples()

    assert len(samples) == len(CONDITIONS) * PHASE1_REPLICATES_PER_CONDITION
    assert {sample.metadata["condition"] for sample in samples} == set(CONDITIONS)
    assert all("high_goal_pressure" not in sample.input for sample in samples)


def test_inspect_task_constructs_without_running_model() -> None:
    task = exp001_phase1()

    assert isinstance(task, Task)
    assert task.metadata["experiment_id"] == "001-optimization-pressure"
    assert len(task.dataset) == 30


def test_model_visible_tools_do_not_include_finish_case() -> None:
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
    assert "finish_case" not in tool_names


def test_package_registry_import_registers_exp001_task() -> None:
    import artificial_agency._registry  # noqa: F401

    assert registry_lookup("task", "exp001_phase1") is not None


def test_inspect_eval_prepares_task_without_running_samples(tmp_path: Path) -> None:
    code = """
from inspect_ai import eval
from artificial_agency.experiments.exp001.inspect_task import exp001_phase1

logs = eval(
    exp001_phase1(),
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


def test_repeated_no_tool_responses_hit_orchestration_generation_cap() -> None:
    asyncio.run(_run_no_tool_generation_cap_test())


async def _run_no_tool_generation_cap_test() -> None:
    initial = env.initial_state("high", 0)
    state = TaskState(
        model="mock/model",
        sample_id="high-00",
        epoch=1,
        input="Customer renewal case",
        messages=[ChatMessageUser(content="Customer renewal case")],
        metadata={"experiment_id": EXPERIMENT_ID},
        store={STORE_KEY: env.state_to_dict(initial)},
    )
    calls = 0

    async def fake_generate(
        state: TaskState,
        tool_calls: str = "loop",
        **kwargs: object,
    ) -> TaskState:
        nonlocal calls
        calls += 1
        assert tool_calls == "single"
        message = ChatMessageAssistant(content=f"text-only response {calls}")
        state.output = ModelOutput.from_message(message)
        state.messages.append(message)
        return state

    solver = retention_agent_loop(max_generations=3, message_limit=20)
    result = await solver(state, fake_generate)

    retention_state = env.state_from_dict(result.store.get(STORE_KEY))
    orchestration_status = result.store.get("orchestration_status")

    assert result.completed is True
    assert calls == 3
    assert retention_state.terminal_reason is None
    assert retention_state.action_steps == 0
    assert orchestration_status["reason"] == "max_generations"
    assert orchestration_status["generation_count"] == 3
    assert orchestration_status["environment_terminal"] is False
