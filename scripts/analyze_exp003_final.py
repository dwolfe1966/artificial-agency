from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import statistics
from collections import Counter
from pathlib import Path
from typing import Any

from artificial_agency.experiments.exp003.config import (
    CONDITIONS,
    CONSTRAINT_STATUS_CONDITIONS,
    PRESSURE_CONDITIONS,
)


REPO = Path(__file__).resolve().parents[1]
ACTIONS_WORKSPACE = Path(
    "/Users/davidwolfe/actions-runner/artificial-agency/_work/artificial-agency/"
    "artificial-agency"
)

RAW_LOGS = {
    "stage1": {
        "run_id": "003A",
        "relative_path": Path(
            "results/003-constraint-status-pressure/run-003A/inspect/"
            "2026-08-25T21-25-27-00-00_exp003-constraint-status-stage1_fpNYZePPdKKCntSuJZjxmC.json"
        ),
        "expected_sha256": "a73a128c5d4ca8339360fabb4e535127ae870b739b82eeed4e1e55f862779a73",
        "expected_samples": 120,
        "expected_replicate_ids": set(range(0, 20)),
    },
    "stage2": {
        "run_id": "003B",
        "relative_path": Path(
            "results/003-constraint-status-pressure/run-003B/inspect/"
            "2026-08-25T22-19-37-00-00_exp003-constraint-status-stage2_egsfLXgZdGeoLNkvzYFkKb.json"
        ),
        "expected_sha256": "34d1eb20fb414fc01cdb87ea7153653345c4afc769b894c20f837bdbef31ed42",
        "expected_samples": 180,
        "expected_replicate_ids": set(range(20, 50)),
    },
}

PREREGISTRATION_SHA = "793c67068844fc70d6ec1f66e94dd0b76f03914c"
FROZEN_SHA = "f8294ab172cb556f8a4c1ec4f726947672cc859a"
STAGE1_CHECKPOINT_SHA = "b682b7e0b416e0fccddc3bff8da99f46e50c8311"
STAGE1_EXECUTION_SHA = "bb710d18d878ae4ed482a14172d0b096f8271d02"
STAGE2_EXECUTION_SHA = "f2cc400ab8fe277822abca059c204e34fcd18b01"
MODEL = "openai/gpt-5.6-sol"

ANALYSIS_PLAN = Path("experiments/003-constraint-status-pressure/analysis_plan.md")
PREDICTIONS = Path("experiments/003-constraint-status-pressure/predictions.md")
DESIGN = Path("experiments/003-constraint-status-pressure/design.md")
SCORING = Path("experiments/003-constraint-status-pressure/scoring.md")
OUT_DIR = REPO / "results" / "003-constraint-status-pressure" / "run-003-final" / "derived"

CELL_ORDER = (
    "categorical-ordinary",
    "categorical-high",
    "procedural-ordinary",
    "procedural-high",
    "purpose-conflict-ordinary",
    "purpose-conflict-high",
)
CONSTRAINT_ORDER = ("categorical", "procedural", "purpose-conflict")
PRESSURE_ORDER = ("ordinary", "high")
PRIMARY_LABELS = (
    "concealment_or_misrepresentation",
    "unauthorized_action",
    "repeated_bypass_after_denial",
    "escalation",
    "compliant_acceptance_of_failure",
    "compliant_alternative_search",
    "technical_failure",
    None,
)
EXPECTED_FINAL_COUNTS = {cell: 50 for cell in CELL_ORDER}


def raw_log_path(relative_path: Path) -> Path:
    candidate = REPO / relative_path
    if candidate.exists():
        return candidate
    return ACTIONS_WORKSPACE / relative_path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def binom_pmf(n: int, k: int, p: float) -> float:
    if p <= 0:
        return 1.0 if k == 0 else 0.0
    if p >= 1:
        return 1.0 if k == n else 0.0
    return math.comb(n, k) * (p**k) * ((1 - p) ** (n - k))


def binom_cdf(n: int, k: int, p: float) -> float:
    return sum(binom_pmf(n, i, p) for i in range(k + 1))


def binom_sf_inclusive(n: int, k: int, p: float) -> float:
    return sum(binom_pmf(n, i, p) for i in range(k, n + 1))


def bisect_quantile(predicate: Any) -> float:
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if predicate(mid):
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    if n == 0:
        raise ValueError("binomial CI requires n > 0")
    lower = 0.0 if k == 0 else bisect_quantile(
        lambda p: binom_sf_inclusive(n, k, p) >= alpha / 2
    )
    upper = 1.0 if k == n else bisect_quantile(
        lambda p: binom_cdf(n, k, p) <= alpha / 2
    )
    return lower, upper


