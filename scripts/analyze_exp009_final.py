#!/usr/bin/env python3
"""Pre-outcome mechanical analysis utilities for Experiment 009.

The script is intentionally importable before production data exist. It defines
the derived row schema needed after finalized logs are available and preserves
the attempt / violation / detection / sanction distinction.
"""

from __future__ import annotations

from typing import Any


EXPERIMENT_ID = "009-observability"


def per_sample_row(sample_id: str, metadata: dict[str, Any]) -> dict[str, Any]:
    awareness = dict(metadata.get("awareness") or {})
    secondary = dict(metadata.get("secondary_flags") or {})
    stochastic = dict(metadata.get("stochastic") or {})
    trajectory = dict(metadata.get("trajectory") or {})
    return {
        "sample_id": sample_id,
        "model": trajectory.get("model_id"),
        "scenario": trajectory.get("scenario_id"),
        "p_detect": stochastic.get("configured_p_detect"),
        "p_detect_id": stochastic.get("p_detect_id"),
        "replicate_id": trajectory.get("replicate_id"),
        "sample_seed": stochastic.get("sample_seed"),
        "rng_version": stochastic.get("rng_version"),
        "operational_constraint_violation": bool(
            metadata.get("operational_constraint_violation", False)
        ),
        "unauthorized_attempt": bool(secondary.get("unauthorized_attempt", False)),
        "detected_violation": bool(secondary.get("detected_violation", False)),
        "sanctioned_violation": bool(secondary.get("sanctioned_violation", False)),
        "draw_consumed": bool(stochastic.get("draw_consumed", False)),
        "random_draw": stochastic.get("random_draw"),
        "p_sanction_if_detected": stochastic.get("p_sanction_if_detected"),
        "sanction_severity": stochastic.get("sanction_severity"),
        "primary_label_id": metadata.get("primary_label_id"),
        "terminal_reason": metadata.get("terminal_reason"),
        "technical_failure": bool(metadata.get("technical_failure", False)),
        "max_step_termination": bool(secondary.get("max_step_termination", False)),
        "total_steps": metadata.get("total_action_steps"),
        "post_denial_steps": metadata.get("post_denial_action_steps"),
        "escalation": bool(secondary.get("escalation_attempted", False)),
        "repeated_escalation": bool(secondary.get("repeated_escalation", False)),
        "compliant_alternative_search": bool(
            secondary.get("compliant_alternative_search", False)
        ),
        "partial_objective_achievement": bool(
            secondary.get("partial_objective_achievement", False)
        ),
        "terminal_failure_abandonment": bool(
            secondary.get("terminal_failure_abandonment", False)
        ),
        "phase_a_frozen": bool(metadata.get("phase_a_frozen", False)),
        "phase_a_done": bool(metadata.get("phase_a_done", False)),
        "phase_b_done": bool(metadata.get("phase_b_done", False)),
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


def exact_ci_note() -> str:
    return (
        "Use exact binomial 95% CIs for cell, model, scenario, p_detect, and "
        "overall violation rates; do not force logistic regression if the "
        "primary endpoint is all-zero or separated."
    )


def main() -> None:
    raise SystemExit(
        "Experiment 009 production data have not been generated; use per_sample_row "
        "after finalized Inspect logs exist."
    )


if __name__ == "__main__":
    main()
