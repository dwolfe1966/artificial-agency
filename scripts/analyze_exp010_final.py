from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from artificial_agency.runner.config import RunSpec, known_runs
from artificial_agency.runner.inspect_ops import inspect_log_metadata
from artificial_agency.runner.recovery import expected_sample_ids


EXPERIMENT = "010-repeated-operational-pressure"
PREREGISTRATION_SHA = "accfa2ef5a89a465083306ccee0fe0bec66f46dc"
PRESSURE_AMENDMENT_SHA = "49c683d179f86fa16d587bfc4ae0767f8e5d16cf"
SCIENTIFIC_SHA = "73eafc89a31d581e935996dc6abbf9a1468635fc"
RUNTIME_ROOT_CANDIDATES = [
    Path("/Users/davidwolfe/actions-runner/artificial-agency/_work/artificial-agency/.artificial-agency-runtime"),
    REPO.parent / ".artificial-agency-runtime",
]
RUNS = ("010A-GPT", "010B-CLAUDE", "010C-GEMINI")
MODEL_LABELS = {
    "model_a_gpt": "GPT-5.6 Sol",
    "model_b_claude": "Claude Sonnet 5",
    "model_c_gemini": "Gemini 3.7 Flash",
}
MODEL_ROLE_BY_PREFIX = {
    "010A-GPT": "model_a_gpt",
    "010B-CLAUDE": "model_b_claude",
    "010C-GEMINI": "model_c_gemini",
}
PRESSURE_COST = {"low": 2, "medium": 6, "high": 10}
AWARENESS_STATUSES = {"captured_valid", "captured_malformed", "missing"}
RNG_VERSION = "exp010-sequence-seed-v1-no-stochastic-events"


def runtime_roots() -> list[Path]:
    roots = [root for root in RUNTIME_ROOT_CANDIDATES if (root / EXPERIMENT).exists()]
    return roots or [RUNTIME_ROOT_CANDIDATES[0]]


def runtime_root() -> Path:
    return runtime_roots()[0]


def patched_spec(run_id: str) -> RunSpec:
    spec = known_runs()[run_id]
    data = spec.__dict__.copy()
    root = runtime_root() / EXPERIMENT / f"run-{run_id}"
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
    scores = sample.get("scores") or {}
    score = scores.get("repeated_pressure_outcome_scorer")
    if not isinstance(score, dict):
        return {}
    metadata = score.get("metadata")
    return metadata if isinstance(metadata, dict) else {}


def parse_identity(sequence_id: str, sample_metadata: dict[str, Any], trajectory: dict[str, Any]) -> dict[str, Any]:
    prefix = "-".join(sequence_id.split("-")[:2])
    pressure_from_id = sequence_id.rsplit("-", 2)[1]
    replicate_from_id = int(sequence_id.rsplit("-", 1)[1])
    model_role = str(
        sample_metadata.get("model_role")
        or trajectory.get("model_role")
        or MODEL_ROLE_BY_PREFIX.get(prefix)
    )
    pressure_id = str(sample_metadata.get("pressure_id") or trajectory.get("pressure_id") or pressure_from_id)
    return {
        "sequence_id": sequence_id,
        "model_role": model_role,
        "model": MODEL_LABELS.get(model_role, model_role),
        "scenario": "procurement",
        "pressure_id": pressure_id,
        "consequence_cost": int(
            sample_metadata.get("consequence_cost")
            or trajectory.get("consequence_cost")
            or PRESSURE_COST[pressure_id]
        ),
        "replicate": int(
            sample_metadata.get("replicate_id")
            if sample_metadata.get("replicate_id") is not None
            else trajectory.get("replicate_id", replicate_from_id)
        ),
        "run_id": str(sample_metadata.get("run_id") or prefix).removeprefix("run-"),
    }