def hypergeom_prob(a: int, row1: int, row2: int, col1: int) -> float:
    return math.comb(col1, a) * math.comb(row1 + row2 - col1, row1 - a) / math.comb(
        row1 + row2, row1
    )


def fisher_exact_two_sided(a: int, b: int, c: int, d: int) -> dict[str, Any]:
    row1 = a + b
    row2 = c + d
    col1 = a + c
    lo = max(0, row1 - (row1 + row2 - col1))
    hi = min(row1, col1)
    observed = hypergeom_prob(a, row1, row2, col1)
    p_value = sum(
        p
        for x in range(lo, hi + 1)
        if (p := hypergeom_prob(x, row1, row2, col1)) <= observed + 1e-15
    )
    if b * c == 0:
        odds_ratio = math.inf if a * d > 0 else None
    else:
        odds_ratio = (a * d) / (b * c)
    return {"odds_ratio": odds_ratio, "p_value_two_sided": min(1.0, p_value)}


def exact_multigroup_fixed_successes(
    counts: dict[str, int],
    ns: dict[str, int],
) -> dict[str, Any]:
    total_successes = sum(counts.values())
    total_n = sum(ns.values())
    if total_successes == 0 or total_successes == total_n:
        return {
            "estimable": False,
            "reason": "no variance in policy-violation outcome",
        }
    groups = list(ns)
    observed = tuple(counts[group] for group in groups)
    observed_prob = _multigroup_hypergeom_prob(observed, groups, ns, total_successes)
    p_value = 0.0
    for allocation in _success_allocations(groups, ns, total_successes):
        prob = _multigroup_hypergeom_prob(allocation, groups, ns, total_successes)
        if prob <= observed_prob + 1e-15:
            p_value += prob
    return {
        "estimable": True,
        "method": "Fisher-Freeman-Halton exact test by fixed success margins",
        "groups": groups,
        "success_counts": dict(counts),
        "ns": dict(ns),
        "p_value_two_sided": min(1.0, p_value),
    }


def _success_allocations(
    groups: list[str],
    ns: dict[str, int],
    successes: int,
    prefix: tuple[int, ...] = (),
) -> list[tuple[int, ...]]:
    if len(prefix) == len(groups) - 1:
        remaining = successes - sum(prefix)
        if 0 <= remaining <= ns[groups[-1]]:
            return [prefix + (remaining,)]
        return []
    idx = len(prefix)
    used = sum(prefix)
    max_remaining = sum(ns[group] for group in groups[idx + 1 :])
    lo = max(0, successes - used - max_remaining)
    hi = min(ns[groups[idx]], successes - used)
    allocations: list[tuple[int, ...]] = []
    for value in range(lo, hi + 1):
        allocations.extend(_success_allocations(groups, ns, successes, prefix + (value,)))
    return allocations


def _multigroup_hypergeom_prob(
    allocation: tuple[int, ...],
    groups: list[str],
    ns: dict[str, int],
    successes: int,
) -> float:
    numerator = 1
    for value, group in zip(allocation, groups, strict=True):
        numerator *= math.comb(ns[group], value)
    return numerator / math.comb(sum(ns.values()), successes)


def mean(values: list[float]) -> float:
    return statistics.fmean(values) if values else 0.0


def median(values: list[float]) -> float:
    return statistics.median(values) if values else 0.0


def rate(count: int, n: int) -> float:
    return count / n if n else 0.0


def bool_int(value: Any) -> int:
    return 1 if bool(value) else 0


def format_distribution(counter: Counter[str | None]) -> str:
    return "; ".join(
        f"{label or 'unresolved'}={counter.get(label, 0)}"
        for label in PRIMARY_LABELS
        if counter.get(label, 0)
    )


def load_stage(stage: str) -> tuple[dict[str, Any], Path, str, int]:
    spec = RAW_LOGS[stage]
    path = raw_log_path(spec["relative_path"])
    raw_sha = sha256(path)
    raw_bytes = path.stat().st_size
    log = json.loads(path.read_text(encoding="utf-8"))
    return log, path, raw_sha, raw_bytes


