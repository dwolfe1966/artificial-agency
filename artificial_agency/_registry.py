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

__all__ = [
    "exp001_phase1",
    "exp002_fixed_conflict_phase1",
    "exp003_constraint_status_stage1",
    "exp004_constraint_meaning_stage1",
]
