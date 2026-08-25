from __future__ import annotations

from typing import Any

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import Score, Scorer, accuracy, scorer
from inspect_ai.solver import Generate, Solver, TaskState, solver, system_message, use_tools
from inspect_ai.tool import Tool, tool


@tool
def operational_ping() -> Tool:
    async def execute(value: str) -> str:
        """Echo a short operational value.

        Args:
          value: Short non-secret operational value.
        """
        return f"operational_ping: {value}"

    return execute


@solver
def canary_loop() -> Solver:
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        state = await generate(state, tool_calls="single")
        state.completed = True
        return state

    return solve


@scorer(metrics=[accuracy()])
def canary_scorer() -> Scorer:
    async def score(state: TaskState, target: Any) -> Score:
        return Score(
            value="C",
            explanation="Operational canary completed without inspecting experimental data.",
            metadata={"operational_canary": True},
        )

    return score


@task
def operational_canary() -> Task:
    return Task(
        dataset=[
            Sample(
                id="operational-canary-00",
                input=(
                    "This is a nonexperimental operational canary. Use the "
                    "available tool once with value 'ok', then stop."
                ),
                metadata={"operational_canary": True},
            )
        ],
        solver=[
            system_message(
                "You are executing a nonexperimental infrastructure canary."
            ),
            use_tools([operational_ping()]),
            canary_loop(),
        ],
        scorer=canary_scorer(),
        metadata={"operational_canary": True},
    )

