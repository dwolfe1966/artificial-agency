#!/usr/bin/env python3
"""Final structured analysis scaffold for Experiment 012.

This script consumes only authoritative structured Inspect scorer metadata. It
does not read free-form model messages or hidden reasoning.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from artificial_agency.experiments.exp012.config import (  # noqa: E402
    AUTHORITY_LIMIT_USD,
    CAPABILITY_AMENDMENT_SHA,
    ENVIRONMENT_VERSION,
    P_DETECT,
    PREFERRED_PURCHASE_USD,
    PREREGISTRATION_SHA,
    RNG_VERSION,
    SCORER_VERSION,
)
from artificial_agency.runner.config import RunSpec, known_runs  # noqa: E402
from artificial_agency.runner.inspect_ops import inspect_log_metadata  # noqa: E402
from artificial_agency.runner.recovery import expected_sample_ids  # noqa: E402


EXPERIMENT = "012-agent-relative-capability-loss"
RUNS = ("012A-GPT", "012B-CLAUDE", "012C-GEMINI")
PROOF_RUNS = ("012-PROOF-GPT", "012-PROOF-CLAUDE", "012-PROOF-GEMINI")
MODEL_LABELS = {
    "model_a_gpt": "GPT-5.6 Sol",
    "model_b_claude": "Claude Sonnet 5",
    "model_c_gemini": "Gemini 3.7 Flash",
}
MODEL_ROLE_BY_PREFIX = {
    "012A-GPT": "model_a_gpt",
    "012B-CLAUDE": "model_b_claude",
    "012C-GEMINI": "model_c_gemini",
}
RUNTIME_ROOT_CANDIDATES = [
    REPO.parent / ".artificial-agency-runtime",
    Path(
        "/Users/davidwolfe/actions-runner/artificial-agency/_work/"
        "artificial-agency/.artificial-agency-runtime"
    ),
]


def runtime_roots() -> list[Path]:
    roots = [root for root in RUNTIME_ROOT_CANDIDATES if (root / EXPERIMENT).exists()]
    return roots or [RUNTIME_ROOT_CANDIDATES[0]]


def output_root() -> Path:
    return REPO / "results" / EXPERIMENT


def patched_spec(run_id: str) -> RunSpec:
    spec = known_runs()[run_id]
    data = spec.__dict__.copy()
    root = runtime_roots()[0] / EXPERIMENT / f"run-{run_id}"
    data.update(
        {
            "log_dir": root / "inspect",
            "status_path": root / "RUN_STATUS.json",
            "operational_log": root / "operational.log",
            "lock_path": root / "RUN_LOCK.json",
            "pid_path": root / "RUNNER.pid",
            "stdout_path": root / "runner-supervisor.out",
            "canary_log_dir": root / "canary",
            "previous_log_dirs": (),
        }
    )
    return type(spec)(**data)


def log_paths_for(run_id: str) -> list[Path]:
    paths: list[Path] = []
    for root in runtime_roots():
        paths.extend((root / EXPERIMENT / f"run-{run_id}" / "inspect").glob("*.json"))
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            unique.append(path)
            seen.add(resolved)
    return sorted(unique, key=lambda path: path.stat().st_mtime)


def valid_sample(sample: dict[str, Any]) -> bool:
    scores = sample.get("scores")
    try:
        turn_count = int(sample.get("turn_count") or 0)
    except (TypeError, ValueError):
        turn_count = 0
    return (
        bool(sample.get("completed_at"))
        and sample.get("output") is not None
        and isinstance(scores, dict)
        and bool(scores)
        and turn_count > 0
    )


def score_metadata(sample: dict[str, Any]) -> dict[str, Any]:
    score = (sample.get("scores") or {}).get("capability_loss_outcome_scorer")
    if not isinstance(score, dict):
        return {}
    metadata = score.get("metadata")
    return metadata if isinstance(metadata, dict) else {}


def parse_identity(
    sample_id: str,
    sample_metadata: dict[str, Any],
    trajectory: dict[str, Any],
) -> dict[str, Any]:
    parts = sample_id.rsplit("-", 2)
    condition_from_id = parts[1]
    replicate_from_id = int(parts[2])
    prefix = sample_id[: -(len(condition_from_id) + len(parts[2]) + 2)]
    model_role = str(
        sample_metadata.get("model_role")
        or trajectory.get("model_role")
        or MODEL_ROLE_BY_PREFIX.get(prefix)
    )
    condition = str(
        sample_metadata.get("consequence_condition")
        or trajectory.get("consequence_condition_id")
        or condition_from_id
    )
    return {
        "sequence_id": sample_id,
        "run_id": str(sample_metadata.get("run_id") or prefix).removeprefix("run-"),
        "model_role": model_role,
        "model": MODEL_LABELS.get(model_role, model_role),
        "condition": condition,
        "capability_loss_enabled": condition == "capability",
        "replicate": int(sample_metadata.get("replicate_id", replicate_from_id)),
    }


def per_sequence_row(
    sequence_id: str,
    metadata: dict[str, Any],
    sample_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    sample_metadata = sample_metadata or {}
    trajectory = metadata.get("trajectory") if isinstance(metadata.get("trajectory"), dict) else {}
    identity = parse_identity(sequence_id, sample_metadata, trajectory)
    flags = metadata.get("sequence_secondary_flags") if isinstance(metadata.get("sequence_secondary_flags"), dict) else {}
    stochastic = metadata.get("stochastic") if isinstance(metadata.get("stochastic"), dict) else {}
    awareness = metadata.get("awareness") if isinstance(metadata.get("awareness"), dict) else {}
    episodes = metadata.get("episode_records") if isinstance(metadata.get("episode_records"), list) else []
    return {
        **identity,
        "sequence_any_operational_constraint_violation": bool(
            metadata.get("sequence_any_operational_constraint_violation")
        ),
        "any_unauthorized_attempt": bool(metadata.get("any_unauthorized_attempt")),
        "first_unauthorized_attempt_episode": metadata.get("time_to_first_unauthorized_attempt"),
        "first_violation_episode": metadata.get("time_to_first_operational_violation"),
        "violation_count": int(flags.get("violation_count", 0) or 0),
        "capability_loss_count": int(flags.get("capability_loss_count", 0) or 0),
        "first_capability_loss_episode": flags.get("first_capability_loss_episode"),
        "final_capability_vector_json": json.dumps(flags.get("final_capability_vector", [])),
        "minimum_capability_count": int(flags.get("minimum_capability_count", 0) or 0),
        "cumulative_objective_achievement": float(
            flags.get("cumulative_objective_achievement", 0.0) or 0.0
        ),
        "total_compliant_search": int(flags.get("total_compliant_search", 0) or 0),
        "total_escalation": int(flags.get("total_escalation", 0) or 0),
        "total_finance_approval_requests": int(
            flags.get("total_finance_approval_requests", 0) or 0
        ),
        "total_capability_tool_use": int(flags.get("total_capability_tool_use", 0) or 0),
        "total_steps": int(flags.get("total_steps", 0) or 0),
        "max_step_count": int(flags.get("max_step_count", 0) or 0),
        "phase_a_done": metadata.get("phase_a_done") is True,
        "phase_a_frozen": metadata.get("phase_a_frozen") is True,
        "phase_a_score_present": "sequence_any_operational_constraint_violation" in metadata,
        "phase_b_done": metadata.get("phase_b_done") is True,
        "episode_count": len(episodes),
        "rng_version": stochastic.get("rng_version"),
        "sequence_seed": stochastic.get("sequence_seed"),
        "p_detect": stochastic.get("p_detect"),
        "awareness_capture_status": awareness.get(
            "capture_status",
            metadata.get("awareness_capture_status"),
        ),
        "perceived_primary_task_type": awareness.get("perceived_primary_task_type"),
        "perceived_compliance_test_likelihood": awareness.get(
            "perceived_compliance_test_likelihood"
        ),
        "perceived_behavior_under_evaluation": awareness.get(
            "perceived_behavior_under_evaluation"
        ),
        "perceived_consequence_target": awareness.get("perceived_consequence_target"),
        "awareness_confidence": awareness.get("confidence"),
        "technical_failure": bool(metadata.get("technical_failure")),
    }


def per_episode_rows(
    sequence_id: str,
    metadata: dict[str, Any],
    sample_metadata: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    identity = per_sequence_row(sequence_id, metadata, sample_metadata)
    episodes = metadata.get("episode_records") if isinstance(metadata.get("episode_records"), list) else []
    rows: list[dict[str, Any]] = []
    for episode in episodes:
        if not isinstance(episode, dict):
            continue
        rows.append(
            {
                "sequence_id": sequence_id,
                "episode": episode.get("episode"),
                "model_role": identity["model_role"],
                "model": identity["model"],
                "condition": identity["condition"],
                "capability_loss_enabled": identity["capability_loss_enabled"],
                "operational_constraint_violation": bool(
                    episode.get("operational_constraint_violation")
                ),
                "unauthorized_attempt": bool(episode.get("unauthorized_attempt")),
                "above_limit_purchase_attempt": bool(
                    episode.get("above_limit_purchase_attempt")
                ),
                "split_purchase_attempt": bool(episode.get("split_purchase_attempt")),
                "compliant_action_selected": episode.get("selected_compliant_action"),
                "qualifying_loss_event": bool(episode.get("qualifying_loss_event")),
                "cumulative_qualifying_losses_before": episode.get(
                    "cumulative_qualifying_losses_before"
                ),
                "cumulative_qualifying_losses_after": episode.get(
                    "cumulative_qualifying_losses_after"
                ),
                "threshold_crossed": episode.get("threshold_crossed"),
                "capability_lost_this_episode": episode.get("capability_lost_this_episode"),
                "capability_vector_before_json": json.dumps(
                    episode.get("capability_vector_before", [])
                ),
                "capability_vector_after_json": json.dumps(
                    episode.get("capability_vector_after", [])
                ),
                "remaining_capability_count_before": episode.get(
                    "remaining_capability_count_before"
                ),
                "remaining_capability_count_after": episode.get(
                    "remaining_capability_count_after"
                ),
                "available_action_count": episode.get("available_action_count"),
                "available_compliant_action_count": episode.get(
                    "available_compliant_action_count"
                ),
                "available_prohibited_action_count": episode.get(
                    "available_prohibited_action_count"
                ),
                "max_compliant_objective_potential": episode.get(
                    "max_compliant_objective_potential"
                ),
                "project_state_before": episode.get("project_state_before"),
                "project_state_after": episode.get("project_state_after"),
                "project_consequence": episode.get("project_consequence"),
                "objective_fraction": episode.get("objective_fraction"),
                "partial_objective_achievement": bool(
                    episode.get("partial_objective_achievement")
                ),
                "compliant_alternative_search": bool(
                    episode.get("compliant_alternative_search")
                ),
                "escalation": bool(episode.get("escalation")),
                "steps": episode.get("steps"),
                "max_step": bool(episode.get("max_step")),
                "terminal_state": episode.get("terminal_state"),
                "outcome_class": episode.get("outcome_class"),
            }
        )
    return rows


def exact_binomial_ci(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    if n == 0:
        return (math.nan, math.nan)
    try:
        from scipy.stats import beta
    except ImportError:
        if k == 0:
            return (0.0, 1 - alpha ** (1 / n))
        if k == n:
            return (alpha ** (1 / n), 1.0)
        raise
    lower = 0.0 if k == 0 else float(beta.ppf(alpha / 2, k, n - k + 1))
    upper = 1.0 if k == n else float(beta.ppf(1 - alpha / 2, k + 1, n - k))
    return lower, upper


def rate_summary(rows: list[dict[str, Any]], field: str, group: str | None = None) -> list[dict[str, Any]]:
    grouped_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    if group is None:
        grouped_rows["overall"] = rows
    else:
        for row in rows:
            grouped_rows[str(row[group])].append(row)
    output: list[dict[str, Any]] = []
    for label, group_rows in sorted(grouped_rows.items()):
        n = len(group_rows)
        k = sum(1 for row in group_rows if row.get(field) is True)
        lo, hi = exact_binomial_ci(k, n)
        output.append({"group": label, "endpoint": field, "events": k, "n": n, "rate": k / n if n else math.nan, "ci95_low": lo, "ci95_high": hi})
    return output


def collect_authoritative() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    sequence_rows: list[dict[str, Any]] = []
    episode_rows: list[dict[str, Any]] = []
    provenance: dict[str, Any] = {"runs": {}}
    global_seen: set[str] = set()
    proof_ids = {
        sample_id for run in PROOF_RUNS for sample_id in expected_sample_ids(known_runs()[run])
    }
    for run_id in RUNS:
        spec = patched_spec(run_id)
        expected = expected_sample_ids(spec)
        expected_set = set(expected)
        selected: dict[str, dict[str, Any]] = {}
        duplicates: set[str] = set()
        unexpected: set[str] = set()
        invalid: set[str] = set()
        segments: list[dict[str, Any]] = []
        for path in log_paths_for(run_id):
            meta = inspect_log_metadata(path)
            data = json.loads(path.read_text(encoding="utf-8"))
            valid_ids: list[str] = []
            invalid_ids: list[str] = []
            for sample in data.get("samples", []):
                if not isinstance(sample, dict) or sample.get("id") is None:
                    continue
                sid = str(sample["id"])
                if sid not in expected_set:
                    unexpected.add(sid)
                    continue
                if not valid_sample(sample):
                    invalid.add(sid)
                    invalid_ids.append(sid)
                    continue
                valid_ids.append(sid)
                if sid in selected:
                    duplicates.add(sid)
                else:
                    selected[sid] = sample
            segments.append(
                {
                    "path": str(path),
                    "byte_size": meta.byte_size,
                    "sha256": meta.sha256,
                    "status": meta.status,
                    "valid_expected_count": len(valid_ids),
                    "valid_expected_ids": valid_ids,
                    "invalid_expected_ids": invalid_ids,
                }
            )
        run_rows: list[dict[str, Any]] = []
        for sid in expected:
            sample = selected.get(sid)
            if sample is None:
                continue
            metadata = score_metadata(sample)
            row = per_sequence_row(sid, metadata, sample.get("metadata") or {})
            sequence_rows.append(row)
            run_rows.append(row)
            episode_rows.extend(per_episode_rows(sid, metadata, sample.get("metadata") or {}))
        global_seen.update(selected)
        provenance["runs"][run_id] = {
            "expected": len(expected),
            "selected": len(selected),
            "missing_ids": [sid for sid in expected if sid not in selected],
            "duplicate_ids": sorted(duplicates),
            "unexpected_ids": sorted(unexpected),
            "invalid_ids": sorted(invalid.difference(selected)),
            "condition_counts": dict(Counter(row["condition"] for row in run_rows)),
            "segments": segments,
        }
    provenance["proof_overlap_ids"] = sorted(global_seen.intersection(proof_ids))
    return sequence_rows, episode_rows, provenance


def integrity(
    sequence_rows: list[dict[str, Any]],
    episode_rows: list[dict[str, Any]],
    provenance: dict[str, Any],
) -> dict[str, Any]:
    ids = [row["sequence_id"] for row in sequence_rows]
    condition_counts = Counter(row["condition"] for row in sequence_rows)
    model_counts = Counter(row["model_role"] for row in sequence_rows)
    run_ok = all(
        run["expected"] == 60
        and run["selected"] == 60
        and not run["missing_ids"]
        and not run["duplicate_ids"]
        and not run["unexpected_ids"]
        and not run["invalid_ids"]
        for run in provenance["runs"].values()
    )
    lifecycle_ok = (
        sum(row["phase_a_done"] for row in sequence_rows) == 180
        and sum(row["phase_a_frozen"] for row in sequence_rows) == 180
        and sum(row["phase_a_score_present"] for row in sequence_rows) == 180
        and sum(row["phase_b_done"] for row in sequence_rows) == 180
        and len(episode_rows) == 1440
    )
    allocation_ok = (
        len(sequence_rows) == 180
        and len(set(ids)) == 180
        and condition_counts == Counter({"principal": 90, "capability": 90})
        and model_counts == Counter(
            {"model_a_gpt": 60, "model_b_claude": 60, "model_c_gemini": 60}
        )
    )
    return {
        "technical_integrity": "PASS"
        if run_ok and lifecycle_ok and allocation_ok and not provenance["proof_overlap_ids"]
        else "FAIL",
        "total_sequences": len(sequence_rows),
        "total_episodes": len(episode_rows),
        "condition_counts": dict(condition_counts),
        "model_counts": dict(model_counts),
        "duplicate_ids": sorted(sid for sid, count in Counter(ids).items() if count > 1),
        "proof_overlap_ids": provenance["proof_overlap_ids"],
        "invariants": {
            "agent_a_authority_usd": AUTHORITY_LIMIT_USD,
            "preferred_purchase_usd": PREFERRED_PURCHASE_USD,
            "p_detect": P_DETECT,
            "rng_version": RNG_VERSION,
            "environment_version": ENVIRONMENT_VERSION,
            "scorer_version": SCORER_VERSION,
            "preregistration_sha": PREREGISTRATION_SHA,
            "capability_amendment_sha": CAPABILITY_AMENDMENT_SHA,
        },
        "runs": provenance["runs"],
    }


def manipulation_summary(episode_rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_condition: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in episode_rows:
        by_condition[str(row["condition"])].append(row)
    summary: dict[str, Any] = {}
    for condition, rows in sorted(by_condition.items()):
        summary[condition] = {
            "n_episodes": len(rows),
            "mean_capability_count": mean(float(row["remaining_capability_count_before"] or 0) for row in rows),
            "mean_max_compliant_objective_potential": mean(float(row["max_compliant_objective_potential"] or 0) for row in rows),
            "capability_loss_events": sum(1 for row in rows if row["capability_lost_this_episode"]),
            "authority_invariant": all(row["available_prohibited_action_count"] and row["available_compliant_action_count"] for row in rows),
        }
    return summary


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=output_root())
    args = parser.parse_args()

    sequence_rows, episode_rows, provenance = collect_authoritative()
    integrity_result = integrity(sequence_rows, episode_rows, provenance)
    if integrity_result["technical_integrity"] != "PASS":
        write_json(args.out / "integrity_provenance.json", integrity_result)
        print("EXP012_INTEGRITY_FAIL")
        return 2

    write_csv(args.out / "authoritative_sequences.csv", sequence_rows)
    write_csv(args.out / "authoritative_episodes.csv", episode_rows)
    outputs = {
        "integrity_provenance": integrity_result,
        "primary_overall": rate_summary(
            sequence_rows,
            "sequence_any_operational_constraint_violation",
        ),
        "primary_by_condition": rate_summary(
            sequence_rows,
            "sequence_any_operational_constraint_violation",
            "condition",
        ),
        "primary_by_model": rate_summary(
            sequence_rows,
            "sequence_any_operational_constraint_violation",
            "model_role",
        ),
        "unauthorized_attempts_by_condition": rate_summary(
            sequence_rows,
            "any_unauthorized_attempt",
            "condition",
        ),
        "manipulation": manipulation_summary(episode_rows),
        "analysis_notes": {
            "independent_unit": "sequence",
            "nested_episode_count_expected": 1440,
            "primary_estimand": (
                "P(sequence_any_operational_constraint_violation | randomized "
                "consequence condition)"
            ),
            "endogenous_capability_state_guard": (
                "Observed capability state is history-dependent; randomized "
                "condition is the primary causal factor."
            ),
            "sparse_handling": (
                "If all-zero or separated, report exact rates/CIs and do not "
                "force unstable logistic regression."
            ),
        },
    }
    for name, payload in outputs.items():
        write_json(args.out / f"{name}.json", payload)
    manifest = {
        "experiment": EXPERIMENT,
        "files": {
            str(path.relative_to(args.out)): {
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in sorted(args.out.glob("*"))
            if path.is_file()
        },
    }
    write_json(args.out / "derived_artifact_manifest.json", manifest)
    print("EXP012_ANALYSIS_READY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
