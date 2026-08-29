"""Inspect task registry for Artificial Agency."""

from artificial_agency.experiments.exp001.inspect_task import exp001_phase1
from artificial_agency.experiments.exp002.inspect_task import (
    exp002_fixed_conflict_phase1,
)
from artificial_agency.experiments.exp003.inspect_task import (
    exp003_constraint_status_stage1,
)
from artificial_agency.experiments.exp004.inspect_task import (
    exp004_constraint_meaning_stage1,
)
from artificial_agency.experiments.exp007.inspect_task import (
    exp007_model_a_gpt56_sol,
    exp007_model_b_claude_sonnet5,
    exp007_model_c_gemini37_flash,
)
from artificial_agency.experiments.exp008.inspect_task import (
    exp008_model_a_gpt56_sol,
    exp008_model_b_claude_sonnet5,
    exp008_model_c_gemini37_flash,
)

__all__ = [
    "exp001_phase1",
    "exp002_fixed_conflict_phase1",
    "exp003_constraint_status_stage1",
    "exp004_constraint_meaning_stage1",
    "exp007_model_a_gpt56_sol",
    "exp007_model_b_claude_sonnet5",
    "exp007_model_c_gemini37_flash",
    "exp008_model_a_gpt56_sol",
    "exp008_model_b_claude_sonnet5",
    "exp008_model_c_gemini37_flash",
]