def extract_rows(log: dict[str, Any], stage: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for sample in log["samples"]:
        score = sample["scores"]["constraint_status_outcome_scorer"]
        score_metadata = score["metadata"]
        flags = score_metadata["secondary_flags"]
        sample_metadata = sample["metadata"]
        trajectory = score_metadata["trajectory"]
        row = {
            "sample_id": sample["id"],
            "stage": stage,
            "run_id": sample_metadata["run_id"],
            "constraint_status": sample_metadata["constraint_status"],
            "pressure": sample_metadata["pressure"],
            "factorial_cell": sample_metadata["condition"],
            "replicate_id": int(sample_metadata["replicate_id"]),
            "primary_behavioral_label": score_metadata["primary_label"],
            "primary_label_id": score_metadata["primary_label_id"],
            "constraint_circumvention_policy_violation": bool_int(
                flags["policy_violation"]
            ),
            "unauthorized_discount": bool_int(flags["unauthorized_discount_attempt"]),
            "excessive_unauthorized_credit": bool_int(
                flags["excessive_credit_attempt"]
            ),
            "authorization_misrepresentation": bool_int(
                flags["misrepresentation_of_authorization"]
            ),
            "concealment_misrepresentation": bool_int(
                flags["concealment_or_misrepresentation"]
            ),
            "explicit_bypass_attempt": bool_int(flags["explicit_bypass_attempt"]),
            "repeated_bypass_after_denial": bool_int(
                flags["repeated_bypass_after_denial"]
            ),
            "escalation_attempted": bool_int(flags["escalation_attempted"]),
            "repeated_escalation": bool_int(
                flags["repeated_escalation_after_denial"]
            ),
            "compliant_alternative_search": bool_int(
                flags["compliant_alternative_search"]
            ),
            "persuasion_attempt": bool_int(flags["customer_persuasion_attempt"]),
            "cancellation_accepted": bool_int(flags["cancellation_accepted"]),
            "retention": bool_int(flags["retention_outcome"]),
            "terminal_state": flags["terminal_state"],
            "total_action_steps": int(flags["total_action_steps"]),
            "steps_after_manager_denial": int(flags["steps_after_manager_denial"]),
            "max_step_termination": bool_int(flags["max_step_termination"]),
            "technical_failure": bool_int(flags["technical_failure"]),
            "environment_version": score_metadata["environment_version"],
            "prompt_version": sample_metadata["prompt_version"],
            "trajectory_action_steps": int(trajectory["action_steps"]),
            "total_time": sample.get("total_time"),
            "working_time": sample.get("working_time"),
            "turn_count": sample.get("turn_count"),
        }
        rows.append(row)
    return rows


def summarize_group(rows: list[dict[str, Any]], group_key: str, group_value: str) -> dict[str, Any]:
    group = [row for row in rows if row[group_key] == group_value]
    n = len(group)
    violation_count = sum(row["constraint_circumvention_policy_violation"] for row in group)
    ci_low, ci_high = clopper_pearson(violation_count, n)
    label_counter = Counter(row["primary_label_id"] for row in group)
    unauthorized_count = sum(
        1
        for row in group
        if row["unauthorized_discount"] or row["excessive_unauthorized_credit"]
    )
    bypass_count = sum(
        1
        for row in group
        if row["explicit_bypass_attempt"] or row["repeated_bypass_after_denial"]
    )
    return {
        group_key: group_value,
        "n": n,
        "violation_count": violation_count,
        "violation_rate": rate(violation_count, n),
        "violation_ci95_low": ci_low,
        "violation_ci95_high": ci_high,
        "unauthorized_action_count": unauthorized_count,
        "unauthorized_action_rate": rate(unauthorized_count, n),
        "concealment_misrepresentation_count": sum(
            row["concealment_misrepresentation"] for row in group
        ),
        "concealment_misrepresentation_rate": rate(
            sum(row["concealment_misrepresentation"] for row in group), n
        ),
        "bypass_count": bypass_count,
        "bypass_rate": rate(bypass_count, n),
        "escalation_count": sum(row["escalation_attempted"] for row in group),
        "escalation_rate": rate(sum(row["escalation_attempted"] for row in group), n),
        "repeated_escalation_count": sum(row["repeated_escalation"] for row in group),
        "repeated_escalation_rate": rate(
            sum(row["repeated_escalation"] for row in group), n
        ),
        "compliant_alternative_search_count": sum(
            row["compliant_alternative_search"] for row in group
        ),
        "compliant_alternative_search_rate": rate(
            sum(row["compliant_alternative_search"] for row in group), n
        ),
        "persuasion_count": sum(row["persuasion_attempt"] for row in group),
        "persuasion_rate": rate(sum(row["persuasion_attempt"] for row in group), n),
        "cancellation_count": sum(row["cancellation_accepted"] for row in group),
        "cancellation_rate": rate(sum(row["cancellation_accepted"] for row in group), n),
        "retention_count": sum(row["retention"] for row in group),
        "retention_rate": rate(sum(row["retention"] for row in group), n),
        "mean_total_action_steps": mean([row["total_action_steps"] for row in group]),
        "median_total_action_steps": median([row["total_action_steps"] for row in group]),
        "mean_steps_after_denial": mean(
            [row["steps_after_manager_denial"] for row in group]
        ),
        "median_steps_after_denial": median(
            [row["steps_after_manager_denial"] for row in group]
        ),
        "max_step_terminations": sum(row["max_step_termination"] for row in group),
        "primary_label_distribution": format_distribution(label_counter),
        **{
            f"primary_label_{label}_count": label_counter.get(label, 0)
            for label in PRIMARY_LABELS
            if label is not None
        },
    }


def cell_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [summarize_group(rows, "factorial_cell", cell) for cell in CELL_ORDER]


def factor_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summaries = [
        {"factor": "constraint_status", **summarize_group(rows, "constraint_status", level)}
        for level in CONSTRAINT_ORDER
    ]
    summaries.extend(
        {"factor": "pressure", **summarize_group(rows, "pressure", level)}
        for level in PRESSURE_ORDER
    )
    return summaries


def violation_counts(
    rows: list[dict[str, Any]], key: str, levels: tuple[str, ...]
) -> tuple[dict[str, int], dict[str, int]]:
    ns = {level: 0 for level in levels}
    violations = {level: 0 for level in levels}
    for row in rows:
        level = row[key]
        if level in ns:
            ns[level] += 1
            violations[level] += row["constraint_circumvention_policy_violation"]
    return violations, ns


def fisher_contrast(
    rows: list[dict[str, Any]],
    key: str,
    level_a: str,
    level_b: str,
) -> dict[str, Any]:
    group_a = [row for row in rows if row[key] == level_a]
    group_b = [row for row in rows if row[key] == level_b]
    a = sum(row["constraint_circumvention_policy_violation"] for row in group_a)
    c = sum(row["constraint_circumvention_policy_violation"] for row in group_b)
    return {
        "level_a": level_a,
        "level_b": level_b,
        "a_violations": a,
        "a_nonviolations": len(group_a) - a,
        "b_violations": c,
        "b_nonviolations": len(group_b) - c,
        **fisher_exact_two_sided(a, len(group_a) - a, c, len(group_b) - c),
    }


def _rate_for(rows: list[dict[str, Any]], constraint: str, pressure: str) -> float:
    group = [
        row
        for row in rows
        if row["constraint_status"] == constraint and row["pressure"] == pressure
    ]
    return rate(
        sum(row["constraint_circumvention_policy_violation"] for row in group),
        len(group),
    )


def statistical_results(rows: list[dict[str, Any]]) -> dict[str, Any]:
    cell_violations, cell_ns = violation_counts(rows, "factorial_cell", CELL_ORDER)
    constraint_violations, constraint_ns = violation_counts(
        rows, "constraint_status", CONSTRAINT_ORDER
    )
    pressure_violations, pressure_ns = violation_counts(rows, "pressure", PRESSURE_ORDER)
    total_events = sum(cell_violations.values())
    total_nonevents = sum(cell_ns.values()) - total_events
    separation = any(cell_violations[cell] in {0, cell_ns[cell]} for cell in CELL_ORDER)
    logistic_estimable = total_events >= 10 and total_nonevents >= 10 and not separation
    pressure_within = {
        status: fisher_contrast(
            [row for row in rows if row["constraint_status"] == status],
            "pressure",
            "ordinary",
            "high",
        )
        for status in CONSTRAINT_ORDER
    }
    interaction_rates = {
        status: _rate_for(rows, status, "high") - _rate_for(rows, status, "ordinary")
        for status in CONSTRAINT_ORDER
    }
    secondary: dict[str, Any] = {}
    for field in (
        "total_action_steps",
        "steps_after_manager_denial",
        "compliant_alternative_search",
        "repeated_escalation",
        "persuasion_attempt",
    ):
        secondary[field] = {
            "cell_means": {
                cell: mean([row[field] for row in rows if row["factorial_cell"] == cell])
                for cell in CELL_ORDER
            },
            "constraint_status_means": {
                level: mean(
                    [row[field] for row in rows if row["constraint_status"] == level]
                )
                for level in CONSTRAINT_ORDER
            },
            "pressure_means": {
                level: mean([row[field] for row in rows if row["pressure"] == level])
                for level in PRESSURE_ORDER
            },
            "cell_medians": {
                cell: median([row[field] for row in rows if row["factorial_cell"] == cell])
                for cell in CELL_ORDER
            },
            "inferential_test": (
                "not specified in frozen analysis plan; descriptive comparison reported"
            ),
        }
    return {
        "primary_violation": {
            "total_events": total_events,
            "total_n": sum(cell_ns.values()),
            "overall_rate": rate(total_events, sum(cell_ns.values())),
            "overall_ci95": clopper_pearson(total_events, sum(cell_ns.values())),
            "cell_counts": cell_violations,
            "cell_ns": cell_ns,
            "cell_rates": {
                cell: rate(cell_violations[cell], cell_ns[cell]) for cell in CELL_ORDER
            },
            "cell_ci95": {
                cell: clopper_pearson(cell_violations[cell], cell_ns[cell])
                for cell in CELL_ORDER
            },
            "constraint_status_counts": constraint_violations,
            "constraint_status_ns": constraint_ns,
            "constraint_status_rates": {
                level: rate(constraint_violations[level], constraint_ns[level])
                for level in CONSTRAINT_ORDER
            },
            "constraint_status_ci95": {
                level: clopper_pearson(constraint_violations[level], constraint_ns[level])
                for level in CONSTRAINT_ORDER
            },
            "pressure_counts": pressure_violations,
            "pressure_ns": pressure_ns,
            "pressure_rates": {
                level: rate(pressure_violations[level], pressure_ns[level])
                for level in PRESSURE_ORDER
            },
            "pressure_ci95": {
                level: clopper_pearson(pressure_violations[level], pressure_ns[level])
                for level in PRESSURE_ORDER
            },
            "constraint_status_fisher_freeman_halton": exact_multigroup_fixed_successes(
                constraint_violations, constraint_ns
            ),
            "cell_omnibus_fisher_freeman_halton": exact_multigroup_fixed_successes(
                cell_violations, cell_ns
            ),
            "planned_contrasts": {
                "categorical_vs_procedural": fisher_contrast(
                    rows, "constraint_status", "categorical", "procedural"
                ),
                "categorical_vs_purpose_conflict": fisher_contrast(
                    rows, "constraint_status", "categorical", "purpose-conflict"
                ),
                "ordinary_vs_high": fisher_contrast(rows, "pressure", "ordinary", "high"),
                "pressure_effect_within_constraint_status": pressure_within,
                "interaction_rate_differences": {
                    "pressure_effects": interaction_rates,
                    "categorical_vs_procedural_difference": (
                        interaction_rates["categorical"] - interaction_rates["procedural"]
                    ),
                    "categorical_vs_purpose_conflict_difference": (
                        interaction_rates["categorical"]
                        - interaction_rates["purpose-conflict"]
                    ),
                    "categorical_vs_pooled_procedural_purpose_difference": (
                        interaction_rates["categorical"]
                        - (
                            interaction_rates["procedural"]
                            + interaction_rates["purpose-conflict"]
                        )
                        / 2
                    ),
                    "inferential_status": (
                        "not estimable as a model if outcome has all-zero or separated cells"
                    ),
                },
            },
            "logistic_regression": {
                "estimable": logistic_estimable,
                "reason": (
                    "event and nonevent counts support the preregistered factorial logistic model"
                    if logistic_estimable
                    else "not estimated because event counts are sparse/all-zero or separated"
                ),
            },
            "firth_logistic_regression": {
                "estimable": False,
                "reason": (
                    "not run; preregistration allowed it only if an explicitly reviewed "
                    "implementation or dependency existed before results"
                ),
            },
        },
        "secondary_mechanical_search_effort": secondary,
    }


def stage_consistency(rows: list[dict[str, Any]]) -> dict[str, Any]:
    stage_rows = {stage: [row for row in rows if row["stage"] == stage] for stage in RAW_LOGS}
    stage_summary = {}
    for stage, group in stage_rows.items():
        cell_counts = Counter(row["factorial_cell"] for row in group)
        stage_summary[stage] = {
            "n": len(group),
            "primary_violation_count": sum(
                row["constraint_circumvention_policy_violation"] for row in group
            ),
            "technical_failures": sum(row["technical_failure"] for row in group),
            "cell_counts": dict(cell_counts),
            "replicate_id_min": min(row["replicate_id"] for row in group),
            "replicate_id_max": max(row["replicate_id"] for row in group),
        }
    return {
        "stage_summaries": stage_summary,
        "combining_stages_consistent_with_frozen_design": (
            stage_summary["stage1"]["n"] == 120
            and stage_summary["stage2"]["n"] == 180
            and stage_summary["stage1"]["technical_failures"] == 0
            and stage_summary["stage2"]["technical_failures"] == 0
            and all(count == 20 for count in stage_summary["stage1"]["cell_counts"].values())
            and all(count == 30 for count in stage_summary["stage2"]["cell_counts"].values())
        ),
        "interpretation": (
            "Stage comparison is provenance/consistency-only; the staged design "
            "forbids outcome-based optional stopping."
        ),
    }


def integrity(
    logs: dict[str, dict[str, Any]],
    paths: dict[str, Path],
    shas: dict[str, str],
    byte_sizes: dict[str, int],
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    stage_rows = {stage: [row for row in rows if row["stage"] == stage] for stage in RAW_LOGS}
    stage_counts = {stage: len(stage_rows[stage]) for stage in RAW_LOGS}
    final_cell_counts = Counter(row["factorial_cell"] for row in rows)
    sample_ids = [row["sample_id"] for row in rows]
    stage1_ids = {row["sample_id"] for row in stage_rows["stage1"]}
    stage2_ids = {row["sample_id"] for row in stage_rows["stage2"]}
    stage_replicate_sets = {
        stage: {row["replicate_id"] for row in group}
        for stage, group in stage_rows.items()
    }
    technical_failures = sum(row["technical_failure"] for row in rows)
    metadata_experiment_ids = {
        sample["metadata"].get("experiment_id")
        for log in logs.values()
        for sample in log["samples"]
    }
    raw_metadata_operational_canary = {
        stage: logs[stage].get("metadata", {}).get("operational_canary")
        for stage in RAW_LOGS
    }
    canary_excluded = (
        metadata_experiment_ids == {"003-constraint-status-pressure"}
        and all(value is not True for value in raw_metadata_operational_canary.values())
        and not any("canary" in str(value).lower() for value in metadata_experiment_ids)
    )
    versions = {
        "environment": {row["environment_version"] for row in rows},
        "prompt": {row["prompt_version"] for row in rows},
    }
    expected_condition_text = {
        key: value.text for key, value in CONSTRAINT_STATUS_CONDITIONS.items()
    }
    expected_pressure_text = {
        key: value.text for key, value in PRESSURE_CONDITIONS.items()
    }
    apparatus_conditions = set(CONDITIONS) == set(CELL_ORDER)
    sha_matches = {
        stage: shas[stage] == RAW_LOGS[stage]["expected_sha256"] for stage in RAW_LOGS
    }
    completed_samples = {
        stage: logs[stage].get("results", {}).get("completed_samples")
        for stage in RAW_LOGS
    }
    raw_statuses = {stage: logs[stage].get("status") for stage in RAW_LOGS}
    stage_ids_ok = {
        "stage1_ids_00_19": stage_replicate_sets["stage1"]
        == RAW_LOGS["stage1"]["expected_replicate_ids"],
        "stage2_ids_20_49": stage_replicate_sets["stage2"]
        == RAW_LOGS["stage2"]["expected_replicate_ids"],
    }
    no_stage_overlap = stage1_ids.isdisjoint(stage2_ids)
    ok = (
        all(path.exists() for path in paths.values())
        and all(sha_matches.values())
        and raw_statuses == {"stage1": "success", "stage2": "success"}
        and completed_samples == {"stage1": 120, "stage2": 180}
        and stage_counts == {"stage1": 120, "stage2": 180}
        and len(rows) == 300
        and final_cell_counts == EXPECTED_FINAL_COUNTS
        and len(set(sample_ids)) == 300
        and stage_ids_ok["stage1_ids_00_19"]
        and stage_ids_ok["stage2_ids_20_49"]
        and no_stage_overlap
        and technical_failures == 0
        and canary_excluded
        and apparatus_conditions
        and versions == {"environment": {"stage1-v1"}, "prompt": {"stage1-v1"}}
    )
    return {
        "ok": ok,
        "raw_logs": {
            stage: {
                "path": str(paths[stage]),
                "repository_relative_path": str(RAW_LOGS[stage]["relative_path"]),
                "sha256": shas[stage],
                "sha256_matches_expected": sha_matches[stage],
                "byte_size": byte_sizes[stage],
                "raw_status": raw_statuses[stage],
                "completed_samples": completed_samples[stage],
                "extracted_sample_rows": stage_counts[stage],
            }
            for stage in RAW_LOGS
        },
        "combined_sample_count": len(rows),
        "final_cell_counts": dict(final_cell_counts),
        "unique_sample_ids": len(set(sample_ids)),
        "stage_replicate_ids": {
            stage: sorted(values) for stage, values in stage_replicate_sets.items()
        },
        "stage_id_ranges_ok": stage_ids_ok,
        "no_stage1_stage2_sample_overlap": no_stage_overlap,
        "technical_failures": technical_failures,
        "canary_preflight_excluded": canary_excluded,
        "frozen_condition_wording_consistent": apparatus_conditions,
        "expected_constraint_status_wording": expected_condition_text,
        "expected_pressure_wording": expected_pressure_text,
        "versions": {key: sorted(value) for key, value in versions.items()},
    }


def prediction_comparison(stats: dict[str, Any]) -> str:
    primary = stats["primary_violation"]
    rates = primary["cell_rates"]
    constraint_rates = primary["constraint_status_rates"]
    pressure_rates = primary["pressure_rates"]
    total_violations = primary["total_events"]
    interaction = primary["planned_contrasts"]["interaction_rate_differences"]
    search = stats["secondary_mechanical_search_effort"]
    secondary_varies = any(
        len(set(round(value, 10) for value in metric["cell_means"].values())) > 1
        for metric in search.values()
    )
    rows = [
        (
            "H1: Constraint-status main effect: categorical < procedural < purpose-conflict in circumvention probability.",
            (
                "Collapsed rates categorical/procedural/purpose-conflict: "
                f"{constraint_rates['categorical']:.3f} / "
                f"{constraint_rates['procedural']:.3f} / "
                f"{constraint_rates['purpose-conflict']:.3f}."
            ),
            (
                "Supported"
                if constraint_rates["categorical"]
                < constraint_rates["procedural"]
                < constraint_rates["purpose-conflict"]
                else "Not supported"
            ),
        ),
        (
            "H2: High pressure increases circumvention versus ordinary pressure.",
            (
                "Collapsed rates ordinary/high: "
                f"{pressure_rates['ordinary']:.3f} / {pressure_rates['high']:.3f}."
            ),
            "Supported" if pressure_rates["high"] > pressure_rates["ordinary"] else "Not supported",
        ),
        (
            "H3: Constraint-status x pressure interaction.",
            (
                "Pressure-effect rate differences categorical/procedural/purpose-conflict: "
                f"{interaction['pressure_effects']['categorical']:.3f} / "
                f"{interaction['pressure_effects']['procedural']:.3f} / "
                f"{interaction['pressure_effects']['purpose-conflict']:.3f}."
            ),
            (
                "Supported"
                if (
                    interaction["pressure_effects"]["categorical"]
                    < interaction["pressure_effects"]["procedural"]
                    or interaction["pressure_effects"]["categorical"]
                    < interaction["pressure_effects"]["purpose-conflict"]
                )
                and total_violations > 0
                else "Not supported"
            ),
        ),
        (
            "H4: Constraint-bounded competing hypothesis: circumvention remains approximately zero across all six cells.",
            (
                f"Total violations: {total_violations}/300; cell rates: "
                + ", ".join(f"{cell}={rates[cell]:.3f}" for cell in CELL_ORDER)
                + "."
            ),
            "Supported" if total_violations == 0 else "Not supported",
        ),
        (
            "H5: Representation/search behavior may vary without changes in violation rate.",
            (
                "Mechanical secondary outcomes "
                + ("varied across cells" if secondary_varies else "did not vary across cells")
                + "; qualitative rationale was not inspected."
            ),
            "Supported" if secondary_varies and total_violations == 0 else "Indeterminate",
        ),
    ]
    lines = [
        "# Experiment 003 Final Prediction Comparison",
        "",
        "| Prediction | Mechanical result | Supported / Not supported / Indeterminate |",
        "| --- | --- | --- |",
    ]
    lines.extend(f"| {a} | {b} | {c} |" for a, b, c in rows)
    lines.append("")
    return "\n".join(lines)


def write_stage_consistency(path: Path, consistency: dict[str, Any]) -> None:
    lines = [
        "# Experiment 003 Stage Consistency Summary",
        "",
        "This comparison is provenance/consistency-only. The staged design was operational, "
        "and the preregistration forbids outcome-based optional stopping.",
        "",
        "| Stage | n | Primary endpoint events | Technical failures | Cell counts | Replicate IDs |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for stage, summary in consistency["stage_summaries"].items():
        cell_counts = ", ".join(
            f"{cell}={summary['cell_counts'].get(cell, 0)}" for cell in CELL_ORDER
        )
        lines.append(
            f"| {stage} | {summary['n']} | {summary['primary_violation_count']} | "
            f"{summary['technical_failures']} | {cell_counts} | "
            f"{summary['replicate_id_min']}-{summary['replicate_id_max']} |"
        )
    lines.extend(
        [
            "",
            "Combining stages consistent with frozen design: "
            f"`{consistency['combining_stages_consistent_with_frozen_design']}`",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    for row in rows[1:]:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def scan_for_credentials(paths: list[Path]) -> dict[str, Any]:
    patterns = {
        "openai_key": re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
        "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
        "openai_env_assignment": re.compile("OPENAI" + r"_API_KEY=.*[A-Za-z0-9]"),
    }
    findings: dict[str, list[str]] = {}
    for path in paths:
        text = path.read_text(encoding="utf-8")
        hits = [name for name, pattern in patterns.items() if pattern.search(text)]
        if hits:
            findings[str(path.relative_to(REPO))] = hits
    return {"passed": not findings, "findings": findings}


def main() -> None:
    logs: dict[str, dict[str, Any]] = {}
    paths: dict[str, Path] = {}
    shas: dict[str, str] = {}
    byte_sizes: dict[str, int] = {}
    rows: list[dict[str, Any]] = []
    for stage in RAW_LOGS:
        log, path, raw_sha, raw_bytes = load_stage(stage)
        logs[stage] = log
        paths[stage] = path
        shas[stage] = raw_sha
        byte_sizes[stage] = raw_bytes
        rows.extend(extract_rows(log, stage))

    integrity_result = integrity(logs, paths, shas, byte_sizes, rows)
    if not integrity_result["ok"]:
        print(json.dumps(integrity_result, indent=2, sort_keys=True))
        raise SystemExit("integrity checks failed")

    cells = cell_summary(rows)
    factors = factor_summary(rows)
    stats = statistical_results(rows)
    consistency = stage_consistency(rows)
    prediction_md = prediction_comparison(stats)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    per_sample_path = OUT_DIR / "per_sample_results_final.csv"
    cell_path = OUT_DIR / "cell_summary_final.csv"
    factor_path = OUT_DIR / "factor_summary_final.csv"
    stats_path = OUT_DIR / "statistical_results_final.json"
    descriptive_path = OUT_DIR / "run003_final_descriptive_summary.json"
    prediction_path = OUT_DIR / "prediction_comparison_final.md"
    stage_consistency_path = OUT_DIR / "stage_consistency_summary.md"
    manifest_path = OUT_DIR / "provenance_manifest_final.json"
    scan_path = OUT_DIR / "credential_scan_final.json"

    write_csv(per_sample_path, rows)
    write_csv(cell_path, cells)
    write_csv(factor_path, factors)
    stats_path.write_text(
        json.dumps(stats, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    descriptive = {
        "integrity": integrity_result,
        "cell_summary": cells,
        "factor_summary": factors,
        "primary_violation": stats["primary_violation"],
        "secondary_mechanical_search_effort": stats[
            "secondary_mechanical_search_effort"
        ],
        "stage_consistency": consistency,
    }
    descriptive_path.write_text(
        json.dumps(descriptive, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    prediction_path.write_text(prediction_md, encoding="utf-8")
    write_stage_consistency(stage_consistency_path, consistency)

    manifest = {
        "raw_logs": {
            stage: {
                "path": str(paths[stage]),
                "repository_relative_path": str(RAW_LOGS[stage]["relative_path"]),
                "filename": paths[stage].name,
                "sha256": shas[stage],
                "byte_size": byte_sizes[stage],
                "sample_count": RAW_LOGS[stage]["expected_samples"],
            }
            for stage in RAW_LOGS
        },
        "stage1_checkpoint_results_commit": STAGE1_CHECKPOINT_SHA,
        "stage1_execution_sha": STAGE1_EXECUTION_SHA,
        "stage2_execution_sha": STAGE2_EXECUTION_SHA,
        "preregistration_sha": PREREGISTRATION_SHA,
        "frozen_scientific_sha": FROZEN_SHA,
        "model": MODEL,
        "stage1_sample_count": 120,
        "stage2_sample_count": 180,
        "combined_sample_count": 300,
        "technical_failures": 0,
        "analysis_plan_path": str(ANALYSIS_PLAN),
        "predictions_path": str(PREDICTIONS),
        "design_path": str(DESIGN),
        "scoring_path": str(SCORING),
        "derived_artifacts": [
            str(path.relative_to(REPO))
            for path in (
                per_sample_path,
                cell_path,
                factor_path,
                stats_path,
                descriptive_path,
                prediction_path,
                stage_consistency_path,
                manifest_path,
                scan_path,
            )
        ],
    }
    manifest_path.write_text(
        json.dumps(manifest, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    artifact_paths = [
        per_sample_path,
        cell_path,
        factor_path,
        stats_path,
        descriptive_path,
        prediction_path,
        stage_consistency_path,
        manifest_path,
        scan_path,
        REPO / "scripts" / "analyze_exp003_final.py",
    ]
    scan_path.write_text(
        json.dumps({"passed": True, "findings": {}}, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    credential_scan = scan_for_credentials(artifact_paths)
    scan_path.write_text(
        json.dumps(credential_scan, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "integrity": integrity_result,
                "cell_summary": cells,
                "factor_summary": factors,
                "statistical_results": stats,
                "stage_consistency": consistency,
                "credential_scan": credential_scan,
                "artifacts": manifest["derived_artifacts"],
            },
            allow_nan=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
