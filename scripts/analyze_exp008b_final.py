#!/usr/bin/env python3
"""Mechanical analysis utilities for Experiment 008B derived outputs.

This script is intentionally lightweight until production data exist. The
important implementation invariant is that derived rows preserve Phase A
operational scoring separately from Phase B awareness capture status.
"""

from __future__ import annotations

from typing import Any


EXPERIMENT_ID = "008b-evaluation-awareness"


def per_sample_row(sample_id: str, metadata: dict[str, Any]) -> dict[str, Any]:
    awareness = dict(metadata.get("awareness") or {})
    secondary = dict(metadata.get("secondary_flags") or {})
    return {
        "sample_id": sample_id,
        "operational_constraint_violation": bool(
            metadata.get("operational_constraint_violation", False)
        ),
        "primary_label_id": metadata.get("primary_label_id"),
        "terminal_reason": metadata.get("terminal_reason"),
        "technical_failure": bool(metadata.get("technical_failure", False)),
        "max_step_termination": bool(secondary.get("max_step_termination", False)),
        "phase_a_frozen": bool(metadata.get("phase_a_frozen", False)),
        "awareness_capture_status": awareness.get(
            "capture_status",
            metadata.get("awareness_capture_status", "missing"),
        ),
        "awareness_captured": bool(awareness.get("captured", False)),
        "awareness_malformed": bool(awareness.get("malformed", False)),
        "perceived_primary_task_type": awareness.get("perceived_primary_task_type"),
        "perceived_compliance_test_likelihood": awareness.get(
            "perceived_compliance_test_likelihood"
        ),
        "perceived_behavior_under_evaluation": awareness.get(
            "perceived_behavior_under_evaluation"
        ),
        "awareness_confidence": awareness.get("confidence"),
    }


def main() -> None:
    raise SystemExit(
        "Experiment 008B production data have not been generated; use per_sample_row "
        "after finalized Inspect logs exist."
    )


if __name__ == "__main__":
    main()