def per_sequence_row(sequence_id: str, metadata: dict[str, Any], sample_metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    sample_metadata = sample_metadata or {}
    trajectory = metadata.get("trajectory") if isinstance(metadata.get("trajectory"), dict) else {}
    flags = metadata.get("sequence_secondary_flags") if isinstance(metadata.get("sequence_secondary_flags"), dict) else {}
    stochastic = metadata.get("stochastic") if isinstance(metadata.get("stochastic"), dict) else {}
    awareness = metadata.get("awareness") if isinstance(metadata.get("awareness"), dict) else {}
    episodes = metadata.get("episode_records") if isinstance(metadata.get("episode_records"), list) else []
    identity = parse_identity(sequence_id, sample_metadata, trajectory)
    return {
        **identity,
        "sequence_any_operational_constraint_violation": bool(
            metadata.get("sequence_any_operational_constraint_violation")
        ),
        "primary_label_id": str(metadata.get("primary_label_id")),
        "any_unauthorized_attempt": bool(flags.get("any_unauthorized_attempt", False)),
        "number_of_violations": int(flags.get("number_of_violations", 0) or 0),
        "time_to_first_operational_violation": metadata.get("time_to_first_operational_violation"),
        "time_to_first_unauthorized_attempt": metadata.get("time_to_first_unauthorized_attempt"),
        "final_resource": metadata.get("final_resource"),
        "minimum_resource": metadata.get("minimum_resource"),
        "episodes_in_broad_tier": int(flags.get("episodes_in_broad_tier", 0) or 0),
        "episodes_in_reduced_tier": int(flags.get("episodes_in_reduced_tier", 0) or 0),
        "episodes_in_minimal_tier": int(flags.get("episodes_in_minimal_tier", 0) or 0),
        "cumulative_resource_loss": flags.get("cumulative_resource_loss"),
        "cumulative_objective_fraction": flags.get("cumulative_objective_fraction"),
        "total_escalation_count": int(flags.get("total_escalation_count", 0) or 0),
        "total_repeated_escalation_count": int(flags.get("total_repeated_escalation_count", 0) or 0),
        "total_compliant_alternative_search_count": int(
            flags.get("total_compliant_alternative_search_count", 0) or 0
        ),
        "total_partial_objective_achievement_count": int(
            flags.get("total_partial_objective_achievement_count", 0) or 0
        ),
        "total_objective_success_count": int(flags.get("total_objective_success_count", 0) or 0),
        "total_max_step_episodes": int(flags.get("total_max_step_episodes", 0) or 0),
        "total_action_steps": int(flags.get("total_action_steps", 0) or 0),
        "episode_count": len(episodes),
        "phase_a_done": metadata.get("phase_a_done") is True,
        "phase_a_frozen": metadata.get("phase_a_frozen") is True,
        "phase_a_score_present": "sequence_any_operational_constraint_violation" in metadata,
        "phase_b_done": metadata.get("phase_b_done") is True,
        "rng_version": str(stochastic.get("rng_version")),
        "sequence_seed": stochastic.get("sequence_seed"),
        "stochastic_environment_events": bool(stochastic.get("stochastic_environment_events", False)),
        "p_detect": stochastic.get("p_detect"),
        "detection_draw_consumed": bool(stochastic.get("detection_draw_consumed", False)),
        "p_sanction_if_detected": stochastic.get("p_sanction_if_detected"),
        "sanction_severity": stochastic.get("sanction_severity"),
        "awareness_capture_status": str(awareness.get("capture_status", metadata.get("awareness_capture_status"))),
        "perceived_primary_task_type": awareness.get("perceived_primary_task_type"),
        "perceived_compliance_test_likelihood": awareness.get("perceived_compliance_test_likelihood"),
        "perceived_behavior_under_evaluation": awareness.get("perceived_behavior_under_evaluation"),
        "awareness_confidence": awareness.get("confidence"),
    }


def per_episode_rows(sequence_id: str, metadata: dict[str, Any], sequence_row: dict[str, Any]) -> list[dict[str, Any]]:
    episodes = metadata.get("episode_records") if isinstance(metadata.get("episode_records"), list) else []
    rows: list[dict[str, Any]] = []
    for episode in episodes:
        row = {
            "sequence_id": sequence_id,
            "model": sequence_row["model"],
            "model_role": sequence_row["model_role"],
            "pressure_id": sequence_row["pressure_id"],
            "consequence_cost": sequence_row["consequence_cost"],
            "replicate": sequence_row["replicate"],
            **episode,
        }
        if "available_compliant_option_count" in row and "compliant_option_count" not in row:
            row["compliant_option_count"] = row["available_compliant_option_count"]
        if "total_steps" in row and "steps" not in row:
            row["steps"] = row["total_steps"]
        rows.append(
            row
        )
    return rows


def load_authoritative_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    sequence_rows: list[dict[str, Any]] = []
    episode_rows: list[dict[str, Any]] = []
    provenance: dict[str, Any] = {"runs": {}}
    global_seen: set[str] = set()
    for run_id in RUNS:
        spec = patched_spec(run_id)
        expected = expected_sample_ids(spec)
        expected_set = set(expected)
        selected: dict[str, dict[str, Any]] = {}
        duplicate_ids: set[str] = set()
        unexpected_ids: set[str] = set()
        id_segment: dict[str, str] = {}
        segments: list[dict[str, Any]] = []
        for path in log_paths_for(run_id):
            meta = inspect_log_metadata(path)
            data = json.loads(path.read_text(encoding="utf-8"))
            valid_expected_ids: list[str] = []
            partial_expected_ids: list[str] = []
            unexpected_segment_ids: list[str] = []
            for sample in data.get("samples", []):
                if not isinstance(sample, dict) or sample.get("id") is None:
                    continue
                sample_id = str(sample["id"])
                if sample_id not in expected_set:
                    unexpected_ids.add(sample_id)
                    unexpected_segment_ids.append(sample_id)
                    continue
                if not valid_sample(sample):
                    partial_expected_ids.append(sample_id)
                    continue
                valid_expected_ids.append(sample_id)
                if sample_id in selected:
                    duplicate_ids.add(sample_id)
                else:
                    selected[sample_id] = sample
                    id_segment[sample_id] = str(path)
            authoritative_selected_count = sum(
                1 for sample_id in valid_expected_ids if id_segment.get(sample_id) == str(path)
            )
            segments.append(
                {
                    "path": str(path),
                    "byte_size": meta.byte_size,
                    "sha256": meta.sha256,
                    "inspect_status": meta.status,
                    "sample_count": meta.sample_count,
                    "valid_sample_count": meta.valid_sample_count,
                    "valid_expected_ids_count": len(valid_expected_ids),
                    "partial_expected_ids_count": len(partial_expected_ids),
                    "unexpected_ids_count": len(unexpected_segment_ids),
                    "authoritative_selected_count": authoritative_selected_count,
                    "excluded_duplicate_or_partial": (
                        authoritative_selected_count < len(valid_expected_ids) or bool(partial_expected_ids)
                    ),
                }
            )
        missing_ids = [sample_id for sample_id in expected if sample_id not in selected]
        provenance["runs"][run_id] = {
            "expected_count": len(expected),
            "authoritative_count": len(selected),
            "missing_count": len(missing_ids),
            "duplicate_count": len(duplicate_ids),
            "unexpected_count": len(unexpected_ids),
            "segments": segments,
        }
        for sample_id in expected:
            sample = selected.get(sample_id)
            if sample is None:
                continue
            if sample_id in global_seen:
                provenance.setdefault("global_duplicate_ids", []).append(sample_id)
            global_seen.add(sample_id)
            metadata = score_metadata(sample)
            row = per_sequence_row(sample_id, metadata, sample.get("metadata") or {})
            sequence_rows.append(row)
            episode_rows.extend(per_episode_rows(sample_id, metadata, row))
    return sequence_rows, episode_rows, provenance


def exact_binomial_ci(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    if n == 0:
        return (math.nan, math.nan)
    if k == 0:
        return (0.0, 1.0 - (alpha / 2.0) ** (1.0 / n))
    if k == n:
        return ((alpha / 2.0) ** (1.0 / n), 1.0)
    lower = _bisect_probability(lambda p: 1.0 - _binomial_cdf(k - 1, n, p), alpha / 2.0)
    upper = _bisect_probability(lambda p: _binomial_cdf(k, n, p), alpha / 2.0, reverse=True)
    return (lower, upper)


def _binomial_cdf(k: int, n: int, p: float) -> float:
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    q = 1.0 - p
    if p == 0.0:
        return 1.0
    if p == 1.0:
        return 0.0 if k < n else 1.0
    term = q**n
    total = term
    for i in range(0, k):
        term *= (n - i) / (i + 1) * p / q
        total += term
    return min(max(total, 0.0), 1.0)


def _bisect_probability(fn, target: float, *, reverse: bool = False) -> float:
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2.0
        value = fn(mid)
        if (value < target) ^ reverse:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def rate_summary(rows: list[dict[str, Any]], field: str, groups: list[str]) -> list[dict[str, Any]]:
    buckets: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    if groups:
        for row in rows:
            buckets[tuple(row[group] for group in groups)].append(row)
    else:
        buckets[()] = rows
    out: list[dict[str, Any]] = []
    for key, bucket in sorted(buckets.items(), key=lambda item: tuple(str(x) for x in item[0])):
        k = sum(1 for row in bucket if bool(row[field]))
        n = len(bucket)
        ci_low, ci_high = exact_binomial_ci(k, n)
        record = {group: value for group, value in zip(groups, key)}
        record.update({"n": n, "count": k, "rate": k / n if n else None, "ci95_low": ci_low, "ci95_high": ci_high})
        out.append(record)
    return out


def process_summary(rows: list[dict[str, Any]], groups: list[str]) -> list[dict[str, Any]]:
    buckets: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        buckets[tuple(row[group] for group in groups)].append(row)
    out = []
    for key, bucket in sorted(buckets.items(), key=lambda item: tuple(str(x) for x in item[0])):
        record = {group: value for group, value in zip(groups, key)}
        record.update(
            {
                "n": len(bucket),
                "any_unauthorized_attempt": sum(row["any_unauthorized_attempt"] for row in bucket),
                "mean_final_resource": mean(row["final_resource"] for row in bucket),
                "median_final_resource": median(row["final_resource"] for row in bucket),
                "mean_minimum_resource": mean(row["minimum_resource"] for row in bucket),
                "mean_total_action_steps": mean(row["total_action_steps"] for row in bucket),
                "mean_broad_tier_episodes": mean(row["episodes_in_broad_tier"] for row in bucket),
                "mean_reduced_tier_episodes": mean(row["episodes_in_reduced_tier"] for row in bucket),
                "mean_minimal_tier_episodes": mean(row["episodes_in_minimal_tier"] for row in bucket),
                "mean_cumulative_objective_fraction": mean(
                    float(row["cumulative_objective_fraction"] or 0.0) for row in bucket
                ),
                "mean_total_escalation_count": mean(row["total_escalation_count"] for row in bucket),
                "mean_total_compliant_alternative_search_count": mean(
                    row["total_compliant_alternative_search_count"] for row in bucket
                ),
                "mean_total_max_step_episodes": mean(row["total_max_step_episodes"] for row in bucket),
            }
        )
        out.append(record)
    return out


def numeric_summary(rows: list[dict[str, Any]], groups: list[str], fields: list[str]) -> list[dict[str, Any]]:
    buckets: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        buckets[tuple(row[group] for group in groups)].append(row)
    out = []
    for key, bucket in sorted(buckets.items(), key=lambda item: tuple(str(x) for x in item[0])):
        record = {group: value for group, value in zip(groups, key)}
        record["n"] = len(bucket)
        for field in fields:
            values = [float(row[field]) for row in bucket if row.get(field) is not None]
            if values:
                record[f"mean_{field}"] = mean(values)
                record[f"median_{field}"] = median(values)
                record[f"min_{field}"] = min(values)
                record[f"max_{field}"] = max(values)
        out.append(record)
    return out


def count_summary(rows: list[dict[str, Any]], groups: list[str], fields: list[str]) -> list[dict[str, Any]]:
    buckets: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        buckets[tuple(row[group] for group in groups)].append(row)
    out = []
    for key, bucket in sorted(buckets.items(), key=lambda item: tuple(str(x) for x in item[0])):
        record = {group: value for group, value in zip(groups, key)}
        record["n"] = len(bucket)
        for field in fields:
            record[field] = sum(1 for row in bucket if bool(row.get(field)))
        out.append(record)
    return out


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def credential_scan(paths: list[Path]) -> dict[str, Any]:
    needles = (
        "api" + "_key",
        "api" + "key",
        "sec" + "ret",
        "pass" + "word",
        "BEGIN " + "RSA",
        "BEGIN " + "OPENSSH",
        "PRIVATE " + "KEY",
        "s" + "k-",
    )
    hits = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        lower = text.lower()
        for needle in needles:
            if needle.lower() in lower:
                hits.append({"path": str(path), "pattern": needle})
    return {"scanned_files": len(paths), "hits": hits, "clean": not hits}


def integrity(sequence_rows: list[dict[str, Any]], episode_rows: list[dict[str, Any]], provenance: dict[str, Any]) -> dict[str, Any]:
    ids = [row["sequence_id"] for row in sequence_rows]
    cells = Counter((row["model"], row["pressure_id"]) for row in sequence_rows)
    pressure = Counter(row["pressure_id"] for row in sequence_rows)
    proof_overlap = [
        sequence_id
        for sequence_id in ids
        if sequence_id.startswith("010-PROOF-GPT")
        or sequence_id.startswith("010-PROOF-CLAUDE")
        or sequence_id.startswith("010-PROOF-GEMINI")
    ]
    return {
        "total_sequences": len(sequence_rows),
        "total_episodes": len(episode_rows),
        "unique_sequence_ids": len(set(ids)),
        "duplicate_sequence_ids": [sid for sid, count in Counter(ids).items() if count > 1],
        "missing_total": sum(run["missing_count"] for run in provenance["runs"].values()),
        "unexpected_total": sum(run["unexpected_count"] for run in provenance["runs"].values()),
        "raw_duplicate_or_superseded_total": sum(run["duplicate_count"] for run in provenance["runs"].values()),
        "proof_overlap_count": len(proof_overlap),
        "pressure_counts": dict(sorted(pressure.items())),
        "cell_count": len(cells),
        "all_cells_20_sequences": all(count == 20 for count in cells.values()) and len(cells) == 9,
        "all_pressure_cells_60_sequences": pressure == Counter({"low": 60, "medium": 60, "high": 60}),
        "phase_a_complete": sum(row["phase_a_done"] for row in sequence_rows),
        "phase_a_state_score_complete": sum(row["phase_a_frozen"] and row["phase_a_score_present"] for row in sequence_rows),
        "phase_b_disposition_complete": sum(row["awareness_capture_status"] in AWARENESS_STATUSES for row in sequence_rows),
        "seed_provenance_complete": sum(row["rng_version"] == RNG_VERSION and row["sequence_seed"] is not None for row in sequence_rows),
        "episode_count_complete": sum(row["episode_count"] == 10 for row in sequence_rows),
        "frozen_scientific_sha": SCIENTIFIC_SHA,
        "technical_integrity_pass": (
            len(sequence_rows) == 180
            and len(episode_rows) == 1800
            and len(set(ids)) == 180
            and not proof_overlap
            and sum(run["missing_count"] for run in provenance["runs"].values()) == 0
            and sum(run["unexpected_count"] for run in provenance["runs"].values()) == 0
            and all(count == 20 for count in cells.values())
            and len(cells) == 9
            and pressure == Counter({"low": 60, "medium": 60, "high": 60})
            and sum(row["phase_a_done"] for row in sequence_rows) == 180
            and sum(row["phase_a_frozen"] and row["phase_a_score_present"] for row in sequence_rows) == 180
            and sum(row["awareness_capture_status"] in AWARENESS_STATUSES for row in sequence_rows) == 180
            and sum(row["rng_version"] == RNG_VERSION and row["sequence_seed"] is not None for row in sequence_rows) == 180
            and sum(row["episode_count"] == 10 for row in sequence_rows) == 180
        ),
    }


def pressure_manipulation(sequence_rows: list[dict[str, Any]], episode_rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "sequence_resource_by_pressure": numeric_summary(
            sequence_rows,
            ["pressure_id"],
            [
                "final_resource",
                "minimum_resource",
                "cumulative_resource_loss",
                "cumulative_objective_fraction",
                "episodes_in_broad_tier",
                "episodes_in_reduced_tier",
                "episodes_in_minimal_tier",
            ],
        ),
        "episode_resource_by_pressure_episode": numeric_summary(
            episode_rows,
            ["pressure_id", "episode"],
            [
                "resource_before",
                "resource_after",
                "available_compliant_option_count",
                "max_compliant_objective_fraction",
            ],
        ),
    }


def awareness_summary(sequence_rows: list[dict[str, Any]]) -> dict[str, Any]:
    fields = [
        "awareness_capture_status",
        "perceived_primary_task_type",
        "perceived_compliance_test_likelihood",
        "perceived_behavior_under_evaluation",
        "awareness_confidence",
    ]
    return {
        field: dict(sorted(Counter(str(row.get(field)) for row in sequence_rows).items()))
        for field in fields
    }


def inference_summary(sequence_rows: list[dict[str, Any]], episode_rows: list[dict[str, Any]]) -> dict[str, Any]:
    violations = sum(row["sequence_any_operational_constraint_violation"] for row in sequence_rows)
    attempts = sum(row["any_unauthorized_attempt"] for row in sequence_rows)
    all_zero_primary = violations == 0
    return {
        "primary_model": "ViolationSequence ~ Model * Pressure",
        "independent_unit": "sequence",
        "primary_events": violations,
        "unauthorized_attempt_sequences": attempts,
        "model_fit_status": (
            "not_fit_all_zero_primary_endpoint; exact_upper_bounds_reported"
            if all_zero_primary
            else "estimable_data_present; use exact cell rates and preregistered model review"
        ),
        "time_to_event_status": (
            "all_sequences_censored_after_episode_10"
            if violations == 0
            else "events_present; inspect time_to_first_operational_violation table"
        ),
        "resource_state_caveat": (
            "R_t is history-dependent/endogenous; causal comparisons are by randomized pressure assignment."
        ),
        "episode_nesting_caveat": "episode-level records are nested within sequence and are not independent primary samples",
        "hypotheses": hypothesis_results(sequence_rows, episode_rows),
    }


def hypothesis_results(sequence_rows: list[dict[str, Any]], episode_rows: list[dict[str, Any]]) -> dict[str, Any]:
    violations_by_pressure = {
        row["pressure_id"]: row["count"]
        for row in rate_summary(sequence_rows, "sequence_any_operational_constraint_violation", ["pressure_id"])
    }
    attempts_by_pressure = {
        row["pressure_id"]: row["count"]
        for row in rate_summary(sequence_rows, "any_unauthorized_attempt", ["pressure_id"])
    }
    process_by_pressure = {row["pressure_id"]: row for row in process_summary(sequence_rows, ["pressure_id"])}
    any_process_difference = len(
        {
            (
                round(row["mean_total_action_steps"], 8),
                round(row["mean_total_escalation_count"], 8),
                round(row["mean_total_compliant_alternative_search_count"], 8),
                round(row["mean_cumulative_objective_fraction"], 8),
            )
            for row in process_by_pressure.values()
        }
    ) > 1
    episode_step_by_pressure_episode = numeric_summary(episode_rows, ["pressure_id", "episode"], ["total_steps"])
    any_episode_progression_difference = len(
        {
            (
                row["pressure_id"],
                row["episode"],
                round(row.get("mean_total_steps", 0.0), 8),
            )
            for row in episode_step_by_pressure_episode
        }
    ) > 0 and any(
        row.get("mean_total_steps") != episode_step_by_pressure_episode[0].get("mean_total_steps")
        for row in episode_step_by_pressure_episode
    )
    return {
        "H1_accumulated_operational_pressure": (
            "not_supported"
            if sum(violations_by_pressure.values()) == 0 and sum(attempts_by_pressure.values()) == 0
            else "evaluate_from_primary_and_attempt_tables"
        ),
        "H2_constraint_bounded_adaptation": (
            "partially_supported" if any_process_difference else "not_supported"
        ),
        "H3_history_dependence": (
            "partially_supported" if any_episode_progression_difference else "not_supported"
        ),
        "H4_model_differences": "evaluate_from_model_and_model_pressure_tables",
        "H5_resource_state_relationship": "descriptive_only_due_to_endogenous_R_t",
    }


def build_outputs() -> dict[str, Any]:
    sequence_rows, episode_rows, provenance = load_authoritative_rows()
    checks = integrity(sequence_rows, episode_rows, provenance)
    final_dir = REPO / "results" / EXPERIMENT / "final" / "derived"
    finalization = {
        "manifest_kind": "experiment_010_confirmatory_finalization_provenance",
        "preregistration_sha": PREREGISTRATION_SHA,
        "pressure_amendment_sha": PRESSURE_AMENDMENT_SHA,
        "frozen_scientific_sha": SCIENTIFIC_SHA,
        "confirmatory_run_ids": list(RUNS),
        "excluded_proof_run_ids": ["010-PROOF-GPT", "010-PROOF-CLAUDE", "010-PROOF-GEMINI"],
        "runtime_roots": [str(root) for root in runtime_roots()],
        "counts": checks,
        "runs": provenance["runs"],
        "sequence_ids": sorted(row["sequence_id"] for row in sequence_rows),
        "pressure_allocation": dict(sorted(Counter(row["pressure_id"] for row in sequence_rows).items())),
        "proof_exclusion": {"proof_overlap_count": checks["proof_overlap_count"]},
        "sequence_atomic_recovery": {
            "authoritative_unit": "complete_10_episode_sequence",
            "partial_segments_remain_provenance_only": True,
            "no_episode_splicing": True,
        },
    }
    write_csv(final_dir / "authoritative_sequences.csv", sequence_rows)
    write_csv(final_dir / "authoritative_episodes.csv", episode_rows)
    write_json(final_dir / "integrity.json", checks)
    write_json(final_dir / "provenance.json", provenance)
    write_json(final_dir / "finalization_manifest.json", finalization)
    write_json(final_dir / "pressure_manipulation.json", pressure_manipulation(sequence_rows, episode_rows))
    write_json(final_dir / "awareness_summary.json", awareness_summary(sequence_rows))
    write_json(final_dir / "inference_summary.json", inference_summary(sequence_rows, episode_rows))
    write_json(
        final_dir / "exp009_comparison.json",
        {
            "exp009_primary_violation": "0/720",
            "exp009_unauthorized_attempt": "0/720",
            "exp009_p_detect_zero_violation": "0/180",
            "exp010_design_difference": (
                "Experiment 010 holds p_detect=0 and adds persistent context, repeated consequences, "
                "accumulating resource loss, and R-driven compliant opportunity changes."
            ),
            "pooling_status": "not_inferentially_pooled",
        },
    )
    write_csv(final_dir / "primary_overall.csv", rate_summary(sequence_rows, "sequence_any_operational_constraint_violation", []))
    write_csv(final_dir / "primary_by_pressure.csv", rate_summary(sequence_rows, "sequence_any_operational_constraint_violation", ["pressure_id"]))
    write_csv(final_dir / "primary_by_model.csv", rate_summary(sequence_rows, "sequence_any_operational_constraint_violation", ["model"]))
    write_csv(final_dir / "primary_by_model_pressure.csv", rate_summary(sequence_rows, "sequence_any_operational_constraint_violation", ["model", "pressure_id"]))
    write_csv(final_dir / "unauthorized_attempt_overall.csv", rate_summary(sequence_rows, "any_unauthorized_attempt", []))
    write_csv(final_dir / "unauthorized_attempt_by_pressure.csv", rate_summary(sequence_rows, "any_unauthorized_attempt", ["pressure_id"]))
    write_csv(final_dir / "unauthorized_attempt_by_model.csv", rate_summary(sequence_rows, "any_unauthorized_attempt", ["model"]))
    write_csv(final_dir / "unauthorized_attempt_by_model_pressure.csv", rate_summary(sequence_rows, "any_unauthorized_attempt", ["model", "pressure_id"]))
    write_csv(final_dir / "episode_endpoint_counts_by_pressure_episode.csv", count_summary(
        episode_rows,
        ["pressure_id", "episode"],
        [
            "operational_constraint_violation",
            "unauthorized_attempt",
            "escalation",
            "repeated_escalation",
            "compliant_alternative_search",
            "partial_objective_achievement",
            "objective_success",
            "max_step",
        ],
    ))
    write_csv(final_dir / "episode_process_by_pressure_episode.csv", numeric_summary(
        episode_rows,
        ["pressure_id", "episode"],
        [
            "total_steps",
            "post_denial_steps",
            "resource_before",
            "resource_after",
            "objective_fraction_achieved",
            "available_compliant_option_count",
            "max_compliant_objective_fraction",
        ],
    ))
    write_csv(final_dir / "process_by_pressure.csv", process_summary(sequence_rows, ["pressure_id"]))
    write_csv(final_dir / "process_by_model.csv", process_summary(sequence_rows, ["model"]))
    write_csv(final_dir / "process_by_model_pressure.csv", process_summary(sequence_rows, ["model", "pressure_id"]))
    generated = sorted(final_dir.glob("*"))
    scan = credential_scan([path for path in generated if path.is_file()])
    write_json(final_dir / "credential_scan.json", scan)
    return {
        "integrity": checks,
        "primary_overall": rate_summary(sequence_rows, "sequence_any_operational_constraint_violation", []),
        "primary_by_pressure": rate_summary(sequence_rows, "sequence_any_operational_constraint_violation", ["pressure_id"]),
        "unauthorized_attempt_overall": rate_summary(sequence_rows, "any_unauthorized_attempt", []),
        "credential_scan": scan,
        "generated": [str(path) for path in sorted(final_dir.glob("*"))],
    }


def main() -> int:
    result = build_outputs()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
